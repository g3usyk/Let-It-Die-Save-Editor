# -*- coding: utf-8 -*-
import time
from core.helpers import get_player_uid, get_masters_db_path

RANK_POINTS_TABLE = {1: 0, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600, 7: 700, 8: 800, 9: 900, 10: 1000, 11: 1500, 12: 1900, 13: 2300, 14: 2700, 15: 3100, 16: 3500, 17: 3900, 18: 4300, 19: 4700, 20: 5500, 21: 6100, 22: 6700, 23: 7300, 24: 7900, 25: 8500, 26: 9100, 27: 9700, 28: 10300, 29: 10900, 30: 11005, 31: 22000, 32: 33000, 33: 44000, 34: 55000, 35: 66000, 36: 77000, 37: 88000, 38: 99000, 39: 110000, 40: 120000, 41: 173000, 42: 226000, 43: 279000, 44: 332000, 45: 385000, 46: 438000, 47: 491000, 48: 544000, 49: 597000, 50: 650000, 51: 715000, 52: 780000, 53: 845000, 54: 910000, 55: 975000, 56: 1040000, 57: 1105000, 58: 1170000, 59: 1235000, 60: 1300005, 61: 1400000, 62: 1500000, 63: 1600000, 64: 1700000, 65: 1800000, 66: 1900000, 67: 2000000, 68: 2100000, 69: 2200000, 70: 14000000, 71: 20100000, 72: 26200000, 73: 32300000, 74: 38400000, 75: 44500000, 76: 50600000, 77: 56700000, 78: 62800000, 79: 68900000, 80: 75000000, 81: 82500000, 82: 90000000, 83: 97500000, 84: 105000000, 85: 150000000, 86: 150000001, 87: 150000002, 88: 150000003, 89: 150000004, 90: 150000005, 91: 280000000, 92: 410000000, 93: 540000000, 94: 670000000, 95: 800000000, 96: 960000000, 97: 1120000000, 98: 1280000000, 99: 1440000000, 100: 1600000000, 101: 1600000001, 102: 1600000002, 103: 1600000003, 104: 1600000004, 105: 1600000005, 106: 2980000000, 107: 4360000000, 108: 5740000000, 109: 7120000000, 110: 8500000000, 111: 10200000000, 112: 11900000000, 113: 13600000000, 114: 15300000000, 115: 17000000000, 116: 17000000001, 117: 17000000002, 118: 17000000003, 119: 17000000004, 120: 17000000005, 121: 31600000000, 122: 36000000000, 123: 54000000000, 124: 72000000000, 125: 90000000000, 126: 108000000000, 127: 126000000000, 128: 144000000000, 129: 162000000000, 130: 180000000000}

def set_currencies(save, dm=None, kc=None, spl=None, bloodnium=None, re_points=None, safe_lvl=None, tank_lvl=None):
    user = save.setdefault("user", {})
    soul = save.setdefault("soul", {})
    
    if dm is not None:
        user["free_medal"] = int(dm)
        user["paid_medal"] = 0
    if kc is not None:
        soul["free_money"] = int(kc)
        soul["paid_money"] = 0
    if spl is not None:
        soul["spirit"] = int(spl)
    if bloodnium is not None:
        soul["bloodnium_point"] = int(bloodnium)
    if re_points is not None:
        soul["recycle_point"] = int(re_points)
    if safe_lvl is not None:
        soul["safe_level"] = int(safe_lvl)
    if tank_lvl is not None:
        soul["spirit_tank_level"] = int(tank_lvl)

def set_death_metals(save, amount):
    user = save.setdefault("user", {})
    user["free_medal"] = int(amount)
    user["paid_medal"] = 0

def set_kill_coins(save, amount):
    soul = save.setdefault("soul", {})
    soul["free_money"] = int(amount)
    soul["paid_money"] = 0

def set_splithium(save, amount):
    soul = save.setdefault("soul", {})
    soul["spirit"] = int(amount)

def set_bloodnium(save, amount):
    soul = save.setdefault("soul", {})
    soul["bloodnium_point"] = int(amount)

def set_recycle_points(save, amount):
    soul = save.setdefault("soul", {})
    soul["recycle_point"] = int(amount)

def get_rank_points_for_rank(rank):
    """Returns the official required rank points for a given Player Rank (1-130)."""
    r = max(1, min(int(rank), 130))
    return RANK_POINTS_TABLE.get(r, 0)

def set_player_rank(save, rank=None, rank_point=None):
    soul = save.setdefault("soul", {})
    if rank is not None:
        rank_val = max(1, min(int(rank), 130))
        soul["rank"] = rank_val
        if rank_point is None:
            rank_point = get_rank_points_for_rank(rank_val)
    if rank_point is not None:
        soul["rank_point"] = int(rank_point)

def upgrade_waiting_room(save, bank_level=100, tank_level=100):
    soul = save.setdefault("soul", {})
    soul["safe_level"] = max(1, min(int(bank_level), 100))
    soul["spirit_tank_level"] = max(1, min(int(tank_level), 100))

def set_vip_pass(save, days=30, passes=99, oneday_passes=99):
    soul = save.setdefault("soul", {})
    vip = soul.setdefault("vip", {})
    now = int(time.time())
    
    # Safe days cap (max 90 days): extreme values (>90d) or automatic_renewal=1
    # cause the elevator clerk's Steam subscription validation to hang infinitely!
    safe_days = max(1, min(int(days), 90))
    
    vip["flag"] = 1
    vip["type"] = 0
    vip["pass_num"] = max(0, min(int(passes), 99))
    vip["oneday_pass_num"] = max(0, min(int(oneday_passes), 99))
    vip["expired_time"] = now + (safe_days * 86400)
    vip["automatic_renewal"] = 0
    vip["friendship"] = 100


def set_tdm_rank(save, rank_id="TDM_RANK_05_03", points=5000, rank=None):
    soul = save.setdefault("soul", {})
    now = int(time.time())
    if rank is not None:
        rank_str = str(rank).strip()
        num_map = {
            "1": "TDM_RANK_05_03", "2": "TDM_RANK_05_02", "3": "TDM_RANK_05_01",
            "4": "TDM_RANK_04_03", "5": "TDM_RANK_04_02", "6": "TDM_RANK_04_01",
            "7": "TDM_RANK_03_03", "8": "TDM_RANK_03_02", "9": "TDM_RANK_03_01",
            "10": "TDM_RANK_02_03", "11": "TDM_RANK_02_02", "12": "TDM_RANK_02_01",
            "13": "TDM_RANK_01_03", "14": "TDM_RANK_01_02", "15": "TDM_RANK_01_01",
        }
        if rank_str in num_map:
            rank_id = num_map[rank_str]
        elif rank_str.startswith("TDM_RANK_"):
            rank_id = rank_str
            
    soul["tdm_rank"] = str(rank_id)
    soul["tdm_point"] = int(points)
    soul["last_tdm_rank"] = str(rank_id)
    # Anti-reset: Keep season active for 30 days so the game does not wipe TDM progress on start
    soul["last_tdm_reset_time"] = now + (30 * 86400)

def get_player_currencies(save):
    user = save.get("user", {})
    soul = save.get("soul", {})
    return {
        "dm": user.get("free_medal", 0) + user.get("paid_medal", 0),
        "kc": soul.get("free_money", 0) + soul.get("paid_money", 0),
        "spl": soul.get("spirit", 0),
        "bloodnium": soul.get("bloodnium_point", 0),
        "re_points": soul.get("recycle_point", 0),
    }

def get_waiting_room_info(save):
    soul = save.get("soul", {})
    return {
        "bank_level": soul.get("safe_level", 100),
        "tank_level": soul.get("spirit_tank_level", 100),
        "rank": soul.get("rank", 100),
    }

def get_vip_status(save):
    soul = save.get("soul", {})
    vip = soul.get("vip", {})
    exp_time = vip.get("expired_time", 0)
    now = time.time()
    active = (vip.get("flag", 0) == 1) and (exp_time > now)
    days_left = max(0, int((exp_time - now) / 86400))
    exp_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(exp_time)) if exp_time else "---"
    return {
        "active": active,
        "days_left": days_left,
        "expires_at": exp_str,
    }

def max_all_currencies(save):
    set_currencies(save, dm=9999, kc=10000000, spl=10000000, bloodnium=999999, re_points=999999)

def activate_vip_express_pass(save, days=30):
    set_vip_pass(save, days=days)
    return int(time.time()) + (days * 86400)

def max_login_streak(save, streak=365):
    """
    Sets consecutive login streak counter.
    """
    user = save.setdefault("user", {})
    user["login_keep"] = int(streak)
    return int(streak)

