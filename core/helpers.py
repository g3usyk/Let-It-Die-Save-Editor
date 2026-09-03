# -*- coding: utf-8 -*-
import os
import sys
import json
import sqlite3

ALL_DECALS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "all_decals_encyclopedia.json")
ALL_EQUIPMENT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "all_equipment_encyclopedia.json")
TOWER_MAP_DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tower_map_data.json")

_EQUIPMENT_META_CACHE = None
_TOWER_MAP_DATA_CACHE = None

def get_equipment_meta(ptid):
    global _EQUIPMENT_META_CACHE
    if _EQUIPMENT_META_CACHE is None:
        _EQUIPMENT_META_CACHE = {}
        if os.path.exists(ALL_EQUIPMENT_FILE):
            try:
                with open(ALL_EQUIPMENT_FILE, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        _EQUIPMENT_META_CACHE[item["id"]] = item
            except Exception:
                pass
    return _EQUIPMENT_META_CACHE.get(ptid, {})

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
    if custom_path and os.path.exists(custom_path):
        return custom_path
    if save_path:
        candidate = os.path.abspath(os.path.join(os.path.dirname(save_path), "..", "BrgGame", "Content", "masters.db"))
        if os.path.exists(candidate):
            return candidate
    try:
        import save_io
        for d in save_io.get_all_detected_steam_dirs():
            candidate = os.path.abspath(os.path.join(d, "..", "BrgGame", "Content", "masters.db"))
            if os.path.exists(candidate):
                return candidate
    except Exception:
        pass
    local_bak = os.path.join(os.path.dirname(__file__), "masters.db.original.bak")
    if os.path.exists(local_bak):
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

