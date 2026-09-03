# -*- coding: utf-8 -*-
import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import modifiers

class TestDecals(unittest.TestCase):
    def setUp(self):
        self.save = {
            "user": {"uid": 443455},
            "soul": {
                "uid": 443455,
                "skl": {
                    "psskl": [],
                    "eqskl": {}
                }
            }
        }

    def test_load_all_known_decals(self):
        decals = modifiers.load_all_known_decals()
        self.assertGreater(len(decals), 500)
        self.assertIn("SKL_HPUP_01", decals)

    def test_add_or_update_decals(self):
        modifiers.add_or_update_decals(self.save, ["SKL_HPUP_01", "SKL_DRAIN_01"], count=3, premium=True)
        psskl = self.save["soul"]["skl"]["psskl"]
        self.assertGreaterEqual(len(psskl), 2)
        decal_map = {d["sklid"]: d for d in psskl}
        self.assertIn("SKL_HPUP_01_P", decal_map)
        self.assertEqual(decal_map["SKL_HPUP_01_P"]["cnt"], 3)

    def test_equip_decal_preset_on_fighter(self):
        preset_name, count = modifiers.equip_decal_preset_on_fighter(self.save, "fighter_1", preset_key="tengoku_climber")
        self.assertGreaterEqual(count, 5)
        user_eq = self.save["soul"]["skl"]["eqskl"]["443455"]
        fighter_decals = [e for e in user_eq if e["cid"] == "fighter_1"]
        self.assertEqual(len(fighter_decals), count)

if __name__ == "__main__":
    unittest.main()
