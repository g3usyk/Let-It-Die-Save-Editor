# -*- coding: utf-8 -*-
import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import modifiers

class TestCurrencies(unittest.TestCase):
    def setUp(self):
        self.save = {
            "user": {"uid": 443455, "free_medal": 10, "paid_medal": 0},
            "soul": {
                "uid": 443455,
                "free_money": 1000,
                "paid_money": 0,
                "spirit": 500,
                "bloodnium_point": 200,
                "recycle_point": 50,
                "vip": {"flag": 0, "expired_time": 0}
            }
        }

    def test_set_currencies(self):
        modifiers.set_currencies(self.save, dm=999, kc=500000, spl=250000, bloodnium=10000, re_points=50000)
        user = self.save["user"]
        soul = self.save["soul"]
        self.assertEqual(user["free_medal"], 999)
        self.assertEqual(soul["free_money"], 500000)
        self.assertEqual(soul["spirit"], 250000)
        self.assertEqual(soul["bloodnium_point"], 10000)
        self.assertEqual(soul["recycle_point"], 50000)

    def test_get_player_currencies(self):
        modifiers.set_currencies(self.save, dm=50, kc=10000)
        curr = modifiers.get_player_currencies(self.save)
        self.assertEqual(curr["dm"], 50)
        self.assertEqual(curr["kc"], 10000)

    def test_max_all_currencies(self):
        modifiers.max_all_currencies(self.save)
        curr = modifiers.get_player_currencies(self.save)
        self.assertGreaterEqual(curr["dm"], 9999)
        self.assertGreaterEqual(curr["kc"], 9999999)

    def test_vip_pass_activation(self):
        modifiers.activate_vip_express_pass(self.save, days=30)
        status = modifiers.get_vip_status(self.save)
        self.assertTrue(status["active"])
        self.assertGreaterEqual(status["days_left"], 29)

if __name__ == "__main__":
    unittest.main()
