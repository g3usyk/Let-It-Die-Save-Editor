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
        modifiers.max_weapon_masteries(self.save, target_lvl=20)
        expert = self.save["soul"]["expert"]
        self.assertEqual(len(expert), 57)

        # Fists check: exactly 47,000 ABP for level 20
        fists = next((item for item in expert if item.get("ptarmtp") == "PTARMTP_00"), None)
        self.assertIsNotNone(fists)
        self.assertEqual(fists["lvl"], 20)
        self.assertEqual(fists["abp"], 47000)
        self.assertEqual(fists["is_checked"], 1)

        # Standard weapons check: exactly 3,800 ABP for level 20
        kamas = next((item for item in expert if item.get("ptarmtp") == "PTARMTP_17"), None)
        self.assertIsNotNone(kamas)
        self.assertEqual(kamas["lvl"], 20)
        self.assertEqual(kamas["abp"], 3800)
        self.assertEqual(kamas["is_checked"], 1)

        # Dummy slots check: PTARMTP_08 and PTARMTP_22 must remain -1
        dummy08 = next((item for item in expert if item.get("ptarmtp") == "PTARMTP_08"), None)
        self.assertIsNotNone(dummy08)
        self.assertEqual(dummy08["abp"], -1)
        self.assertEqual(dummy08["lvl"], 1)
        self.assertEqual(dummy08["is_checked"], 0)

        dummy22 = next((item for item in expert if item.get("ptarmtp") == "PTARMTP_22"), None)
        self.assertIsNotNone(dummy22)
        self.assertEqual(dummy22["abp"], -1)
        self.assertEqual(dummy22["lvl"], 1)
        self.assertEqual(dummy22["is_checked"], 0)

    def test_set_single_weapon_mastery(self):
        # Clamping check: target_lvl > 20 must safely clamp to 20
        modifiers.set_single_weapon_mastery(self.save, "PTARMTP_17", target_lvl=30)
        kamas = next((item for item in self.save["soul"]["expert"] if item.get("ptarmtp") == "PTARMTP_17"), None)
        self.assertIsNotNone(kamas)
        self.assertEqual(kamas["lvl"], 20)
        self.assertEqual(kamas["abp"], 3800)

        # Fists single check
        modifiers.set_single_weapon_mastery(self.save, "PTARMTP_00", target_lvl=20)
        fists = next((item for item in self.save["soul"]["expert"] if item.get("ptarmtp") == "PTARMTP_00"), None)
        self.assertEqual(fists["lvl"], 20)
        self.assertEqual(fists["abp"], 47000)

    def test_repair_and_sanitize_mastery(self):
        # Corrupted expert list: contains fake categories and broken ABP values
        self.save["soul"]["expert"] = [
            {"ptarmtp": "PTARMTP_00", "lvl": 25, "abp": 999999, "is_checked": 1},
            {"ptarmtp": "PTARMTP_09", "lvl": 20, "abp": 50000, "is_checked": 1},  # Invalid fake category
            {"ptarmtp": "PTARMTP_08", "lvl": 20, "abp": 15000, "is_checked": 1},  # Dummy slot modified
            {"ptarmtp": "PTARMTP_17", "lvl": 20, "abp": 15000, "is_checked": 1},  # Overflow ABP
        ]
        repaired = modifiers.repair_and_sanitize_mastery(self.save)
        self.assertGreaterEqual(repaired, 55)

        expert = self.save["soul"]["expert"]
        self.assertEqual(len(expert), 57)
        # Fake category PTARMTP_09 must be removed
        self.assertIsNone(next((item for item in expert if item.get("ptarmtp") == "PTARMTP_09"), None))

        # Fists ABP must be clamped to 47,000 max
        fists = next((item for item in expert if item.get("ptarmtp") == "PTARMTP_00"), None)
        self.assertEqual(fists["lvl"], 20)
        self.assertEqual(fists["abp"], 47000)

        # Kamas ABP must be corrected to authentic table (3,800)
        kamas = next((item for item in expert if item.get("ptarmtp") == "PTARMTP_17"), None)
        self.assertEqual(kamas["lvl"], 20)
        self.assertEqual(kamas["abp"], 3800)

        # Dummy slot PTARMTP_08 must be restored to -1
        dummy08 = next((item for item in expert if item.get("ptarmtp") == "PTARMTP_08"), None)
        self.assertEqual(dummy08["abp"], -1)
        self.assertEqual(dummy08["lvl"], 1)
        self.assertEqual(dummy08["is_checked"], 0)

if __name__ == "__main__":
    unittest.main()
