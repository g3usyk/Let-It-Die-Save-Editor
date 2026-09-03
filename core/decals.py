# -*- coding: utf-8 -*-
import time
import uuid
import random
from core.helpers import load_all_known_decals, get_player_uid

DECAL_PRESETS = {'tengoku_climber': {'name': 'Tengoku God Climber (Pisos 51F - 350F+)', 'decals': ['SKL_FIGHTER_STUP_01_P', 'SKL_ATKUP_NODMG_P', 'SKL_ATKUP_03_P', 'SKL_DRAIN_01_P', 'SKL_HPUP_03_P', 'SKL_ARRNG_STATUP_ALL_P', 'SKL_STRENGTHEN_BODY_01_P', 'SKL_HEADSHOTUP_P']}, 'kamas_god': {'name': 'Tirador KAMAS Definitivo (Full Shooter Meta)', 'decals': ['SKL_HEADSHOTUP_P', 'SKL_ATKUP_NODMG_P', 'SKL_FIGHTER_STUP_01_P', 'SKL_ATKUP_03_P', 'SKL_WEP_SPDUP_P', 'SKL_CRIUP_02_P', 'SKL_DRAIN_01_P', 'SKL_SEARCHUP_ITEM_P']}, 'melee_melter': {'name': 'Destructor Melee (Mayal / Machete / Katana)', 'decals': ['SKL_FIGHTER_STUP_01_P', 'SKL_ATKUP_03_P', 'SKL_ATKUP_NODMG_P', 'SKL_DRAIN_01_P', 'SKL_HPUP_02_P', 'SKL_DEFUP_02_P', 'SKL_STRENGTHEN_BODY_01_P', 'SKL_RGSPDUP_02_P']}, 'tdm_defense': {'name': 'Pesadilla de Defensa TDM (Invulnerable Tank)', 'decals': ['SKL_HPUP_03_P', 'SKL_HPUP_02_P', 'SKL_DEFUP_02_P', 'SKL_SNOWWHITE_P', 'SKL_STRENGTHEN_BODY_01_P', 'SKL_ATKDEFUP_HPLOW_01_P', 'SKL_FIGHTER_STUP_01_P', 'SKL_ATKUP_CRIUP_DEFDWN_P']}}

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
    body_uid = get_player_uid(save)
        
    soul = save.setdefault("soul", {})
    skl = soul.setdefault("skl", {})
    eqskl = skl.setdefault("eqskl", {})
    user_eq = eqskl.setdefault(body_uid, [])
    
    # Remove existing equipped decals for this cid
    cleaned_eq = [e for e in user_eq if isinstance(e, dict) and e.get("cid") != cid]
    
    # Equip all decals defined in preset (up to 8 slots for Tier 8 / Grade 6 uncapped)
    equipped_count = 0
    for idx, did in enumerate(decals[:8]):
        cleaned_eq.append({
            "cid": cid,
            "sklid": did,
            "slot": idx
        })
        equipped_count += 1
        
    eqskl[body_uid] = cleaned_eq
    return preset["name"], equipped_count

# ================= ENDGAME SETS INJECTOR (44CE, JACKALS, TENGOKU) =================

