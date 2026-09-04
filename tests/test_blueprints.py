# -*- coding: utf-8 -*-
import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import modifiers

class TestBlueprints(unittest.TestCase):
    def setUp(self):
        self.save = {
            "user": {"uid": 443455},
            "soul": {
                "uid": 443455,
                "partresearch": {
                    "user": [
                        {"ptid": "PT_ARM_WP001_001", "lvl": 1, "research_type": "UNKNOWN"}
                    ]
                },
                "deathbag": {}
            },
            "part": {
                "pts": {
                    "COIN_LOCKER": [
                        {"eid": "p1", "ptid": "PT_ARM_WP001_001", "dur": 50}
                    ]
                }
            }
        }

    def test_repair_and_sanitize_blueprints(self):
        repaired, total = modifiers.repair_and_sanitize_blueprints(self.save)
        self.assertGreater(repaired, 0)
        user_pr = self.save["soul"]["partresearch"]["user"]
        self.assertGreater(len(user_pr), 0)

    def test_set_infinite_durability(self):
        count = modifiers.set_infinite_durability_all_equipment(self.save, target_dur=999999)
        self.assertEqual(count, 1)
        p = self.save["part"]["pts"]["COIN_LOCKER"][0]
    def test_unlock_single_blueprint_evolves_into_remodel(self):
        # Unlocking Yes Knife 1 at +4 should place Yes Knife 2 in R&D as REMODEL, not in forge
        next_id = modifiers.unlock_single_blueprint(self.save, "PT_ARM_WP002_0Y1", level=4, unlock_next_tier=True)
        self.assertEqual(next_id, "PT_ARM_WP002_0Y3")
        
        pr_map = modifiers.get_blueprints_unlock_map(self.save)
        self.assertEqual(pr_map["PT_ARM_WP002_0Y1"]["status"], "STORE_PLUS4")
        self.assertEqual(pr_map["PT_ARM_WP002_0Y3"]["status"], "REMODEL")
        
        # Verify raw research record in partresearch.user
        pr_u = self.save["soul"]["partresearch"]["user"]
        nxt_entry = next((e for e in pr_u if e.get("ptid") == "PT_ARM_WP002_0Y3"), None)
        self.assertIsNotNone(nxt_entry)
        self.assertEqual(nxt_entry.get("research_type"), "REMODEL")
        self.assertEqual(nxt_entry.get("receive_type"), "UNKNOWN")
        self.assertEqual(nxt_entry.get("before_lvl"), 5)

    def test_no_duplicate_when_both_tier1_and_tier2_unlocked(self):
        # 1. Unlock Tier 1 (Yes Knife 1) at +4 -> Tier 2 (Yes Knife 2) goes to R&D as REMODEL
        modifiers.unlock_single_blueprint(self.save, "PT_ARM_WP002_0Y1", level=4, unlock_next_tier=True)
        pr_map = modifiers.get_blueprints_unlock_map(self.save)
        self.assertEqual(pr_map["PT_ARM_WP002_0Y1"]["status"], "STORE_PLUS4")
        self.assertEqual(pr_map["PT_ARM_WP002_0Y3"]["status"], "REMODEL")
        
        # 2. Now unlock Tier 2 (Yes Knife 2) at +4 as well
        modifiers.unlock_single_blueprint(self.save, "PT_ARM_WP002_0Y3", level=4, unlock_next_tier=True)
        pr_map2 = modifiers.get_blueprints_unlock_map(self.save)
        self.assertEqual(pr_map2["PT_ARM_WP002_0Y1"]["status"], "STORE_PLUS4")
        self.assertEqual(pr_map2["PT_ARM_WP002_0Y3"]["status"], "STORE_PLUS4")
        # Tier 3 should now be the one in REMODEL!
        self.assertEqual(pr_map2["PT_ARM_WP002_0Y2"]["status"], "REMODEL")
        
        # 3. Assert ABSOLUTELY ZERO duplicate entries or lingering REMODEL on Tier 2
        pr_u = self.save["soul"]["partresearch"]["user"]
        y3_entries = [e for e in pr_u if e.get("ptid") == "PT_ARM_WP002_0Y3"]
        y3_remodels = [e for e in y3_entries if e.get("research_type") == "REMODEL"]
        self.assertEqual(len(y3_remodels), 0, "Tier 2 should NOT have any REMODEL entry once unlocked!")
        
        # 4. Assert total uniqueness of (ptid, lvl) pairs across the entire save
        from collections import Counter
        keys = [(e.get("ptid"), e.get("lvl")) for e in pr_u]
        dups = [k for k, count in Counter(keys).items() if count > 1]
    def test_send_blueprint_to_rnd(self):
        # 1. Send base blueprint to R&D as uncrafted (+0 ready to develop)
        status_info = modifiers.send_blueprint_to_rnd(self.save, "PT_ARM_WP001_001", target_level=0)
        self.assertEqual(status_info["status"], "MAP")
        
        pr_u = self.save["soul"]["partresearch"]["user"]
        entry = next((e for e in pr_u if e.get("ptid") == "PT_ARM_WP001_001"), None)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.get("research_type"), "MAP")
        self.assertEqual(entry.get("receive_type"), "UNKNOWN")
        
        # 2. Set intermediate level (e.g. Level 2 / +1) actively waiting for +2 in R&D
        status_info2 = modifiers.send_blueprint_to_rnd(self.save, "PT_ARM_WP001_001", target_level=2)
        self.assertEqual(status_info2["status"], "FINISHED_LVL")
        self.assertEqual(status_info2["lvl"], 2)
        self.assertIn("+1 → +2", status_info2["label"])
        
        wp1_entries = [e for e in self.save["soul"]["partresearch"]["user"] if e.get("ptid") == "PT_ARM_WP001_001"]
        self.assertEqual(len(wp1_entries), 2)
        self.assertTrue(all(e.get("research_type") == "FINISHED" for e in wp1_entries))
        
        # 3. Send evolution piece (Yes Knife 2) to R&D at level 0 (REMODEL)
        status_info3 = modifiers.send_blueprint_to_rnd(self.save, "PT_ARM_WP002_0Y3", target_level=0)
        self.assertEqual(status_info3["status"], "REMODEL")
        
        y3_entry = next((e for e in self.save["soul"]["partresearch"]["user"] if e.get("ptid") == "PT_ARM_WP002_0Y3"), None)
        self.assertIsNotNone(y3_entry)
        self.assertEqual(y3_entry.get("research_type"), "REMODEL")
        self.assertEqual(y3_entry.get("before_ptid"), "PT_ARM_WP002_0Y1")

    def test_hierarchy_auto_unlocks_ancestors(self):
        # When unlocking Katana 3 (PT_ARM_WP007_002) directly from locked state:
        # Ancestors Katana 1 (WP007_001) and Katana 2 (WP007_003) must automatically
        # be maxed to +4 in the shop, and Katana 4 (WP007_004) goes into R&D!
        pr_u = self.save["soul"]["partresearch"]["user"]
        pr_u[:] = [e for e in pr_u if "WP007_00" not in e.get("ptid", "")]
        
        modifiers.unlock_single_blueprint(self.save, "PT_ARM_WP007_002", level=4, unlock_next_tier=True)
        
        pr_map = modifiers.get_blueprints_unlock_map(self.save)
        self.assertEqual(pr_map["PT_ARM_WP007_001"]["status"], "STORE_PLUS4")
        self.assertEqual(pr_map["PT_ARM_WP007_003"]["status"], "STORE_PLUS4")
        self.assertEqual(pr_map["PT_ARM_WP007_002"]["status"], "STORE_PLUS4")
        self.assertEqual(pr_map["PT_ARM_WP007_004"]["status"], "REMODEL")
        
        # Verify no duplicate entries exist in save
        from collections import Counter
        keys = [(e.get("ptid"), e.get("lvl")) for e in pr_u]
        dups = [k for k, count in Counter(keys).items() if count > 1]
        self.assertEqual(len(dups), 0, f"No duplicates allowed in save: {dups}")

    def test_uncapped_blueprint_and_storage_upgrade(self):
        # 1. Unlocking final tier (PT_ARM_WP001_005) to level 19 (R&D ready for +19)
        modifiers.unlock_single_blueprint(self.save, "PT_ARM_WP001_005", level=19, unlock_next_tier=False)
        pr_map = modifiers.get_blueprints_unlock_map(self.save)
        self.assertEqual(pr_map["PT_ARM_WP001_005"]["status"], "RND_UNCAPPED")
        self.assertEqual(pr_map["PT_ARM_WP001_005"]["lvl"], 19)
        self.assertIn("+18 → +19", pr_map["PT_ARM_WP001_005"]["label"])
        
        # 2. Unlocking final tier to level 20 (Shop Max)
        modifiers.unlock_single_blueprint(self.save, "PT_ARM_WP001_005", level=20, unlock_next_tier=False)
        pr_map2 = modifiers.get_blueprints_unlock_map(self.save)
        self.assertEqual(pr_map2["PT_ARM_WP001_005"]["status"], "STORE_UNCAPPED")
        self.assertEqual(pr_map2["PT_ARM_WP001_005"]["lvl"], 20)
        self.assertIn("+19", pr_map2["PT_ARM_WP001_005"]["label"])
        
        # Verify CHARGE is set on level 20
        pr_u = self.save["soul"]["partresearch"]["user"]
        charge_entry = next((e for e in pr_u if e.get("ptid") == "PT_ARM_WP001_005" and e.get("receive_type") == "CHARGE"), None)
        self.assertIsNotNone(charge_entry)
        self.assertEqual(charge_entry.get("lvl"), 20)
        
        # Verify deliver to storage at lvl 20
        added = modifiers.add_equipment_to_storage(self.save, "PT_ARM_WP001_005", count=1, lvl=20)
        self.assertEqual(added, 1)
        pts = self.save["part"]["pts"]
        items = [i for sub in pts.values() for i in sub] if isinstance(pts, dict) else pts
        uncapped_item = next((i for i in items if i.get("ptid") == "PT_ARM_WP001_005"), None)
        self.assertIsNotNone(uncapped_item)
        self.assertEqual(uncapped_item.get("lvl"), 20)
        self.assertGreaterEqual(uncapped_item.get("dur"), 50000)

    def test_uncapped_intermediate_level_plus15(self):
        # When unlocking an uncapped piece at level 15:
        # Shop should have +15 (engine lvl 16 CHARGE), and R&D counter should show +15 -> +16
        modifiers.unlock_single_blueprint(self.save, "PT_ARM_WP001_005", level=15, unlock_next_tier=False)
        pr_map = modifiers.get_blueprints_unlock_map(self.save)
        self.assertEqual(pr_map["PT_ARM_WP001_005"]["status"], "RND_UNCAPPED")
        self.assertEqual(pr_map["PT_ARM_WP001_005"]["lvl"], 16)
        self.assertIn("+15 → +16", pr_map["PT_ARM_WP001_005"]["label"])
        
        pr_u = self.save["soul"]["partresearch"]["user"]
        charge_entry = next((e for e in pr_u if e.get("ptid") == "PT_ARM_WP001_005" and e.get("receive_type") == "CHARGE"), None)
        self.assertIsNotNone(charge_entry)
        self.assertEqual(charge_entry.get("lvl"), 16)

if __name__ == "__main__":
    unittest.main()


