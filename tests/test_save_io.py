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

REAL_SAVE_PATH = os.path.join(BASE_DIR, "CurrentSave", "76561198324473152.sav")

class TestSaveIO(unittest.TestCase):
    def setUp(self):
        self.assertTrue(os.path.exists(REAL_SAVE_PATH), f"Real save not found at {REAL_SAVE_PATH}")

    def test_decompress_real_save(self):
        data, ver = save_io.decompress_save(REAL_SAVE_PATH)
        self.assertEqual(ver, 2)
        self.assertIsInstance(data, dict)
        self.assertIn("user", data)
        self.assertIn("soul", data)
        self.assertIn("item", data)
        self.assertIn("part", data)

    def test_roundtrip_compression(self):
        original_data, ver = save_io.decompress_save(REAL_SAVE_PATH)
        compressed_bytes = save_io.compress_save(original_data, version=ver)
        
        self.assertTrue(compressed_bytes.startswith(b"BRG\x00"))
        
        with tempfile.NamedTemporaryFile(suffix=".sav", delete=False) as tmp:
            tmp.write(compressed_bytes)
            tmp_path = tmp.name

        try:
            re_data, re_ver = save_io.decompress_save(tmp_path)
            self.assertEqual(re_ver, ver)
            self.assertEqual(original_data.get("user"), re_data.get("user"))
            self.assertEqual(original_data.get("soul"), re_data.get("soul"))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_create_backup(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_save = os.path.join(tmp_dir, "test.sav")
            shutil.copyfile(REAL_SAVE_PATH, test_save)
            
            bak_path = save_io.create_backup(test_save, backup_dir=tmp_dir)
            self.assertTrue(os.path.exists(bak_path))
            self.assertGreater(os.path.getsize(bak_path), 0)
            orig_bak = os.path.join(tmp_dir, "test.sav.ORIGINAL.bak")
            self.assertTrue(os.path.exists(orig_bak), "ORIGINAL.bak must be created on first backup")

    def test_save_to_file_preserves_clean_save_without_invasive_mutations(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_save = os.path.join(tmp_dir, "test.sav")
            shutil.copyfile(REAL_SAVE_PATH, test_save)

            data, ver = save_io.decompress_save(test_save)
            orig_team = data.get("soul", {}).get("team_id")
            orig_tdm_rank = data.get("soul", {}).get("tdm_rank")
            
            # Edit only KC
            data["soul"]["free_money"] = 777777
            save_io.save_to_file(data, test_save, version=ver, make_backup=True)

            re_data, re_ver = save_io.decompress_save(test_save)
            self.assertEqual(re_data["soul"]["free_money"], 777777)
            # Must NOT alter team_id or tdm_rank if already set
            self.assertEqual(re_data.get("soul", {}).get("team_id"), orig_team)
            self.assertEqual(re_data.get("soul", {}).get("tdm_rank"), orig_tdm_rank)

if __name__ == "__main__":
    unittest.main()
