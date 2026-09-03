import json
import time
import os
import uuid
import sqlite3
from collections import Counter
from game_data import CLASS_CODE_ALIASES

ALL_DECALS_FILE = os.path.join(os.path.dirname(__file__), "all_decals_encyclopedia.json")
ALL_EQUIPMENT_FILE = os.path.join(os.path.dirname(__file__), "all_equipment_encyclopedia.json")

def load_all_known_decals():
    if os.path.exists(ALL_DECALS_FILE):
        try:
            with open(ALL_DECALS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data and isinstance(data, list) and isinstance(data[0], dict):
                    return [d["id"] for d in data if "id" in d]
                return data
        except Exception:
            pass
    return []

def load_all_equipment():
    res = {"weapons": [], "heads": [], "tops": [], "btms": [], "all": []}
    if os.path.exists(ALL_EQUIPMENT_FILE):
        try:
            with open(ALL_EQUIPMENT_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)
                for it in items:
                    it_id = it.get("id")
                    if not it_id:
                        continue
                    res["all"].append(it_id)
                    raw_type = it.get("raw_type", "")
                    if raw_type == "PTTP_HEAD" or "_HEAD_" in it_id:
                        res["heads"].append(it_id)
                    elif raw_type == "PTTP_BODY" or "_TOPS_" in it_id:
                        res["tops"].append(it_id)
                    elif raw_type in ("PTTP_PANTS", "PTTP_LEGS") or "_BTM_" in it_id:
                        res["btms"].append(it_id)
                    else:
                        res["weapons"].append(it_id)
                return res
        except Exception:
            pass
    return res

def get_save_summary(save):
    uid = str(save.get("user", {}).get("uid", "Unknown"))
    user = save.get("user", {})
    soul = save.get("soul", {})
    
    fighters = save.get("bodyuser", {}).get(uid, [])
    dead_fighters = 0
    for f in fighters:
        if f.get("hp", 0) <= 0 or f.get("die", 0) == 1:
            dead_fighters += 1
            
    vip = soul.get("vip", {})
    vip_active = (vip.get("flag", 0) == 1) and (vip.get("expired_time", 0) > time.time())
    
    psskl = soul.get("skl", {}).get("psskl", [])
    total_decals = sum(d.get("cnt", 0) for d in psskl)
    
    pr_list = soul.get("partresearch", {}).get("user", [])
    unique_bps = len(set(r.get("ptid") for r in pr_list if "ptid" in r))
    
    equipment_count = len(save.get("part", {}).get("pts", {}).get(uid, []))
    materials_count = len(save.get("item", {}).get("items", []))
    mushrooms_count = len(save.get("mushroom", {}).get("msrs", []))
    beasts_count = len(save.get("beast", {}).get("bsts", []))
    
    tdm_rank_id = soul.get("tdm_rank", "TDM_RANK_01_01")
    tdm_points = soul.get("tdm_point", 0)
    tdm_name_map = {
        "TDM_RANK_05_03": "Diamante I",
        "TDM_RANK_05_02": "Diamante II",
        "TDM_RANK_05_01": "Diamante III",
        "TDM_RANK_04_03": "Platino I",
        "TDM_RANK_04_02": "Platino II",
        "TDM_RANK_04_01": "Platino III",
        "TDM_RANK_03_03": "Oro I",
        "TDM_RANK_03_02": "Oro II",
        "TDM_RANK_03_01": "Oro III",
        "TDM_RANK_02_03": "Plata I",
        "TDM_RANK_02_02": "Plata II",
        "TDM_RANK_02_01": "Plata III",
        "TDM_RANK_01_03": "Bronce I",
        "TDM_RANK_01_02": "Bronce II",
        "TDM_RANK_01_01": "Bronce III",
    }
    tdm_display = tdm_name_map.get(tdm_rank_id, tdm_rank_id if tdm_rank_id else "Bronce III")
    
    return {
        "player_name": user.get("nm", "Unknown"),
        "uid": uid,
        "player_rank": soul.get("rank", 1),
        "rank_points": soul.get("rank_point", 0),
        "tdm_rank": tdm_display,
        "tdm_rank_id": tdm_rank_id,
        "tdm_points": tdm_points,
        "death_metals_free": user.get("free_medal", 0),
        "death_metals_paid": user.get("paid_medal", 0),
        "death_metals_total": user.get("free_medal", 0) + user.get("paid_medal", 0),
        "kill_coins": soul.get("free_money", 0),
        "splithium": soul.get("spirit", 0),
        "bloodnium": soul.get("bloodnium_point", 0),
        "recycle_points": soul.get("recycle_point", 0),
        "bank_level": soul.get("safe_level", 0),
        "tank_level": soul.get("spirit_tank_level", 0),
        "vip_active": vip_active,
        "vip_days_remaining": max(0, int((vip.get("expired_time", 0) - time.time()) / 86400)),
        "vip_oneday_passes": vip.get("oneday_pass_num", 0),
        "vip_express_passes": vip.get("pass_num", 0),
        "total_fighters": len(fighters),
        "dead_fighters": dead_fighters,
        "unique_decals": len(psskl),
        "total_decals_count": total_decals,
        "unlocked_blueprints_count": unique_bps,
        "death_bag_capacity": soul.get("bag_slot", 20),
        "storage_equipment_count": equipment_count,
        "storage_materials_count": materials_count,
        "storage_items_count": materials_count,
        "storage_mushrooms_count": mushrooms_count,
        "storage_beasts_count": beasts_count
    }

def set_currencies(save, dm=None, kc=None, spl=None, bloodnium=None, re_points=None, safe_lvl=None, tank_lvl=None):
    user = save.setdefault("user", {})
    soul = save.setdefault("soul", {})
    
    if dm is not None:
        user["free_medal"] = int(dm)
        user["paid_medal"] = 0
    if kc is not None:
        soul["free_money"] = int(kc)
        soul["paid_money"] = 0
    if spl is not None:
        soul["spirit"] = int(spl)
    if bloodnium is not None:
        soul["bloodnium_point"] = int(bloodnium)
    if re_points is not None:
        soul["recycle_point"] = int(re_points)
    if safe_lvl is not None:
        soul["safe_level"] = int(safe_lvl)
    if tank_lvl is not None:
        soul["spirit_tank_level"] = int(tank_lvl)

def set_death_metals(save, amount):
    user = save.setdefault("user", {})
    user["free_medal"] = int(amount)
    user["paid_medal"] = 0

def set_kill_coins(save, amount):
    soul = save.setdefault("soul", {})
    soul["free_money"] = int(amount)
    soul["paid_money"] = 0

def set_splithium(save, amount):
    soul = save.setdefault("soul", {})
    soul["spirit"] = int(amount)

def set_bloodnium(save, amount):
    soul = save.setdefault("soul", {})
    soul["bloodnium_point"] = int(amount)

def set_recycle_points(save, amount):
    soul = save.setdefault("soul", {})
    soul["recycle_point"] = int(amount)

def set_player_rank(save, rank=None, rank_point=None):
    soul = save.setdefault("soul", {})
    if rank is not None:
        soul["rank"] = int(rank)
    if rank_point is not None:
        soul["rank_point"] = int(rank_point)

def upgrade_waiting_room(save, bank_level=10, tank_level=10):
    soul = save.setdefault("soul", {})
    soul["safe_level"] = int(bank_level)
    soul["spirit_tank_level"] = int(tank_level)

def max_fighter_level_and_stats(save, fighter_index=0, level=247):
    uid = str(save.get("user", {}).get("uid", "443455"))
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

def max_all_weapon_mastery(save, level=20):
    max_weapon_masteries(save, target_lvl=int(level))

def set_weapon_mastery(save, ptarmtp, level=20):
    set_single_weapon_mastery(save, ptarmtp, target_lvl=level)

def set_vip_pass(save, days=3650, passes=99, oneday_passes=99):
    soul = save.setdefault("soul", {})
    vip = soul.setdefault("vip", {})
    now = int(time.time())
    
    vip["flag"] = 1
    vip["type"] = 1
    vip["pass_num"] = int(passes)
    vip["oneday_pass_num"] = int(oneday_passes)
    vip["expired_time"] = now + (days * 86400)
    vip["automatic_renewal"] = 1
    vip["friendship"] = 100

def max_weapon_masteries(save, target_lvl=20):
    soul = save.setdefault("soul", {})
    expert_list = soul.setdefault("expert", [])
    
    abp_map = {
        1: 0, 5: 500, 10: 2000, 15: 5000, 20: 15000, 25: 35000, 30: 60000
    }
    target_abp = abp_map.get(target_lvl, target_lvl * 1000)
    
    for item in expert_list:
        item["lvl"] = target_lvl
        item["abp"] = max(item.get("abp", 0), target_abp)
        item["is_checked"] = 1

def set_single_weapon_mastery(save, ptarmtp, target_lvl, abp=None):
    soul = save.setdefault("soul", {})
    expert_list = soul.setdefault("expert", [])
    
    if abp is None:
        abp_map = {1: 0, 5: 500, 10: 2000, 15: 5000, 20: 15000, 25: 35000, 30: 60000}
        abp = abp_map.get(target_lvl, target_lvl * 1000)
        
    for item in expert_list:
        if item.get("ptarmtp") == ptarmtp:
            item["lvl"] = int(target_lvl)
            item["abp"] = int(abp)
            item["is_checked"] = 1
            return
            
    expert_list.append({
        "ptarmtp": ptarmtp,
        "abp": int(abp),
        "lvl": int(target_lvl),
        "is_checked": 1
    })

def revive_all_fighters(save):
    uid = str(save.get("user", {}).get("uid", "443455"))
    fighters = save.get("bodyuser", {}).get(uid, [])
    chr_chrs = save.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])
    
    save.get("soul", {})["current_died_cid"] = False
    save.get("soul", {})["die_flag"] = 0
    save.get("soul", {})["resurrection"] = 0
    
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

def update_fighter(save, fighter_idx, name=None, clazz=None, grade=None, lvl=None, hp=None, str_stat=None, dex=None, vit=None, stm=None, luk=None, bag=None, param_hp=None, param_stm=None, param_str=None, param_dex=None, param_vit=None, param_luk=None):
    uid = str(save.get("user", {}).get("uid", "443455"))
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
            # BagAddMax is 3 in the engine; values > 3 cause crash on levelup!
            f["bag"] = min(3, max(0, int(bag)))
            
    if 0 <= fighter_idx < len(chr_chrs):
        c = chr_chrs[fighter_idx]
        if name is not None:
            c["name"] = str(name)
        if clazz is not None:
            # Map any UI aliases to official engine codes
            engine_class = CLASS_CODE_ALIASES.get(str(clazz).upper(), str(clazz).upper())
            if engine_class not in ["BAL", "BRE", "DEF", "TEC", "SHT", "COL", "SKI", "LUK"]:
                engine_class = "BAL"
            c["type"] = engine_class
        if grade is not None:
            c["grade"] = min(6, max(1, int(grade)))
        if lvl is not None:
            c["lvl"] = int(lvl)
        if hp is not None and int(hp) > 45:
            c["hp"] = int(hp)

def add_or_update_decals(save, decal_ids, count=5, premium=True):
    soul = save.setdefault("soul", {})
    skl = soul.setdefault("skl", {})
    psskl = skl.setdefault("psskl", [])
    
    now = int(time.time())
    
    # Fix any legacy invalid IDs in psskl
    for entry in psskl:
        if entry.get("sklid") == "SKL_TANK_P":
            entry["sklid"] = "SKL_HPUP_01_P"
            
    existing = {d.get("sklid"): d for d in psskl}
    
    DECAL_ALIASES = {
        "SKL_TANK": "SKL_HPUP_01",
        "SKL_TANK_P": "SKL_HPUP_01_P",
        "SKL_HEAVY_TANK": "SKL_HPUP_02",
        "SKL_HEAVY_TANK_P": "SKL_HPUP_02_P",
        "SKL_VAMPIRE_01_P": "SKL_DRAIN_01_P",
        "SKL_VAMPIRE_01": "SKL_DRAIN_01",
        "SKL_ARRNG_STATUP_ALL": "SKL_ARRNG_STATUP_ALL_P",
    }
    
    target_ids = set()
    for did in decal_ids:
        raw_id = DECAL_ALIASES.get(did, did)
        if raw_id.endswith("_P"):
            target_ids.add(raw_id)
            if not premium:
                # Also include standard version
                target_ids.add(raw_id[:-2])
        else:
            target_ids.add(raw_id)
            if premium:
                target_ids.add(f"{raw_id}_P")
                
    for tid in target_ids:
        tid = DECAL_ALIASES.get(tid, tid)
        if tid in existing:
            existing[tid]["cnt"] = int(count)
            existing[tid]["updated"] = now
            existing[tid]["is_checked"] = 0
        else:
            new_entry = {
                "sklid": tid,
                "cnt": int(count),
                "updated": now,
                "is_checked": 0
            }
            psskl.append(new_entry)
            existing[tid] = new_entry

def unlock_all_decals(save, count=3, premium=True, include_premium=None):
    if include_premium is not None:
        premium = bool(include_premium)
    all_decals = load_all_known_decals()
    if all_decals:
        add_or_update_decals(save, all_decals, count=count, premium=premium)

DUMMY_OR_CLOSED_PARTS = {
    'PT_ARM_FirstAid', 'PT_ARM_Food', 'PT_ARM_Sand', 'PT_ARM_WP000_001',
    'PT_ARM_WP011_0C1', 'PT_ARM_WP023_001', 'PT_ARM_WP025_0A4',
    'PT_GAS_HEAD_001', 'PT_GAS_HEAD_002', 'PT_GAS_HEAD_003', 'PT_GAS_HEAD_004',
    'PT_GAS_HEAD_005', 'PT_GAS_HEAD_006', 'PT_GAS_HEAD_007', 'PT_GAS_HEAD_008',
    'PT_MASK_001', 'PT_MASK_002', 'PT_MIL_BTM_1003', 'PT_MIL_HEAD_1003',
    'PT_MIL_TOPS_1003', 'PT_NONE_BTM_001', 'PT_NONE_HEAD_001', 'PT_NONE_MASK_001',
    'PT_NONE_PANTS_001', 'PT_NONE_TOPS_001', 'PT_PANTS_001', 'PT_PANTS_002'
}

def repair_and_sanitize_blueprints(save):
    soul = save.setdefault("soul", {})
    pr_dict = soul.setdefault("partresearch", {})
    pr_list = pr_dict.setdefault("user", [])
    
    # Connect to master_part to query authentic evolution links
    next_map = {}
    parent_map = {}
    db_path = r"E:\SteamLibrary\steamapps\common\LET IT DIE\BrgGame\Content\masters.db"
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
            
    repaired_list = []
    repaired_count = 0
    all_known_ptids = set(by_ptid.keys())
    
    for ptid, entries in by_ptid.items():
        if ptid in DUMMY_OR_CLOSED_PARTS:
            continue
            
        entries_by_lvl = {e.get("lvl"): e for e in entries}
        has_next = (ptid in next_map)
        parent = parent_map.get(ptid, "")
        
        # If it's a REMODEL entry, preserve it
        if 1 in entries_by_lvl and entries_by_lvl[1].get("research_type") == "REMODEL":
            repaired_list.append(entries_by_lvl[1])
        else:
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
        
    # Ensure REMODEL entries for all evolving pieces that don't yet exist
    existing_keys = set((e.get("ptid"), e.get("lvl")) for e in repaired_list)
    for ptid in sorted(all_known_ptids):
        nxt = next_map.get(ptid)
        if nxt and (nxt, 1) not in existing_keys:
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
            existing_keys.add((nxt, 1))
            
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

def _assign_to_coin_locker(save, eid, item_type):
    """
    Assigns an entity ID (eid) to the next available slot in soul.cl (Coin Locker).
    Item types:
      0: PART (Equipment / Weapon / Armor)
      1: MUSHROOM
      2: BEAST
      3: ITEM (Material)
    """
    soul = save.setdefault("soul", {})
    cl = soul.setdefault("cl", [])
    
    # Search for an existing empty slot (type == -1 or empty eid)
    for entry in cl:
        if entry.get("type") == -1 or not entry.get("eid"):
            entry["type"] = item_type
            entry["eid"] = eid
            return True
            
    # If no empty slot exists and under capacity limit, append a new slot
    if len(cl) < 10000:
        cl.append({
            "slot": len(cl),
            "type": item_type,
            "eid": eid
        })
        return True
        
    return False

def sync_storage_slots(save):
    """
    Scans all items, mushrooms, beasts, and equipment with owner COIN_LOCKER
    and assigns any orphaned items to empty slots in soul.cl.
    """
    soul = save.setdefault("soul", {})
    cl = soul.setdefault("cl", [])
    assigned_eids = set(c.get("eid") for c in cl if c.get("eid"))
    
    unassigned = []
    for it in save.get("item", {}).get("items", []):
        if isinstance(it, dict) and it.get("owner") == "COIN_LOCKER" and it.get("eid") not in assigned_eids:
            unassigned.append((it.get("eid"), 3))
            
    for m in save.get("mushroom", {}).get("msrs", []):
        if isinstance(m, dict) and m.get("owner") == "COIN_LOCKER" and m.get("eid") not in assigned_eids:
            unassigned.append((m.get("eid"), 1))
            
    for b in save.get("beast", {}).get("bsts", []):
        if isinstance(b, dict) and b.get("owner") == "COIN_LOCKER" and b.get("eid") not in assigned_eids:
            unassigned.append((b.get("eid"), 2))
            
    pts = save.get("part", {}).get("pts", [])
    pts_iter = pts.values() if isinstance(pts, dict) else (pts if isinstance(pts, list) else [])
    for p in pts_iter:
        if isinstance(p, dict) and p.get("owner") == "COIN_LOCKER" and p.get("eid") not in assigned_eids:
            unassigned.append((p.get("eid"), 0))
            
    assigned_count = 0
    cl_idx = 0
    for eid, itype in unassigned:
        while cl_idx < len(cl):
            if cl[cl_idx].get("type") == -1 or not cl[cl_idx].get("eid"):
                cl[cl_idx]["type"] = itype
                cl[cl_idx]["eid"] = eid
                assigned_count += 1
                cl_idx += 1
                break
            cl_idx += 1
        else:
            if len(cl) < 2000:
                cl.append({"slot": len(cl), "type": itype, "eid": eid})
                assigned_count += 1
            else:
                break
    return assigned_count

def add_materials_to_storage(save, item_id, count=20):
    items = save.setdefault("item", {}).setdefault("items", [])
    now = int(time.time())
    added = 0
    for _ in range(count):
        eid = str(uuid.uuid4())
        items.append({
            "eid": eid,
            "gettime": now,
            "itemid": item_id,
            "owner": "COIN_LOCKER"
        })
        if _assign_to_coin_locker(save, eid, 3):
            added += 1
    return added

def add_mushrooms_to_storage(save, msr_id, count=10):
    msrs = save.setdefault("mushroom", {}).setdefault("msrs", [])
    now = int(time.time())
    added = 0
    for _ in range(count):
        eid = str(uuid.uuid4())
        msrs.append({
            "eid": eid,
            "gettime": now,
            "owner": "COIN_LOCKER",
            "msrid": msr_id,
            "eefcid": "",
            "tefcid": "",
            "posonce": 1,
            "state": 0
        })
        if _assign_to_coin_locker(save, eid, 1):
            added += 1
    return added

def add_beasts_to_storage(save, bst_id, count=5):
    bsts = save.setdefault("beast", {}).setdefault("bsts", [])
    now = int(time.time())
    added = 0
    for _ in range(count):
        eid = str(uuid.uuid4())
        bsts.append({
            "eid": eid,
            "gettime": now,
            "owner": "COIN_LOCKER",
            "bstid": bst_id,
            "rwdemsrid": "",
            "state": 0,
            "lvl": 1,
            "posonce": 0
        })
        if _assign_to_coin_locker(save, eid, 2):
            added += 1
    return added

def repair_all_storage_equipment(save):
    pts = save.get("part", {}).get("pts", [])
    pts_iter = pts.values() if isinstance(pts, dict) else (pts if isinstance(pts, list) else [])
    for p in pts_iter:
        if isinstance(p, dict):
            p["dur"] = 50000
            p["rest"] = 0
            p["spare"] = 0

def add_equipment_to_storage(save, ptid, count=1, lvl=5, dur=50000):
    uid_int = int(save.get("user", {}).get("uid", 443455))
    pts_list = save.setdefault("part", {}).setdefault("pts", [])
    if isinstance(pts_list, dict):
        uid_str = str(uid_int)
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

def add_rainbow_bags(save, count=10):
    soul = save.setdefault("soul", {})
    mbags = soul.setdefault("mysterybag", {})
    r_list = mbags.setdefault("RAINBOW", [])
    now = int(time.time())
    
    valid_generators = [
        "MYSTERYBAG_GEN_RAINBOW_106", "MYSTERYBAG_GEN_RAINBOW_107",
        "MYSTERYBAG_GEN_RAINBOW_108", "MYSTERYBAG_GEN_RAINBOW_109",
        "MYSTERYBAG_GEN_RAINBOW_133", "MYSTERYBAG_GEN_RAINBOW_144",
        "MYSTERYBAG_GEN_RAINBOW_145", "MYSTERYBAG_GEN_RAINBOW_147"
    ]
    for i in range(count):
        gen_id = valid_generators[i % len(valid_generators)]
        r_list.append({
            "rarity": "RAINBOW",
            "cntgen": gen_id
        })
    # Also deliver directly into Uncle Death's Reward Box (soul.present)
    send_present_to_reward_box(save, p_type="LOSTBAG", num=count, kind="MYSTERYBAG_RAINBOW", val0="RAINBOW")
    return len(r_list)

def add_all_mystery_bags(save, count_each=10, count_per_type=None):
    if count_per_type is not None:
        count_each = count_per_type
    soul = save.setdefault("soul", {})
    mbags = soul.setdefault("mysterybag", {})
    now = int(time.time())
    for rarity in ["RAINBOW", "PLATINUM", "GOLD", "SILVER", "COPPER"]:
        bag_list = mbags.setdefault(rarity, [])
        for i in range(count_each):
            bag_list.append({
                "rarity": rarity,
                "cntgen": f"MYSTERYBAG_GEN_{rarity}_{now % 1000 + i + 1}"
            })
        send_present_to_reward_box(save, p_type="LOSTBAG", num=count_each, kind=f"MYSTERYBAG_{rarity}", val0=rarity)

def add_mystery_bags(save, count=10):
    add_all_mystery_bags(save, count_each=count)

def unlock_all_tower_elevators(save):
    soul = save.setdefault("soul", {})
    openelv = soul.setdefault("openelvflr", [])
    
    official_elevators = [
        "ELV_MAIN_HUB",
        "ELV_MAIN_AMS_FLR_01", "ELV_MAIN_AMS_FLR_03", "ELV_MAIN_AMS_FLR_05", "ELV_MAIN_AMS_FLR_10",
        "ELV_MAIN_ARC_FLR_01", "ELV_MAIN_ARC_FLR_02", "ELV_MAIN_ARC_FLR_03", "ELV_MAIN_ARC_FLR_06", "ELV_MAIN_ARC_FLR_09", "ELV_MAIN_ARC_FLR_10",
        "ELV_MAIN_MET_FLR_01", "ELV_MAIN_MET_FLR_03", "ELV_MAIN_MET_FLR_04", "ELV_MAIN_MET_FLR_05", "ELV_MAIN_MET_FLR_06", "ELV_MAIN_MET_FLR_08", "ELV_MAIN_MET_FLR_09", "ELV_MAIN_MET_FLR_10",
        "ELV_MAIN_RFT_FLR_01", "ELV_MAIN_RFT_FLR_03",
        "ELV_SUB01_AMS_FLR_02_A", "ELV_SUB01_AMS_FLR_07_A", "ELV_SUB01_ARC_FLR_05", "ELV_SUB01_ARC_FLR_10",
        "ELV_SUB02_AMS_FLR_02_B", "ELV_SUB03_AMS_FLR_02_C", "ELV_SUB1_MET_FLR_02", "ELV_SUB1_MET_FLR_10"
    ]
    
    existing = {e.get("id") for e in openelv if isinstance(e, dict) and "id" in e}
    for elv in official_elevators:
        if elv not in existing:
            openelv.append({"id": elv})
            
    return len(openelv)

def set_all_stamps_perfect(save):
    soul = save.setdefault("soul", {})
    floor = save.setdefault("floor", {})
    stamp_dict = floor.setdefault("stamp", {})
    
    now = int(time.time())
    
    # 1. Complete all 40 tower floor stamps in PERFECT (offset=0)
    stamps = []
    for idx in range(40):
        stamps.append({
            "idx": idx,
            "offset": 0,  # 0 is PERFECT
            "created": now
        })
    stamp_dict["stamps"] = stamps
    stamp_dict["flrstamps"] = {}
    
    # 2. Uncle Death Stamp Multipliers (researchstamp)
    soul["researchstamp"] = [
        {"type": "SLASH", "rate": 2.8},
        {"type": "HIT", "rate": 1.6},
        {"type": "LEGS", "rate": 1.2},
        {"type": "HEAD", "rate": 0.6},
        {"type": "BODY", "rate": 1.4}
    ]
    
    # 3. Unlock Uncle Death's Legendary Scythe in Chokufunsha R&D (PT_ARM_WP050_001)
    pr_list = soul.setdefault("partresearch", {}).setdefault("user", [])
    existing_pr = {(r.get("ptid"), r.get("lvl")): r for r in pr_list if isinstance(r, dict)}
    
    scythe_id = "PT_ARM_WP050_001"
    for lvl in range(1, 5):
        key = (scythe_id, lvl)
        if key not in existing_pr:
            pr_list.append({
                "ptid": scythe_id,
                "lvl": lvl,
                "research_type": "FINISHED",
                "receive_type": "FINISHED",
                "is_announced": 1,
                "is_checked": 1,
                "before_ptid": scythe_id if lvl > 1 else "",
                "before_lvl": lvl - 1 if lvl > 1 else 0
            })
        else:
            existing_pr[key]["research_type"] = "FINISHED"
            existing_pr[key]["receive_type"] = "FINISHED"
            
    # Level 5 (Completed +4, available to purchase in Chokufunsha with Kill Coins)
    key5 = (scythe_id, 5)
    if key5 not in existing_pr:
        pr_list.append({
            "ptid": scythe_id,
            "lvl": 5,
            "research_type": "FINISHED",
            "receive_type": "CHARGE",
            "is_announced": 1,
            "is_checked": 3,
            "before_ptid": scythe_id,
            "before_lvl": 4
        })
    else:
        existing_pr[key5]["research_type"] = "FINISHED"
        existing_pr[key5]["receive_type"] = "CHARGE"
        existing_pr[key5]["is_checked"] = 3
        
    # Deliver 1 unit to Storage
    add_equipment_to_storage(save, scythe_id, count=1, lvl=5, dur=50000)
    
    return len(stamps)

def expand_death_bag(save, slots=50, fighter_index=None):
    # In LET IT DIE, bodyuser['bag'] is the M.I.N.G.O. upgrade stat which has BagAddMax=3.
    # Exceeding 3 causes 'body_deathbag distribute failed' crash on levelup!
    # True deathbag capacity is expanded naturally by Royal Express VIP pass (+10) and Collector class.
    uid = str(save.get("user", {}).get("uid", "443455"))
    fighters = save.get("bodyuser", {}).get(uid, [])
    if fighter_index is not None and 0 <= fighter_index < len(fighters):
        fighters[fighter_index]["bag"] = 3
    else:
        for f in fighters:
            f["bag"] = 3
    save.setdefault("soul", {})["bag_slot"] = int(slots)
    return slots

def set_tdm_rank(save, rank_id="TDM_RANK_05_03", points=5000, rank=None):
    soul = save.setdefault("soul", {})
    now = int(time.time())
    if rank is not None:
        rank_str = str(rank).strip()
        num_map = {
            "1": "TDM_RANK_05_03", "2": "TDM_RANK_05_02", "3": "TDM_RANK_05_01",
            "4": "TDM_RANK_04_03", "5": "TDM_RANK_04_02", "6": "TDM_RANK_04_01",
            "7": "TDM_RANK_03_03", "8": "TDM_RANK_03_02", "9": "TDM_RANK_03_01",
            "10": "TDM_RANK_02_03", "11": "TDM_RANK_02_02", "12": "TDM_RANK_02_01",
            "13": "TDM_RANK_01_03", "14": "TDM_RANK_01_02", "15": "TDM_RANK_01_01",
        }
        if rank_str in num_map:
            rank_id = num_map[rank_str]
        elif rank_str.startswith("TDM_RANK_"):
            rank_id = rank_str
            
    soul["tdm_rank"] = str(rank_id)
    soul["tdm_point"] = int(points)
    soul["last_tdm_rank"] = str(rank_id)
    # Anti-reset: Keep season active for 30 days so the game does not wipe TDM progress on start
    soul["last_tdm_reset_time"] = now + (30 * 86400)

def set_free_continues(save, count=999):
    soul = save.setdefault("soul", {})
    soul["free_continue_count"] = int(count)
    soul["free_continue_max_count"] = int(count)

def send_present_to_reward_box(save, p_type="LOSTBAG", num=10, kind="MYSTERYBAG_RAINBOW", val0="RAINBOW"):
    soul = save.setdefault("soul", {})
    presents = soul.setdefault("present", {})
    if isinstance(presents, list):
        soul["present"] = {}
        presents = soul["present"]
        
    now = int(time.time())
    pid = str(uuid.uuid4())
    
    presents[pid] = {
        "pid": pid,
        "from": "ADMIN",
        "type": str(p_type),
        "num": int(num),
        "created": now,
        "fromval": "TDM Rewards",
        "kind": str(kind),
        "val0": str(val0),
        "val1": "0",
        "val2": "0",
        "val3": "0",
        "val4": "0"
    }
    return len(presents)

def complete_encyclopedia_books(save):
    soul = save.setdefault("soul", {})
    msrbook = soul.setdefault("msrbook", [])
    bstbook = soul.setdefault("bstbook", [])
    
    official_msrs = [
        'MSR_001', 'MSR_007', 'MSR_024', 'MSR_023', 'MSR_016', 'MSR_010', 'MSR_012', 'MSR_013', 'MSR_021', 'MSR_006',
        'MSR_015', 'MSR_025', 'MSR_020', 'MSR_017', 'MSR_009', 'MSR_014', 'MSR_029', 'MSR_022', 'MSR_031', 'MSR_033',
        'MSR_035', 'MSR_037', 'MSR_039', 'MSR_041', 'MSR_043', 'MSR_045', 'MSR_047', 'MSR_049', 'MSR_032', 'MSR_034',
        'MSR_036', 'MSR_038', 'MSR_040', 'MSR_042', 'MSR_044', 'MSR_046', 'MSR_048', 'MSR_050', 'MSR_051', 'MSR_052',
        'MSR_053', 'MSR_200', 'MSR_201', 'MSR_202', 'MSR_300', 'MSR_302', 'MSR_303', 'MSR_304', 'MSR_305', 'MSR_002',
        'MSR_306', 'MSR_307', 'MSR_308', 'MSR_301', 'MSR_309', 'MSR_310', 'MSR_311', 'MSR_312', 'MSR_313', 'MSR_314',
        'MSR_400', 'MSR_401', 'MSR_402'
    ]
    
    official_bsts = [
        'BST_FROG', 'BST_SCORPION', 'BST_RAT', 'BST_BASS', 'BST_SNAIL', 'BST_CRAB', 'BST_PILLBUG', 'BST_LIZARD',
        'BST_HONEYCOMB', 'BST_TURTLE', 'BST_CASSOWARY', 'BST_GFROG', 'BST_GSCORPION', 'BST_GRAT', 'BST_GBASS',
        'BST_GSNAIL', 'BST_GCRAB', 'BST_GPILLBUG', 'BST_GLIZARD', 'BST_GHONEYCOMB', 'BST_GTURTLE', 'BST_GCASSOWARY',
        'BST_SCORPION02', 'BST_BASS02'
    ]
    
    # In LET IT DIE saves, msrbook and bstbook use schema {"id": str, "flag": 5}
    msr_map = {m.get("id"): m for m in msrbook if isinstance(m, dict) and "id" in m}
    for mid in official_msrs:
        if mid not in msr_map:
            entry = {"id": mid, "flag": 5}
            msrbook.append(entry)
            msr_map[mid] = entry
        else:
            msr_map[mid]["flag"] = 5
            
    bst_map = {b.get("id"): b for b in bstbook if isinstance(b, dict) and "id" in b}
    for bid in official_bsts:
        if bid not in bst_map:
            entry = {"id": bid, "flag": 5}
            bstbook.append(entry)
            bst_map[bid] = entry
        else:
            bst_map[bid]["flag"] = 5
            
    return len(msrbook), len(bstbook)

def upgrade_fighter_tier8(save, fighter_idx=0):
    return max_fighter_level_and_stats(save, fighter_index=fighter_idx, level=247)

def analyze_storage_stock(save):
    """
    Returns an analysis of storage slots (used, total, free) and
    the exact stock count of each itemid currently stored in the Coin Locker.
    """
    soul = save.setdefault("soul", {})
    cl = soul.setdefault("cl", [])
    
    cl_eids = set(c.get("eid") for c in cl if c.get("eid") and c.get("type") != -1)
    used_slots = len(cl_eids)
    total_slots = len(cl)
    free_slots = max(0, total_slots - used_slots)
    
    stock_by_id = Counter()
    for it in save.get("item", {}).get("items", []):
        if it.get("eid") in cl_eids:
            stock_by_id[it.get("itemid")] += 1
            
    for m in save.get("mushroom", {}).get("msrs", []):
        if m.get("eid") in cl_eids:
            stock_by_id[m.get("msrid")] += 1
            
    for b in save.get("beast", {}).get("bsts", []):
        if b.get("eid") in cl_eids:
            stock_by_id[b.get("bstid")] += 1
            
    return {
        "total_slots": total_slots,
        "used_slots": used_slots,
        "free_slots": free_slots,
        "stock_by_id": stock_by_id
    }

def analyze_active_recipes_materials(save, db_path=None):
    """
    Analyzes all in-progress R&D recipes (REMODEL, MAP, LEVELUP) in partresearch.user,
    calculates total material requirements, compares against current stock in storage,
    and returns a list of items with their required, in-stock, and deficit quantities.
    """
    if db_path is None:
        default_p = r"E:\SteamLibrary\steamapps\common\LET IT DIE\BrgGame\Content\masters.db"
        local_bak = os.path.join(os.path.dirname(__file__), "masters.db.original.bak")
        if os.path.exists(default_p):
            db_path = default_p
        elif os.path.exists(local_bak):
            db_path = local_bak
        else:
            db_path = default_p
        
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

def smart_supply_missing_materials(save, buffer=0, db_path=None):
    """
    Supplies ONLY the exact deficit quantities required for active R&D recipes.
    Does NOT add anything for materials that already have enough stock.
    Respects free storage slots.
    """
    analysis = analyze_active_recipes_materials(save, db_path)
    free_slots = analysis["storage_free"]
    
    deficit_items = [m for m in analysis["materials"] if m["deficit"] > 0]
    if not deficit_items or free_slots <= 0:
        return 0, 0
        
    added_types = 0
    total_units = 0
    
    for item in deficit_items:
        if free_slots <= 0:
            break
        to_add = item["deficit"] + buffer
        to_add = min(to_add, free_slots)
        if to_add <= 0:
            continue
            
        mat_id = item["itemid"]
        if mat_id.startswith("MSR_"):
            count_added = add_mushrooms_to_storage(save, mat_id, count=to_add)
        elif mat_id.startswith("BST_"):
            count_added = add_beasts_to_storage(save, mat_id, count=to_add)
        else:
            count_added = add_materials_to_storage(save, mat_id, count=to_add)
            
        if count_added > 0:
            added_types += 1
            total_units += count_added
            free_slots -= count_added
            
    return added_types, total_units

def smart_top_up_materials(save, target_qty=10, materials_list=None):
    """
    Tops up materials in materials_list (or all standard materials) up to target_qty.
    If current stock is already >= target_qty, adds 0 (avoids unnecessary excess).
    Respects free storage slots.
    """
    stock_res = analyze_storage_stock(save)
    stock = stock_res["stock_by_id"]
    free_slots = stock_res["free_slots"]
    
    if free_slots <= 0:
        return 0, 0
        
    if materials_list is None:
        # Default: all standard faction metals + base materials
        materials_list = []
        for f in ["DIY", "SPO", "FAN", "MIL"]:
            for t in range(1, 7):
                materials_list.append(f"ITMT_STONE_{f}_{t}")
        for b in ["IRON", "COPPER", "ALUMI", "OIL", "WOOD", "FIBER"]:
            for t in range(1, 6):
                materials_list.append(f"ITMT_{b}_{t}")
                
    added_types = 0
    total_units = 0
    
    for mat_id in materials_list:
        if free_slots <= 0:
            break
        current = stock.get(mat_id, 0)
        needed = max(0, target_qty - current)
        if needed <= 0:
            continue
            
        to_add = min(needed, free_slots)
        if to_add <= 0:
            continue
            
        if mat_id.startswith("MSR_"):
            count_added = add_mushrooms_to_storage(save, mat_id, count=to_add)
        elif mat_id.startswith("BST_"):
            count_added = add_beasts_to_storage(save, mat_id, count=to_add)
        else:
            count_added = add_materials_to_storage(save, mat_id, count=to_add)
            
        if count_added > 0:
            added_types += 1
            total_units += count_added
            free_slots -= count_added
            
    return added_types, total_units

def expand_storage_capacity(save, target_capacity=6000, db_path=None):
    """
    Expands the Coin Locker capacity to target_capacity:
    1. Updates COINLOCKER_EXPAND_LIMIT_COUNT in masters.db.
    2. Expands soul.cl in save to target_capacity slots.
    Returns (old_capacity, new_capacity).
    """
    if db_path is None:
        db_path = r"E:\SteamLibrary\steamapps\common\LET IT DIE\BrgGame\Content\masters.db"
        
    soul = save.setdefault("soul", {})
    cl = soul.setdefault("cl", [])
    old_capacity = len(cl)
    
    target_capacity = int(target_capacity)
    if target_capacity <= old_capacity:
        return old_capacity, old_capacity
        
    # 1. Update masters.db
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("UPDATE master_const_int SET value=? WHERE id='COINLOCKER_EXPAND_LIMIT_COUNT';", (target_capacity,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Warning: Could not update masters.db: {e}")
            
    # 2. Expand soul.cl
    for i in range(old_capacity, target_capacity):
        cl.append({
            "slot": i,
            "type": -1,
            "eid": ""
        })
        
    return old_capacity, target_capacity

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
    
    unlock_map = {}
    for r in pr_u:
        if not isinstance(r, dict):
            continue
        ptid = r.get("ptid")
        rtype = r.get("research_type", "")
        lvl = r.get("lvl", 1)
        
        if rtype == "FINISHED":
            if lvl >= 4:
                unlock_map[ptid] = {"status": "STORE_PLUS4", "lvl": lvl, "label": "⭐ Tienda (+4)"}
            else:
                unlock_map[ptid] = {"status": "FINISHED_LVL", "lvl": lvl, "label": f"⚡ Forja (+{lvl-1})"}
        elif rtype == "REMODEL":
            unlock_map[ptid] = {"status": "REMODEL", "lvl": lvl, "label": "🔨 En I+D (REMODEL)"}
        elif rtype == "MAP":
            unlock_map[ptid] = {"status": "MAP", "lvl": lvl, "label": "🗺️ En I+D (Plano)"}
            
    return unlock_map

def get_player_currencies(save):
    user = save.get("user", {})
    soul = save.get("soul", {})
    return {
        "dm": user.get("free_medal", 0) + user.get("paid_medal", 0),
        "kc": soul.get("free_money", 0) + soul.get("paid_money", 0),
        "spl": soul.get("spirit", 0),
        "bloodnium": soul.get("bloodnium_point", 0),
        "re_points": soul.get("recycle_point", 0),
    }

def get_waiting_room_info(save):
    soul = save.get("soul", {})
    return {
        "bank_level": soul.get("safe_level", 10),
        "tank_level": soul.get("spirit_tank_level", 10),
        "rank": soul.get("rank", 100),
    }

def get_vip_status(save):
    soul = save.get("soul", {})
    vip = soul.get("vip", {})
    exp_time = vip.get("expired_time", 0)
    now = time.time()
    active = (vip.get("flag", 0) == 1) and (exp_time > now)
    days_left = max(0, int((exp_time - now) / 86400))
    exp_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(exp_time)) if exp_time else "---"
    return {
        "active": active,
        "days_left": days_left,
        "expires_at": exp_str,
    }

def get_mystery_bags_summary(save):
    soul = save.get("soul", {})
    mbags = soul.get("mysterybag", {})
    res = {}
    for r in ["RAINBOW", "PLATINUM", "GOLD", "SILVER", "COPPER"]:
        res[r] = len(mbags.get(r, []))
    return res

def get_all_fighters_info(save):
    uid = str(save.get("user", {}).get("uid", "443455"))
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
            "die": f.get("die", 0)
        })
    return res

def max_all_currencies(save):
    set_currencies(save, dm=9999, kc=10000000, spl=10000000, bloodnium=999999, re_points=999999)

def activate_vip_express_pass(save, days=30):
    set_vip_pass(save, days=days)
    return int(time.time()) + (days * 86400)

def add_material_to_storage(save, itemid, count=50):
    if itemid.startswith("MSR_"):
        return add_mushrooms_to_storage(save, itemid, count=count)
    elif itemid.startswith("BST_"):
        return add_beasts_to_storage(save, itemid, count=count)
    else:
        return add_materials_to_storage(save, itemid, count=count)

def add_all_materials_to_storage(save, count=100):
    mat_db_path = os.path.join(os.path.dirname(__file__), "all_materials_db.json")
    if not os.path.exists(mat_db_path):
        mat_db_path = os.path.join(os.path.dirname(__file__), "all_materials_encyclopedia.json")
    if os.path.exists(mat_db_path):
        with open(mat_db_path, "r", encoding="utf-8") as f:
            materials = json.load(f)
        for m in materials:
            add_materials_to_storage(save, m["itemid"], count=count)

def expand_coin_locker_capacity(save, target_capacity=2000):
    return expand_storage_capacity(save, target_capacity=target_capacity)

def add_top_meta_decals(save, count=5):
    top_meta = [
        "SKL_FIGHTER_STUP_01_P",   # Ultimate Fighter
        "SKL_ATKUP_NODMG_P",       # Serial Killer
        "SKL_ATKUP_03_P",          # Golden Gym
        "SKL_SEARCHUP_ITEM_P",     # Treasure Hunter
        "SKL_DRAIN_01_P",          # Vampire
        "SKL_HPUP_02_P",           # Heavy Tank
        "SKL_HPUP_03_P",           # Super Heavy Tank
        "SKL_DEFUP_02_P",          # Diamond
        "SKL_WEP_SPDUP_P",         # Barbarian
        "SKL_HEADSHOTUP_P",        # One Shot One Kill
        "SKL_ATKDEFUP_HPLOW_01_P", # Bull
        "SKL_SPDUP_02_P",          # Marathon Runner
        "SKL_CRIUP_02_P",          # Five-Leaf Clover
        "SKL_SNOWWHITE_P",         # Poison Eater
        "SKL_ATKUP_CRIUP_DEFDWN_P",# Special Unit Captain
        "SKL_ARRNG_STATUP_ALL_P",  # Professional Cosplayer
        "SKL_STRENGTHEN_BODY_01_P",# Joker
        "SKL_RGSPDUP_02_P"         # King of the Wolves
    ]
    add_or_update_decals(save, top_meta, count=count, premium=True)

def unlock_single_blueprint(save, ptid, level=4):
    soul = save.setdefault("soul", {})
    pr_dict = soul.setdefault("partresearch", {})
    pr_list = pr_dict.setdefault("user", [])
    
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
            "before_ptid": ptid if l > 1 else "",
            "before_lvl": l - 1 if l > 1 else 0
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

def unlock_all_elevators(save):
    return unlock_all_tower_elevators(save)

def unlock_all_hub_customizations(save):
    """
    Unlocks all 113 Waiting Room themes, floors, fountains, pillars, posters, and flags
    in save['soul']['hubcustom'], setting locked items (flg: 0) to owned (flg: 1).
    """
    soul = save.setdefault("soul", {})
    hubcustom = soul.setdefault("hubcustom", [])
    
    all_hub_ids = [
        "HUB_CSTM_ET0_AUTUMN", "HUB_CSTM_ET0_NONE", "HUB_CSTM_ET0_SPRING", "HUB_CSTM_ET0_SUMMER", "HUB_CSTM_ET0_WINTER",
        "HUB_CSTM_FLG_BLACK", "HUB_CSTM_FLG_BLOODY", "HUB_CSTM_FLG_BLUE", "HUB_CSTM_FLG_BROKEN", "HUB_CSTM_FLG_DIGITAL",
        "HUB_CSTM_FLG_DOT", "HUB_CSTM_FLG_FLOWER", "HUB_CSTM_FLG_GREEN", "HUB_CSTM_FLG_NONE", "HUB_CSTM_FLG_ORANGE",
        "HUB_CSTM_FLG_PURPLE", "HUB_CSTM_FLG_RED", "HUB_CSTM_FLG_STRIPE", "HUB_CSTM_FLG_YELLOW", "HUB_CSTM_FLR_AUTUMN",
        "HUB_CSTM_FLR_DIY", "HUB_CSTM_FLR_FAN", "HUB_CSTM_FLR_MIL", "HUB_CSTM_FLR_NONE", "HUB_CSTM_FLR_SPRING",
        "HUB_CSTM_FLR_SPT", "HUB_CSTM_FLR_SUMMER", "HUB_CSTM_FLR_WINTER", "HUB_CSTM_FLR_WOT", "HUB_CSTM_FNT_AUTUMN",
        "HUB_CSTM_FNT_DIY", "HUB_CSTM_FNT_FAN", "HUB_CSTM_FNT_MIL", "HUB_CSTM_FNT_NONE", "HUB_CSTM_FNT_SPRING",
        "HUB_CSTM_FNT_SPT", "HUB_CSTM_FNT_SUMMER", "HUB_CSTM_FNT_WINTER", "HUB_CSTM_FNT_WOT", "HUB_CSTM_ILM_AUTUMN",
        "HUB_CSTM_ILM_NONE", "HUB_CSTM_ILM_SPRING", "HUB_CSTM_ILM_SUMMER", "HUB_CSTM_ILM_WINTER", "HUB_CSTM_OBJ_AUTUMN",
        "HUB_CSTM_OBJ_DIY", "HUB_CSTM_OBJ_DVS", "HUB_CSTM_OBJ_FAN", "HUB_CSTM_OBJ_MIL", "HUB_CSTM_OBJ_NONE",
        "HUB_CSTM_OBJ_SPRING", "HUB_CSTM_OBJ_SPT", "HUB_CSTM_OBJ_SUMMER", "HUB_CSTM_OBJ_WINTER", "HUB_CSTM_OBJ_WOT",
        "HUB_CSTM_PLR_AUTUMN", "HUB_CSTM_PLR_DIY", "HUB_CSTM_PLR_FAN", "HUB_CSTM_PLR_MIL", "HUB_CSTM_PLR_NONE",
        "HUB_CSTM_PLR_SPRING", "HUB_CSTM_PLR_SPT", "HUB_CSTM_PLR_SUMMER", "HUB_CSTM_PLR_WINTER", "HUB_CSTM_PLR_WOT",
        "HUB_CSTM_PLT_AUTUMN", "HUB_CSTM_PLT_DIY", "HUB_CSTM_PLT_FAN", "HUB_CSTM_PLT_MIL", "HUB_CSTM_PLT_NONE",
        "HUB_CSTM_PLT_SPRING", "HUB_CSTM_PLT_SPT", "HUB_CSTM_PLT_SUMMER", "HUB_CSTM_PLT_WINTER", "HUB_CSTM_PLT_WOT",
        "HUB_CSTM_PST_AUTUMN", "HUB_CSTM_PST_DIY", "HUB_CSTM_PST_DVS01", "HUB_CSTM_PST_DVS02", "HUB_CSTM_PST_FAN",
        "HUB_CSTM_PST_GC0", "HUB_CSTM_PST_GC1", "HUB_CSTM_PST_GC2", "HUB_CSTM_PST_GC3", "HUB_CSTM_PST_GC4",
        "HUB_CSTM_PST_GC5", "HUB_CSTM_PST_GC6", "HUB_CSTM_PST_MIL", "HUB_CSTM_PST_NONE", "HUB_CSTM_PST_PR",
        "HUB_CSTM_PST_PR02", "HUB_CSTM_PST_PR03", "HUB_CSTM_PST_PR04", "HUB_CSTM_PST_PR05", "HUB_CSTM_PST_PR06",
        "HUB_CSTM_PST_PR07", "HUB_CSTM_PST_SPRING", "HUB_CSTM_PST_SPT", "HUB_CSTM_PST_SUMMER", "HUB_CSTM_PST_UNCLEDEATHAWARD01",
        "HUB_CSTM_PST_UNCLEDEATHAWARD02", "HUB_CSTM_PST_WINTER", "HUB_CSTM_PST_WOT", "HUB_CSTM_WAL_AUTUMN", "HUB_CSTM_WAL_DIY",
        "HUB_CSTM_WAL_FAN", "HUB_CSTM_WAL_MIL", "HUB_CSTM_WAL_NONE", "HUB_CSTM_WAL_SPRING", "HUB_CSTM_WAL_SPT",
        "HUB_CSTM_WAL_SUMMER", "HUB_CSTM_WAL_WINTER", "HUB_CSTM_WAL_WOT"
    ]
    
    existing = {item.get("cstmid"): item for item in hubcustom if isinstance(item, dict)}
    unlocked_count = 0
    
    for cid in all_hub_ids:
        if cid in existing:
            if existing[cid].get("flg", 0) == 0:
                existing[cid]["flg"] = 1
                unlocked_count += 1
        else:
            hubcustom.append({"cstmid": cid, "flg": 1})
            unlocked_count += 1
            
    return len(hubcustom), unlocked_count

def instant_open_deathboxes(save):
    """
    Sets opentime to the past for all timed deathboxes / lost bags, allowing immediate opening.
    """
    soul = save.setdefault("soul", {})
    deathboxes = soul.get("deathbox", [])
    now = int(time.time())
    count = 0
    if isinstance(deathboxes, list):
        for b in deathboxes:
            if isinstance(b, dict) and b.get("opentime", 0) > now:
                b["opentime"] = now - 10
                count += 1
    return count

def reset_wandering_shop_timer(save):
    """
    Resets Gyaku-Funsha secret wandering shop cooldown timer so it reappears immediately.
    """
    soul = save.setdefault("soul", {})
    soul["last_visiting_shop_time"] = 0
    soul["automaticshop_lamp"] = 1
    soul["automaticshop_weekly_lamp"] = 1
    return True

# ================= ADVANCED WEAPON & EQUIPMENT MODIFIERS =================

def set_infinite_durability_all_equipment(save, target_dur=999999):
    """
    Sets extreme durability on all equipment stored in Coin Locker and fighters' bags.
    """
    uid = str(save.get("user", {}).get("uid", "443455"))
    pts_dict = save.setdefault("part", {}).setdefault("pts", {})
    pts_list = pts_dict.setdefault(uid, [])
    
    modified_count = 0
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
    uid = str(save.get("user", {}).get("uid", "443455"))
    pts_dict = save.setdefault("part", {}).setdefault("pts", {})
    pts_list = pts_dict.setdefault(uid, [])
    
    modified_count = 0
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
    Upgrades all equipment in storage to the specified level (e.g. 19 for Tier 4 +19 uncapped).
    """
    uid = str(save.get("user", {}).get("uid", "443455"))
    pts_dict = save.setdefault("part", {}).setdefault("pts", {})
    pts_list = pts_dict.setdefault(uid, [])
    
    modified_count = 0
    for p in pts_list:
        if isinstance(p, dict):
            p["lvl"] = max(p.get("lvl", 1), int(target_lvl))
            modified_count += 1
    return modified_count

# ================= META DECAL PRESETS FOR FIGHTERS =================

DECAL_PRESETS = {
    "tengoku_climber": {
        "name": "Tengoku God Climber (Pisos 51F - 350F+)",
        "decals": [
            "SKL_FIGHTER_STUP_01_P",   # Ultimate Fighter (+10% stats base)
            "SKL_ATKUP_NODMG_P",       # Serial Killer (+100% ataque acumulativo)
            "SKL_ATKUP_03_P",          # Golden Gym (+30% ataque general)
            "SKL_DRAIN_01_P",          # Vampire (7% lifesteal)
            "SKL_HPUP_03_P",           # Super Heavy Tank (+50% HP)
            "SKL_ARRNG_STATUP_ALL_P",  # Professional Cosplayer (Gran boost si llevas set)
            "SKL_STRENGTHEN_BODY_01_P",# Joker (+15% ATK/DEF/Crit)
            "SKL_HEADSHOTUP_P"         # One Shot One Kill (+70% Headshot)
        ]
    },
    "kamas_god": {
        "name": "Tirador KAMAS Definitivo (Full Shooter Meta)",
        "decals": [
            "SKL_HEADSHOTUP_P",        # One Shot One Kill (+70% Headshot)
            "SKL_ATKUP_NODMG_P",       # Serial Killer (+100% ATK)
            "SKL_FIGHTER_STUP_01_P",   # Ultimate Fighter (+10% stats)
            "SKL_ATKUP_03_P",          # Golden Gym (+30% ATK)
            "SKL_WEP_SPDUP_P",         # Barbarian (+20% Two-handed)
            "SKL_CRIUP_02_P",          # Five-Leaf Clover (+20% Crit)
            "SKL_DRAIN_01_P",          # Vampire (Lifesteal)
            "SKL_SEARCHUP_ITEM_P"      # Treasure Hunter (Radar)
        ]
    },
    "melee_melter": {
        "name": "Destructor Melee (Mayal / Machete / Katana)",
        "decals": [
            "SKL_FIGHTER_STUP_01_P",   # Ultimate Fighter (+10% stats)
            "SKL_ATKUP_03_P",          # Golden Gym (+30% ATK)
            "SKL_ATKUP_NODMG_P",       # Serial Killer (+100% ATK)
            "SKL_DRAIN_01_P",          # Vampire (Lifesteal)
            "SKL_HPUP_02_P",           # Heavy Tank (+40% HP)
            "SKL_DEFUP_02_P",          # Diamond (+20% DEF)
            "SKL_STRENGTHEN_BODY_01_P",# Joker (+15% ATK/DEF/Crit)
            "SKL_RGSPDUP_02_P"         # King of the Wolves (Rage generator)
        ]
    },
    "tdm_defense": {
        "name": "Pesadilla de Defensa TDM (Invulnerable Tank)",
        "decals": [
            "SKL_HPUP_03_P",           # Super Heavy Tank (+50% HP)
            "SKL_HPUP_02_P",           # Heavy Tank (+40% HP)
            "SKL_DEFUP_02_P",          # Diamond (+20% DEF)
            "SKL_SNOWWHITE_P",         # Poison Eater (Veneno te cura)
            "SKL_STRENGTHEN_BODY_01_P",# Joker (+15% ATK/DEF/Crit)
            "SKL_ATKDEFUP_HPLOW_01_P", # Bull (+60% ATK & DEF a baja salud)
            "SKL_FIGHTER_STUP_01_P",   # Ultimate Fighter (+10% stats)
            "SKL_ATKUP_CRIUP_DEFDWN_P" # Special Unit Captain (+30% ATK)
        ]
    }
}

def apply_decal_preset_to_inventory(save, preset_key="tengoku_climber", count=5):
    if preset_key not in DECAL_PRESETS:
        preset_key = "tengoku_climber"
    preset = DECAL_PRESETS[preset_key]
    add_or_update_decals(save, preset["decals"], count=count, premium=True)
    return preset["name"], len(preset["decals"])

def equip_decal_preset_on_fighter(save, cid, preset_key="tengoku_climber"):
    """
    Equips the given meta decal preset directly into the active slots
    of the specified fighter (cid). Also adds copies to psskl (inventory)
    so the game does not unequip them upon loading.
    """
    if preset_key not in DECAL_PRESETS:
        preset_key = "tengoku_climber"
    preset = DECAL_PRESETS[preset_key]
    decals = preset["decals"]
    
    # 1. Ensure decals exist in inventory
    add_or_update_decals(save, decals, count=1, premium=True)
    
    # 2. Get body_uid
    body_uid = list(save.get("bodyuser", {}).keys())[0] if save.get("bodyuser") else None
    if not body_uid:
        body_uid = str(save.get("soul", {}).get("uid", "443455"))
        
    soul = save.setdefault("soul", {})
    skl = soul.setdefault("skl", {})
    eqskl = skl.setdefault("eqskl", {})
    user_eq = eqskl.setdefault(body_uid, [])
    
    # Remove existing equipped decals for this cid
    cleaned_eq = [e for e in user_eq if isinstance(e, dict) and e.get("cid") != cid]
    
    # Equip up to 5 decals from preset
    equipped_count = 0
    for idx, did in enumerate(decals[:5]):
        cleaned_eq.append({
            "cid": cid,
            "sklid": did,
            "slot": idx
        })
        equipped_count += 1
        
    eqskl[body_uid] = cleaned_eq
    return preset["name"], equipped_count

# ================= ENDGAME SETS INJECTOR (44CE, JACKALS, TENGOKU) =================

ENDGAME_SETS = {
    "white_steel": {
        "name": "44CE White Steel (D.O.D. Arms)",
        "parts": [
            ("PT_ARM_WP055_001", "Masajeador Estático 44CE (Static Massager)", 5),
            ("PT_ARM_WP002_001", "Bate de Púas +4 (Spike Bat)", 5),
            ("PT_DIY_HEAD_4F_01", "Casco White Steel 44CE", 5),
            ("PT_DIY_TOPS_4F_01", "Peto White Steel 44CE", 5),
            ("PT_DIY_BTM_4F_01", "Pantalones White Steel 44CE", 5),
        ]
    },
    "red_napalm": {
        "name": "44CE Red Napalm (War Ensemble)",
        "parts": [
            ("PT_ARM_WP056_001", "Lanzador M2G-87 Red Napalm (Spike Launcher)", 5),
            ("PT_MIL_HEAD_4F_01", "Casco Red Napalm 44CE", 5),
            ("PT_MIL_TOPS_4F_01", "Peto Red Napalm 44CE", 5),
            ("PT_MIL_BTM_4F_01", "Pantalones Red Napalm 44CE", 5),
        ]
    },
    "black_thunder": {
        "name": "44CE Black Thunder (Candle Wolf)",
        "parts": [
            ("PT_ARM_WP057_001", "Espada de Energía 44CE (Energy Sword)", 5),
            ("PT_FAN_HEAD_4F_01", "Casco Black Thunder 44CE", 5),
            ("PT_FAN_TOPS_4F_01", "Peto Black Thunder 44CE", 5),
            ("PT_FAN_BTM_4F_01", "Pantalones Black Thunder 44CE", 5),
        ]
    },
    "pale_wind": {
        "name": "44CE Pale Wind (M.I.L.K.)",
        "parts": [
            ("PT_ARM_WP058_001", "Vara de Fuerza 44CE (Force Wand)", 5),
            ("PT_SPO_HEAD_4F_01", "Casco Pale Wind 44CE", 5),
            ("PT_SPO_TOPS_4F_01", "Peto Pale Wind 44CE", 5),
            ("PT_SPO_BTM_4F_01", "Pantalones Pale Wind 44CE", 5),
        ]
    },
    "jackals_gear": {
        "name": "Sets Jackals v1 / v2 / v3",
        "parts": [
            ("PT_ARM_WP001_JAC_11", "Espada Jackal X", 5),
            ("PT_ARM_WP016_JAC_11", "Pistola Jackal Y (Blaster)", 5),
            ("PT_ARM_WP027_JAC_11", "Yo-Yo Jackal Z", 5),
            ("PT_JAC_HEAD_101", "Casco Jackal X", 5),
            ("PT_JAC_TOPS_101", "Traje Jackal X", 5),
            ("PT_JAC_BTM_101", "Pantalón Jackal X", 5),
            ("PT_JAC_HEAD_102", "Casco Jackal Y", 5),
            ("PT_JAC_TOPS_102", "Traje Jackal Y", 5),
            ("PT_JAC_BTM_102", "Pantalón Jackal Y", 5),
            ("PT_JAC_HEAD_103", "Casco Jackal Z", 5),
            ("PT_JAC_TOPS_103", "Traje Jackal Z", 5),
            ("PT_JAC_BTM_103", "Pantalón Jackal Z", 5),
        ]
    },
    "tengoku_weapons": {
        "name": "Armas Legendarias de Tengoku (51F+)",
        "parts": [
            ("PT_ARM_WP060_001", "Muspelheim (Ballesta de Fuego Tengoku)", 5),
            ("PT_ARM_WP061_001", "Judgement Day (Francotirador Tengoku)", 5),
            ("PT_ARM_WP062_001", "Predator (Machete Tengoku)", 5),
            ("PT_ARM_WP063_001", "Emperor (Lanzagranadas Tengoku)", 5),
            ("PT_ARM_WP064_001", "Lethal Weapon (KAMAS Tengoku)", 5),
        ]
    }
}

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

def complete_all_quests(save):
    """
    Marks all official quests as cleared (clrcnt = 1) so rewards can be claimed in the game.
    """
    soul = save.setdefault("soul", {})
    quest_dict = soul.setdefault("quest", {})
    user_quests = quest_dict.setdefault("user", [])
    
    db_path = os.path.join(os.path.dirname(__file__), "masters.db.original.bak")
    qids = []
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT qid FROM master_quest;")
            qids = [r[0] for r in c.fetchall()]
            conn.close()
        except Exception:
            pass
            
    existing_map = {q.get("qid"): q for q in user_quests if isinstance(q, dict) and "qid" in q}
    
    completed_count = 0
    if qids:
        for qid in qids:
            if qid in existing_map:
                existing_map[qid]["ordcnt"] = 1
                existing_map[qid]["clrcnt"] = 1
            else:
                user_quests.append({"qid": qid, "ordcnt": 1, "clrcnt": 1})
            completed_count += 1
    else:
        for q in user_quests:
            if isinstance(q, dict):
                q["ordcnt"] = 1
                q["clrcnt"] = 1
                completed_count += 1
            
    return completed_count

def unlock_all_magazines(save):
    """
    Sets all 36 Uncle Death comic and Yotsuyama magazine issues to read (status 2).
    """
    soul = save.setdefault("soul", {})
    mag = soul.setdefault("magazine", {})
    mag["status_list"] = ",".join(["2"] * 36)
    return 36

def unlock_all_radio_music(save):
    """
    Unlocks and powers on the Waiting Room Radio Jukebox with full access.
    """
    soul = save.setdefault("soul", {})
    radio = soul.setdefault("radio", {})
    user = radio.setdefault("user", {})
    user["channel"] = "000"
    user["power"] = 1
    radio["rank"] = {
        "rank1": "SN_BGM_Radio_Music_0001",
        "rank2": "SN_BGM_Radio_Music_0002",
        "rank3": "SN_BGM_Radio_Music_0003",
        "rank4": "SN_BGM_Radio_Music_0004",
        "rank5": "SN_BGM_Radio_Music_0005"
    }
    return True
