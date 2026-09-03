# -*- coding: utf-8 -*-
import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import modifiers

class TestFighters(unittest.TestCase):
    def setUp(self):
        self.save = {
            "user": {"uid": 443455},
            "bodyuser": {
                "443455": [
                    {
                        "uid": 443455,
                        "cid": "fighter_1",
                        "die": 1,
                        "hp": 0,
                        "str": 10,
                        "dex": 10,
                        "vit": 10,
                        "stm": 10,
                        "luk": 10,
                        "lvl": 25,
                        "bag": 0
                    }
                ]
            },
            "soul": {
                "uid": 443455,
                "current_died_cid": "fighter_1",
                "die_flag": 1,
                "resurrection": 1,
                "chr": {
                    "chrs": {
                        "443455": [
                            {
                                "uid": 443455,
                                "cid": "fighter_1",
                                "name": "Senpai",
                                "type": "BAL",
                                "grade": 1,
                                "lvl": 25,
                                "hp": 0,
                                "state": "DEAD"
                            }
                        ]
                    }
                }
            },
            "diedchara": {
                "dchrs": {
                    "443455": [{"cid": "fighter_1", "floor": 20}],
                    "-2": [{"cid": "npc_hater"}]
                }
            }
        }

    def test_revive_all_fighters(self):
        modifiers.revive_all_fighters(self.save)
        
        c = self.save["soul"]["chr"]["chrs"]["443455"][0]
        self.assertEqual(c["state"], "GUARD")
        self.assertGreater(c["hp"], 0)
        
        self.assertEqual(self.save["soul"]["die_flag"], 0)
        self.assertEqual(self.save["diedchara"]["dchrs"]["443455"], [])
        self.assertEqual(len(self.save["diedchara"]["dchrs"]["-2"]), 1)

    def test_update_fighter(self):
        modifiers.update_fighter(
            self.save,
            fighter_idx=0,
            name="Champion",
            grade=5,
            lvl=100,
            hp=5000,
            bag=2
        )
        c = self.save["soul"]["chr"]["chrs"]["443455"][0]
        f = self.save["bodyuser"]["443455"][0]
        self.assertEqual(c["name"], "Champion")
        self.assertEqual(c["grade"], 5)
        self.assertEqual(f["lvl"], 100)
        self.assertEqual(f["bag"], 2)

    def test_get_all_fighters_info(self):
        info = modifiers.get_all_fighters_info(self.save)
        self.assertEqual(len(info), 1)
        self.assertEqual(info[0]["cid"], "fighter_1")
        self.assertEqual(info[0]["name"], "Senpai")

    def test_grade6_transformation_prevents_freeze(self):
        # Transforming a 1-star fighter into 6-star with high stats must synchronize limit_break & bonuses!
        modifiers.update_fighter(
            self.save,
            fighter_idx=0,
            grade=6,
            lvl=247,
            str_stat=45,
            dex=45
        )
        c = self.save["soul"]["chr"]["chrs"]["443455"][0]
        f = self.save["bodyuser"]["443455"][0]
        self.assertEqual(c["grade"], 6)
        self.assertEqual(c["limit_break"], 4)
        self.assertEqual(f["skill"], 3)
        self.assertEqual(f["rage"], 1)
        self.assertEqual(f["hp_bonus"], 20)
        self.assertEqual(f["str_bonus"], 20)

    def test_update_fighter_character_model(self):
        # Update character model to Female 3
        modifiers.update_fighter(self.save, fighter_idx=0, body_model="Female 3")
        c = self.save["soul"]["chr"]["chrs"]["443455"][0]
        self.assertEqual(c["body"], "BODY_FEMALE_003")
        self.assertEqual(c["gasmask"], "ASSET_NF_GAS_HEAD_003")

        # Update character model to Male 7
        modifiers.update_fighter(self.save, fighter_idx=0, body_model="BODY_MALE_007")
        self.assertEqual(c["body"], "BODY_MALE_007")
        self.assertEqual(c["gasmask"], "ASSET_NM_GAS_HEAD_007")

    def test_swap_fighter_positions(self):
        # Add a second fighter to test swap
        self.save["bodyuser"]["443455"].append({"uid": 443455, "cid": "fighter_2", "lvl": 50})
        self.save["soul"]["chr"]["chrs"]["443455"].append({"uid": 443455, "cid": "fighter_2", "name": "Second"})
        
        self.assertEqual(self.save["soul"]["chr"]["chrs"]["443455"][0]["cid"], "fighter_1")
        self.assertEqual(self.save["soul"]["chr"]["chrs"]["443455"][1]["cid"], "fighter_2")
        
        success = modifiers.swap_fighter_positions(self.save, 0, 1)
        self.assertTrue(success)
        self.assertEqual(self.save["soul"]["chr"]["chrs"]["443455"][0]["cid"], "fighter_2")
        self.assertEqual(self.save["soul"]["chr"]["chrs"]["443455"][1]["cid"], "fighter_1")

    def test_move_fighter_up_and_down_game_freezer_order(self):
        # Save has 2 fighters: index 0 (F1) and index 1 (F2)
        self.save["bodyuser"]["443455"].append({"uid": 443455, "cid": "fighter_2", "lvl": 50})
        self.save["soul"]["chr"]["chrs"]["443455"].append({"uid": 443455, "cid": "fighter_2", "name": "Second"})
        
        # Move Slot 2 (index 1, F2) UP: F2 becomes Slot 1!
        success_up = modifiers.move_fighter_up(self.save, 1)
        self.assertTrue(success_up)
        self.assertEqual(self.save["bodyuser"]["443455"][0]["cid"], "fighter_2")
        self.assertEqual(self.save["bodyuser"]["443455"][1]["cid"], "fighter_1")
        
        # Move Slot 1 (index 0, F2) DOWN: F2 goes back to Slot 2!
        success_down = modifiers.move_fighter_down(self.save, 0)
        self.assertTrue(success_down)
        self.assertEqual(self.save["bodyuser"]["443455"][0]["cid"], "fighter_1")
        self.assertEqual(self.save["bodyuser"]["443455"][1]["cid"], "fighter_2")


    def test_create_new_fighter(self):
        ok, new_cid = modifiers.create_new_fighter(
            self.save,
            name="Alpha Striker",
            clazz="BRE",
            grade=6,
            body_model="Male 2",
            max_stats=True
        )
        self.assertTrue(ok)
        self.assertIsNotNone(new_cid)
        
        fighters = self.save["bodyuser"]["443455"]
        chrs = self.save["soul"]["chr"]["chrs"]["443455"]
        self.assertEqual(len(fighters), 2)
        self.assertEqual(fighters[1]["cid"], new_cid)
        self.assertEqual(fighters[1]["lvl"], 247)
        self.assertEqual(fighters[1]["hp_bonus"], 20)
        self.assertEqual(chrs[1]["name"], "Alpha Striker")
        self.assertEqual(chrs[1]["body"], "BODY_MALE_002")
        self.assertEqual(chrs[1]["type"], "BRE")
        
        # Check slot sync
        slots = self.save["soul"]["chr"]["slots"]["443455"]
        self.assertEqual(slots[1]["cid"], new_cid)

    def test_clone_fighter(self):
        # Add decal to original fighter
        self.save.setdefault("soul", {}).setdefault("skl", {}).setdefault("eqskl", {})["443455"] = [
            {"uid": 443455, "cid": "fighter_1", "slot": 0, "sklid": "SKL_01"}
        ]
        # Add equipped armor and weapon to deathbag
        self.save.setdefault("part", {}).setdefault("pts", {})["443455"] = [
            {"uid": 443455, "eid": "armor_eid_1", "ptid": "PT_REC_HEAD_102_G", "dur": 1000, "lvl": 4}
        ]
        self.save.setdefault("soul", {}).setdefault("deathbag", {})["443455"] = {
            "fighter_1": [
                {"uid": 443455, "cid": "fighter_1", "slot": 0, "type": 0, "eid": "armor_eid_1", "site": "EQSITE_HEAD", "arm_slot": -1}
            ]
        }
        
        ok, clone_cid = modifiers.clone_fighter(self.save, 0, new_name="Senpai Clone")
        self.assertTrue(ok)
        
        fighters = self.save["bodyuser"]["443455"]
        chrs = self.save["soul"]["chr"]["chrs"]["443455"]
        self.assertEqual(len(fighters), 2)
        self.assertEqual(chrs[1]["name"], "Senpai Clone")
        self.assertEqual(fighters[1]["cid"], clone_cid)
        
        # Check cloned decals
        eq_list = self.save["soul"]["skl"]["eqskl"]["443455"]
        self.assertEqual(len(eq_list), 2)
        self.assertTrue(any(d["cid"] == clone_cid and d["sklid"] == "SKL_01" for d in eq_list))
        
        # Check cloned deathbag & equipped armor
        clone_db = self.save["soul"]["deathbag"]["443455"][clone_cid]
        self.assertEqual(len(clone_db), 1)
        self.assertEqual(clone_db[0]["cid"], clone_cid)
        self.assertEqual(clone_db[0]["site"], "EQSITE_HEAD")
        clone_eid = clone_db[0]["eid"]
        self.assertNotEqual(clone_eid, "armor_eid_1")
        
        # Check that part.pts contains the cloned armor entity
        pts_list = self.save["part"]["pts"]["443455"]
        self.assertEqual(len(pts_list), 2)
        cloned_pt = next((p for p in pts_list if p.get("eid") == clone_eid), None)
        self.assertIsNotNone(cloned_pt)
        self.assertEqual(cloned_pt["ptid"], "PT_REC_HEAD_102_G")
        self.assertEqual(cloned_pt["dur"], 1000)

    def test_delete_fighter(self):
        # Create a second fighter first
        ok, cid2 = modifiers.create_new_fighter(self.save, name="Temp Fighter")
        self.assertTrue(ok)
        self.assertEqual(len(self.save["bodyuser"]["443455"]), 2)
        
        # Cannot delete in-use fighter
        self.save["soul"]["chr"]["chrs"]["443455"][0]["state"] = "USE"
        del_fail, _ = modifiers.delete_fighter(self.save, 0)
        self.assertFalse(del_fail)
        
        # Can delete second fighter
        del_ok, _ = modifiers.delete_fighter(self.save, 1)
        self.assertTrue(del_ok)
        self.assertEqual(len(self.save["bodyuser"]["443455"]), 1)
        
        # Cannot delete the only remaining fighter
        self.save["soul"]["chr"]["chrs"]["443455"][0]["state"] = "GUARD"
        last_del_fail, _ = modifiers.delete_fighter(self.save, 0)
        self.assertFalse(last_del_fail)


if __name__ == "__main__":
    unittest.main()



