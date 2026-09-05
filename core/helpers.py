# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import sqlite3

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALL_DECALS_FILE = os.path.join(PROJECT_ROOT, "all_decals_encyclopedia.json")
ALL_EQUIPMENT_FILE = os.path.join(PROJECT_ROOT, "all_equipment_encyclopedia.json")
TOWER_MAP_DATA_FILE = os.path.join(PROJECT_ROOT, "tower_map_data.json")

_EQUIPMENT_META_CACHE = None
_TOWER_MAP_DATA_CACHE = None

def get_or_create_list(container, key):
    """
    Safely retrieves or normalizes a list under container[key].
    In some LET IT DIE saves, empty collections (or associative arrays)
    are serialized as empty dicts {} instead of [].
    If it's a dict containing item objects with 'eid', converts values to a list.
    Always ensures container[key] is a valid Python list.
    """
    if not isinstance(container, dict):
        return []
    val = container.get(key)
    if isinstance(val, list):
        return val
    elif isinstance(val, dict):
        if val and any(isinstance(v, dict) for v in val.values()):
            new_list = list(val.values())
        else:
            new_list = []
        container[key] = new_list
        return new_list
    else:
        new_list = []
        container[key] = new_list
        return new_list

def repair_save_list_structures(save, uid=None):
    """
    Guarantees all list containers that LET IT DIE engine expects as arrays are valid lists,
    matching the exact repair specification in LID - Save Editor (save_ops.py).
    """
    if not isinstance(save, dict):
        return
    if uid is None:
        uid = str(get_player_uid(save))
    
    soul = save.setdefault("soul", {})
    skl = soul.setdefault("skl", {})
    get_or_create_list(skl, "psskl")
    
    pr = soul.setdefault("partresearch", {})
    get_or_create_list(pr, "user")
    
    gflg = save.setdefault("gameflg", {})
    for sec in ("cl", "sv"):
        get_or_create_list(gflg, sec)
        
    it = save.setdefault("item", {})
    get_or_create_list(it, "items")
    
    pt = save.setdefault("part", {})
    pts = pt.setdefault("pts", {})
    if uid:
        get_or_create_list(pts, uid)
        
    bu = save.setdefault("bodyuser", {})
    if uid:
        get_or_create_list(bu, uid)
        
    chr_root = soul.setdefault("chr", {})
    chrs = chr_root.setdefault("chrs", {})
    slots = chr_root.setdefault("slots", {})
    if uid:
        get_or_create_list(chrs, uid)
        get_or_create_list(slots, uid)
        
    db_root = soul.setdefault("deathbag", {})
    if uid:
        db_user = db_root.setdefault(uid, {})
        for cid in list(db_user.keys()):
            get_or_create_list(db_user, cid)
            
    for k in ("openelvflr", "areaescflag", "msrbook", "bstbook", "unlockfighter", "expert", "cl"):
        get_or_create_list(soul, k)

    # Auto-repair VIP friendship bug: friendship > 1 causes the elevator attendant animation/voice
    # to fail to load, resulting in an infinite loading hang in the Royal Express elevator!
    vip = soul.get("vip", {})
    if isinstance(vip, dict) and vip.get("friendship", 0) > 1:
        vip["friendship"] = 1

    # Auto-repair weapon mastery corruption: ensure expert entries are authentic and ABP is valid
    try:
        from core.mastery import repair_and_sanitize_mastery
        repair_and_sanitize_mastery(save)
    except Exception:
        pass

    # Auto-repair fighters corruption: ensure rage/skill/bag are 0 and HP is authentic
    try:
        from core.fighters import sanitize_fighters
        sanitize_fighters(save)
    except Exception:
        pass

    # Auto-repair Tokyo Death Metro corruption: season reset loop & invasion matchmaking hang
    try:
        from core.tdm import repair_and_sanitize_tdm
        repair_and_sanitize_tdm(save)
    except Exception:
        pass

def get_equipment_meta(ptid):
    global _EQUIPMENT_META_CACHE
    if _EQUIPMENT_META_CACHE is None:
        _EQUIPMENT_META_CACHE = {}
        candidate_paths = [
            ALL_EQUIPMENT_FILE,
            os.path.join(os.path.dirname(sys.executable), "all_equipment_encyclopedia.json"),
            os.path.join(os.path.dirname(sys.executable), "_internal", "all_equipment_encyclopedia.json"),
            os.path.join(getattr(sys, "_MEIPASS", ""), "all_equipment_encyclopedia.json")
        ]
        for p in candidate_paths:
            if p and os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        for item in json.load(f):
                            _EQUIPMENT_META_CACHE[item["id"]] = item
                    if _EQUIPMENT_META_CACHE:
                        break
                except Exception:
                    pass
    return _EQUIPMENT_META_CACHE.get(ptid, {})

_AUTHENTIC_UNCAP_CACHE = None

def get_authentic_uncap_ptids(db_path=None):
    """
    Returns a set of all equipment ptids that authentically uncap in LET IT DIE.
    In the game engine (master_part), uncap items have is_limitbreak == 5,
    reflvllmt == 20, or end with '_G'.
    For these pieces, in-game displayed level is: 4 + research_level.
    Hence, engine level 15 displays as +19 (authentic uncap cap), and engine level 20 displays as +24.
    """
    global _AUTHENTIC_UNCAP_CACHE
    if _AUTHENTIC_UNCAP_CACHE is not None and db_path is None:
        return _AUTHENTIC_UNCAP_CACHE

    uncap_set = set()
    target_db = get_masters_db_path(db_path)
    if os.path.exists(target_db):
        try:
            conn = sqlite3.connect(target_db)
            cur = conn.cursor()
            cur.execute("SELECT id FROM master_part WHERE is_limitbreak = 5 OR reflvllmt = 20 OR id LIKE '%_G'")
            for r in cur.fetchall():
                if r[0]:
                    uncap_set.add(r[0])
            conn.close()
        except Exception:
            pass

    # Fallback from encyclopedia if database cannot be reached
    if not uncap_set:
        global _EQUIPMENT_META_CACHE
        if _EQUIPMENT_META_CACHE is None:
            get_equipment_meta("")
        if _EQUIPMENT_META_CACHE:
            for pid, meta in _EQUIPMENT_META_CACHE.items():
                if pid.endswith("_G"):
                    uncap_set.add(pid)

    if db_path is None and uncap_set:
        _AUTHENTIC_UNCAP_CACHE = uncap_set
    return uncap_set

_FIREARMS_CAPACITY_CACHE = None

def get_firearms_capacity(db_path=None):
    """
    Returns a dict of {ptid: (capacity, spare)} for all authentic ranged firearms,
    launchers, and bows in LET IT DIE from master_part.
    """
    global _FIREARMS_CAPACITY_CACHE
    if _FIREARMS_CAPACITY_CACHE is not None and db_path is None:
        return _FIREARMS_CAPACITY_CACHE

    firearms_dict = {}
    target_db = get_masters_db_path(db_path)
    if os.path.exists(target_db):
        try:
            conn = sqlite3.connect(target_db)
            cur = conn.cursor()
            cur.execute("SELECT id, capacity, spare FROM master_part WHERE id LIKE 'PT_ARM_%' AND capacity > 0")
            for r in cur.fetchall():
                if r[0]:
                    firearms_dict[r[0]] = (int(r[1] or 0), int(r[2] or 0))
            conn.close()
        except Exception:
            pass

    if db_path is None and firearms_dict:
        _FIREARMS_CAPACITY_CACHE = firearms_dict
    return firearms_dict

def get_tower_map_data():
    global _TOWER_MAP_DATA_CACHE
    if _TOWER_MAP_DATA_CACHE is None:
        _TOWER_MAP_DATA_CACHE = {}
        candidate_paths = [
            TOWER_MAP_DATA_FILE,
            os.path.join(os.path.dirname(sys.executable), "tower_map_data.json"),
            os.path.join(os.path.dirname(sys.executable), "_internal", "tower_map_data.json"),
            os.path.join(getattr(sys, "_MEIPASS", ""), "tower_map_data.json")
        ]
        for p in candidate_paths:
            if p and os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        _TOWER_MAP_DATA_CACHE = json.load(f)
                        if _TOWER_MAP_DATA_CACHE:
                            break
                except Exception:
                    pass
    return _TOWER_MAP_DATA_CACHE

def get_player_uid(save):
    """
    Robustly resolves the primary player UID from user, soul, bodyuser, or pts.
    Never hardcodes a developer UID fallback.
    """
    if not isinstance(save, dict):
        return "0"
    user_uid = save.get("user", {}).get("uid")
    if user_uid is not None:
        return str(user_uid)
    soul_uid = save.get("soul", {}).get("uid")
    if soul_uid is not None:
        return str(soul_uid)
    bodyuser = save.get("bodyuser", {})
    if isinstance(bodyuser, dict) and bodyuser:
        return str(next(iter(bodyuser.keys())))
    pts = save.get("part", {}).get("pts", {})
    if isinstance(pts, dict) and pts:
        valid_keys = [k for k in pts.keys() if k != "-1"]
        if valid_keys:
            return str(valid_keys[0])
    return "0"

def get_masters_db_path(custom_path=None, save_path=None):
    """
    Dynamically discovers the authentic masters.db file:
    1. custom_path if provided and exists
    2. Relative to save_path: ../../BrgGame/Content/masters.db
    3. Detected Steam libraries from save_io
    4. Local masters.db.original.bak in project directory
    """
    def _is_valid_db(p):
        return p and os.path.isfile(p) and os.path.getsize(p) > 0

    if custom_path and _is_valid_db(custom_path):
        return custom_path
    if save_path:
        candidate = os.path.abspath(os.path.join(os.path.dirname(save_path), "..", "BrgGame", "Content", "masters.db"))
        if _is_valid_db(candidate):
            return candidate
    try:
        import save_io
        for d in save_io.get_all_detected_steam_dirs():
            candidate = os.path.abspath(os.path.join(d, "..", "BrgGame", "Content", "masters.db"))
            if _is_valid_db(candidate):
                return candidate
    except Exception:
        pass
    local_db = os.path.join(PROJECT_ROOT, "masters.db")
    if _is_valid_db(local_db):
        return local_db
    local_bak = os.path.join(PROJECT_ROOT, "masters.db.original.bak")
    if _is_valid_db(local_bak):
        return local_bak
    return r"E:\SteamLibrary\steamapps\common\LET IT DIE\BrgGame\Content\masters.db"

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
    uid = get_player_uid(save)
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
    raw_it = save.get("item", {}).get("items", [])
    materials_count = len(raw_it) if isinstance(raw_it, (list, dict)) else 0
    raw_msr = save.get("mushroom", {}).get("msrs", [])
    mushrooms_count = len(raw_msr) if isinstance(raw_msr, (list, dict)) else 0
    raw_bst = save.get("beast", {}).get("bsts", [])
    beasts_count = len(raw_bst) if isinstance(raw_bst, (list, dict)) else 0
    
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

def get_account_overview(save):
    """
    Retrieves metadata about the player account, login streaks, and timestamps.
    """
    user = save.get("user", {})
    soul = save.get("soul", {})
    return {
        "uid": user.get("uid", soul.get("uid", "---")),
        "steam_id": user.get("psnacid", "---"),
        "login_count": user.get("login_count", 1),
        "login_streak": user.get("login_keep", 1),
        "created_ts": user.get("created", 0),
        "modified_ts": user.get("modified", 0),
    }

