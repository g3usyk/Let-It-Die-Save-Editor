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
            
            bak_path = save_io.create_backup(test_save)
            self.assertTrue(os.path.exists(bak_path))
            self.assertGreater(os.path.getsize(bak_path), 0)

if __name__ == "__main__":
    unittest.main()
