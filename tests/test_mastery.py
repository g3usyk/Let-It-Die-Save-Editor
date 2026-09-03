# -*- coding: utf-8 -*-
import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import modifiers

class TestMastery(unittest.TestCase):
    def setUp(self):
        self.save = {
            "soul": {
                "expert": [
                    {"ptarmtp": "PTARMTP_00", "lvl": 1, "abp": 0, "is_checked": 0}
                ]
            }
        }

    def test_max_weapon_masteries_populates_all_weapons(self):
        modifiers.max_weapon_masteries(self.save, target_lvl=25)
        expert = self.save["soul"]["expert"]
        self.assertGreaterEqual(len(expert), 40)
        self.assertTrue(all(item["lvl"] == 25 for item in expert))
        self.assertTrue(all(item["abp"] >= 35000 for item in expert))
        self.assertTrue(all(item["is_checked"] == 1 for item in expert))

    def test_set_single_weapon_mastery(self):
        modifiers.set_single_weapon_mastery(self.save, "PTARMTP_17", target_lvl=30)
        kamas = next((item for item in self.save["soul"]["expert"] if item.get("ptarmtp") == "PTARMTP_17"), None)
        self.assertIsNotNone(kamas)
        self.assertEqual(kamas["lvl"], 30)
        self.assertEqual(kamas["abp"], 60000)

if __name__ == "__main__":
    unittest.main()
