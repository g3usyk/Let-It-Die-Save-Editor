import os
import sys
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from save_io import get_default_save_path, decompress_save, save_to_file, create_backup
import modifiers

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    print("=" * 68)
    print("      💀  LET IT DIE (Offline) - DEEP SAVE FILE MODIFIER  💀      ")
    print("=" * 68)

def main():
    save_path = get_default_save_path()
    if not save_path or not os.path.exists(save_path):
        local_cur = os.path.join(PROJECT_ROOT, "CurrentSave")
        if os.path.isdir(local_cur):
            local_savs = [os.path.join(local_cur, f) for f in os.listdir(local_cur) if f.endswith(".sav")]
            if local_savs:
                save_path = local_savs[0]

    if not save_path or not os.path.exists(save_path):
        print("Save file not found at default location.")
        user_input = input("Enter full path to .sav file: ").strip().strip('"')
        if not os.path.exists(user_input):
            print(f"Error: Path does not exist: {user_input}")
            return
        save_path = user_input

    try:
        save_json, version = decompress_save(save_path)
    except Exception as e:
        print(f"Error loading save file: {e}")
        return

    while True:
        clear_screen()
        print_banner()
        print(f"📁 Loaded File: {save_path}")
        summary = modifiers.get_save_summary(save_json)
        print(f"👤 Player: {summary['player_name']} (UID: {summary['uid']}) | Rank: {summary['player_rank']}")
        print("-" * 68)
        print(f"  💎 Death Metals (DM):      {summary['death_metals_total']:,}")
        print(f"  🪙 Kill Coins (KC):         {summary['kill_coins']:,}")
        print(f"  ⚡ SPLithium (SPL):         {summary['splithium']:,}")
        print(f"  🩸 Bloodnium:               {summary['bloodnium']:,}")
        print(f"  ♻️  RE / Recycle Points:     {summary['recycle_points']:,}")
        print(f"  🎫 VIP Express Pass:        {'Active (' + str(summary['vip_days_remaining']) + ' days)' if summary['vip_active'] else 'Inactive'}")
        print(f"  📜 Blueprints Unlocked:     {summary['unlocked_blueprints_count']} / 1,346")
        print(f"  🤼 Fighters in Freezer:     {summary['total_fighters']} ({summary['dead_fighters']} dead/lost)")
        print(f"  🏷️  Decals Owned:            {summary['unique_decals']} unique ({summary['total_decals_count']} total)")
        print("=" * 68)
        print("  [1] Max Currencies (9999 DM, 10,000,000 KC, SPL, 999,999 Bloodnium, RE)")
        print("  [2] Custom Currency Values")
        print("  [3] Grant Royal VIP Express Pass (30 Safe Days + 99 Passes)")
        print("  [4] Unlock ALL 1,346 Blueprints (Max Tier +4 in Chokufunsha)")
        print("  [5] Max All Weapon Masteries (PTARMTP_00..64 to Lv 20 / 30)")
        print("  [6] Revive & Heal All Fighters (Free Salvage)")
        print("  [7] Unlock ALL 626 Decals (x3 each, Normal & Premium)")
        print("  [8] Add Top 18 Meta Decals (Ultimate Fighter, Serial Killer, Golden Gym...)")
        print("  [9] Add 20x of ALL Rare Crafting Materials & Repair Equipment")
        print(" [10] Complete Uncle Death Compendiums (63 Mushrooms + 24 Beasts 100%)")
        print(" [11] Unlock All 113 Waiting Room Customizations (Floors, Fountains, Themes)")
        print(" [12] Inject Endgame Sets (44CE White Steel, Red Napalm, Jackals, Tengoku)")
        print(" [13] Infinite Durability (999,999) & Massive Ammo (9,999) on Gear")
        print(" [14] Complete All 232 Official Quests (Misiones con recompensas DM)")
        print(" [15] Unlock All 36 Magazines & Radio Jukebox")
        print(" [16] Unlock Tower Map & 61 Elevators (980 Rooms, 1,119 Escalators)")
        print(" [17] Export Save to Uncompressed JSON (for manual editing)")
        print(" [18] Import Save from JSON file")
        print(" [19] Save Changes & Apply to Game (.sav with rolling auto-backup)")
        print("  [0] Exit without saving")
        print("=" * 68)

        choice = input("Select an option (0-19): ").strip()

        if choice == "1":
            modifiers.set_currencies(save_json, dm=9999, kc=10000000, spl=10000000, bloodnium=999999, re_points=999999, safe_lvl=64, tank_lvl=64)
            print("\n✅ Currencies and Bank capacities maximized!")
            input("Press Enter to continue...")

        elif choice == "2":
            print("\nEnter new amounts (leave blank to keep current):")
            dm = input(f"Death Metals [{summary['death_metals_total']}]: ").strip()
            kc = input(f"Kill Coins [{summary['kill_coins']}]: ").strip()
            spl = input(f"SPLithium [{summary['splithium']}]: ").strip()
            bl = input(f"Bloodnium [{summary['bloodnium']}]: ").strip()
            re = input(f"RE Points [{summary['recycle_points']}]: ").strip()
            
            modifiers.set_currencies(
                save_json,
                dm=int(dm) if dm else None,
                kc=int(kc) if kc else None,
                spl=int(spl) if spl else None,
                bloodnium=int(bl) if bl else None,
                re_points=int(re) if re else None
            )
            print("\n✅ Currencies updated!")
            input("Press Enter to continue...")

        elif choice == "3":
            modifiers.set_vip_pass(save_json, days=30, passes=99, oneday_passes=99)
            print("\n✅ Royal VIP Express Pass activated for 30 safe days (+99 reserve tickets)!")
            input("Press Enter to continue...")

        elif choice == "4":
            total, added = modifiers.unlock_blueprints(save_json, category="all", max_level=4)
            print(f"\n✅ Unlocked all {total} blueprints with max research level in Chokufunsha!")
            input("Press Enter to continue...")

        elif choice == "5":
            lvl = input("Enter target level (20 or 30, default 20): ").strip()
            target_lvl = int(lvl) if lvl.isdigit() else 20
            modifiers.max_weapon_masteries(save_json, target_lvl=target_lvl)
            print(f"\n✅ All weapon masteries set to Lv {target_lvl}!")
            input("Press Enter to continue...")

        elif choice == "6":
            modifiers.revive_all_fighters(save_json)
            print("\n✅ All dead and lost fighters revived and healed!")
            input("Press Enter to continue...")

        elif choice == "7":
            modifiers.unlock_all_decals(save_json, count=3, premium=True)
            print("\n✅ All 626 official Decals added (3x each) to your inventory!")
            input("Press Enter to continue...")

        elif choice == "8":
            modifiers.add_top_meta_decals(save_json, count=5)
            print("\n✅ Top 18 Meta Decals added (5x each)!")
            input("Press Enter to continue...")

        elif choice == "9":
            modifiers.repair_all_storage_equipment(save_json)
            from game_data import RARE_MATERIALS
            for mat_id, _, _ in RARE_MATERIALS:
                modifiers.add_materials_to_storage(save_json, mat_id, 20)
            print("\n✅ All rare materials added (20x) and equipment repaired to 100%!")
            input("Press Enter to continue...")

        elif choice == "10":
            m_cnt, b_cnt = modifiers.complete_encyclopedia_books(save_json)
            print(f"\n✅ Uncle Death Compendiums 100% completed: {m_cnt} Mushrooms and {b_cnt} Beasts!")
            input("Press Enter to continue...")

        elif choice == "11":
            tot, unl = modifiers.unlock_all_hub_customizations(save_json)
            print(f"\n✅ All {tot} Waiting Room customizations unlocked ({unl} newly added)!")
            input("Press Enter to continue...")

        elif choice == "12":
            print("\nSelect Endgame Set:")
            print("  [1] 44CE White Steel (D.O.D. Arms)")
            print("  [2] 44CE Red Napalm (War Ensemble)")
            print("  [3] 44CE Black Thunder (Candle Wolf)")
            print("  [4] 44CE Pale Wind (M.I.L.K.)")
            print("  [5] Sets Jackals v1 / v2 / v3")
            print("  [6] Armas Legendarias de Tengoku (51F+)")
            s_c = input("Choice (1-6): ").strip()
            k_map = {
                "1": "white_steel", "2": "red_napalm", "3": "black_thunder",
                "4": "pale_wind", "5": "jackals_gear", "6": "tengoku_weapons"
            }
            key = k_map.get(s_c, "white_steel")
            s_name, added = modifiers.inject_endgame_set(save_json, set_key=key, count=1, dur=999999, lvl=5)
            print(f"\n✅ Injected {added} pieces of {s_name} with 999,999 durability into your Storage & R&D!")
            input("Press Enter to continue...")

        elif choice == "13":
            dur_cnt = modifiers.set_infinite_durability_all_equipment(save_json, target_dur=999999)
            ammo_cnt = modifiers.set_massive_ammo_all_weapons(save_json, ammo=9999)
            up_cnt = modifiers.upgrade_all_equipment_max_level(save_json, target_lvl=19)
            print(f"\n✅ God Gear applied:")
            print(f"   • {dur_cnt} items set to 999,999 Durability (indestructible)")
            print(f"   • {ammo_cnt} weapons set to 9,999 Ammo in magazine")
            print(f"   • {up_cnt} items upgraded to Tier 4 +19 (Uncapped)")
            input("Press Enter to continue...")

        elif choice == "14":
            q_cnt = modifiers.complete_all_quests(save_json)
            print(f"\n✅ Completed {q_cnt} official Tower of Barbs Quests!")
            print("   Claim hundreds of Death Metals, rare metals and blueprints in your Reward Box!")
            input("Press Enter to continue...")

        elif choice == "15":
            modifiers.unlock_all_magazines(save_json)
            modifiers.unlock_all_radio_music(save_json)
            print("\n✅ All 36 Uncle Death magazines and full Radio Jukebox unlocked!")
            input("Press Enter to continue...")

        elif choice == "16":
            elv_cnt = modifiers.unlock_all_tower_elevators(save_json)
            print(f"\n✅ Unlocked all {elv_cnt} official elevators and discovered all 980 rooms and 1,119 escalators on Tower Map!")
            input("Press Enter to continue...")

        elif choice == "17":
            out_json = os.path.join(os.path.dirname(save_path), "save_decompressed.json")
            with open(out_json, "w", encoding="utf-8") as f:
                json.dump(save_json, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Saved decompressed JSON to:\n{out_json}")
            print("You can open and edit this file with VSCode or Notepad, then use option [18] to re-import it.")
            input("Press Enter to continue...")

        elif choice == "18":
            in_json = os.path.join(os.path.dirname(save_path), "save_decompressed.json")
            if not os.path.exists(in_json):
                in_json = input("Enter path to JSON file: ").strip().strip('"')
            if os.path.exists(in_json):
                with open(in_json, "r", encoding="utf-8") as f:
                    save_json = json.load(f)
                print(f"\n✅ Successfully imported from {in_json}!")
            else:
                print(f"\n❌ File not found: {in_json}")
            input("Press Enter to continue...")

        elif choice == "19":
            backup_file = create_backup(save_path)
            save_to_file(save_json, save_path, version=version, make_backup=False)
            print(f"\n🎉 Save file updated successfully!")
            print(f"📦 Backup created at:\n   {backup_file}")
            input("Press Enter to continue...")

        elif choice == "0":
            print("\nExiting. No unsaved changes applied.")
            break

if __name__ == "__main__":
    main()
