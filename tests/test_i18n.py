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

    def test_locales_directory_loading(self):
        self.assertTrue(os.path.isdir(i18n.LOCALES_DIR))
        available = i18n.get_available_languages()
        self.assertIn("es", available)
        self.assertIn("en", available)
        self.assertIn("zh", available)

    def test_entity_helpers(self):
        fake_item = {
            "id": "TEST_ITEM_01",
            "name_en": "Super Armor",
            "name_es": "Súper Armadura",
            "desc_en": "Protects against attacks.",
            "desc_es": "Protege contra ataques."
        }
        i18n.set_language("en")
        self.assertEqual(i18n.get_item_name(fake_item), "Super Armor")
        self.assertEqual(i18n.get_item_desc(fake_item), "Protects against attacks.")

        i18n.set_language("es")
        self.assertEqual(i18n.get_item_name(fake_item), "Súper Armadura")
        self.assertEqual(i18n.get_item_desc(fake_item), "Protege contra ataques.")

        i18n.set_language("zh")
        # Falls back to en if no zh name provided
        self.assertEqual(i18n.get_item_name(fake_item), "Super Armor")

    def test_weapon_expert_localization(self):
        i18n.set_language("es")
        self.assertEqual(i18n.get_expert_weapon_name("PTARMTP_00"), "Manos Desnudas")
        i18n.set_language("en")
        self.assertEqual(i18n.get_expert_weapon_name("PTARMTP_00"), "Bare Fists")
        i18n.set_language("zh")
        self.assertEqual(i18n.get_expert_weapon_name("PTARMTP_00"), "空手")

    def test_default_language_is_en_and_persists_user_choice(self):
        self.assertEqual(i18n.DEFAULT_LANGUAGE, "en")
        
        # Test preference saving and loading
        i18n.set_language("es")
        self.assertEqual(i18n.get_language(), "es")
        self.assertEqual(i18n.load_saved_language(), "es")

        i18n.set_language("zh")
        self.assertEqual(i18n.get_language(), "zh")
        self.assertEqual(i18n.load_saved_language(), "zh")

        i18n.set_language("en")
        self.assertEqual(i18n.get_language(), "en")
        self.assertEqual(i18n.load_saved_language(), "en")

    def test_multilingual_filter_tokens(self):
        from ui.tabs.materials_tab import MaterialsTabMixin

        for lang in ("es", "en", "zh"):
            i18n.set_language(lang)
            for k in ("mat_all", "decal_all", "bp_slot_all", "bp_fac_all", "bp_poss_all", "bp_dmg_all"):
                val = t(k)
                self.assertTrue(bool(val), f"Missing translation for {k} in {lang}")
            
            # Universal 'All' filter pass-through
            all_token = t("mat_all")
            self.assertTrue(MaterialsTabMixin._match_material_category(all_token, "Aluminio (Aluminum)"))
            self.assertTrue(MaterialsTabMixin._match_material_category(all_token, "Boss Metals"))

        # Category matching with Chinese labels
        self.assertTrue(MaterialsTabMixin._match_material_category("铝 (Aluminum)", "Aluminio"))
        self.assertTrue(MaterialsTabMixin._match_material_category("铜 (Copper)", "Cobre (Copper)"))
        self.assertTrue(MaterialsTabMixin._match_material_category("铁与钢 (Iron & Steel)", "Hierro y Acero"))
        self.assertTrue(MaterialsTabMixin._match_material_category("Boss金属 (Boss Metals)", "Boss Metals"))
        self.assertTrue(MaterialsTabMixin._match_material_category("类固醇 / Rostest (Fighters)", "Esteroides / Rostest"))

if __name__ == "__main__":
    unittest.main()
