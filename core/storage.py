# -*- coding: utf-8 -*-
import os
import json
import uuid
import time
import sqlite3
from collections import Counter
from core.helpers import get_player_uid, get_masters_db_path

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
    # Also deliver directly into Uncle Death's in-game Reward Box (soul.deathbox)
    send_present_to_reward_box(save, p_type="LOSTBAG", num=count, kind="MYSTERYBAG_RAINBOW", val0="RAINBOW", rarity="RAINBOW")
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
        send_present_to_reward_box(save, p_type="LOSTBAG", num=count_each, kind=f"MYSTERYBAG_{rarity}", val0=rarity, rarity=rarity)

def add_mystery_bags(save, count=10):
    add_all_mystery_bags(save, count_each=count)

def send_present_to_reward_box(save, p_type="LOSTBAG", num=10, kind="MYSTERYBAG_RAINBOW", val0="RAINBOW", rarity="RAINBOW"):
    soul = save.setdefault("soul", {})
    deathbox = soul.get("deathbox")
    if not isinstance(deathbox, list):
        deathbox = []
        soul["deathbox"] = deathbox
        
    now = int(time.time())
    p_type_up = str(p_type).upper().strip()
    
    if "LOST" in p_type_up or "BAG" in p_type_up:
        actual_rarity = str(val0 or rarity or "RAINBOW").upper()
        for _ in range(max(1, int(num))):
            deathbox.append({
                "bid": "",
                "rarity": actual_rarity,
                "type": "LOSTBAG",
                "created": now,
                "opentime": now - 10,
                "num": 1,
                "val0": actual_rarity,
                "val1": "",
                "val2": "",
                "val3": ""
            })
    elif "SPL" in p_type_up or "SPIRIT" in p_type_up:
        deathbox.append({
            "bid": "",
            "rarity": "NONE",
            "type": "SPIRIT",
            "created": now,
            "opentime": now - 10,
            "num": int(num),
            "val0": "",
            "val1": "",
            "val2": "",
            "val3": ""
        })
    elif "DM" in p_type_up or "MEDAL" in p_type_up:
        user = save.setdefault("user", {})
        user["free_medal"] = min(99999, user.get("free_medal", 0) + int(num))
        deathbox.append({
            "bid": "",
            "rarity": "GOLD",
            "type": "MONEY",
            "created": now,
            "opentime": now - 10,
            "num": int(num) * 5000,
            "val0": "",
            "val1": "",
            "val2": "",
            "val3": ""
        })
    elif "MONEY" in p_type_up or "KC" in p_type_up or "COIN" in p_type_up:
        deathbox.append({
            "bid": "",
            "rarity": "NONE",
            "type": "MONEY",
            "created": now,
            "opentime": now - 10,
            "num": int(num),
            "val0": "",
            "val1": "",
            "val2": "",
            "val3": ""
        })
    elif "MUSHROOM" in p_type_up or "MSR" in p_type_up:
        deathbox.append({
            "bid": "",
            "rarity": str(rarity or "SILVER"),
            "type": "MUSHROOM",
            "created": now,
            "opentime": now - 10,
            "num": max(1, int(num)),
            "val0": str(val0 or "MSR_043"),
            "val1": "",
            "val2": "",
            "val3": ""
        })
    else:
        deathbox.append({
            "bid": "",
            "rarity": str(rarity or "NONE"),
            "type": str(p_type),
            "created": now,
            "opentime": now - 10,
            "num": int(num),
            "val0": str(val0),
            "val1": "",
            "val2": "",
            "val3": ""
        })

    # Keep soul.present populated for legacy systems
    presents = soul.setdefault("present", {})
    if isinstance(presents, dict):
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
        
    return len(deathbox)

def sync_mystery_bags_to_deathbox(save):
    """
    Transfers any uncollected Mystery Bags from soul.mysterybag into soul.deathbox
    so they immediately appear in Uncle Death's in-game Reward Box in the Waiting Room.
    Returns number of bags transferred.
    """
    soul = save.setdefault("soul", {})
    mbags = soul.get("mysterybag", {})
    if not mbags:
        return 0
        
    deathbox = soul.get("deathbox")
    if not isinstance(deathbox, list):
        deathbox = []
        soul["deathbox"] = deathbox
        
    now = int(time.time())
    transferred = 0
    for rarity, items in mbags.items():
        if isinstance(items, list) and items:
            for _ in items:
                deathbox.append({
                    "bid": "",
                    "rarity": str(rarity),
                    "type": "LOSTBAG",
                    "created": now,
                    "opentime": now - 10,
                    "num": 1,
                    "val0": str(rarity),
                    "val1": "",
                    "val2": "",
                    "val3": ""
                })
                transferred += 1
            mbags[rarity] = []
            
    return transferred

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

def smart_supply_missing_materials(save, buffer=0, db_path=None):
    """
    Supplies ONLY the exact deficit quantities required for active R&D recipes.
    Does NOT add anything for materials that already have enough stock.
    Respects free storage slots.
    """
    from core.blueprints import analyze_active_recipes_materials
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
    Adjusts the Coin Locker capacity to target_capacity (both expanding and safely shrinking):
    1. Extracts all occupied items (type != -1 or eid != "").
    2. Guarantees target_capacity >= len(occupied) so no player items are lost.
    3. Re-indexes occupied items and pads/trims empty slots to target_capacity.
    4. Updates COINLOCKER_EXPAND_LIMIT_COUNT in masters.db.
    Returns (old_capacity, new_capacity).
    """
    db_path = get_masters_db_path(db_path)
        
    soul = save.setdefault("soul", {})
    cl = soul.setdefault("cl", [])
    old_capacity = len(cl)
    
    target_capacity = int(target_capacity)
    
    # 1. Identify occupied items vs empty slots
    occupied = [item for item in cl if item.get("type", -1) != -1 or item.get("eid", "") != ""]
    min_required = len(occupied)
    
    if target_capacity < min_required:
        target_capacity = min_required
        
    # 2. Rebuild soul.cl: occupied items first, then empty slots up to target_capacity
    new_cl = []
    for i, item in enumerate(occupied):
        item["slot"] = i
        new_cl.append(item)
        
    for i in range(len(occupied), target_capacity):
        new_cl.append({
            "slot": i,
            "type": -1,
            "eid": ""
        })
        
    soul["cl"] = new_cl
    new_capacity = len(new_cl)
    
    # 3. Update masters.db
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("UPDATE master_const_int SET value=? WHERE id='COINLOCKER_EXPAND_LIMIT_COUNT';", (new_capacity,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Warning: Could not update masters.db: {e}")
            
    return old_capacity, new_capacity

def get_mystery_bags_summary(save):
    soul = save.get("soul", {})
    mbags = soul.get("mysterybag", {})
    res = {}
    for r in ["RAINBOW", "PLATINUM", "GOLD", "SILVER", "COPPER"]:
        res[r] = len(mbags.get(r, []))
    return res

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

