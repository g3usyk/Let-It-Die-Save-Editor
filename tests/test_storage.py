# -*- coding: utf-8 -*-
import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import modifiers

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.save = {
            "soul": {
                "cl": [{"slot": i, "type": -1, "eid": ""} for i in range(50)]
            },
            "item": {"items": []},
            "mushroom": {"msrs": []},
            "beast": {"bsts": []},
            "part": {"pts": []}
        }

    def test_expand_coin_locker_capacity(self):
        old_cap, new_cap = modifiers.expand_coin_locker_capacity(self.save, target_capacity=100)
        self.assertEqual(old_cap, 50)
        self.assertEqual(new_cap, 100)
        self.assertEqual(len(self.save["soul"]["cl"]), 100)

    def test_add_material_to_storage(self):
        added = modifiers.add_material_to_storage(self.save, "ITMT_IRON_1", count=5)
        self.assertEqual(added, 5)
        self.assertEqual(len(self.save["item"]["items"]), 5)
        
        analysis = modifiers.analyze_storage_stock(self.save)
        self.assertEqual(analysis["used_slots"], 5)
        self.assertEqual(analysis["total_items"], 5)
        self.assertEqual(analysis["capacity"], analysis["total_slots"])
        self.assertEqual(analysis["stock_by_id"]["ITMT_IRON_1"], 5)

    def test_add_mushrooms_and_beasts(self):
        added_m = modifiers.add_material_to_storage(self.save, "MSR_001", count=3)
        added_b = modifiers.add_material_to_storage(self.save, "BST_GFROG", count=2)
        
        self.assertEqual(added_m, 3)
        self.assertEqual(added_b, 2)
        self.assertEqual(len(self.save["mushroom"]["msrs"]), 3)
        self.assertEqual(len(self.save["beast"]["bsts"]), 2)

    def test_smart_top_up_materials(self):
        modifiers.add_material_to_storage(self.save, "ITMT_COPPER_1", count=5)
        modifiers.add_material_to_storage(self.save, "ITMT_ALUMI_1", count=20)
        
        types, units = modifiers.smart_top_up_materials(
            self.save,
            target_qty=15,
            materials_list=["ITMT_COPPER_1", "ITMT_ALUMI_1"]
        )
        self.assertEqual(types, 1)
        self.assertEqual(units, 10)
        
        analysis = modifiers.analyze_storage_stock(self.save)
        self.assertEqual(analysis["stock_by_id"]["ITMT_COPPER_1"], 15)
        self.assertEqual(analysis["stock_by_id"]["ITMT_ALUMI_1"], 20)

    def test_add_all_materials_to_storage(self):
        added = modifiers.add_all_materials_to_storage(self.save, count=2)
        self.assertGreaterEqual(added, 100)
        self.assertGreaterEqual(len(self.save["item"]["items"]), 200)

    def test_add_materials_to_dict_schema_save(self):
        dict_save = {
            "soul": {"cl": []},
            "item": {"items": {}},
            "mushroom": {"msrs": {}},
            "beast": {"bsts": {}}
        }
        added = modifiers.add_material_to_storage(dict_save, "ITMT_IRON_1", count=50)
        self.assertEqual(added, 50)
        self.assertIsInstance(dict_save["item"]["items"], list)
        self.assertEqual(len(dict_save["item"]["items"]), 50)

if __name__ == "__main__":
    unittest.main()
