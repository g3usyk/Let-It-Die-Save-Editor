# -*- coding: utf-8 -*-
import unittest
import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import modifiers


class TestTDM(unittest.TestCase):
    def setUp(self):
        self.save = {
            "user": {"uid": 443455},
            "soul": {
                "uid": 443455,
                "is_fort_ready": 0,
                "last_tdm_reset_time": 0,
                "last_tdm_rank": "",
                "tdm_rank": "TDM_RANK_01_01",
                "tdm_point": 0,
                "rank": 123,
                "rank_point": 54000000000,
                "team_id": "",
                "chr": {
                    "chrs": {
                        "443455": [
                            {"cid": "c1", "grade": 6},
                            {"cid": "c2", "grade": 6},
                            {"cid": "c3", "grade": 6}
                        ]
                    }
                }
            },
            "bodyuser": {
                "443455": [
                    {"cid": "c1", "lvl": 247, "grade": 6},
                    {"cid": "c2", "lvl": 247, "grade": 6},
                    {"cid": "c3", "lvl": 247, "grade": 6}
                ]
            },
            "fortmatch": {"443455": {}},
            "fortzmbsetting": {},
            "fortresult": {},
            "teamhate": {},
            "tdmsituation": [{"idx": 1, "data": "{}"}]
        }

    def test_season_reset_popup_protection(self):
        now = int(time.time())
        modifiers.repair_and_sanitize_tdm(self.save)
        soul = self.save["soul"]
        self.assertEqual(soul["is_fort_ready"], 1)
        self.assertGreater(soul["last_tdm_reset_time"], now)
        self.assertEqual(soul["last_tdm_rank"], soul["tdm_rank"])

    def test_infinite_loading_structures_repaired(self):
        modifiers.repair_and_sanitize_tdm(self.save)
        self.assertIsInstance(self.save["fortmatch"]["443455"], list)
        self.assertGreater(len(self.save["fortmatch"]["443455"]), 0)
        self.assertIsInstance(self.save["fortzmbsetting"], list)
        self.assertIsInstance(self.save["fortresult"], list)
        self.assertIsInstance(self.save["teamhate"], list)
        self.assertGreaterEqual(len(self.save["teamhate"]), 0)
        self.assertEqual(self.save["soul"]["team_id"], "52")
        self.assertEqual(self.save["teammember"]["tid"], 52)
        self.assertEqual(self.save["tdmsituation"][0]["data"], "[]")

    def test_player_rank_mathematical_formula(self):
        calc_rank = modifiers.calculate_player_rank(self.save)
        # 3 Grade 6 fighters: (6-1)*15 + 3 = 78
        self.assertEqual(calc_rank, 78)
        modifiers.repair_and_sanitize_tdm(self.save)
        soul = self.save["soul"]
        self.assertEqual(soul["rank"], 78)
        self.assertLess(soul["rank_point"], 54000000000)

    def test_dummy_defenders_preserved_and_populated(self):
        # Corrupt save with foreign positive UID and rogue negative UID
        self.save["bodyuser"]["999999"] = [{"cid": "bad"}]
        self.save["bodyuser"]["-99"] = [{"cid": "bad_neg"}]
        modifiers.repair_and_sanitize_tdm(self.save)

        bu = self.save["bodyuser"]
        ch = self.save["soul"]["chr"]["chrs"]
        # Must retain player UID 443455
        self.assertIn("443455", bu)
        self.assertIn("443455", ch)
        # Must retain valid dummy negative UIDs (-1 through -13)
        for i in range(1, 14):
            neg_uid = f"-{i}"
            self.assertIn(neg_uid, bu)
            self.assertIn(neg_uid, ch)
            self.assertGreater(len(bu[neg_uid]), 0)
            self.assertGreater(len(ch[neg_uid]), 0)
        # Foreign positive and unrecognized negative UIDs must be cleaned
        self.assertNotIn("999999", bu)
        self.assertNotIn("-99", bu)
