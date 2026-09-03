# -*- coding: utf-8 -*-
import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.helpers import get_save_summary, get_account_overview, get_player_uid, get_masters_db_path

class TestHelpers(unittest.TestCase):
    def test_get_save_summary_empty_and_valid(self):
        summary_empty = get_save_summary({})
        self.assertIsInstance(summary_empty, dict)
        self.assertEqual(summary_empty["player_name"], "Unknown")
        self.assertIn("vip_days_remaining", summary_empty)

        valid_save = {
            "user": {"nm": "Senpai", "uid": "12345", "free_medal": 50},
            "soul": {"rank": 100, "vip": {"flag": 1, "expired_time": 9999999999}}
        }
        summary = get_save_summary(valid_save)
        self.assertEqual(summary["player_name"], "Senpai")
        self.assertTrue(summary["vip_active"])
        self.assertGreater(summary["vip_days_remaining"], 0)

    def test_get_account_overview(self):
        overview = get_account_overview({"user": {"uid": "777", "login_count": 42}})
        self.assertEqual(overview["uid"], "777")
        self.assertEqual(overview["login_count"], 42)

    def test_get_player_uid_fallbacks(self):
        self.assertEqual(get_player_uid({}), "0")
        self.assertEqual(get_player_uid({"user": {"uid": 999}}), "999")
        self.assertEqual(get_player_uid({"soul": {"uid": "888"}}), "888")

if __name__ == "__main__":
    unittest.main()
