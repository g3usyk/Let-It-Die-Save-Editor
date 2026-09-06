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
        zh_keys = set(i18n.TRANSLATIONS["zh"].keys())
        self.assertEqual(len(es_keys ^ en_keys), 0, f"ES/EN mismatch: {es_keys ^ en_keys}")
        self.assertEqual(len(en_keys ^ zh_keys), 0, f"EN/ZH mismatch: {en_keys ^ zh_keys}")
        self.assertGreater(len(es_keys), 400)

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

        i18n.set_language("zh")
        s_zh = t("inv_cap_lbl", used=10, total=100, free=90, pct=10.0)
        self.assertIn("10", s_zh)
        self.assertIn("仓库", s_zh)

    def test_unknown_key_fallback(self):
        res = t("non_existent_key_12345")
        self.assertEqual(res, "non_existent_key_12345")

if __name__ == "__main__":
    unittest.main()
