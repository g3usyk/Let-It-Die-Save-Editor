# -*- coding: utf-8 -*-
import os
import sqlite3
import shutil
import uuid
import copy
from game_data import CLASS_CODE_ALIASES
from core.helpers import get_player_uid, get_masters_db_path, PROJECT_ROOT, get_or_create_list


def is_tutorial_cleared(save):
    """
    Checks if the save has completed the tutorial and unlocked the Fighter Freezer.
    """
    cl = save.get("gameflg", {}).get("cl", [])
    has_kiwako = any(f.get("var") == "KGF_FIRST_KIWAKOROOM" and f.get("value") == 1 for f in cl if isinstance(f, dict))
    sv = save.get("gameflg", {}).get("sv", [])
    tut_prog = next((f.get("value", 0) for f in sv if isinstance(f, dict) and f.get("var") == "KGF_TUTORIAL_PROGRESS"), 0)
    return has_kiwako and tut_prog >= 100

def _ensure_freezer_accessible(save):
    """
    Automatically completes the tutorial and unlocks Waiting Room facilities
    if modifying/creating fighters on a fresh save, preventing Kiwako Seto lockout.
    """
    if not is_tutorial_cleared(save):
        try:
            from core.tower import unlock_tutorial_and_waiting_room
            unlock_tutorial_and_waiting_room(save)
        except Exception:
            pass

def max_fighter_level_and_stats(save, fighter_index=0, level=247):
    _ensure_freezer_accessible(save)
    uid = get_player_uid(save)
    fighters = save.get("bodyuser", {}).get(uid, [])
    chr_chrs = save.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])
    if 0 <= fighter_index < len(fighters):
        f = fighters[fighter_index]
        for k in ["param_hp", "param_stm", "param_str", "param_dex", "param_vit", "param_luk", "clazz", "name", "grade"]:
            f.pop(k, None)
        f["lvl"] = int(level)
        # Max stat allocation points (45 for Grade 6 limit_break 4 / Tier 8)
        f["hp"] = 45
        f["str"] = 45
        f["dex"] = 45
        f["vit"] = 45
        f["stm"] = 45
        f["luk"] = 45
        # Muerteroides / Steroid bonuses
        f["hp_bonus"] = 20
        f["str_bonus"] = 20
        f["dex_bonus"] = 20
        f["vit_bonus"] = 20
        f["stm_bonus"] = 20
        f["luk_bonus"] = 20
        # Decal slot expansion (3 extra slots -> unlocks slots 6, 7 and 8!)
        f["skill"] = 3
        # Max bag addition (3 is the safe max for MINGO upgrade)
        f["bag"] = 3
        # Max rage gauge addition
        f["rage"] = 1
        f["die"] = 0
    if 0 <= fighter_index < len(chr_chrs):
        c = chr_chrs[fighter_index]
        c["grade"] = 6
        c["limit_break"] = 4
        c["lvl"] = int(level)
        c["hp"] = 20000
        c["escdie"] = 0
        c["state"] = "GUARD"

def revive_all_fighters(save):
    uid = get_player_uid(save)
    fighters = save.get("bodyuser", {}).get(uid, [])
    chr_chrs = save.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])
    
    soul = save.setdefault("soul", {})
    soul["current_died_cid"] = ""
    soul["die_flag"] = 0
    soul["resurrection"] = 0
    
    # Reset crash force shutdown counts
    fs_counts = save.get("force_shutdown_counts", {})
    if isinstance(fs_counts, dict):
        for k in fs_counts:
            fs_counts[k] = 0
            
    # Clear dead character tower hater records to prevent duplicate roaming haters/desync
    diedchara = save.get("diedchara")
    if isinstance(diedchara, dict):
        dchrs = diedchara.get("dchrs")
        if isinstance(dchrs, dict) and uid in dchrs:
            dchrs[uid] = []
    
    for f in fighters:
        f["die"] = 0
        if f.get("hp", 0) <= 0:
            f["hp"] = 3000
            
    for c in chr_chrs:
        c["escdie"] = 0
        if c.get("hp", 0) <= 0:
            c["hp"] = 3000
        if c.get("state") == "DEAD":
            c["state"] = "GUARD"

def update_fighter(save, fighter_idx, name=None, clazz=None, grade=None, lvl=None, hp=None, str_stat=None, dex=None, vit=None, stm=None, luk=None, bag=None, param_hp=None, param_stm=None, param_str=None, param_dex=None, param_vit=None, param_luk=None, body_model=None):
    _ensure_freezer_accessible(save)
    uid = get_player_uid(save)
    fighters = save.get("bodyuser", {}).get(uid, [])
    chr_chrs = save.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])
    
    if 0 <= fighter_idx < len(fighters):
        f = fighters[fighter_idx]
        # Clean up legacy invalid fields if present
        for k in ["param_hp", "param_stm", "param_str", "param_dex", "param_vit", "param_luk", "clazz", "grade"]:
            f.pop(k, None)
            
        if lvl is not None:
            f["lvl"] = int(lvl)
            
        # Stats allocation points (1..45 points per stat)
        if param_hp is not None:
            f["hp"] = min(45, max(1, int(param_hp)))
        elif hp is not None and int(hp) <= 45:
            f["hp"] = int(hp)
            
        if str_stat is not None:
            f["str"] = min(45, max(1, int(str_stat)))
        elif param_str is not None:
            f["str"] = min(45, max(1, int(param_str)))
            
        if dex is not None:
            f["dex"] = min(45, max(1, int(dex)))
        elif param_dex is not None:
            f["dex"] = min(45, max(1, int(param_dex)))
            
        if vit is not None:
            f["vit"] = min(45, max(1, int(vit)))
        elif param_vit is not None:
            f["vit"] = min(45, max(1, int(param_vit)))
            
        if stm is not None:
            f["stm"] = min(45, max(1, int(stm)))
        elif param_stm is not None:
            f["stm"] = min(45, max(1, int(param_stm)))
            
        if luk is not None:
            f["luk"] = min(45, max(1, int(luk)))
        elif param_luk is not None:
            f["luk"] = min(45, max(1, int(param_luk)))
            
        if bag is not None:
            bag_val = int(bag)
            # BagAddMax is 3 in the engine; values > 3 cause crash on levelup!
            f["bag"] = min(3, max(0, bag_val))
            # True total deathbag capacity lives in soul["bag_slot"]
            if bag_val >= 20:
                save.setdefault("soul", {})["bag_slot"] = bag_val
            
    if 0 <= fighter_idx < len(chr_chrs):
        c = chr_chrs[fighter_idx]
        f = fighters[fighter_idx] if fighter_idx < len(fighters) else {}
        if name is not None:
            c["name"] = str(name)
        if clazz is not None:
            # Map any UI aliases to official engine codes
            engine_class = CLASS_CODE_ALIASES.get(str(clazz).upper(), str(clazz).upper())
            if engine_class not in ["BAL", "BRE", "DEF", "TEC", "SHT", "COL", "SKI", "LUK"]:
                engine_class = "BAL"
            c["type"] = engine_class
        if grade is not None:
            grade_val = min(6, max(1, int(grade)))
            c["grade"] = grade_val
            # Prevent Mingo Head progression machine freeze:
            # When transforming to Grade 6, synchronize limit_break, decal slots, and bonuses
            if grade_val == 6:
                cur_lvl = int(f.get("lvl", c.get("lvl", 1)))
                has_high_stats = any(int(f.get(st, 1)) > 30 for st in ["hp", "str", "dex", "vit", "stm", "luk"])
                if cur_lvl > 140 or has_high_stats:
                    c["limit_break"] = 4
                    f["skill"] = 3
                    f["bag"] = 3
                    f["rage"] = 1
                    for st in ["hp", "str", "dex", "vit", "stm", "luk"]:
                        f[f"{st}_bonus"] = 20
                else:
                    c.setdefault("limit_break", 0)
                    f.setdefault("skill", 0)
                    f.setdefault("bag", 3)
                    f.setdefault("rage", 0)
            elif grade_val < 6:
                c["limit_break"] = 0
                f["skill"] = 0
                f["rage"] = 0
                for st in ["hp", "str", "dex", "vit", "stm", "luk"]:
                    f.pop(f"{st}_bonus", None)

        if lvl is not None:
            c["lvl"] = int(lvl)
        if hp is not None and int(hp) > 45:
            c["hp"] = int(hp)

        if body_model is not None:
            import re
            b_str = str(body_model).upper()
            m_num = re.search(r"\d+", b_str)
            num = int(m_num.group()) if m_num else 1
            num = max(1, min(8, num))
            if "FEMALE" in b_str or "FEM" in b_str or "MUJER" in b_str:
                c["body"] = f"BODY_FEMALE_{num:03d}"
                c["gasmask"] = f"ASSET_NF_GAS_HEAD_{num:03d}"
            else:
                c["body"] = f"BODY_MALE_{num:03d}"
                c["gasmask"] = f"ASSET_NM_GAS_HEAD_{num:03d}"


def expand_death_bag(save, slots=50, fighter_index=None):
    # In LET IT DIE, bodyuser['bag'] is the M.I.N.G.O. upgrade stat which has BagAddMax=3.
    # Exceeding 3 causes 'body_deathbag distribute failed' crash on levelup!
    # True deathbag capacity is expanded naturally by Royal Express VIP pass (+10) and Collector class.
    uid = get_player_uid(save)
    fighters = save.get("bodyuser", {}).get(uid, [])
    if fighter_index is not None and 0 <= fighter_index < len(fighters):
        fighters[fighter_index]["bag"] = 3
    else:
        for f in fighters:
            f["bag"] = 3
    save.setdefault("soul", {})["bag_slot"] = int(slots)
    return slots

def upgrade_fighter_tier8(save, fighter_idx=0):
    return max_fighter_level_and_stats(save, fighter_index=fighter_idx, level=247)

def get_deathbag_masters_status(db_path=None):
    """
    Returns the current Death Bag modification status from masters.db.
    """
    db_path = get_masters_db_path(db_path)
    if not os.path.exists(db_path):
        return {"exists": False, "db_path": db_path}
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT MIN(bag_capacity), MAX(bag_capacity) FROM master_body_detail;")
        min_bag, max_bag = cur.fetchone()
        cur.execute("SELECT value FROM master_const_int WHERE id='VIP_INCREASE_DEATHBAG';")
        r = cur.fetchone()
        vip_val = r[0] if r else 10
        conn.close()
        is_modded = bool(min_bag and min_bag > 18 or vip_val > 10)
        return {
            "exists": True,
            "db_path": db_path,
            "min_bag": min_bag,
            "max_bag": max_bag,
            "vip_bonus": vip_val,
            "is_modded": is_modded
        }
    except Exception as e:
        return {"exists": True, "db_path": db_path, "error": str(e), "is_modded": False}

def expand_deathbag_capacity(target_capacity=60, vip_bonus=10, db_path=None):
    """
    Expands the Death Bag capacity in masters.db for all fighter classes and grades:
    1. Backs up masters.db to masters.db.bak if not already present.
    2. Updates master_body_detail.bag_capacity to at least target_capacity.
    3. Updates master_bodylvl_status_value.bag to at least target_capacity.
    4. Updates master_const_int.VIP_INCREASE_DEATHBAG.
    Returns summary dict.
    """
    db_path = get_masters_db_path(db_path)
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"masters.db not found at: {db_path}")
        
    bak_path = db_path + ".bak"
    if not os.path.exists(bak_path):
        try:
            shutil.copy2(db_path, bak_path)
        except Exception as e:
            print(f"Warning: Could not create backup {bak_path}: {e}")
            
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    target_capacity = int(target_capacity)
    vip_bonus = int(vip_bonus)
    
    cur.execute("UPDATE master_body_detail SET bag_capacity = MAX(bag_capacity, ?);", (target_capacity,))
    rows_detail = cur.rowcount
    
    cur.execute("UPDATE master_bodylvl_status_value SET bag = MAX(bag, ?);", (target_capacity,))
    rows_lvl = cur.rowcount
    
    cur.execute("UPDATE master_const_int SET value = ? WHERE id = 'VIP_INCREASE_DEATHBAG';", (vip_bonus,))
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "target_capacity": target_capacity,
        "vip_bonus": vip_bonus,
        "rows_detail": rows_detail,
        "rows_lvl": rows_lvl,
        "db_path": db_path
    }

def restore_deathbag_capacity(db_path=None):
    """
    Restores original Death Bag capacity in masters.db using masters.db.original.bak or masters.db.bak.
    """
    db_path = get_masters_db_path(db_path)
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"masters.db not found at: {db_path}")
        
    local_orig = os.path.join(PROJECT_ROOT, "masters.db.original.bak")
    bak_path = db_path + ".bak"
    src_path = local_orig if os.path.exists(local_orig) else (bak_path if os.path.exists(bak_path) else None)
    
    if not src_path or not os.path.exists(src_path):
        raise FileNotFoundError("No original masters.db backup found to restore from.")
        
    src_conn = sqlite3.connect(src_path)
    src_cur = src_conn.cursor()
    orig_details = src_cur.execute("SELECT type, grade, limit_break, bag_capacity FROM master_body_detail;").fetchall()
    orig_lvls = src_cur.execute("SELECT lvl, type, grade, limit_break, bag FROM master_bodylvl_status_value;").fetchall()
    orig_vip_row = src_cur.execute("SELECT value FROM master_const_int WHERE id='VIP_INCREASE_DEATHBAG';").fetchone()
    orig_vip = orig_vip_row[0] if orig_vip_row else 10
    src_conn.close()
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for t, g, lb, cap in orig_details:
        cur.execute("UPDATE master_body_detail SET bag_capacity = ? WHERE type = ? AND grade = ? AND limit_break = ?;", (cap, t, g, lb))
        
    for lvl, t, g, lb, bag in orig_lvls:
        cur.execute("UPDATE master_bodylvl_status_value SET bag = ? WHERE lvl = ? AND type = ? AND grade = ? AND limit_break = ?;", (bag, lvl, t, g, lb))
        
    cur.execute("UPDATE master_const_int SET value = ? WHERE id = 'VIP_INCREASE_DEATHBAG';", (orig_vip,))
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "restored_details": len(orig_details),
        "restored_lvls": len(orig_lvls),
        "vip_bonus": orig_vip,
        "db_path": db_path
    }

def get_all_fighters_info(save):
    uid = get_player_uid(save)
    fighters = save.get("bodyuser", {}).get(uid, [])
    chr_chrs = save.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])
    res = []
    class_map = {
        "BAL": "All-Rounder", "BRE": "Striker", "DEF": "Defender",
        "TEC": "Attacker", "SHT": "Shooter", "COL": "Collector",
        "SKI": "Skill Master", "LUK": "Lucky Star"
    }
    for idx, f in enumerate(fighters):
        c = chr_chrs[idx] if idx < len(chr_chrs) else {}
        cls_code = c.get("type") or f.get("clazz", "BAL")
        cls_name = class_map.get(cls_code, "All-Rounder")
        res.append({
            "cid": f.get("cid", f"cid_{idx}"),
            "name": c.get("name") or f.get("name", f"Luchador #{idx+1}"),
            "class": cls_code,
            "class_name": cls_name,
            "grade": c.get("grade") or f.get("grade", 1),
            "level": f.get("lvl", 1),
            "hp": c.get("hp", 1000),
            "bag": f.get("bag", 0),
            "hp_pts": f.get("hp", 20),
            "stm": f.get("stm", 20),
            "str": f.get("str", 20),
            "dex": f.get("dex", 20),
            "vit": f.get("vit", 20),
            "luk": f.get("luk", 20),
            "die": f.get("die", 0),
            "body": c.get("body", "BODY_MALE_001"),
            "gasmask": c.get("gasmask", "ASSET_NM_GAS_HEAD_001"),
            "limit_break": c.get("limit_break", 0)
        })
    return res

def swap_fighter_positions(save, idx_a, idx_b):
    """
    Swaps the freezer slot positions of two fighters in both bodyuser and soul.chr.chrs.
    """
    uid = get_player_uid(save)
    fighters = save.get("bodyuser", {}).get(uid, [])
    chr_chrs = save.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])
    
    if not (0 <= idx_a < len(fighters) and 0 <= idx_b < len(fighters)):
        return False
    if not (0 <= idx_a < len(chr_chrs) and 0 <= idx_b < len(chr_chrs)):
        return False
    if idx_a == idx_b:
        return True
        
    fighters[idx_a], fighters[idx_b] = fighters[idx_b], fighters[idx_a]
    chr_chrs[idx_a], chr_chrs[idx_b] = chr_chrs[idx_b], chr_chrs[idx_a]
    sync_fighter_slots(save)
    return True

def move_fighter_up(save, idx):
    """
    Moves a fighter one slot up in the Fighter Freezer (towards Slot 1).
    """
    if idx <= 0:
        return False
    return swap_fighter_positions(save, idx, idx - 1)

def move_fighter_down(save, idx):
    """
    Moves a fighter one slot down in the Fighter Freezer (towards Slot N).
    """
    uid = get_player_uid(save)
    fighters = save.get("bodyuser", {}).get(uid, [])
    if idx >= len(fighters) - 1:
        return False
    return swap_fighter_positions(save, idx, idx + 1)


def sync_fighter_slots(save):
    """
    Synchronizes soul.chr.slots with the current bodyuser list.
    Ensures freezer slots 0-9 cleanly reference each fighter's CID.
    """
    uid = get_player_uid(save)
    fighters = save.get("bodyuser", {}).get(uid, [])
    slots = save.setdefault("soul", {}).setdefault("chr", {}).setdefault("slots", {}).setdefault(uid, [])
    while len(slots) < 10:
        slots.append({"uid": int(uid), "slot": len(slots), "cid": ""})
    for s_idx in range(len(slots)):
        slots[s_idx]["slot"] = s_idx
        if s_idx < len(fighters):
            slots[s_idx]["cid"] = fighters[s_idx].get("cid", "")
        else:
            slots[s_idx]["cid"] = ""

def clone_fighter(save, fighter_idx, new_name=None):
    """
    Clones an existing fighter, duplicating stats, grade, limit break, model, and equipped decals.
    Returns (True, new_cid) on success or (False, error_msg) on failure.
    """
    uid = get_player_uid(save)
    fighters = save.get("bodyuser", {}).get(uid, [])
    chr_chrs = save.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])
    
    if len(fighters) >= 10:
        return False, "Freezer is full (Max 10 fighters)"
    if not (0 <= fighter_idx < len(fighters) and 0 <= fighter_idx < len(chr_chrs)):
        return False, "Invalid fighter index"
        
    new_cid = str(uuid.uuid4())
    orig_cid = fighters[fighter_idx].get("cid", "")
    
    new_bu = copy.deepcopy(fighters[fighter_idx])
    new_bu["cid"] = new_cid
    new_bu["die"] = 0
    
    new_ch = copy.deepcopy(chr_chrs[fighter_idx])
    new_ch["cid"] = new_cid
    new_ch["name"] = new_name or f"{new_ch.get('name', 'Luchador')} (Copia)"
    new_ch["state"] = "GUARD"
    new_ch["hp"] = 20000
    
    fighters.append(new_bu)
    chr_chrs.append(new_ch)
    
    # Clone equipped decals in soul.skl.eqskl
    eq_list = save.get("soul", {}).get("skl", {}).get("eqskl", {}).get(uid, [])
    orig_decals = [copy.deepcopy(e) for e in eq_list if e.get("cid") == orig_cid]
    for d in orig_decals:
        d["cid"] = new_cid
        eq_list.append(d)
        
    # Clone deathbag and all equipped equipment (armors, weapons, mushrooms, beasts, items)
    orig_db = save.get("soul", {}).get("deathbag", {}).get(uid, {}).get(orig_cid, [])
    new_db = []
    pts_list = save.setdefault("part", {}).setdefault("pts", {}).setdefault(uid, [])
    msrs_list = get_or_create_list(save.setdefault("mushroom", {}), "msrs")
    bsts_list = get_or_create_list(save.setdefault("beast", {}), "bsts")
    items_list = get_or_create_list(save.setdefault("item", {}), "items")

    for slot_item in orig_db:
        new_slot = copy.deepcopy(slot_item)
        new_slot["cid"] = new_cid
        old_eid = slot_item.get("eid", "")
        item_type = slot_item.get("type", -1)
        
        if old_eid and item_type != -1:
            new_eid = str(uuid.uuid4())
            new_slot["eid"] = new_eid
            
            if item_type == 0:  # Equipment (Weapon or Armor)
                orig_pt = next((p for p in pts_list if p.get("eid") == old_eid), None)
                if orig_pt:
                    new_pt = copy.deepcopy(orig_pt)
                    new_pt["eid"] = new_eid
                    pts_list.append(new_pt)
            elif item_type == 1:  # Mushroom
                orig_m = next((m for m in msrs_list if m.get("eid") == old_eid), None)
                if orig_m:
                    new_m = copy.deepcopy(orig_m)
                    new_m["eid"] = new_eid
                    msrs_list.append(new_m)
            elif item_type == 2:  # Beast
                orig_b = next((b for b in bsts_list if b.get("eid") == old_eid), None)
                if orig_b:
                    new_b = copy.deepcopy(orig_b)
                    new_b["eid"] = new_eid
                    bsts_list.append(new_b)
            elif item_type == 3:  # Material / Item
                orig_i = next((i for i in items_list if i.get("eid") == old_eid), None)
                if orig_i:
                    new_i = copy.deepcopy(orig_i)
                    new_i["eid"] = new_eid
                    items_list.append(new_i)
                    
        new_db.append(new_slot)

    save.setdefault("soul", {}).setdefault("deathbag", {}).setdefault(uid, {})[new_cid] = new_db
    sync_fighter_slots(save)
    _ensure_freezer_accessible(save)
    return True, new_cid


def create_new_fighter(save, name, clazz="BAL", grade=6, body_model="Female 1", max_stats=True):
    """
    Creates a new fighter from scratch with authentic attributes.
    Returns (True, new_cid) on success or (False, error_msg) on failure.
    """
    uid = get_player_uid(save)
    fighters = save.get("bodyuser", {}).get(uid, [])
    chr_chrs = save.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])
    
    if len(fighters) >= 10:
        return False, "Freezer is full (Max 10 fighters)"
        
    new_cid = str(uuid.uuid4())
    
    # Resolve body model and gasmask
    model_map = {
        "Female 1": ("BODY_FEMALE_001", "ASSET_NF_GAS_HEAD_001"),
        "Female 2": ("BODY_FEMALE_002", "ASSET_NF_GAS_HEAD_002"),
        "Female 3": ("BODY_FEMALE_003", "ASSET_NF_GAS_HEAD_003"),
        "Female 4": ("BODY_FEMALE_004", "ASSET_NF_GAS_HEAD_004"),
        "Female 5": ("BODY_FEMALE_005", "ASSET_NF_GAS_HEAD_005"),
        "Female 6": ("BODY_FEMALE_006", "ASSET_NF_GAS_HEAD_006"),
        "Female 7": ("BODY_FEMALE_007", "ASSET_NF_GAS_HEAD_007"),
        "Female 8": ("BODY_FEMALE_008", "ASSET_NF_GAS_HEAD_008"),
        "Male 1": ("BODY_MALE_001", "ASSET_NM_GAS_HEAD_001"),
        "Male 2": ("BODY_MALE_002", "ASSET_NM_GAS_HEAD_002"),
        "Male 3": ("BODY_MALE_003", "ASSET_NM_GAS_HEAD_003"),
        "Male 4": ("BODY_MALE_004", "ASSET_NM_GAS_HEAD_004"),
        "Male 5": ("BODY_MALE_005", "ASSET_NM_GAS_HEAD_005"),
        "Male 6": ("BODY_MALE_006", "ASSET_NM_GAS_HEAD_006"),
        "Male 7": ("BODY_MALE_007", "ASSET_NM_GAS_HEAD_007"),
        "Male 8": ("BODY_MALE_008", "ASSET_NM_GAS_HEAD_008"),
    }
    body_code, gasmask_code = model_map.get(body_model, ("BODY_FEMALE_001", "ASSET_NF_GAS_HEAD_001"))
    if body_model.startswith("BODY_FEMALE_"):
        num_str = body_model.replace("BODY_FEMALE_", "")
        body_code = body_model
        gasmask_code = f"ASSET_NF_GAS_HEAD_{num_str}"
    elif body_model.startswith("BODY_MALE_"):
        num_str = body_model.replace("BODY_MALE_", "")
        body_code = body_model
        gasmask_code = f"ASSET_NM_GAS_HEAD_{num_str}"

    grade_int = int(grade)
    is_tier8 = (grade_int == 6 and max_stats)
    
    if is_tier8:
        lvl = 247
        stat_alloc = 45
        limit_break = 4
        skill = 3
        bag = 3
        rage = 1
        bonus = 20
    else:
        base_lvls = {1: 25, 2: 50, 3: 75, 4: 100, 5: 125, 6: 140}
        base_stats = {1: 10, 2: 15, 3: 20, 4: 25, 5: 30, 6: 30}
        lvl = base_lvls.get(grade_int, 25)
        stat_alloc = base_stats.get(grade_int, 10)
        limit_break = 0
        skill = 0
        bag = 0
        rage = 0
        bonus = 0

    new_bu = {
        "uid": int(uid),
        "cid": new_cid,
        "lvl": lvl,
        "hp": stat_alloc,
        "str": stat_alloc,
        "dex": stat_alloc,
        "vit": stat_alloc,
        "stm": stat_alloc,
        "luk": stat_alloc,
        "skill": skill,
        "bag": bag,
        "rage": rage,
        "hp_bonus": bonus,
        "str_bonus": bonus,
        "dex_bonus": bonus,
        "vit_bonus": bonus,
        "stm_bonus": bonus,
        "luk_bonus": bonus
    }
    new_ch = {
        "uid": int(uid),
        "cid": new_cid,
        "body": body_code,
        "gasmask": gasmask_code,
        "type": clazz,
        "grade": grade_int,
        "limit_break": limit_break,
        "money": 0,
        "spirit": 0,
        "bloodnium": 0,
        "bloodnium_result": "{\"enemy_count\":0,\"bloodnium\":0,\"elapsed_time\":0,\"max_floor_id\":\"\"}",
        "hp": 20000,
        "escdie": 0,
        "total_exp": 0,
        "rest_exp": 0,
        "gain_exp": 0,
        "start_exp": 0,
        "sklgauge": 0,
        "pause": "",
        "abid": "",
        "name": name,
        "state": "GUARD",
        "select_arm_slots": "1,2",
        "hunter_win": -1,
        "hunter_lose": -1,
        "hunter_draw": -1
    }
    
    fighters.append(new_bu)
    chr_chrs.append(new_ch)
    save.setdefault("soul", {}).setdefault("deathbag", {}).setdefault(uid, {})[new_cid] = []
    sync_fighter_slots(save)
    _ensure_freezer_accessible(save)
    return True, new_cid

def delete_fighter(save, fighter_idx):
    """
    Permanently removes a fighter from the Freezer.
    Returns (True, "Deleted") on success or (False, error_msg) on failure.
    """
    uid = get_player_uid(save)
    fighters = save.get("bodyuser", {}).get(uid, [])
    chr_chrs = save.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])
    
    if len(fighters) <= 1:
        return False, "Cannot delete the only fighter on account"
    if not (0 <= fighter_idx < len(fighters) and 0 <= fighter_idx < len(chr_chrs)):
        return False, "Invalid fighter index"
        
    cid = fighters[fighter_idx].get("cid", "")
    if chr_chrs[fighter_idx].get("state") == "USE":
        return False, "Cannot delete the active fighter in use"
        
    fighters.pop(fighter_idx)
    chr_chrs.pop(fighter_idx)
    
    # Remove equipped decals for this cid
    eq_list = save.get("soul", {}).get("skl", {}).get("eqskl", {}).get(uid, [])
    if eq_list:
        save.setdefault("soul", {}).setdefault("skl", {}).setdefault("eqskl", {})[uid] = [e for e in eq_list if e.get("cid") != cid]

    
    # Remove deathbag entry and clean up associated item entities
    db_items = save.get("soul", {}).get("deathbag", {}).get(uid, {}).pop(cid, [])
    del_eids = {item.get("eid") for item in db_items if item.get("eid")}
    if del_eids:
        pts = save.get("part", {}).get("pts", {}).get(uid, [])
        if pts:
            save["part"]["pts"][uid] = [p for p in pts if p.get("eid") not in del_eids]
        msrs = get_or_create_list(save.setdefault("mushroom", {}), "msrs")
        if msrs:
            save["mushroom"]["msrs"] = [m for m in msrs if isinstance(m, dict) and m.get("eid") not in del_eids]
        bsts = get_or_create_list(save.setdefault("beast", {}), "bsts")
        if bsts:
            save["beast"]["bsts"] = [b for b in bsts if isinstance(b, dict) and b.get("eid") not in del_eids]
        items = get_or_create_list(save.setdefault("item", {}), "items")
        if items:
            save["item"]["items"] = [i for i in items if isinstance(i, dict) and i.get("eid") not in del_eids]
            
    sync_fighter_slots(save)
    return True, "Fighter deleted"





