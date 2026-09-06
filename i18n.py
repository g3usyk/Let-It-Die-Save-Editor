# -*- coding: utf-8 -*-
"""
Internationalization (i18n) Module for LET IT DIE Save Editor.
Decoupled, JSON-based localization engine supporting dynamic language switching,
clean fallback cascade, entity translation helpers, and PyInstaller bundling.
"""

import os
import sys
import json
import locale
import glob

# Determine base paths for development vs frozen executable (PyInstaller)
if getattr(sys, "frozen", False):
    APP_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(sys.executable)))
    CONFIG_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_DIR = APP_DIR

CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def _find_locales_dir():
    candidates = [
        os.path.join(APP_DIR, "locales"),
        os.path.join(CONFIG_DIR, "locales"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "locales")
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return candidates[0]

LOCALES_DIR = _find_locales_dir()

def _detect_system_language():
    try:
        loc = locale.getdefaultlocale()[0] or ""
        loc_lower = loc.lower()
        if "es" in loc_lower:
            return "es"
        elif "zh" in loc_lower:
            return "zh"
        elif "ja" in loc_lower:
            return "ja"
        else:
            return "en"
    except Exception:
        return "en"

# Master Translations Dictionary populated from locales/*.json
TRANSLATIONS = {}

def load_translations_from_disk():
    global TRANSLATIONS
    loaded = {}
    if os.path.isdir(LOCALES_DIR):
        for filepath in glob.glob(os.path.join(LOCALES_DIR, "*.json")):
            lang_code = os.path.splitext(os.path.basename(filepath))[0].lower()
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        loaded[lang_code] = data
            except Exception as e:
                print(f"[i18n] Error loading locale '{filepath}': {e}", file=sys.stderr)
    
    # Ensure standard default languages exist in memory
    for fallback_lang in ("en", "es", "zh"):
        if fallback_lang not in loaded:
            loaded[fallback_lang] = {}
            
    TRANSLATIONS = loaded
    return TRANSLATIONS

# Initial load
load_translations_from_disk()

LANGUAGE_METADATA = {
    "en": {"name": "English", "native": "English", "flag": "🇺🇸"},
    "es": {"name": "Spanish", "native": "Español", "flag": "🇪🇸"},
    "zh": {"name": "Chinese", "native": "中文", "flag": "🇨🇳"},
    "ja": {"name": "Japanese", "native": "日本語", "flag": "🇯🇵"},
    "de": {"name": "German", "native": "Deutsch", "flag": "🇩🇪"},
    "fr": {"name": "French", "native": "Français", "flag": "🇫🇷"},
    "ru": {"name": "Russian", "native": "Русский", "flag": "🇷🇺"},
    "ko": {"name": "Korean", "native": "한국어", "flag": "🇰🇷"},
    "pt": {"name": "Portuguese", "native": "Português", "flag": "🇧🇷"},
}

def get_installed_languages():
    """
    Returns a dict mapping language code to native display label
    (e.g. {'es': 'Español', 'en': 'English', 'zh': '中文'}).
    Dynamically discovered from loaded translations.
    """
    langs = {}
    for code in sorted(TRANSLATIONS.keys()):
        meta = LANGUAGE_METADATA.get(code)
        if meta:
            langs[code] = meta["native"]
        else:
            langs[code] = code.upper()
    return langs

def get_available_languages():
    """Returns list of all available language codes loaded from locales/."""
    return list(TRANSLATIONS.keys())

_current_language = None

def get_language():
    global _current_language
    if _current_language is None:
        _current_language = load_saved_language()
    return _current_language

def set_language(lang_code):
    global _current_language
    lang_code = str(lang_code).lower().strip()
    if lang_code in TRANSLATIONS or lang_code in ("es", "en", "zh"):
        _current_language = lang_code
        save_language_preference(lang_code)

DEFAULT_LANGUAGE = "en"

def load_saved_language():
    """Loads saved language preference from config.json. Defaults to English ('en') if not set."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                lang = cfg.get("language")
                if lang and (lang in TRANSLATIONS or lang in ("es", "en", "zh")):
                    return lang
        except Exception:
            pass
    return DEFAULT_LANGUAGE

def save_language_preference(lang_code):
    cfg = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}
    cfg["language"] = lang_code
    try:
        cfg_dir = os.path.dirname(CONFIG_FILE)
        if cfg_dir:
            os.makedirs(cfg_dir, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def t(key, default=None, **kwargs):
    """
    Translates a key into current language with fallback cascade (lang -> en -> es -> default/key).
    Supports safe format interpolation with kwargs.
    """
    lang = get_language()
    val = TRANSLATIONS.get(lang, {}).get(key)
    if val is None and lang != "en":
        val = TRANSLATIONS.get("en", {}).get(key)
    if val is None and lang != "es":
        val = TRANSLATIONS.get("es", {}).get(key)
    if val is None:
        val = default if default is not None else key
    
    if kwargs:
        try:
            return val.format(**kwargs)
        except Exception:
            return val
    return val

def get_item_name(item):
    """Universal name resolver with fallback cascade across languages."""
    if not item:
        return ""
    lang = get_language()
    val = item.get(f"name_{lang}")
    if val:
        return val
    fallback_id = str(item.get("id", item.get("itemid", "")))
    if lang == "es":
        return item.get("name_es") or item.get("name_en") or item.get("name") or fallback_id
    else:
        return item.get("name_en") or item.get("name_es") or item.get("name") or fallback_id

def get_item_desc(item):
    """Universal description resolver with fallback cascade across languages."""
    if not item:
        return ""
    lang = get_language()
    desc = item.get(f"desc_{lang}")
    if not desc:
        if lang == "es":
            desc = item.get("desc_es") or item.get("desc_en") or ""
        else:
            desc = item.get("desc_en") or item.get("desc_es") or ""
    if "//" in desc:
        desc = desc.replace("//", "\n")
    return desc

def get_set_name(set_obj):
    """Universal set name resolver with fallback cascade across languages."""
    if not set_obj:
        return ""
    lang = get_language()
    val = set_obj.get(f"name_{lang}")
    if val:
        return val
    if lang == "es":
        return set_obj.get("name_es") or set_obj.get("name_en") or set_obj.get("id", "")
    else:
        return set_obj.get("name_en") or set_obj.get("name_es") or set_obj.get("id", "")

def get_expert_weapon_name(ptid):
    """Returns localized weapon mastery category name using translation keys with fallback."""
    key = f"wp_{ptid}"
    localized = t(key, default=None)
    if localized and localized != key:
        return localized
    
    if get_language() == "en":
        return EXPERT_WEAPON_NAMES_EN.get(ptid, EXPERT_WEAPON_NAMES_ES.get(ptid, ptid))
    else:
        return EXPERT_WEAPON_NAMES_ES.get(ptid, EXPERT_WEAPON_NAMES_EN.get(ptid, ptid))

# Legacy backward-compatibility dictionaries populated dynamically
EXPERT_WEAPON_NAMES_ES = {
    k[3:]: v for k, v in TRANSLATIONS.get("es", {}).items() if k.startswith("wp_PTARMTP_")
}
EXPERT_WEAPON_NAMES_EN = {
    k[3:]: v for k, v in TRANSLATIONS.get("en", {}).items() if k.startswith("wp_PTARMTP_")
}
