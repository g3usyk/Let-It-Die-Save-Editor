# -*- coding: utf-8 -*-
import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import modifiers

class TestTower(unittest.TestCase):
    def setUp(self):
        self.save = {
            "soul": {
                "openelvflr": [],
                "areaflag": [],
                "areaescflag": [],
                "quest": {"user": []}
            },
            "playlog": {"base": {}},
            "gameflg": {"cl": []},
            "floor": {"stamp": {}}
        }

    def test_unlock_all_tower_elevators_and_map(self):
        count = modifiers.unlock_all_tower_elevators(self.save)
        self.assertIsInstance(count, int)
        self.assertIsInstance(self.save["soul"]["openelvflr"], list)

    def test_set_all_stamps_perfect(self):
        stamps_count = modifiers.set_all_stamps_perfect(self.save)
        self.assertEqual(stamps_count, 40)
        stamps = self.save["floor"]["stamp"]["stamps"]
        self.assertEqual(len(stamps), 40)
        self.assertTrue(all(s["offset"] == 0 for s in stamps))
        pr_user = self.save["soul"].get("partresearch", {}).get("user", [])
        scythe_entries = [r for r in pr_user if r.get("ptid") == "PT_ARM_WP050_001"]
        self.assertGreaterEqual(len(scythe_entries), 5)

    def test_complete_encyclopedia_books(self):
        maquest = modifiers.complete_encyclopedia_books(self.save)
        self.assertGreater(len(self.save["soul"]["msrbook"]), 50)
        self.assertGreater(len(self.save["soul"]["bstbook"]), 20)

    def test_complete_all_quests(self):
        count = modifiers.complete_all_quests(self.save)
        self.assertGreater(count, 0)
        user_quests = self.save["soul"]["quest"]['user']
        self.assertGreater(len(user_quests), 0)

if __name__ == "__main__":
    unittest.main()
