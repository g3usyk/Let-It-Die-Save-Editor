# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import sqlite3
from core.helpers import get_tower_map_data, get_player_uid, get_masters_db_path, PROJECT_ROOT, get_or_create_list
from core.blueprints import add_equipment_to_storage


def unlock_all_tower_elevators(save):
    """
    Completely unlocks all 61 official elevators, unlocks the full Tower map (all 980 rooms & 1,119 escalators),
    opens all 122 one-way tower gates, unlocks the Waiting Room gate to Floor 41+ (Hazama) and Tengoku 51+,
    and sets playlog max_floor to 51.
    """
    soul = save.setdefault("soul", {})
    now = int(time.time())
    
    # 1. Unlocks all 61 official elevators in soul["openelvflr"]
    openelv = get_or_create_list(soul, "openelvflr")
    official_elevators = [
        "ELV_MAIN_HUB",
        "ELV_MAIN_AMS_FLR_01", "ELV_MAIN_AMS_FLR_03", "ELV_MAIN_AMS_FLR_05", "ELV_MAIN_AMS_FLR_07", "ELV_MAIN_AMS_FLR_10",
        "ELV_MAIN_ARC_FLR_01", "ELV_MAIN_ARC_FLR_02", "ELV_MAIN_ARC_FLR_03", "ELV_MAIN_ARC_FLR_06", "ELV_MAIN_ARC_FLR_09", "ELV_MAIN_ARC_FLR_10",
        "ELV_MAIN_MET_FLR_01", "ELV_MAIN_MET_FLR_03", "ELV_MAIN_MET_FLR_04", "ELV_MAIN_MET_FLR_05", "ELV_MAIN_MET_FLR_06", "ELV_MAIN_MET_FLR_08", "ELV_MAIN_MET_FLR_09", "ELV_MAIN_MET_FLR_10",
        "ELV_MAIN_RFT_FLR_01", "ELV_MAIN_RFT_FLR_03", "ELV_MAIN_RFT_FLR_06", "ELV_MAIN_RFT_FLR_07", "ELV_MAIN_RFT_FLR_09", "ELV_MAIN_RFT_FLR_10",
        "ELV_MAIN_HZM_FLR_01", "ELV_MAIN_HVN_FLR_01",
        "ELV_SUB01_AMS_FLR_02_A", "ELV_SUB01_AMS_FLR_05_A", "ELV_SUB01_AMS_FLR_07_A",
        "ELV_SUB01_ARC_FLR_05", "ELV_SUB01_ARC_FLR_10",
        "ELV_SUB02_AMS_FLR_02_B", "ELV_SUB02_AMS_FLR_06_B", "ELV_SUB02_AMS_FLR_09_B", "ELV_SUB02_AMS_FLR_10_B",
        "ELV_SUB03_AMS_FLR_02_C", "ELV_SUB03_AMS_FLR_09_C",
        "ELV_SUB04_AMS_FLR_02_C", "ELV_SUB04_AMS_FLR_07_C",
        "ELV_SUB05_AMS_FLR_02_D", "ELV_SUB05_AMS_FLR_05_D", "ELV_SUB05_AMS_FLR_07_D", "ELV_SUB05_AMS_FLR_09_D",
        "ELV_SUB1_MET_FLR_02", "ELV_SUB1_MET_FLR_10",
        "ELV_SUB2_MET_FLR_03_B", "ELV_SUB2_MET_FLR_08_B",
        "ELV_SUB_A01_RFT_FLR_04", "ELV_SUB_A01_RFT_FLR_08",
        "ELV_SUB_B01_RFT_FLR_04", "ELV_SUB_B01_RFT_FLR_09",
        "ELV_SUB_C01_RFT_FLR_01", "ELV_SUB_C01_RFT_FLR_08",
        "ELV_SUB_C02_RFT_FLR_03", "ELV_SUB_C02_RFT_FLR_10",
        "ELV_SUB_D01_RFT_FLR_03", "ELV_SUB_D01_RFT_FLR_06",
        "ELV_SUB_D02_RFT_FLR_07", "ELV_SUB_D02_RFT_FLR_09"
    ]
    existing_elvs = {e.get("id") for e in openelv if isinstance(e, dict) and "id" in e}
    for elv in official_elevators:
        if elv not in existing_elvs:
            openelv.append({"id": elv})

    # 2. Unlock all 980 Tower Rooms on Map in soul["areaflag"]
    t_data = get_tower_map_data()
    room_indices = t_data.get("room_indices", [])
    areaflag = get_or_create_list(soul, "areaflag")
    existing_rooms = {a.get("idx"): a for a in areaflag if isinstance(a, dict) and "idx" in a}
    for r_idx in room_indices:
        if r_idx not in existing_rooms:
            areaflag.append({"idx": r_idx, "val": 33})
        else:
            cur_val = existing_rooms[r_idx].get("val", 33)
            # Clear lock bit 64 (0x40) so no padlocks remain on visited rooms
            clean_val = cur_val & ~64
            existing_rooms[r_idx]["val"] = max(clean_val, 33)

    # 3. Unlock all 1,119 Escalators on Map in soul["areaescflag"]
    esc_indices = t_data.get("escalator_indices", [])
    areaescflag = get_or_create_list(soul, "areaescflag")
    existing_escs = {a.get("idx"): a for a in areaescflag if isinstance(a, dict) and "idx" in a}
    for e_idx in esc_indices:
        if e_idx not in existing_escs:
            areaescflag.append({"idx": e_idx, "val": 7})
        else:
            existing_escs[e_idx]["val"] = max(existing_escs[e_idx].get("val", 0), 7)

    # 4. Register Tower Exploration Progress in playlog (Floors 1 to 51)
    playlog = save.setdefault("playlog", {})
    base = playlog.setdefault("base", {})
    if base.get("max_floor", 0) < 51:
        base["max_floor"] = 51

    # 5. Unlock all 122 Tower Gates & Story Progression Flags in gameflg["cl"]
    gameflg = save.setdefault("gameflg", {})
    cl = get_or_create_list(gameflg, "cl")
    existing_flags = {f.get("var"): f for f in cl if isinstance(f, dict)}

    # Gates (RELEASE_GATE)
    for g_var in t_data.get("gate_flags", []):
        if g_var in existing_flags:
            existing_flags[g_var]["value"] = 1
            existing_flags[g_var]["modified"] = now
        else:
            cl.append({"var": g_var, "value": 1, "modified": now})

    # Progression flags (KGF_GAME_CLEAR, KGF_HZM_FIRST_TIME_ENTRANCE_GATE, etc.)
    for p_var in t_data.get("progression_flags", []):
        if p_var in existing_flags:
            existing_flags[p_var]["value"] = 1
            existing_flags[p_var]["modified"] = now
        else:
            cl.append({"var": p_var, "value": 1, "modified": now})

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
    pr_list = get_or_create_list(soul.setdefault("partresearch", {}), "user")
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

def set_free_continues(save, count=999):
    soul = save.setdefault("soul", {})
    soul["free_continue_count"] = int(count)
    soul["free_continue_max_count"] = int(count)

def complete_encyclopedia_books(save):
    soul = save.setdefault("soul", {})
    msrbook = get_or_create_list(soul, "msrbook")
    bstbook = get_or_create_list(soul, "bstbook")
    
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

def unlock_all_elevators(save):
    return unlock_all_tower_elevators(save)

def unlock_all_hub_customizations(save):
    """
    Unlocks all 113 Waiting Room themes, floors, fountains, pillars, posters, and flags
    in save['soul']['hubcustom'], setting locked items (flg: 0) to owned (flg: 1).
    """
    soul = save.setdefault("soul", {})
    hubcustom = get_or_create_list(soul, "hubcustom")
    
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

def complete_all_quests(save):
    """
    Marks all authentic current quests as cleared (clrcnt = 1) so rewards can be claimed.
    If the save has active quest records in quest.dis, it strictly completes only those recognized
    quests. This prevents injecting 6,000+ obsolete or foreign event quests from masters.db,
    which causes the game engine to freeze in an infinite loop during escalator/floor transitions.
    """
    soul = save.setdefault("soul", {})
    quest_dict = soul.setdefault("quest", {})
    user_quests = get_or_create_list(quest_dict, "user")
    
    dis = quest_dict.get("dis", {})
    valid_qids = set(dis.keys()) if isinstance(dis, dict) and dis else None
    
    db_path = get_masters_db_path()
    if not os.path.exists(db_path):
        fallback_bak = os.path.join(PROJECT_ROOT, "masters.db.original.bak")
        if os.path.exists(fallback_bak):
            db_path = fallback_bak
            
    qids = []
    if valid_qids:
        qids = list(valid_qids)
    elif os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT qid FROM master_quest WHERE qid NOT LIKE '%COL%' AND qid NOT LIKE '%EVT%';")
            rows = c.fetchall()
            qids = [r[0] for r in rows if r and r[0]]
            if not qids:
                c.execute("SELECT qid FROM master_quest LIMIT 100;")
                qids = [r[0] for r in c.fetchall() if r and r[0]]
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

def reset_floor_to_waiting_room(save):
    """
    Rescues a fighter stuck in an infinite elevator/escalator loading loop
    by safely resetting floor.rlg and associated active floor caches back to Waiting Room state.
    """
    floor = save.setdefault("floor", {})
    floor["rlg"] = {"user": {}, "archive": {}}
    floor["pop"] = {'item': {}, 'trbox': {}, 'msr': {}, 'bst': {}, 'mbs': {}, 'ffm': {}, 'vm': {}, 'xzmb': {}, 'xzk': {}}
    floor["dust"] = []
    floor["closed_area_flags"] = {}
    return True

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

def get_tower_playlog(save):
    """
    Retrieves Tower exploration records and play statistics from save['playlog']['base'].
    """
    pl = save.get("playlog", {}).get("base", {})
    sec = pl.get("total_play_time", 0)
    hours = round(sec / 3600.0, 1)
    return {
        "max_floor": pl.get("max_floor", 40),
        "playtime_hours": hours,
        "playtime_seconds": sec,
        "interruptions": pl.get("interruption", 0),
        "elevators": pl.get("elevator_cnt", 0),
        "escalators": pl.get("escalator_cnt", 0),
        "materials_collected": pl.get("total_get_material_cnt", 0),
        "weapons_collected": pl.get("total_get_weapon_cnt", 0),
        "armors_collected": pl.get("total_get_armor_cnt", 0),
        "researches": pl.get("total_research_cnt", 0),
        "boss_kills": pl.get("circle_crusher", 0)
    }

def set_tower_max_floor(save, max_floor=51):
    """
    Sets the maximum floor reached in the Tower of Barbs (e.g. 40, 51 Tengoku, 100+).
    """
    playlog = save.setdefault("playlog", {})
    base = playlog.setdefault("base", {})
    base["max_floor"] = int(max_floor)
    return int(max_floor)

def reset_tower_interruptions(save):
    """
    Clears all tower disconnection / force shutdown penalty counters, protecting fighters.
    """
    playlog = save.setdefault("playlog", {})
    base = playlog.setdefault("base", {})
    old_cnt = base.get("interruption", 0)
    base["interruption"] = 0
    save["force_shutdown_counts"] = 0
    return old_cnt

