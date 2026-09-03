# -*- coding: utf-8 -*-
import os
import json
import time
import uuid
import sqlite3
from collections import Counter
from core.helpers import get_player_uid, get_masters_db_path, get_equipment_meta, load_all_equipment
from core.storage import _assign_to_coin_locker, analyze_storage_stock

DUMMY_OR_CLOSED_PARTS = {'PT_ARM_FirstAid', 'PT_ARM_Food', 'PT_ARM_Sand', 'PT_ARM_WP000_001', 'PT_ARM_WP011_0C1', 'PT_ARM_WP023_001', 'PT_ARM_WP025_0A4', 'PT_GAS_HEAD_001', 'PT_GAS_HEAD_002', 'PT_GAS_HEAD_003', 'PT_GAS_HEAD_004', 'PT_GAS_HEAD_005', 'PT_GAS_HEAD_006', 'PT_GAS_HEAD_007', 'PT_GAS_HEAD_008', 'PT_MASK_001', 'PT_MASK_002', 'PT_MIL_BTM_1003', 'PT_MIL_HEAD_1003', 'PT_MIL_TOPS_1003', 'PT_NONE_BTM_001', 'PT_NONE_HEAD_001', 'PT_NONE_MASK_001', 'PT_NONE_PANTS_001', 'PT_NONE_TOPS_001', 'PT_PANTS_001', 'PT_PANTS_002'}

ENDGAME_SETS = {'white_steel': {'name': '44CE White Steel (D.O.D. Arms)', 'parts': [('PT_ARM_WP055_001', 'Masajeador Estático 44CE (Static Massager)', 5), ('PT_ARM_WP002_001', 'Bate de Púas +4 (Spike Bat)', 5), ('PT_DIY_HEAD_4F_01', 'Casco White Steel 44CE', 5), ('PT_DIY_TOPS_4F_01', 'Peto White Steel 44CE', 5), ('PT_DIY_BTM_4F_01', 'Pantalones White Steel 44CE', 5)]}, 'red_napalm': {'name': '44CE Red Napalm (War Ensemble)', 'parts': [('PT_ARM_WP056_001', 'Lanzador M2G-87 Red Napalm (Spike Launcher)', 5), ('PT_MIL_HEAD_4F_01', 'Casco Red Napalm 44CE', 5), ('PT_MIL_TOPS_4F_01', 'Peto Red Napalm 44CE', 5), ('PT_MIL_BTM_4F_01', 'Pantalones Red Napalm 44CE', 5)]}, 'black_thunder': {'name': '44CE Black Thunder (Candle Wolf)', 'parts': [('PT_ARM_WP057_001', 'Espada de Energía 44CE (Energy Sword)', 5), ('PT_FAN_HEAD_4F_01', 'Casco Black Thunder 44CE', 5), ('PT_FAN_TOPS_4F_01', 'Peto Black Thunder 44CE', 5), ('PT_FAN_BTM_4F_01', 'Pantalones Black Thunder 44CE', 5)]}, 'pale_wind': {'name': '44CE Pale Wind (M.I.L.K.)', 'parts': [('PT_ARM_WP058_001', 'Vara de Fuerza 44CE (Force Wand)', 5), ('PT_SPO_HEAD_4F_01', 'Casco Pale Wind 44CE', 5), ('PT_SPO_TOPS_4F_01', 'Peto Pale Wind 44CE', 5), ('PT_SPO_BTM_4F_01', 'Pantalones Pale Wind 44CE', 5)]}, 'jackals_gear': {'name': 'Sets Jackals v1 / v2 / v3', 'parts': [('PT_ARM_WP001_JAC_11', 'Espada Jackal X', 5), ('PT_ARM_WP016_JAC_11', 'Pistola Jackal Y (Blaster)', 5), ('PT_ARM_WP027_JAC_11', 'Yo-Yo Jackal Z', 5), ('PT_JAC_HEAD_101', 'Casco Jackal X', 5), ('PT_JAC_TOPS_101', 'Traje Jackal X', 5), ('PT_JAC_BTM_101', 'Pantalón Jackal X', 5), ('PT_JAC_HEAD_102', 'Casco Jackal Y', 5), ('PT_JAC_TOPS_102', 'Traje Jackal Y', 5), ('PT_JAC_BTM_102', 'Pantalón Jackal Y', 5), ('PT_JAC_HEAD_103', 'Casco Jackal Z', 5), ('PT_JAC_TOPS_103', 'Traje Jackal Z', 5), ('PT_JAC_BTM_103', 'Pantalón Jackal Z', 5)]}, 'tengoku_weapons': {'name': 'Armas Legendarias de Tengoku (51F+)', 'parts': [('PT_ARM_WP060_001', 'Muspelheim (Ballesta de Fuego Tengoku)', 5), ('PT_ARM_WP061_001', 'Judgement Day (Francotirador Tengoku)', 5), ('PT_ARM_WP062_001', 'Predator (Machete Tengoku)', 5), ('PT_ARM_WP063_001', 'Emperor (Lanzagranadas Tengoku)', 5), ('PT_ARM_WP064_001', 'Lethal Weapon (KAMAS Tengoku)', 5)]}}

def repair_and_sanitize_blueprints(save):
    soul = save.setdefault("soul", {})
    pr_dict = soul.setdefault("partresearch", {})
    pr_list = pr_dict.setdefault("user", [])
    
    # Connect to master_part to query authentic evolution links
    next_map = {}
    parent_map = {}
    db_path = get_masters_db_path()
    if os.path.exists(db_path):
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT id, nextptid FROM master_part WHERE nextptid != '';")
            for p, nxt in cur.fetchall():
                if nxt:
                    next_map[p] = nxt
                    parent_map[nxt] = p
            conn.close()
        except Exception:
            pass
            
    by_ptid = {}
    for e in pr_list:
        if isinstance(e, dict) and "ptid" in e:
            ptid = e.get("ptid")
            by_ptid.setdefault(ptid, []).append(e)
            
    # 1. Identify all ptids that represent researched/repairable pieces vs pure REMODEL
    researched_ptids = set()
    for ptid, entries in by_ptid.items():
        if ptid in DUMMY_OR_CLOSED_PARTS:
            continue
        is_pure_remodel = (len(entries) == 1 and entries[0].get("research_type") == "REMODEL")
        if not is_pure_remodel:
            researched_ptids.add(ptid)

    # Ensure hierarchy completeness: if a child tier is researched,
    # all its prerequisite ancestors must also be considered researched!
    ancestor_additions = set()
    for ptid in list(researched_ptids):
        for anc in get_equipment_ancestors(ptid, parent_map):
            if anc not in researched_ptids and anc not in DUMMY_OR_CLOSED_PARTS:
                ancestor_additions.add(anc)
    researched_ptids.update(ancestor_additions)
            
    repaired_list = []
    repaired_count = 0

    
    # 2. Rebuild clean FINISHED entries for each researched piece (levels 1-4 + level 5 CHARGE if evolves)
    # This completely eliminates any corrupted or duplicate REMODEL entries for pieces already researched!
    for ptid in sorted(researched_ptids):
        has_next = (ptid in next_map)
        parent = parent_map.get(ptid, "")
        
        repaired_list.append({
            "ptid": ptid,
            "lvl": 1,
            "research_type": "FINISHED",
            "receive_type": "FINISHED",
            "is_announced": 1,
            "is_checked": 1,
            "before_ptid": parent if parent else "",
            "before_lvl": 5 if parent else 0
        })
        
        for lvl in (2, 3, 4):
            repaired_list.append({
                "ptid": ptid,
                "lvl": lvl,
                "research_type": "FINISHED",
                "receive_type": "FINISHED",
                "is_announced": 1,
                "is_checked": 1,
                "before_ptid": ptid,
                "before_lvl": lvl - 1
            })
            
        if has_next:
            repaired_list.append({
                "ptid": ptid,
                "lvl": 5,
                "research_type": "FINISHED",
                "receive_type": "CHARGE",
                "is_announced": 1,
                "is_checked": 1,
                "before_ptid": ptid,
                "before_lvl": 4
            })
        repaired_count += 1
        
    # 3. Add REMODEL evolution entries ONLY for immediate next tiers that are NOT already researched!
    # If ptid is researched to Level 5 and its next tier nxt is NOT in researched_ptids:
    # -> It gets exactly one REMODEL entry in R&D.
    # -> If nxt is ALREADY researched, NO REMODEL entry is added (prevents the duplicate Tier bug!)
    for ptid in sorted(researched_ptids):
        nxt = next_map.get(ptid)
        if nxt and nxt not in DUMMY_OR_CLOSED_PARTS:
            if nxt not in researched_ptids:
                repaired_list.append({
                    "ptid": nxt,
                    "lvl": 1,
                    "research_type": "REMODEL",
                    "receive_type": "UNKNOWN",
                    "is_announced": 0,
                    "is_checked": 1,
                    "before_ptid": ptid,
                    "before_lvl": 5
                })
                
    # 4. Preserve any standalone MAP blueprints found in chests that are not already researched
    for ptid, entries in by_ptid.items():
        if ptid not in researched_ptids and ptid not in DUMMY_OR_CLOSED_PARTS:
            for e in entries:
                if e.get("research_type") == "MAP":
                    repaired_list.append(e)
                    
    pr_dict["user"] = repaired_list
    return repaired_count, len(repaired_list)


def unlock_blueprints(save, category="all", max_level=4):
    eq = load_all_equipment()
    if category == "all":
        target_ids = eq.get("all", [])
    else:
        target_ids = eq.get(category, [])
        
    soul = save.setdefault("soul", {})
    pr_dict = soul.setdefault("partresearch", {})
    pr_list = pr_dict.setdefault("user", [])
    
    by_ptid = {}
    for e in pr_list:
        if isinstance(e, dict) and "ptid" in e:
            by_ptid.setdefault(e.get("ptid"), []).append(e)
            
    added = 0
    for bp_id in target_ids:
        if bp_id in DUMMY_OR_CLOSED_PARTS:
            continue
        if bp_id not in by_ptid:
            added += 1
        bp_entries = [
            {
                "ptid": bp_id,
                "lvl": lvl,
                "research_type": "FINISHED",
                "receive_type": "FINISHED",
                "is_announced": 1,
                "is_checked": 1,
                "before_ptid": bp_id if lvl > 1 else "",
                "before_lvl": lvl - 1 if lvl > 1 else 0
            }
            for lvl in range(1, 5)
        ]
        # Level 5 (Completed +4, available to purchase in Chokufunsha)
        bp_entries.append({
            "ptid": bp_id,
            "lvl": 5,
            "research_type": "FINISHED",
            "receive_type": "CHARGE",
            "is_announced": 1,
            "is_checked": 3,
            "before_ptid": bp_id,
            "before_lvl": 4
        })
        by_ptid[bp_id] = bp_entries
        
    clean_list = []
    for ptid, entries in by_ptid.items():
        if ptid in DUMMY_OR_CLOSED_PARTS:
            continue
        entries_by_lvl = {e.get("lvl"): e for e in entries}
        max_l = max(entries_by_lvl.keys(), default=1)
        for lvl in range(1, max_l + 1):
            if lvl in entries_by_lvl:
                clean_list.append(entries_by_lvl[lvl])
            else:
                clean_list.append({
                    "ptid": ptid,
                    "lvl": lvl,
                    "research_type": "FINISHED",
                    "receive_type": "FINISHED",
                    "is_announced": 1,
                    "is_checked": 1,
                    "before_ptid": ptid if lvl > 1 else "",
                    "before_lvl": lvl - 1 if lvl > 1 else 0
                })
            
    pr_dict["user"] = clean_list
    return len(target_ids), added

def repair_all_storage_equipment(save):
    pts = save.get("part", {}).get("pts", [])
    pts_iter = pts.values() if isinstance(pts, dict) else (pts if isinstance(pts, list) else [])
    for p in pts_iter:
        if isinstance(p, dict):
            p["dur"] = 50000
            p["rest"] = 0
            p["spare"] = 0

def add_equipment_to_storage(save, ptid, count=1, lvl=5, dur=50000):
    meta = get_equipment_meta(ptid)
    can_uncap = meta.get("can_uncap", True)
    lvl = int(lvl)
    # Intermediate tiers that evolve into next tiers cap at Level 5 (+4)
    if not can_uncap and lvl > 5:
        lvl = 5
    uid_str = get_player_uid(save)
    try:
        uid_int = int(uid_str)
    except ValueError:
        uid_int = 0
    pts_list = save.setdefault("part", {}).setdefault("pts", [])
    if isinstance(pts_list, dict):
        pts_list = pts_list.setdefault(uid_str, [])
    now = int(time.time())
    added = 0
    for _ in range(count):
        eid = str(uuid.uuid4())
        pts_list.append({
            "uid": uid_int,
            "eid": eid,
            "gettime": now,
            "owner": "COIN_LOCKER",
            "created": now,
            "modified": now,
            "ptid": ptid,
            "rest": 0,
            "spare": 0,
            "grade": 0,
            "dur": int(dur),
            "lvl": int(lvl)
        })
        if _assign_to_coin_locker(save, eid, 0):
            added += 1
    return added

def analyze_active_recipes_materials(save, db_path=None):
    """
    Analyzes all in-progress R&D recipes (REMODEL, MAP, LEVELUP) in partresearch.user,
    calculates total material requirements, compares against current stock in storage,
    and returns a list of items with their required, in-stock, and deficit quantities.
    """
    db_path = get_masters_db_path(db_path)
        
    stock_res = analyze_storage_stock(save)
    stock = stock_res["stock_by_id"]
    
    soul = save.setdefault("soul", {})
    pr_u = soul.get("partresearch", {}).get("user", [])
    active_recipes = [e for e in pr_u if e.get("research_type") in ("REMODEL", "MAP", "LEVELUP")]
    
    needed = Counter()
    recipe_sources = {}
    
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            for r in active_recipes:
                ptid = r.get("ptid")
                cur.execute("""
                    SELECT mate1_id, craft_mate1_num, mate2_id, craft_mate2_num, mate3_id, craft_mate3_num, mate4_id, craft_mate4_num, mate5_id, craft_mate5_num 
                    FROM master_part_research 
                    WHERE ptid=?;
                """, (ptid,))
                row = cur.fetchone()
                if row:
                    for i in range(0, 10, 2):
                        mat_id = row[i]
                        qty = int(row[i+1]) if row[i+1] else 0
                        if mat_id and qty > 0:
                            needed[mat_id] += qty
                            recipe_sources.setdefault(mat_id, []).append(ptid)
            
            # Fetch names in a fast query
            names = {}
            if needed:
                placeholders = ",".join("?" for _ in needed)
                mat_list = list(needed.keys())
                cur.execute(f"""
                    SELECT mi.itemid, COALESCE(mt.txt, mi.name) 
                    FROM master_item mi 
                    LEFT JOIN master_text mt ON (mt.id = REPLACE(mi.name, 'MATERIAL.', '') AND mt.lang = 'esn')
                    WHERE mi.itemid IN ({placeholders});
                """, mat_list)
                for iid, n in cur.fetchall():
                    names[iid] = n
                    
                # Check any mushrooms in needed
                msr_list = [m for m in needed if m.startswith("MSR_")]
                if msr_list:
                    placeholders_msr = ",".join("?" for _ in msr_list)
                    cur.execute(f"""
                        SELECT mm.id, COALESCE(mt.txt, mm.c_name)
                        FROM master_mushroom mm
                        LEFT JOIN master_text mt ON (mt.id = REPLACE(mm.c_name, 'MUSHROOM.', '') AND mt.lang = 'esn')
                        WHERE mm.id IN ({placeholders_msr});
                    """, msr_list)
                    for mid, n in cur.fetchall():
                        names[mid] = n
            conn.close()
        except Exception:
            names = {}
    else:
        names = {}
        
    materials_list = []
    for mat_id, req in needed.items():
        curr = stock.get(mat_id, 0)
        deficit = max(0, req - curr)
        materials_list.append({
            "itemid": mat_id,
            "name": names.get(mat_id, mat_id),
            "needed": req,
            "stock": curr,
            "deficit": deficit,
            "status": "FALTA" if deficit > 0 else "OK"
        })
        
    # Sort: Deficit items first (highest deficit first), then OK items
    materials_list.sort(key=lambda x: (x["deficit"] <= 0, -x["deficit"], x["name"]))
    
    return {
        "storage_used": stock_res["used_slots"],
        "storage_total": stock_res["total_slots"],
        "storage_free": stock_res["free_slots"],
        "total_active_recipes": len(active_recipes),
        "total_materials_needed": len(needed),
        "materials": materials_list
    }

def get_equipment_inventory_counts(save):
    """
    Returns two Counters: (storage_counts, bag_counts)
    mapping ptid -> quantity owned in Coin Locker and in Fighter Deathbag/Equipped.
    """
    storage_counts = Counter()
    bag_counts = Counter()
    
    pts = save.get("part", {}).get("pts", {})
    if isinstance(pts, dict):
        for uid_key, p_list in pts.items():
            if isinstance(p_list, list):
                for p in p_list:
                    if isinstance(p, dict):
                        ptid = p.get("ptid")
                        owner = p.get("owner")
                        if owner == "COIN_LOCKER" or uid_key == "-1":
                            storage_counts[ptid] += 1
                        else:
                            bag_counts[ptid] += 1
    elif isinstance(pts, list):
        for p in pts:
            if isinstance(p, dict):
                ptid = p.get("ptid")
                owner = p.get("owner")
                if owner == "COIN_LOCKER":
                    storage_counts[ptid] += 1
                else:
                    bag_counts[ptid] += 1
                    
    return storage_counts, bag_counts

def get_equipment_ancestors(ptid, parent_map=None):
    """
    Returns the list of ancestor ptids in chronological evolution order
    (from the root ancestor down to the immediate parent).
    Example for Katana 3: ['PT_ARM_WP007_001', 'PT_ARM_WP007_003']
    """
    if parent_map is None:
        db_path = get_masters_db_path()
        parent_map = {}
        if os.path.exists(db_path):
            try:
                import sqlite3
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("SELECT id, nextptid FROM master_part WHERE nextptid IS NOT NULL AND nextptid != '';")
                for p, nxt in c.fetchall():
                    parent_map[nxt] = p
                conn.close()
            except Exception:
                pass
                
    ancestors = []
    curr = ptid
    visited = set()
    while curr in parent_map and parent_map[curr]:
        p = parent_map[curr]
        if p in visited or p in DUMMY_OR_CLOSED_PARTS:
            break
        visited.add(p)
        ancestors.append(p)
        curr = p
        
    return list(reversed(ancestors))

def get_blueprints_unlock_map(save):
    """
    Returns a dictionary mapping ptid -> status info:
    {
        "status": "STORE_PLUS4" | "FINISHED_LVL" | "REMODEL" | "MAP" | "LOCKED",
        "lvl": int,
        "label": str (e.g. "⭐ Tienda (+4)", "🔨 En I+D (REMODEL)", "❌ Bloqueado")
    }
    """
    soul = save.setdefault("soul", {})
    pr_u = soul.get("partresearch", {}).get("user", [])
    
    max_finished_lvl = {}
    special_types = {}
    for r in pr_u:
        if not isinstance(r, dict):
            continue
        ptid = r.get("ptid")
        rtype = r.get("research_type", "")
        lvl = r.get("lvl", 1)
        if rtype == "FINISHED":
            max_finished_lvl[ptid] = max(max_finished_lvl.get(ptid, 0), lvl)
        elif rtype in ("REMODEL", "MAP"):
            special_types[ptid] = (rtype, lvl)
            
    unlock_map = {}
    for ptid, lvl in max_finished_lvl.items():
        if lvl >= 5:
            unlock_map[ptid] = {"status": "STORE_PLUS4", "lvl": lvl, "label": "⭐ Tienda (+4)"}
        else:
            unlock_map[ptid] = {
                "status": "FINISHED_LVL",
                "lvl": lvl,
                "label": f"🔨 En I+D (+{lvl-1} → +{lvl})"
            }
            
    for ptid, (rtype, lvl) in special_types.items():
        if ptid not in unlock_map:
            if rtype == "REMODEL":
                unlock_map[ptid] = {"status": "REMODEL", "lvl": lvl, "label": "🔨 En I+D (Evolución +0)"}
            elif rtype == "MAP":
                unlock_map[ptid] = {"status": "MAP", "lvl": lvl, "label": "📜 En I+D (Plano +0)"}
                
    return unlock_map

def send_blueprint_to_rnd(save, ptid, target_level=0, auto_unlock_ancestors=True):
    """
    Places an equipment piece directly into Chokufunsha R&D (Development).
    - If target_level == 0:
      Places the piece in R&D as an uncrafted Blueprint (+0 ready to develop):
      Uses "MAP" for base pieces, or "REMODEL" if it evolves from a parent tier.
    - If target_level > 0 (e.g. 1 for +0 in shop & +1 in R&D, 2 for +1 in shop & +2 in R&D, etc.):
      Sets the piece as researched up to target_level in the shop,
      leaving the NEXT level actively waiting for materials in R&D!
    - If auto_unlock_ancestors is True:
      All prerequisite evolution ancestors (e.g. Katana 1, Katana 2) are automatically
      unlocked to Level 5 (+4 CHARGE in shop), ensuring authentic consistency without errors!
    Returns the assigned status dict.
    """
    soul = save.setdefault("soul", {})
    pr_dict = soul.setdefault("partresearch", {})
    pr_list = pr_dict.setdefault("user", [])
    
    # 1. Prerequisite Hierarchy: If this piece is an evolution (e.g. Katana 3),
    # its ancestors MUST be completed at Level 5 (+4 CHARGE in shop) for the evolution to exist!
    if auto_unlock_ancestors:
        ancestors = get_equipment_ancestors(ptid)
        for anc in ancestors:
            anc_entries = [e for e in pr_list if e.get("ptid") == anc]
            has_lvl5 = any(e.get("lvl") == 5 and e.get("research_type") == "FINISHED" for e in anc_entries)
            if not has_lvl5:
                unlock_single_blueprint(save, anc, level=4, unlock_next_tier=False, auto_unlock_ancestors=False)
    
    parent = ""
    db_path = get_masters_db_path()
    if os.path.exists(db_path):
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT id FROM master_part WHERE nextptid = ?;", (ptid,))
            row = c.fetchone()
            if row:
                parent = row[0]
            conn.close()
        except Exception:
            pass

    # Remove all existing entries for this ptid
    pr_list[:] = [e for e in pr_list if e.get("ptid") != ptid]

    if target_level <= 0:
        # Brand new blueprint in R&D (+0 to be developed)
        rtype = "REMODEL" if parent else "MAP"
        pr_list.append({
            "ptid": ptid,
            "lvl": 1,
            "research_type": rtype,
            "receive_type": "UNKNOWN",
            "is_announced": 0,
            "is_checked": 1,
            "before_ptid": parent if parent else "",
            "before_lvl": 5 if parent else 0
        })
    else:
        # Researched up to target_level in shop, next level actively waiting in R&D
        meta = get_equipment_meta(ptid)
        can_uncap = meta.get("can_uncap", True)
        if not can_uncap and target_level > 4:
            target_level = 4
            
        for l in range(1, target_level + 1):
            pr_list.append({
                "ptid": ptid,
                "lvl": l,
                "research_type": "FINISHED",
                "receive_type": "FINISHED",
                "is_announced": 1,
                "is_checked": 1,
                "before_ptid": (parent if l == 1 and parent else (ptid if l > 1 else "")),
                "before_lvl": (5 if l == 1 and parent else (l - 1 if l > 1 else 0))
            })
            
    return get_blueprints_unlock_map(save).get(ptid, {})


def unlock_single_blueprint(save, ptid, level=4, unlock_next_tier=True, auto_unlock_ancestors=True):
    soul = save.setdefault("soul", {})
    pr_dict = soul.setdefault("partresearch", {})
    pr_list = pr_dict.setdefault("user", [])
    
    # 1. Prerequisite Hierarchy: If this piece is an evolution (e.g. Katana 3),
    # automatically ensure that all predecessor tiers (Katana 1, Katana 2)
    # are unlocked to at least Level 5 (+4 CHARGE in shop), maintaining authentic consistency!
    if auto_unlock_ancestors:
        ancestors = get_equipment_ancestors(ptid)
        for anc in ancestors:
            anc_entries = [e for e in pr_list if e.get("ptid") == anc]
            has_lvl5 = any(e.get("lvl") == 5 and e.get("research_type") == "FINISHED" for e in anc_entries)
            if not has_lvl5:
                unlock_single_blueprint(save, anc, level=4, unlock_next_tier=False, auto_unlock_ancestors=False)
    
    meta = get_equipment_meta(ptid)
    can_uncap = meta.get("can_uncap", True)
    nextptid = meta.get("nextptid", "")
    parent = ""
    
    db_path = get_masters_db_path()
    if os.path.exists(db_path):
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT id FROM master_part WHERE nextptid = ?;", (ptid,))
            row = c.fetchone()
            if row:
                parent = row[0]
            conn.close()
        except Exception:
            pass
    
    # If this tier cannot uncap, its maximum research level is 4 (CHARGE at lvl 5)
    if not can_uncap and level > 4:
        level = 4
        
    # Remove existing entries for this ptid
    pr_list[:] = [e for e in pr_list if e.get("ptid") != ptid]
    
    for l in range(1, level + 1):
        pr_list.append({
            "ptid": ptid,
            "lvl": l,
            "research_type": "FINISHED",
            "receive_type": "FINISHED",
            "is_announced": 1,
            "is_checked": 1,
            "before_ptid": (parent if l == 1 and parent else (ptid if l > 1 else "")),
            "before_lvl": (5 if l == 1 and parent else (l - 1 if l > 1 else 0))
        })

    if level >= 4:
        pr_list.append({
            "ptid": ptid,
            "lvl": 5,
            "research_type": "FINISHED",
            "receive_type": "CHARGE",
            "is_announced": 1,
            "is_checked": 3,
            "before_ptid": ptid,
            "before_lvl": 4
        })
        # If this tier evolves into a next tier at level 4, unlock next tier in Chokufunsha R&D (REMODEL)!
        # BUT ONLY IF NEXT TIER IS NOT ALREADY RESEARCHED/FINISHED (prevents the duplicate Tier bug!)
        if unlock_next_tier and nextptid:
            existing_next = [e for e in pr_list if e.get("ptid") == nextptid]
            is_next_already_finished = any(e.get("research_type") == "FINISHED" for e in existing_next)
            if not is_next_already_finished:
                # Remove any conflicting or duplicate entries for nextptid
                pr_list[:] = [e for e in pr_list if e.get("ptid") != nextptid]
                pr_list.append({
                    "ptid": nextptid,
                    "lvl": 1,
                    "research_type": "REMODEL",
                    "receive_type": "UNKNOWN",
                    "is_announced": 0,
                    "is_checked": 1,
                    "before_ptid": ptid,
                    "before_lvl": 5
                })
    return nextptid if (level >= 4 and nextptid) else None



def unlock_all_blueprints(save, level=4):
    unlock_blueprints(save, category="all", max_level=level)

def repair_unlocked_blueprints_states(save):
    rep_cnt, _ = repair_and_sanitize_blueprints(save)
    return rep_cnt

def get_part_research_status(save):
    return get_blueprints_unlock_map(save)

def get_storage_equipment_counts(save):
    st, _ = get_equipment_inventory_counts(save)
    return st

def get_bag_equipment_counts(save):
    _, bg = get_equipment_inventory_counts(save)
    return bg

def set_infinite_durability_all_equipment(save, target_dur=999999):
    """
    Sets extreme durability on all equipment stored in Coin Locker and fighters' bags.
    """
    pts_dict = save.setdefault("part", {}).setdefault("pts", {})
    pts_lists = list(pts_dict.values()) if isinstance(pts_dict, dict) else [pts_dict]
    
    modified_count = 0
    for pts_list in pts_lists:
        if isinstance(pts_list, list):
            for p in pts_list:
                if isinstance(p, dict):
                    p["dur"] = int(target_dur)
                    modified_count += 1
            
    # Also update any equipment in fighters' deathbags
    deathbags = save.get("soul", {}).get("deathbag", {})
    if isinstance(deathbags, dict):
        for bag_items in deathbags.values():
            if isinstance(bag_items, list):
                for b_item in bag_items:
                    if isinstance(b_item, dict) and "dur" in b_item:
                        b_item["dur"] = int(target_dur)
                        modified_count += 1
                        
    return modified_count

def set_massive_ammo_all_weapons(save, ammo=9999):
    """
    Sets magazine capacity (rest) and spare reserve ammo (spare) on all ranged weapons.
    """
    pts_dict = save.setdefault("part", {}).setdefault("pts", {})
    pts_lists = list(pts_dict.values()) if isinstance(pts_dict, dict) else [pts_dict]
    
    modified_count = 0
    for pts_list in pts_lists:
        if isinstance(pts_list, list):
            for p in pts_list:
                if isinstance(p, dict):
                    ptid = str(p.get("ptid", ""))
                    # Any weapon (PT_ARM_) gets massive capacity and reserve ammo
                    if ptid.startswith("PT_ARM_") or "rest" in p or "spare" in p:
                        p["rest"] = int(ammo)
                        p["spare"] = int(ammo)
                        modified_count += 1
    return modified_count

def upgrade_all_equipment_max_level(save, target_lvl=19):
    """
    Upgrades all equipment in storage and fighter inventories.
    Final tier items (can_uncap) are upgraded to target_lvl (e.g. 20 for +19, 25 for +24).
    Intermediate tier items (Tier 1/2/3 that evolve at +4) are safely capped at Level 5 (+4).
    """
    target_lvl = int(target_lvl)
    uncap_internal = target_lvl + 1 if target_lvl in (19, 24) else target_lvl
    
    pts_dict = save.setdefault("part", {}).setdefault("pts", {})
    pts_lists = list(pts_dict.values()) if isinstance(pts_dict, dict) else [pts_dict]
    
    modified_count = 0
    for pts_list in pts_lists:
        if isinstance(pts_list, list):
            for p in pts_list:
                if isinstance(p, dict):
                    ptid = str(p.get("ptid", ""))
                    meta = get_equipment_meta(ptid)
                    can_uncap = meta.get("can_uncap", True)
                    p["lvl"] = uncap_internal if can_uncap else min(5, uncap_internal)
                    modified_count += 1

    # Also update any equipment in fighters' deathbags
    deathbags = save.get("soul", {}).get("deathbag", {})
    if isinstance(deathbags, dict):
        for bag_items in deathbags.values():
            if isinstance(bag_items, list):
                for b_item in bag_items:
                    if isinstance(b_item, dict) and "lvl" in b_item:
                        ptid = str(b_item.get("ptid", ""))
                        meta = get_equipment_meta(ptid)
                        can_uncap = meta.get("can_uncap", True)
                        b_item["lvl"] = uncap_internal if can_uncap else min(5, uncap_internal)
                        modified_count += 1
                        
    return modified_count

# ================= META DECAL PRESETS FOR FIGHTERS =================

def inject_endgame_set(save, set_key="white_steel", count=1, dur=999999, lvl=5):
    if set_key not in ENDGAME_SETS:
        set_key = "white_steel"
    set_info = ENDGAME_SETS[set_key]
    added = 0
    for ptid, name, def_lvl in set_info["parts"]:
        target_lvl = lvl if lvl else def_lvl
        add_equipment_to_storage(save, ptid, count=count, lvl=target_lvl, dur=dur)
        unlock_single_blueprint(save, ptid, level=min(4, target_lvl))
        added += count
    return set_info["name"], added

# ================= QUESTS, MAGAZINES & RADIO COLLECTIBLES =================

