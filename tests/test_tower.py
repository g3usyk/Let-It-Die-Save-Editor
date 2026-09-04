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
        self.assertEqual(count, 61)
        self.assertGreaterEqual(len(self.save["soul"]["areaflag"]), 900)
        self.assertGreaterEqual(len(self.save["soul"]["areaescflag"]), 1000)
        self.assertGreaterEqual(self.save["playlog"]["base"]["max_floor"], 51)

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

    def test_reset_tower_interruptions(self):
        self.save["playlog"]["base"]["interruption"] = 5
        self.save["force_shutdown_counts"] = {"session_1": 2, "session_2": 3}
        old_cnt = modifiers.reset_tower_interruptions(self.save)
        self.assertEqual(old_cnt, 5)
        self.assertEqual(self.save["playlog"]["base"]["interruption"], 0)
        self.assertIsInstance(self.save["force_shutdown_counts"], dict)
        self.assertEqual(self.save["force_shutdown_counts"]["session_1"], 0)
        self.assertEqual(self.save["force_shutdown_counts"]["session_2"], 0)

    def test_unlock_tutorial_and_waiting_room(self):
        fresh_save = {
            "user": {"uid": 99999},
            "soul": {"stgid": "STG_MET_TUTORIAL", "flrid": "FLR_01", "areaid": "AREA_01"}
        }
        res = modifiers.unlock_tutorial_and_waiting_room(fresh_save)
        self.assertTrue(res)
        
        # Verify sv flags
        sv = fresh_save.get("gameflg", {}).get("sv", [])
        tut_prog = next((f.get("value") for f in sv if f.get("var") == "KGF_TUTORIAL_PROGRESS"), None)
        self.assertEqual(tut_prog, 100)
        
        # Verify cl flags
        cl = fresh_save.get("gameflg", {}).get("cl", [])
        cl_dict = {f.get("var"): f.get("value") for f in cl}
        self.assertEqual(cl_dict.get("KGF_FIRST_KIWAKOROOM"), 1)
        self.assertEqual(cl_dict.get("KGF_FIRST_BASE"), 1)
        self.assertEqual(cl_dict.get("KGF_FIRST_SHOP_BASE"), 1)
        self.assertEqual(cl_dict.get("KGF_FIRST_KINOKOYA"), 1)
        self.assertEqual(cl_dict.get("KGF_FIRST_NAOMI"), 1)
        self.assertEqual(cl_dict.get("KGF_FIRST_VIP_ELEVATORGIRL"), 1)
        self.assertEqual(cl_dict.get("KGF_MET_TUTORIAL_CLEAR"), 1)
        self.assertEqual(cl_dict.get("KGF_TUTORIAL_COMP"), 1)
        
        # Verify safe waiting room coordinates
        self.assertEqual(fresh_save["soul"]["stgid"], "")
        self.assertEqual(fresh_save["soul"]["flrid"], "")
        self.assertEqual(fresh_save["soul"]["areaid"], "")

    def test_unlock_all_tower_elevators_also_unlocks_tutorial(self):
        fresh_save = {"user": {"uid": 88888}}
        modifiers.unlock_all_tower_elevators(fresh_save)
        self.assertTrue(modifiers.is_tutorial_cleared(fresh_save))

if __name__ == "__main__":
    unittest.main()
