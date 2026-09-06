# -*- coding: utf-8 -*-
"""
Save Slots & Profile Manager for LET IT DIE Save Editor.
Provides isolated multi-slot save storage, deep metadata extraction (haters, floor, coins),
and dedicated per-slot historical backup archives.
"""

import os
import sys
import json
import time
import shutil
import save_io

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if getattr(sys, "frozen", False):
    APP_DATA_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    APP_DATA_DIR = PROJECT_ROOT

PROJECT_SLOTS_DIR = os.path.join(APP_DATA_DIR, "SaveSlots")
ACTIVE_SLOT_FILE = os.path.join(PROJECT_SLOTS_DIR, "active_slot.json")
TOTAL_SLOTS = 10


def ensure_slots_directory():
    """Ensures the root SaveSlots directory and slot folders exist."""
    if not os.path.exists(PROJECT_SLOTS_DIR):
        os.makedirs(PROJECT_SLOTS_DIR, exist_ok=True)
    for i in range(1, TOTAL_SLOTS + 1):
        s_dir = get_slot_dir(i)
        os.makedirs(s_dir, exist_ok=True)
        os.makedirs(os.path.join(s_dir, "backups"), exist_ok=True)


def get_active_slot():
    """Returns the currently active slot number (1-10) or None if none recorded."""
    if os.path.exists(ACTIVE_SLOT_FILE):
        try:
            with open(ACTIVE_SLOT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                num = data.get("active_slot")
                if isinstance(num, int) and 1 <= num <= TOTAL_SLOTS:
                    return num
        except Exception:
            pass
    return None


def set_active_slot(slot_num):
    """Persists the active slot number (1-10). Pass None to clear."""
    ensure_slots_directory()
    try:
        if slot_num is None:
            if os.path.exists(ACTIVE_SLOT_FILE):
                os.remove(ACTIVE_SLOT_FILE)
        else:
            with open(ACTIVE_SLOT_FILE, "w", encoding="utf-8") as f:
                json.dump({"active_slot": slot_num, "updated_at": time.time()}, f, indent=2)
    except Exception:
        pass


def get_slot_dir(slot_num):
    """Returns the absolute directory path for a specific slot number (1-10)."""
    return os.path.join(PROJECT_SLOTS_DIR, f"slot_{slot_num:02d}")


def get_slot_save_path(slot_num):
    """Returns the path to savedata.sav within the slot."""
    return os.path.join(get_slot_dir(slot_num), "savedata.sav")


def get_slot_backups_dir(slot_num):
    """Returns the path to the backups directory for a slot."""
    return os.path.join(get_slot_dir(slot_num), "backups")


def get_slot_meta_path(slot_num):
    """Returns the path to slot_meta.json within the slot."""
    return os.path.join(get_slot_dir(slot_num), "slot_meta.json")


def extract_save_metadata(save_data):
    """
    Extracts comprehensive game metadata from decoded save data:
    - Player name, Steam ID, and UID
    - Active fighter name, class, grade, level
    - Tower max floor reached (from playlog.base.max_floor)
    - Haters eliminated (from playlog.kill.kill_PlayerEnemy_cnt)
    - Currencies: Kill Coins, Death Metals, SPLithium, Bloodnium
    - Playtime in hours
    """
    if not isinstance(save_data, dict):
        return {}

    user = save_data.get("user", {})
    soul = save_data.get("soul", {})
    uid = str(user.get("uid") or soul.get("uid") or "1")

    fighters = save_data.get("bodyuser", {}).get(uid, [])
    chr_chrs = soul.get("chr", {}).get("chrs", {}).get(uid, [])

    # Identify currently active fighter or first fighter
    f_active = None
    c_active = None

    if chr_chrs and isinstance(chr_chrs, list):
        for idx, c in enumerate(chr_chrs):
            if isinstance(c, dict) and c.get("state") == "USE":
                c_active = c
                if idx < len(fighters):
                    f_active = fighters[idx]
                break

    if not c_active and chr_chrs and isinstance(chr_chrs, list) and isinstance(chr_chrs[0], dict):
        c_active = chr_chrs[0]
        if fighters and isinstance(fighters, list) and isinstance(fighters[0], dict):
            f_active = fighters[0]

    f_active = f_active or {}
    c_active = c_active or {}

    pl = save_data.get("playlog", {})
    pl_base = pl.get("base", {})
    pl_kill = pl.get("kill", {})

    total_play_sec = pl_base.get("total_play_time", 0)
    play_hrs = round(total_play_sec / 3600.0, 1)

    max_floor = pl_base.get("max_floor", 1)
    haters_killed = pl_kill.get("kill_PlayerEnemy_cnt", 0)
    total_enemies = pl_kill.get("total_enemy_cnt", 0)

    kc = soul.get("free_money", 0)
    dm = user.get("free_medal", 0) + user.get("paid_medal", 0)
    spl = soul.get("spirit", 0)
    bl = soul.get("bloodnium_point", 0)
    re_pts = soul.get("recycle_point", 0)

    fighter_name = c_active.get("name") or f_active.get("name") or "Fighter 1"
    fighter_class = str(c_active.get("type", "BAL")).upper()
    fighter_grade = c_active.get("grade", 1)
    fighter_lvl = f_active.get("lvl") or c_active.get("lvl") or 1

    return {
        "player_name": user.get("nm", "Senpai"),
        "steam_id": str(user.get("psnacid", "---")),
        "uid": uid,
        "fighter_name": fighter_name,
        "fighter_class": fighter_class,
        "fighter_grade": fighter_grade,
        "fighter_lvl": fighter_lvl,
        "max_floor": max_floor,
        "haters_killed": haters_killed,
        "total_enemies": total_enemies,
        "kill_coins": kc,
        "death_metals": dm,
        "splithium": spl,
        "bloodnium": bl,
        "recycle_points": re_pts,
        "playtime_hours": play_hrs,
        "playtime_seconds": total_play_sec,
        "total_fighters": len(fighters) if isinstance(fighters, list) else 0,
        "bag_slots": soul.get("bag_slot", 20),
        "rank": soul.get("rank", 1),
        "tdm_rank": soul.get("tdm_rank", "TDM_RANK_01_01"),
        "last_saved": time.strftime("%Y-%m-%d %H:%M:%S")
    }


def find_matching_slot(save_data):
    """
    Finds a slot number matching the given save data by comparing UID and Steam ID.
    If multiple match, returns the recorded active slot if among them, or the first match.
    """
    if not isinstance(save_data, dict):
        return None
    meta = extract_save_metadata(save_data)
    t_uid = meta.get("uid")
    t_steam = meta.get("steam_id")
    if not t_uid and not t_steam:
        return None

    active_num = get_active_slot()
    matching_slots = []

    for i in range(1, TOTAL_SLOTS + 1):
        slot_info = get_slot_info(i)
        if slot_info["is_empty"]:
            continue
        s_meta = slot_info.get("meta", {})
        if t_steam and s_meta.get("steam_id") == t_steam:
            matching_slots.append(i)
        elif t_uid and s_meta.get("uid") == t_uid:
            matching_slots.append(i)

    if not matching_slots:
        return None

    if active_num in matching_slots:
        return active_num
    return matching_slots[0]


def get_backup_metadata(bak_path):
    """
    Extracts summary metadata for a backup (.bak) file.
    Returns dict with fighter_name, max_floor, haters_killed, currencies, date_str.
    """
    if not os.path.exists(bak_path):
        return {}
    try:
        data, ver = save_io.decompress_save(bak_path)
        meta = extract_save_metadata(data)
        st = os.stat(bak_path)
        meta["mtime"] = st.st_mtime
        meta["date_str"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime))
        meta["size_kb"] = st.st_size // 1024
        return meta
    except Exception as e:
        return {"error": str(e)}


def get_slot_info(slot_num, force_refresh=False):
    """
    Returns information and metadata about a specific slot.
    Uses cached slot_meta.json if valid, or extracts directly from savedata.sav.
    """
    ensure_slots_directory()
    save_path = get_slot_save_path(slot_num)
    meta_path = get_slot_meta_path(slot_num)
    backups_dir = get_slot_backups_dir(slot_num)

    # Check if slot has a save file
    is_empty = not (os.path.exists(save_path) and os.path.getsize(save_path) > 0)
    
    # Count backups
    backups = []
    if os.path.exists(backups_dir):
        for f in sorted(os.listdir(backups_dir), reverse=True):
            if f.endswith(".bak"):
                fp = os.path.join(backups_dir, f)
                try:
                    st = os.stat(fp)
                    is_orig = "ORIGINAL" in f
                    is_session = "_session_" in f
                    backups.append({
                        "filename": f,
                        "path": fp,
                        "size": st.st_size,
                        "mtime": st.st_mtime,
                        "date_str": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)),
                        "is_original": is_orig,
                        "is_session": is_session
                    })
                except Exception:
                    pass

    # Sort backups: ORIGINAL first, then newest descending
    backups.sort(key=lambda b: (0 if b["is_original"] else 1, -b["mtime"]))

    if is_empty:
        return {
            "slot_num": slot_num,
            "slot_id": f"slot_{slot_num:02d}",
            "is_empty": True,
            "save_path": save_path,
            "backups_dir": backups_dir,
            "backups_count": len(backups),
            "backups": backups,
            "meta": {}
        }

    # If occupied, read or regenerate metadata
    meta = {}
    save_mtime = os.path.getmtime(save_path)
    meta_valid = False

    if not force_refresh and os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
                if meta.get("file_mtime") == save_mtime:
                    meta_valid = True
        except Exception:
            meta_valid = False

    if not meta_valid:
        try:
            data, ver = save_io.decompress_save(save_path)
            meta = extract_save_metadata(data)
            meta["file_mtime"] = save_mtime
            meta["save_version"] = ver
            meta["file_size_kb"] = os.path.getsize(save_path) // 1024
            # Cache meta
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
        except Exception as e:
            meta = {
                "player_name": "Corrupted / Unreadable",
                "error": str(e),
                "file_size_kb": os.path.getsize(save_path) // 1024,
                "last_saved": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(save_mtime))
            }

    return {
        "slot_num": slot_num,
        "slot_id": f"slot_{slot_num:02d}",
        "is_empty": False,
        "save_path": save_path,
        "backups_dir": backups_dir,
        "backups_count": len(backups),
        "backups": backups,
        "meta": meta
    }


def get_all_slots(force_refresh=False):
    """Returns a list of all 10 slots with their metadata."""
    ensure_slots_directory()
    return [get_slot_info(i, force_refresh=force_refresh) for i in range(1, TOTAL_SLOTS + 1)]


def save_current_to_slot(save_json, save_version, slot_num):
    """
    Saves the provided save data into the specified slot (1-10),
    creates a rolling backup in the slot's backups folder, and caches metadata.
    """
    ensure_slots_directory()
    slot_save_path = get_slot_save_path(slot_num)
    backups_dir = get_slot_backups_dir(slot_num)

    # 1. If an existing save was in the slot, create an automated rolling backup first
    if os.path.exists(slot_save_path) and os.path.getsize(slot_save_path) > 0:
        create_slot_backup(slot_num)

    # 2. Write save atomically
    save_io.save_to_file(save_json, slot_save_path, version=save_version, make_backup=False)

    # 3. Create initial ORIGINAL.bak for this slot if not existing
    orig_bak = os.path.join(backups_dir, f"slot_{slot_num:02d}.ORIGINAL.bak")
    if not os.path.exists(orig_bak):
        try:
            shutil.copyfile(slot_save_path, orig_bak)
        except Exception:
            pass

    # 4. Extract and cache metadata
    meta = extract_save_metadata(save_json)
    meta["file_mtime"] = os.path.getmtime(slot_save_path)
    meta["save_version"] = save_version
    meta["file_size_kb"] = os.path.getsize(slot_save_path) // 1024

    meta_path = get_slot_meta_path(slot_num)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    set_active_slot(slot_num)
    return get_slot_info(slot_num, force_refresh=True)


def load_slot_to_active(slot_num, active_target_path):
    """
    Loads a slot's savedata.sav into the active Steam save location.
    Backs up the current active save before overwriting.
    Returns (True, data, ver) or (False, error_msg, None).
    """
    slot_save = get_slot_save_path(slot_num)
    if not os.path.exists(slot_save) or os.path.getsize(slot_save) == 0:
        return False, "Slot is empty", None

    if not active_target_path:
        return False, "No active save path provided", None

    try:
        # Create safety backup of active save before overwriting
        if os.path.exists(active_target_path):
            save_io.create_backup(active_target_path)

        # Copy slot save to active target path atomically
        shutil.copyfile(slot_save, active_target_path)
        data, ver = save_io.decompress_save(active_target_path)
        set_active_slot(slot_num)
        return True, data, ver
    except Exception as e:
        return False, str(e), None


def create_slot_backup(slot_num, tag=None):
    """
    Creates a timestamped backup inside the slot's backups directory.
    Enforces rolling retention of up to 25 backups (preserving ORIGINAL.bak).
    """
    slot_save = get_slot_save_path(slot_num)
    backups_dir = get_slot_backups_dir(slot_num)

    if not os.path.exists(slot_save) or os.path.getsize(slot_save) == 0:
        return None

    os.makedirs(backups_dir, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    bak_filename = f"slot_{slot_num:02d}_{tag}_{ts}.bak" if tag else f"slot_{slot_num:02d}_{ts}.bak"
    bak_path = os.path.join(backups_dir, bak_filename)

    shutil.copyfile(slot_save, bak_path)

    # Rolling retention: keep 25 most recent regular backups
    baks = [f for f in os.listdir(backups_dir) if f.endswith(".bak") and not f.endswith(".ORIGINAL.bak")]
    if len(baks) > 25:
        baks.sort(key=lambda x: os.path.getmtime(os.path.join(backups_dir, x)))
        for old in baks[:-25]:
            try:
                os.remove(os.path.join(backups_dir, old))
            except Exception:
                pass

    return bak_path


def record_session_backup(slot_num, save_json, save_version, min_interval_sec=15, force=False):
    """
    Automatically archives a session backup and syncs the slot's savedata and metadata whenever changes are made.
    """
    ensure_slots_directory()
    slot_save_path = get_slot_save_path(slot_num)
    backups_dir = get_slot_backups_dir(slot_num)
    os.makedirs(backups_dir, exist_ok=True)

    # 1. Guarantee pristine ORIGINAL.bak exists
    orig_bak = os.path.join(backups_dir, f"slot_{slot_num:02d}.ORIGINAL.bak")
    if not os.path.exists(orig_bak):
        if os.path.exists(slot_save_path) and os.path.getsize(slot_save_path) > 0:
            shutil.copyfile(slot_save_path, orig_bak)
        else:
            save_io.save_to_file(save_json, orig_bak, version=save_version, make_backup=False)

    # 2. Timing check for generating a new backup point
    now = time.time()
    should_backup = force

    if not should_backup:
        session_baks = [
            os.path.join(backups_dir, f) for f in os.listdir(backups_dir)
            if f.endswith(".bak") and not f.endswith(".ORIGINAL.bak")
        ]
        if not session_baks:
            should_backup = True
        else:
            latest_mtime = max(os.path.getmtime(p) for p in session_baks)
            if (now - latest_mtime) >= min_interval_sec:
                should_backup = True

    if should_backup:
        ts = time.strftime("%Y%m%d_%H%M%S")
        bak_filename = f"slot_{slot_num:02d}_session_{ts}.bak"
        bak_path = os.path.join(backups_dir, bak_filename)
        save_io.save_to_file(save_json, bak_path, version=save_version, make_backup=False)

        # Rolling retention: keep 25 most recent backups
        baks = [f for f in os.listdir(backups_dir) if f.endswith(".bak") and not f.endswith(".ORIGINAL.bak")]
        if len(baks) > 25:
            baks.sort(key=lambda x: os.path.getmtime(os.path.join(backups_dir, x)))
            for old in baks[:-25]:
                try:
                    os.remove(os.path.join(backups_dir, old))
                except Exception:
                    pass

    # 3. Always keep slot's savedata.sav and slot_meta.json in sync with live changes
    save_io.save_to_file(save_json, slot_save_path, version=save_version, make_backup=False)
    meta = extract_save_metadata(save_json)
    meta["file_mtime"] = os.path.getmtime(slot_save_path)
    meta["save_version"] = save_version
    meta["file_size_kb"] = os.path.getsize(slot_save_path) // 1024
    meta_path = get_slot_meta_path(slot_num)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    set_active_slot(slot_num)
    return get_slot_info(slot_num, force_refresh=True)


def restore_slot_backup(slot_num, bak_filename, active_target_path=None):
    """
    Restores a backup into the slot's savedata.sav, and optionally copies it to active target path.
    """
    backups_dir = get_slot_backups_dir(slot_num)
    bak_path = os.path.join(backups_dir, bak_filename)

    if not os.path.exists(bak_path):
        raise FileNotFoundError(f"Backup {bak_filename} not found in slot {slot_num}")

    slot_save = get_slot_save_path(slot_num)
    shutil.copyfile(bak_path, slot_save)

    # Invalidate / refresh slot metadata
    get_slot_info(slot_num, force_refresh=True)

    if active_target_path:
        # Backup active first, then copy
        if os.path.exists(active_target_path):
            save_io.create_backup(active_target_path)
        shutil.copyfile(bak_path, active_target_path)

    return True


def clear_slot(slot_num):
    """Clears a slot (removes savedata.sav and slot_meta.json, but preserves historical backups)."""
    slot_save = get_slot_save_path(slot_num)
    meta_path = get_slot_meta_path(slot_num)

    if os.path.exists(slot_save):
        try:
            os.remove(slot_save)
        except Exception:
            pass

    if os.path.exists(meta_path):
        try:
            os.remove(meta_path)
        except Exception:
            pass

    return True


def import_save_file_to_slot(src_path, slot_num):
    """Imports an external .sav file directly into a slot."""
    ensure_slots_directory()
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source save not found: {src_path}")

    # Validate by decompressing
    data, ver = save_io.decompress_save(src_path)
    return save_current_to_slot(data, ver, slot_num)
