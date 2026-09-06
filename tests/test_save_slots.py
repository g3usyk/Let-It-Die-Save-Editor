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
        save_slots.PROJECT_SLOTS_DIR = os.path.join(self.tmp_dir, "SaveSlots")
        save_slots.ensure_slots_directory()

        self.save_data, self.version = save_io.decompress_save(REAL_SAVE_PATH)

    def tearDown(self):
        save_slots.PROJECT_SLOTS_DIR = self.orig_slots_dir
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


if __name__ == "__main__":
    unittest.main()
