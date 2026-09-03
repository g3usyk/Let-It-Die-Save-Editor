# -*- coding: utf-8 -*-
import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import i18n
from i18n import t

class TestI18n(unittest.TestCase):
    def test_key_parity_between_languages(self):
        es_keys = set(i18n.TRANSLATIONS["es"].keys())
        en_keys = set(i18n.TRANSLATIONS["en"].keys())
        diff = es_keys ^ en_keys
        self.assertEqual(len(diff), 0, f"Translation key mismatch: {diff}")
        self.assertGreater(len(es_keys), 350)

    def test_translation_formatting(self):
        i18n.set_language("en")
        s_en = t("inv_cap_lbl", used=10, total=100, free=90, pct=10.0)
        self.assertIn("10", s_en)
        self.assertIn("100", s_en)
        self.assertIn("Locker", s_en)
        
        i18n.set_language("es")
        s_es = t("inv_cap_lbl", used=10, total=100, free=90, pct=10.0)
        self.assertIn("10", s_es)
        self.assertIn("Almacén", s_es)

    def test_unknown_key_fallback(self):
        res = t("non_existent_key_12345")
        self.assertEqual(res, "non_existent_key_12345")

if __name__ == "__main__":
    unittest.main()
