# -*- coding: utf-8 -*-
import unittest
import os
import shutil
import tempfile
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import save_io
from tests.test_save_io import REAL_SAVE_PATH
import core.save_slots as save_slots


class TestSaveSlots(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.orig_slots_dir = save_slots.PROJECT_SLOTS_DIR
        self.orig_active_file = save_slots.ACTIVE_SLOT_FILE
        save_slots.PROJECT_SLOTS_DIR = os.path.join(self.tmp_dir, "SaveSlots")
        save_slots.ACTIVE_SLOT_FILE = os.path.join(save_slots.PROJECT_SLOTS_DIR, "active_slot.json")
        save_slots.ensure_slots_directory()

        self.save_data, self.version = save_io.decompress_save(REAL_SAVE_PATH)

    def tearDown(self):
        save_slots.PROJECT_SLOTS_DIR = self.orig_slots_dir
        save_slots.ACTIVE_SLOT_FILE = self.orig_active_file
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_extract_save_metadata(self):
        meta = save_slots.extract_save_metadata(self.save_data)
        self.assertIsInstance(meta, dict)
        self.assertEqual(meta.get("player_name"), "Geus")
        self.assertEqual(meta.get("steam_id"), "76561198324473152")
        self.assertEqual(meta.get("max_floor"), 55)
        self.assertEqual(meta.get("haters_killed"), 34)
        self.assertEqual(meta.get("fighter_name"), "Allyson")
        self.assertEqual(meta.get("fighter_class"), "COL")
        self.assertEqual(meta.get("fighter_grade"), 6)
        self.assertEqual(meta.get("fighter_lvl"), 247)
        self.assertGreater(meta.get("kill_coins", 0), 1000000)
        self.assertEqual(meta.get("death_metals"), 9999)
        self.assertGreater(meta.get("splithium", 0), 2000000)

    def test_save_to_slot_and_retrieve_info(self):
        slot_info = save_slots.save_current_to_slot(self.save_data, self.version, 1)
        self.assertFalse(slot_info["is_empty"])
        self.assertEqual(slot_info["slot_num"], 1)
        self.assertEqual(slot_info["meta"]["player_name"], "Geus")
        self.assertEqual(slot_info["meta"]["max_floor"], 55)
        self.assertEqual(slot_info["meta"]["haters_killed"], 34)

        # Verify initial ORIGINAL backup exists
        self.assertGreaterEqual(slot_info["backups_count"], 1)
        self.assertTrue(any("ORIGINAL" in b["filename"] for b in slot_info["backups"]))

        # Verify other slots remain empty
        slot2 = save_slots.get_slot_info(2)
        self.assertTrue(slot2["is_empty"])

    def test_slot_backups_and_restore(self):
        save_slots.save_current_to_slot(self.save_data, self.version, 2)
        bak1 = save_slots.create_slot_backup(2)
        self.assertTrue(os.path.exists(bak1))

        # Modify KC in save and save again
        modified_data = dict(self.save_data)
        modified_data["soul"]["free_money"] = 12345
        save_slots.save_current_to_slot(modified_data, self.version, 2)

        info = save_slots.get_slot_info(2)
        self.assertEqual(info["meta"]["kill_coins"], 12345)

        # Restore bak1
        bak1_name = os.path.basename(bak1)
        save_slots.restore_slot_backup(2, bak1_name)

        restored_info = save_slots.get_slot_info(2, force_refresh=True)
        self.assertEqual(restored_info["meta"]["kill_coins"], 1856509)

    def test_load_slot_to_active(self):
        save_slots.save_current_to_slot(self.save_data, self.version, 3)

        target_active = os.path.join(self.tmp_dir, "active_steam.sav")
        shutil.copyfile(REAL_SAVE_PATH, target_active)

        ok, loaded_data, loaded_ver = save_slots.load_slot_to_active(3, target_active)
        self.assertTrue(ok)
        self.assertEqual(loaded_ver, self.version)
        self.assertEqual(loaded_data["user"]["nm"], "Geus")

    def test_slot_isolation_and_clearing(self):
        save_slots.save_current_to_slot(self.save_data, self.version, 1)
        save_slots.save_current_to_slot(self.save_data, self.version, 2)

        save_slots.clear_slot(1)
        self.assertTrue(save_slots.get_slot_info(1)["is_empty"])
        self.assertFalse(save_slots.get_slot_info(2)["is_empty"])

    def test_record_session_backup_and_sync(self):
        # Save initially
        save_slots.save_current_to_slot(self.save_data, self.version, 2)
        info1 = save_slots.get_slot_info(2)
        initial_baks = info1["backups_count"]

        # Make a change and record session backup
        mod_data = dict(self.save_data)
        mod_data["soul"]["free_money"] = 555555
        res = save_slots.record_session_backup(2, mod_data, self.version, force=True)

        self.assertEqual(res["meta"]["kill_coins"], 555555)
        self.assertGreater(res["backups_count"], initial_baks)

        # Verify a session backup was created with _session_ in filename
        session_baks = [b for b in res["backups"] if b.get("is_session")]
        self.assertGreaterEqual(len(session_baks), 1)

        # Test extracting metadata directly from the backup file
        bak_meta = save_slots.get_backup_metadata(session_baks[0]["path"])
        self.assertEqual(bak_meta.get("kill_coins"), 555555)
        self.assertEqual(bak_meta.get("player_name"), "Geus")

    def test_active_slot_persistence_and_matching(self):
        save_slots.set_active_slot(2)
        self.assertEqual(save_slots.get_active_slot(), 2)

        # Save to slot 2 and match
        save_slots.save_current_to_slot(self.save_data, self.version, 2)
        matched = save_slots.find_matching_slot(self.save_data)
        self.assertEqual(matched, 2)

    def test_slot_custom_name_persistence(self):
        # Set custom name on empty slot
        save_slots.set_slot_custom_name(4, "Speedrun Tengoku")
        info_empty = save_slots.get_slot_info(4)
        self.assertEqual(info_empty["custom_name"], "Speedrun Tengoku")

        # Save game data to slot 4, custom_name must persist
        save_slots.save_current_to_slot(self.save_data, self.version, 4)
        info_saved = save_slots.get_slot_info(4)
        self.assertEqual(info_saved["custom_name"], "Speedrun Tengoku")

        # Record session backup, custom_name must still persist
        save_slots.record_session_backup(4, self.save_data, self.version, force=True)
        info_session = save_slots.get_slot_info(4)
        self.assertEqual(info_session["custom_name"], "Speedrun Tengoku")


if __name__ == "__main__":
    unittest.main()
