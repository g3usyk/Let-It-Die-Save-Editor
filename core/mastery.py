# -*- coding: utf-8 -*-
"""
Weapon Mastery (Expert / ABP) Service for LET IT DIE.
Synchronized 100% with the official game database table master_expert_lvl_reward.
"""

from game_data import WEAPON_CATEGORIES
from core.helpers import get_or_create_list

# Authentic level-to-ABP tables from master_expert_lvl_reward
FISTS_ABP_TABLE = {
    1: 0, 2: 5, 3: 100, 4: 200, 5: 300, 6: 400, 7: 550, 8: 750, 9: 1050,
    10: 1400, 11: 1900, 12: 3000, 13: 5000, 14: 8000, 15: 12000, 16: 17000,
    17: 23000, 18: 30000, 19: 38000, 20: 47000
}

WEAPON_ABP_TABLE = {
    1: 0, 2: 5, 3: 100, 4: 200, 5: 300, 6: 400, 7: 550, 8: 700, 9: 850,
    10: 1050, 11: 1250, 12: 1450, 13: 1700, 14: 1950, 15: 2200, 16: 2500,
    17: 2800, 18: 3100, 19: 3450, 20: 3800
}

VALID_DB_WEAPON_TYPES = {wt for wt, _, _ in WEAPON_CATEGORIES}
ENGINE_UNUSED_SLOTS = {'PTARMTP_08', 'PTARMTP_22'}


def get_required_abp(ptarmtp, level):
    lvl = max(1, min(20, int(level)))
    table = FISTS_ABP_TABLE if ptarmtp == "PTARMTP_00" else WEAPON_ABP_TABLE
    return table.get(lvl, 0)


def max_all_weapon_mastery(save, level=20):
    max_weapon_masteries(save, target_lvl=int(level))


def set_weapon_mastery(save, ptarmtp, level=20):
    set_single_weapon_mastery(save, ptarmtp, target_lvl=level)


def max_weapon_masteries(save, target_lvl=20):
    soul = save.setdefault("soul", {})
    expert_list = get_or_create_list(soul, "expert")
    target_lvl = max(1, min(20, int(target_lvl)))

    # First clean up any invalid or duplicate items
    repair_and_sanitize_mastery(save)
    expert_list = soul.get("expert", [])

    existing_map = {}
    for item in expert_list:
        wt = item.get("ptarmtp")
        if wt and wt not in ENGINE_UNUSED_SLOTS and wt in VALID_DB_WEAPON_TYPES:
            existing_map[wt] = item
            item["lvl"] = target_lvl
            item["abp"] = get_required_abp(wt, target_lvl)
            item["is_checked"] = 1

    # Add any authentic weapon categories not yet in the save
    for wt, _, _ in WEAPON_CATEGORIES:
        if wt not in existing_map:
            new_entry = {
                "ptarmtp": wt,
                "abp": get_required_abp(wt, target_lvl),
                "lvl": target_lvl,
                "is_checked": 1
            }
            expert_list.append(new_entry)
            existing_map[wt] = new_entry


def set_single_weapon_mastery(save, ptarmtp, target_lvl, abp=None):
    if ptarmtp in ENGINE_UNUSED_SLOTS:
        return
    soul = save.setdefault("soul", {})
    expert_list = get_or_create_list(soul, "expert")
    target_lvl = max(1, min(20, int(target_lvl)))

    if abp is None:
        abp = get_required_abp(ptarmtp, target_lvl)
    else:
        max_abp = get_required_abp(ptarmtp, 20)
        abp = max(0, min(max_abp, int(abp)))

    for item in expert_list:
        if item.get("ptarmtp") == ptarmtp:
            item["lvl"] = target_lvl
            item["abp"] = int(abp)
            item["is_checked"] = 1
            return

    expert_list.append({
        "ptarmtp": ptarmtp,
        "abp": int(abp),
        "lvl": target_lvl,
        "is_checked": 1
    })


def repair_and_sanitize_mastery(save):
    """
    Sanitizes soul['expert'] against official database rules:
    1. Removes any counterfeit/fictitious ptarmtp entries not present in masters.db.
    2. Keeps unused engine slots (PTARMTP_08, PTARMTP_22) safely at abp: -1, lvl: 1, is_checked: 0.
    3. Clamps levels strictly between 1 and 20.
    4. Ensures ABP is synchronized with level requirements so the game never resets mastery to 0.
    """
    soul = save.setdefault("soul", {})
    expert_list = soul.get("expert")
    if not isinstance(expert_list, list):
        expert_list = []
        soul["expert"] = expert_list
        return 0

    repaired_count = 0
    clean_list = []
    seen = set()

    for item in expert_list:
        if not isinstance(item, dict):
            repaired_count += 1
            continue
        wt = item.get("ptarmtp")
        if not wt or wt in seen:
            repaired_count += 1
            continue
        seen.add(wt)

        if wt in ENGINE_UNUSED_SLOTS:
            if item.get("abp") != -1 or item.get("lvl") != 1 or item.get("is_checked") != 0:
                item["abp"] = -1
                item["lvl"] = 1
                item["is_checked"] = 0
                repaired_count += 1
            clean_list.append(item)
        elif wt in VALID_DB_WEAPON_TYPES:
            lvl = max(1, min(20, int(item.get("lvl", 1))))
            max_abp = get_required_abp(wt, 20)
            req_abp = get_required_abp(wt, lvl)
            cur_abp = int(item.get("abp", 0))

            # Synchronize ABP with level requirements
            target_abp = max(cur_abp, req_abp)
            if target_abp > max_abp:
                target_abp = max_abp
            if cur_abp < req_abp:
                target_abp = req_abp

            if lvl != item.get("lvl") or target_abp != cur_abp:
                repaired_count += 1

            item["lvl"] = lvl
            item["abp"] = target_abp
            item["is_checked"] = 1 if (lvl > 1 or target_abp > 0) else item.get("is_checked", 0)
            clean_list.append(item)
        else:
            # Fake category not in masters.db
            repaired_count += 1

    # Ensure all authentic categories exist
    existing_wts = {e.get("ptarmtp") for e in clean_list}
    for wt, _, _ in WEAPON_CATEGORIES:
        if wt not in existing_wts:
            clean_list.append({
                "ptarmtp": wt,
                "abp": 0,
                "lvl": 1,
                "is_checked": 0
            })
            repaired_count += 1

    # Ensure engine dummy slots exist with authentic -1 values
    for dummy_wt in ("PTARMTP_08", "PTARMTP_22"):
        if dummy_wt not in existing_wts:
            clean_list.append({
                "ptarmtp": dummy_wt,
                "abp": -1,
                "lvl": 1,
                "is_checked": 0
            })
            repaired_count += 1

    def _pt_key(item):
        p = item.get("ptarmtp", "")
        try:
            return int(p.split("_")[-1])
        except Exception:
            return 999

    clean_list.sort(key=_pt_key)
    soul["expert"] = clean_list
    return repaired_count


