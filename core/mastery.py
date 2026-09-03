from game_data import WEAPON_CATEGORIES
from core.helpers import get_or_create_list

def max_all_weapon_mastery(save, level=20):
    max_weapon_masteries(save, target_lvl=int(level))

def set_weapon_mastery(save, ptarmtp, level=20):
    set_single_weapon_mastery(save, ptarmtp, target_lvl=level)

def max_weapon_masteries(save, target_lvl=20):
    soul = save.setdefault("soul", {})
    expert_list = get_or_create_list(soul, "expert")
    
    abp_map = {
        1: 0, 5: 500, 10: 2000, 15: 5000, 20: 15000, 25: 35000, 30: 60000
    }
    target_abp = abp_map.get(target_lvl, target_lvl * 1000)
    
    existing_map = {}
    for item in expert_list:
        wt = item.get("ptarmtp")
        if wt:
            existing_map[wt] = item
            item["lvl"] = int(target_lvl)
            item["abp"] = max(item.get("abp", 0), target_abp)
            item["is_checked"] = 1
            
    # Add any weapon categories not yet discovered/used by the player
    for wt, _, _ in WEAPON_CATEGORIES:
        if wt not in existing_map:
            new_entry = {
                "ptarmtp": wt,
                "abp": int(target_abp),
                "lvl": int(target_lvl),
                "is_checked": 1
            }
            expert_list.append(new_entry)
            existing_map[wt] = new_entry

def set_single_weapon_mastery(save, ptarmtp, target_lvl, abp=None):
    soul = save.setdefault("soul", {})
    expert_list = get_or_create_list(soul, "expert")
    
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

