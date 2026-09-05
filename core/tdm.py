# -*- coding: utf-8 -*-
import os
import sys
import json
import time
from core.helpers import get_player_uid, get_or_create_list, PROJECT_ROOT
from core.currencies import get_rank_points_for_rank

TEAMHATE_FILE = os.path.join(PROJECT_ROOT, "teamhate_template.json")
DUMMY_TEMPLATE_FILE = os.path.join(PROJECT_ROOT, "tdm_dummy_template.json")
DUMMY_DEFENDERS_TEMPLATE_FILE = os.path.join(PROJECT_ROOT, "tdm_dummy_defenders_template.json")


def calculate_player_rank(save):
    """
    Calculates authentic player rank according to the official Let It Die formula:
    [(Highest Fighter Grade - 1) * 15] + (Number of fighters of that grade)
    Maximum attainable rank in the game is 115.
    """
    uid = str(get_player_uid(save))
    fighters = save.get("bodyuser", {}).get(uid, [])
    chr_chrs = save.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])

    grades = []
    for c in chr_chrs:
        if isinstance(c, dict) and "grade" in c:
            grades.append(int(c["grade"]))
    if not grades:
        for f in fighters:
            if isinstance(f, dict) and "grade" in f:
                grades.append(int(f["grade"]))

    if not grades:
        return 1

    max_grade = max(grades)
    count_of_max = grades.count(max_grade)
    rank = (max_grade - 1) * 15 + count_of_max
    return min(115, max(1, rank))


def repair_and_sanitize_tdm(save):
    """
    Auto-repairs Tokyo Death Metro (TDM) corruption:
    1. Fixes TDM Season Reset Loop popup:
       Maintains an active future season timestamp (now + 30 days) and ensures last_tdm_rank is valid.
    2. Fixes infinite black screen on invasion:
       - Clears active crashed fort state (deffending_lock: 0, auid: 0, ouid: 0, expire: 0).
       - Clears soul['pause'] = "" and soul['relief_point'] = "".
       - Removes foreign dummy keys from bodyuser, part.pts, and fortmatch.
       - Restores authentic verified TDM dummies to dummy.user from tdm_dummy_template.json.
       - Ensures fortmatch[uid] only contains valid targets present in dummy.user.
       - Ensures fortzmbsetting is a valid list with defending fighters.
    3. Fixes infinite loading screen when searching for invasion/raid targets:
       - Ensures soul['is_fort_ready'] = 1 (Waiting room defense ready).
       - Ensures soul['team_id'] is assigned (default: 52 Mexico if unset).
       - Normalizes fortzmbsetting, fortresult, teamhate, shpprd, screenshot, unlockfighter to arrays.
       - Restores authentic 344-relationship teamhate table if missing or corrupted.
       - Fixes tdmsituation items where data == "{}" -> "[]".
       - Clamps Player Rank to authentic formula bounds (max 115).
    """
    if not isinstance(save, dict):
        return

    uid = str(get_player_uid(save))
    soul = save.setdefault("soul", {})
    now = int(time.time())

    # 1. Season reset loop protection
    if soul.get("is_fort_ready") != 1:
        soul["is_fort_ready"] = 1

    last_reset = soul.get("last_tdm_reset_time", 0)
    if not isinstance(last_reset, (int, float)) or last_reset <= now:
        soul["last_tdm_reset_time"] = now + (30 * 86400)

    soul["tdm_rank"] = "TDM_RANK_01_01"
    soul["last_tdm_rank"] = "TDM_RANK_01_01"
    soul["tdm_point"] = 50

    # 2. Reset stuck raid lock & crash pause flags
    fort = save.setdefault("fort", {})
    fort["auid"] = 0
    fort["ouid"] = 0
    fort["expire"] = 0
    fort["sbhp"] = 0
    fort["sbmoney"] = 0
    fort["sthp"] = 0
    fort["stspirit"] = 0
    fort["deffending_lock"] = 0

    soul["pause"] = ""
    soul["relief_point"] = ""

    # Sanitize fortorder (removes corrupted isabduct: 1 if captive missing, and guarantees contiguous orders)
    if "fortorder" in save and isinstance(save["fortorder"], dict):
        fo = save["fortorder"]
        for f_uid, orders in fo.items():
            if isinstance(orders, list):
                # Filter out captive spawns if no captive is in abduct
                valid_orders = [o for o in orders if isinstance(o, dict) and (o.get("isabduct") != 1 or len(save.get("abduct", [])) > 0)]
                # Ensure orders in each waveidx are strictly contiguous: 0, 1, 2, ...
                # UE3 Array indexing crashes at 0x12dbbf5 if there is an order index gap!
                by_wave = {}
                for o in valid_orders:
                    w = o.get("waveidx", 0)
                    by_wave.setdefault(w, []).append(o)
                sorted_orders = []
                for w in sorted(by_wave.keys()):
                    by_wave[w].sort(key=lambda x: x.get("order", 0))
                    for idx, o in enumerate(by_wave[w]):
                        o["order"] = idx
                    sorted_orders.extend(by_wave[w])
                fo[f_uid] = sorted_orders

    # 3. Team membership
    raw_tid = soul.get("team_id")
    try:
        team_id = int(raw_tid)
    except (ValueError, TypeError):
        team_id = 52
    if team_id < 1 or team_id > 164:
        team_id = 52
    soul["team_id"] = str(team_id)
    soul["favorite_team"] = str(team_id)

    tm = save.setdefault("teammember", {})
    if isinstance(tm, dict):
        tm["tid"] = team_id
        if not tm.get("created"):
            tm["created"] = int(now)
        tm["modified"] = int(now)

    # 4. Player rank mathematical sanity
    cur_rank = soul.get("rank", 1)
    legit_rank = calculate_player_rank(save)
    if not isinstance(cur_rank, int) or cur_rank > 115 or cur_rank <= 0 or cur_rank != legit_rank:
        soul["rank"] = legit_rank
        soul["rank_point"] = get_rank_points_for_rank(legit_rank)
    elif soul.get("rank_point", 0) > get_rank_points_for_rank(legit_rank):
        soul["rank_point"] = get_rank_points_for_rank(legit_rank)

    # 5. Restore authentic dummy defenders (bodies, chrs, equipment, decals)
    # The offline PC engine requires negative UIDs (-1..-13) in bodyuser, soul.chr.chrs,
    # part.pts, and soul.skl.eqskl to spawn defenders. If stripped, fort generate zombie
    # aborts and the subway train hangs forever!
    save["abduct"] = []
    soul["prison"] = {}

    candidate_defender_paths = [
        DUMMY_DEFENDERS_TEMPLATE_FILE,
        os.path.join(os.path.dirname(sys.executable), "tdm_dummy_defenders_template.json"),
        os.path.join(os.path.dirname(sys.executable), "_internal", "tdm_dummy_defenders_template.json"),
        os.path.join(getattr(sys, "_MEIPASS", ""), "tdm_dummy_defenders_template.json")
    ]
    loaded_template = None
    for dp in candidate_defender_paths:
        if dp and os.path.exists(dp):
            try:
                with open(dp, "r", encoding="utf-8") as f:
                    loaded_template = json.load(f)
                break
            except Exception:
                pass

    bu = save.setdefault("bodyuser", {})
    pts = save.setdefault("part", {}).setdefault("pts", {})
    chrs = soul.setdefault("chr", {}).setdefault("chrs", {})
    eqskl = soul.setdefault("skl", {}).setdefault("eqskl", {})

    if loaded_template and isinstance(loaded_template, dict):
        dummy_users = loaded_template.get("user", [])
        save.setdefault("dummy", {})["user"] = dummy_users

        for k, v in loaded_template.get("bodyuser", {}).items():
            bu[k] = v
        for k, v in loaded_template.get("chr_chrs", {}).items():
            chrs[k] = v
        for k, v in loaded_template.get("part_pts", {}).items():
            pts[k] = v
        for k, v in loaded_template.get("eqskl", {}).items():
            eqskl[k] = v

        valid_defender_uids = {uid} | set(loaded_template.get("bodyuser", {}).keys())
    else:
        valid_defender_uids = {uid} | {str(k) for k in bu.keys() if str(k).startswith("-")}
        dummy_users = save.setdefault("dummy", {}).get("user", [])

    # Clean foreign UIDs that are not the player and not recognized dummy defenders
    for d in [bu, pts, chrs, eqskl]:
        for k in list(d.keys()):
            if str(k) not in valid_defender_uids:
                del d[k]


    fm = save.setdefault("fortmatch", {})
    for k in list(fm.keys()):
        if str(k) != uid:
            del fm[k]

    if "deathbag" in soul:
        for k in list(soul["deathbag"].keys()):
            if str(k) != uid:
                del soul["deathbag"][k]

    if "relationship" in soul and "revenge" in soul["relationship"]:
        for k in list(soul["relationship"]["revenge"].keys()):
            if str(k) != uid:
                del soul["relationship"]["revenge"][k]

    # 6. Ensure fortmatch[uid] contains valid targets matching active dummy.user
    get_or_create_list(fm, uid)
    target_candidates = [u["uid"] for u in dummy_users if isinstance(u, dict) and "uid" in u and str(u["uid"]) in bu]
    if not target_candidates:
        target_candidates = [u["uid"] for u in dummy_users if isinstance(u, dict) and "uid" in u]
    if target_candidates:
        fm[uid] = [{"uid": t_uid, "expire": now + (14 * 86400)} for t_uid in target_candidates[:8]]

    # 8. List normalization for TDM containers
    fzs = get_or_create_list(save, "fortzmbsetting")
    if len(fzs) == 0:
        chr_chrs = save.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])
        for idx, c_item in enumerate(chr_chrs):
            if isinstance(c_item, dict) and c_item.get("state") != "USE" and len(fzs) < 9:
                fzs.append({
                    "wave": 0,
                    "order": len(fzs),
                    "cid": c_item.get("cid", ""),
                    "body": c_item.get("body", "BODY_FEMALE_001"),
                    "grade": c_item.get("grade", 6),
                    "type": c_item.get("type", "BAL"),
                    "lvl": c_item.get("lvl", 247),
                    "max_limit_break": c_item.get("limit_break", 4),
                    "is_equip_whistle": 0
                })

    get_or_create_list(save, "fortresult")
    get_or_create_list(save, "shpprd")
    get_or_create_list(soul, "screenshot")
    get_or_create_list(soul, "unlockfighter")

    # 9. teamhate table
    th = save.get("teamhate")
    if not isinstance(th, list) or len(th) == 0:
        candidate_paths = [
            TEAMHATE_FILE,
            os.path.join(os.path.dirname(sys.executable), "teamhate_template.json"),
            os.path.join(os.path.dirname(sys.executable), "_internal", "teamhate_template.json"),
            os.path.join(getattr(sys, "_MEIPASS", ""), "teamhate_template.json")
        ]
        loaded = False
        for p in candidate_paths:
            if p and os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        save["teamhate"] = json.load(f)
                    loaded = True
                    break
                except Exception:
                    pass
        if not loaded:
            save["teamhate"] = []

    # 10. tdmsituation repair
    tdm_sit = save.get("tdmsituation")
    if isinstance(tdm_sit, list):
        for item in tdm_sit:
            if isinstance(item, dict) and item.get("data") == "{}":
                item["data"] = "[]"
