# -*- coding: utf-8 -*-

def max_all_weapon_mastery(save, level=20):
    max_weapon_masteries(save, target_lvl=int(level))

def set_weapon_mastery(save, ptarmtp, level=20):
    set_single_weapon_mastery(save, ptarmtp, target_lvl=level)

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

