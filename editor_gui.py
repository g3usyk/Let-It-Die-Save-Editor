# -*- coding: utf-8 -*-
"""
LET IT DIE (Offline) - Deep Save Editor Pro v3.5 (Master Cyberpunk Encyclopedia Edition)
Complete Visual Redesign matching ArmorSetViewerDialog quality standard across all tabs.
"""

import os
import sys
import json
import time
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from PIL import Image, ImageTk

import save_io
from save_io import get_default_save_path, decompress_save, save_to_file
import modifiers
import updater
import i18n
from i18n import t, get_item_name, get_item_desc, get_set_name

# Base paths
if getattr(sys, "frozen", False):
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    mei_dir = getattr(sys, "_MEIPASS", exe_dir)
    BASE_DIR = exe_dir if os.path.isdir(os.path.join(exe_dir, "icons")) else mei_dir
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ICONS_DIR = os.path.join(BASE_DIR, "icons")
ICON_ICO_PATH = os.path.join(ICONS_DIR, "app_icon.ico")
ICON_PNG_PATH = os.path.join(ICONS_DIR, "app_icon.png")
ICON_MAP_PATH = os.path.join(BASE_DIR, "icon_map.json")
MATERIALS_DB_PATH = os.path.join(BASE_DIR, "all_materials_db.json")
EQUIPMENT_DB_PATH = os.path.join(BASE_DIR, "all_equipment_encyclopedia.json")
DECALS_DB_PATH = os.path.join(BASE_DIR, "all_decals_encyclopedia.json")
ARMOR_SETS_PATH = os.path.join(BASE_DIR, "armor_sets_encyclopedia.json")
SHROOMS_BEASTS_DB_PATH = os.path.join(BASE_DIR, "all_shrooms_beasts_db.json")

# Premium Cyberpunk Dark Theme Color Palette
from ui.theme import (
    BG_DARK, BG_PANEL, BG_CARD, BG_CARD_LIGHT, BG_CARD_HOVER,
    FG_MAIN, FG_MUTED, ACCENT_GOLD, ACCENT_CYAN, ACCENT_BLUE,
    ACCENT_GREEN, ACCENT_RED, ACCENT_PURPLE, ACCENT_PINK
)
from ui.components import ScrollableFrame
from ui.dialogs import (
    SmartInventoryAnalyzerDialog,
    InventoryViewerDialog,
    ArmorSetViewerDialog,
    CreateFighterDialog
)


from game_data import SPECIAL_MUSHROOMS, SPECIAL_BEASTS, WEAPON_CATEGORIES, FIGHTER_CLASSES
WEAPON_MASTERY_ICONS = {wt: img for wt, nm, img in WEAPON_CATEGORIES}

EXPERT_WEAPON_NAMES_ES = {
    "PTARMTP_00": "Manos Desnudas",
    "PTARMTP_01": "Machete (DOD ARMS)",
    "PTARMTP_02": "Martillo (DOD ARMS)",
    "PTARMTP_03": "Plancha (DOD ARMS)",
    "PTARMTP_04": "Pistola de Clavos (DOD ARMS)",
    "PTARMTP_05": "Sierra Circular (DOD ARMS)",
    "PTARMTP_06": "Picahielo (DOD ARMS)",
    "PTARMTP_07": "Palo de Golf (WAR ENSEMBLE)",
    "PTARMTP_08": "Cuchillo de Caza (WAR ENSEMBLE)",
    "PTARMTP_09": "Hacha de Batalla (CANDLE WOLF)",
    "PTARMTP_10": "Espada Larga (CANDLE WOLF)",
    "PTARMTP_11": "Maza de Guerra / Mayal (CANDLE WOLF)",
    "PTARMTP_12": "Cuchillo Arrojadizo / Shuriken",
    "PTARMTP_13": "Lanza (CANDLE WOLF)",
    "PTARMTP_14": "Vara de Trueno (CANDLE WOLF)",
    "PTARMTP_15": "Guantelete / Garras (WAR ENSEMBLE)",
    "PTARMTP_16": "Pistola Mágnum (WAR ENSEMBLE)",
    "PTARMTP_17": "Fusil de Asalto KAMAS (WAR ENSEMBLE)",
    "PTARMTP_18": "Escopeta (WAR ENSEMBLE)",
    "PTARMTP_19": "Fusil Francotirador (WAR ENSEMBLE)",
    "PTARMTP_20": "Lanzacohetes (WAR ENSEMBLE)",
    "PTARMTP_21": "Lanzador de Fuegos Artificiales (DOD ARMS)",
    "PTARMTP_22": "Motosierra (DOD ARMS)",
    "PTARMTP_23": "Motor Psycho (WAR ENSEMBLE)",
    "PTARMTP_24": "Taladro (DOD ARMS)",
    "PTARMTP_25": "Katana Masamune (CANDLE WOLF)",
    "PTARMTP_26": "Bate de Béisbol (M.I.L.K.)",
    "PTARMTP_27": "Palo de Hockey (M.I.L.K.)",
    "PTARMTP_28": "Bolas de Bolos (M.I.L.K.)",
    "PTARMTP_29": "Estatua Shishimai",
    "PTARMTP_30": "Sable Cortador (WAR ENSEMBLE)",
    "PTARMTP_31": "Lanzallamas (DOD ARMS)",
    "PTARMTP_32": "Arma Taser (DOD ARMS)",
    "PTARMTP_33": "Pala de Trinchera (DOD ARMS)",
    "PTARMTP_34": "Ballesta (CANDLE WOLF)",
    "PTARMTP_35": "Lanza Dragon Buster (CANDLE WOLF)",
    "PTARMTP_36": "Vara Eléctrica / Stun Rod (M.I.L.K.)",
    "PTARMTP_37": "Palo de Madera (DOD ARMS)",
    "PTARMTP_38": "Máquina de Pitching (M.I.L.K.)",
    "PTARMTP_39": "Guantelete de Boxeo (M.I.L.K.)",
    "PTARMTP_40": "Bate de Clavos (M.I.L.K.)",
    "PTARMTP_41": "Katana Láser Beam (NO MORE HEROES)",
    "PTARMTP_42": "Pistola de Bengalas (WAR ENSEMBLE)",
    "PTARMTP_43": "Espadón (CANDLE WOLF)",
    "PTARMTP_44": "Yo-yo de Combate (DOD ARMS)",
    "PTARMTP_45": "Látigo (M.I.L.K.)",
    "PTARMTP_46": "Maza Pesada (TENGOKU)",
    "PTARMTP_47": "Navaja Mariposa",
    "PTARMTP_48": "Nunchaku (WAR ENSEMBLE)",
    "PTARMTP_50": "Pistola de Plasma (TENGOKU)",
    "PTARMTP_51": "Sable EMP (TENGOKU)",
    "PTARMTP_52": "Lanzador EMP (TENGOKU)",
    "PTARMTP_53": "Fusil Láser TDM",
    "PTARMTP_54": "Maza Pesada TDM",
    "PTARMTP_55": "Masajeador Estático (44CE White Steel)",
    "PTARMTP_56": "Lanzador de Púas M2G (44CE Red Napalm)",
    "PTARMTP_57": "Espada de Energía (44CE Black Thunder)",
    "PTARMTP_58": "Pistola de Bolas / Bobbin Gun (44CE Pale Wind)",
    "PTARMTP_59": "Esquís de Combate (TENGOKU)",
    "PTARMTP_62": "Blaster Jackal X",
    "PTARMTP_63": "Sable Jackal Y",
    "PTARMTP_64": "Yo-yo Jackal Z"
}

EXPERT_WEAPON_NAMES_EN = {
    "PTARMTP_00": "Bare Fists",
    "PTARMTP_01": "Machete (DOD ARMS)",
    "PTARMTP_02": "Hammer (DOD ARMS)",
    "PTARMTP_03": "Red Hot Iron (DOD ARMS)",
    "PTARMTP_04": "Nail Gun (DOD ARMS)",
    "PTARMTP_05": "Buzzsaw (DOD ARMS)",
    "PTARMTP_06": "Pickaxe (DOD ARMS)",
    "PTARMTP_07": "Golf Club (WAR ENSEMBLE)",
    "PTARMTP_08": "Hunting Knife (WAR ENSEMBLE)",
    "PTARMTP_09": "Battle Axe (CANDLE WOLF)",
    "PTARMTP_10": "Longsword (CANDLE WOLF)",
    "PTARMTP_11": "Flail (CANDLE WOLF)",
    "PTARMTP_12": "Shuriken",
    "PTARMTP_13": "Spear (CANDLE WOLF)",
    "PTARMTP_14": "Thunder Rod (CANDLE WOLF)",
    "PTARMTP_15": "Claws (WAR ENSEMBLE)",
    "PTARMTP_16": "Magnum (WAR ENSEMBLE)",
    "PTARMTP_17": "KAMAS Assault Rifle (WAR ENSEMBLE)",
    "PTARMTP_18": "Shotgun (WAR ENSEMBLE)",
    "PTARMTP_19": "Sniper Rifle (WAR ENSEMBLE)",
    "PTARMTP_20": "Rocket Launcher (WAR ENSEMBLE)",
    "PTARMTP_21": "Fireworks Launcher (DOD ARMS)",
    "PTARMTP_22": "Chainsaw (DOD ARMS)",
    "PTARMTP_23": "Motor Psycho (WAR ENSEMBLE)",
    "PTARMTP_24": "Drill Arm (DOD ARMS)",
    "PTARMTP_25": "Masamune Katana (CANDLE WOLF)",
    "PTARMTP_26": "Baseball Bat (M.I.L.K.)",
    "PTARMTP_27": "Hockey Stick (M.I.L.K.)",
    "PTARMTP_28": "Bowling Ball (M.I.L.K.)",
    "PTARMTP_29": "Shishimai Statue",
    "PTARMTP_30": "Cleaver Saber (WAR ENSEMBLE)",
    "PTARMTP_31": "Flamethrower (DOD ARMS)",
    "PTARMTP_32": "Taser Gun (DOD ARMS)",
    "PTARMTP_33": "Trench Shovel (DOD ARMS)",
    "PTARMTP_34": "Crossbow (CANDLE WOLF)",
    "PTARMTP_35": "Dragon Buster Sword (CANDLE WOLF)",
    "PTARMTP_36": "Stun Rod (M.I.L.K.)",
    "PTARMTP_37": "Timber (DOD ARMS)",
    "PTARMTP_38": "Pitching Machine (M.I.L.K.)",
    "PTARMTP_39": "Boxing Glove (M.I.L.K.)",
    "PTARMTP_40": "Spiked Bat (M.I.L.K.)",
    "PTARMTP_41": "Beam Katana (NO MORE HEROES)",
    "PTARMTP_42": "Flare Gun (WAR ENSEMBLE)",
    "PTARMTP_43": "Greatsword (CANDLE WOLF)",
    "PTARMTP_44": "Combat Yo-yo (DOD ARMS)",
    "PTARMTP_45": "Whip (M.I.L.K.)",
    "PTARMTP_46": "Heavy Mace (TENGOKU)",
    "PTARMTP_47": "Butterfly Knife",
    "PTARMTP_48": "Nunchaku (WAR ENSEMBLE)",
    "PTARMTP_50": "Plasma Pistol (TENGOKU)",
    "PTARMTP_51": "EMP Saber (TENGOKU)",
    "PTARMTP_52": "EMP Launcher (TENGOKU)",
    "PTARMTP_53": "TDM Laser Rifle",
    "PTARMTP_54": "TDM Heavy Mace",
    "PTARMTP_55": "Static Massager (44CE White Steel)",
    "PTARMTP_56": "M2G-87 Spike Launcher (44CE Red Napalm)",
    "PTARMTP_57": "Energy Sword (44CE Black Thunder)",
    "PTARMTP_58": "Bobbin Gun (44CE Pale Wind)",
    "PTARMTP_59": "Ski Blades (TENGOKU)",
    "PTARMTP_62": "Jackal X Blaster",
    "PTARMTP_63": "Jackal Y Saber",
    "PTARMTP_64": "Jackal Z Yo-yo"
}

def get_expert_weapon_name(ptid):
    if i18n.get_language() == "en":
        return EXPERT_WEAPON_NAMES_EN.get(ptid, EXPERT_WEAPON_NAMES_ES.get(ptid, ptid))
    else:
        return EXPERT_WEAPON_NAMES_ES.get(ptid, EXPERT_WEAPON_NAMES_EN.get(ptid, ptid))

class CompleteSaveEditorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LET IT DIE (Offline) - Deep Save Editor Pro v3.5 (Master Cyberpunk Edition)")
        self.geometry("1240x820")
        self.minsize(1040, 700)
        self.configure(bg=BG_DARK)
        
        self._apply_dark_theme()
        
        # Window Icons
        if os.path.exists(ICON_ICO_PATH):
            try: self.iconbitmap(ICON_ICO_PATH)
            except Exception: pass
        if os.path.exists(ICON_PNG_PATH):
            try:
                self.icon_photo = tk.PhotoImage(file=ICON_PNG_PATH)
                self.iconphoto(True, self.icon_photo)
            except Exception: pass
            
        self.img_cache = {}
        self.tree_images = {}
        self.icon_map = {}
        self.materials_db = []
        self.equipment_db = []
        self.decals_db = []
        self.decals_map = {}
        self.shrooms_beasts_db = {}
        self._load_all_databases()
        
        self.save_path = get_default_save_path()
        self.save_json = None
        self.version = 2
        self.current_fighter_idx = 0
        self.current_decal_selection = None
        self.current_bp_selection = None
        self.current_mat_selection = None
        
        self._build_ui()
        
        # Check for GitHub updates in the background (starts 1.5s after launch)
        self.after(1500, lambda: updater.check_updates_background(self, silent=True))
        
        if self.save_path and os.path.exists(self.save_path):
            self.load_save(self.save_path)
        else:
            self.status_var.set("No se detectó partida automáticamente. Haz clic en 'Examinar' para abrir tu archivo .sav")

    def _apply_dark_theme(self):
        # 1. Option database defaults for Tk widgets, popups, and dropdown menus
        self.option_add("*background", BG_DARK)
        self.option_add("*foreground", FG_MAIN)
        self.option_add("*font", ("Segoe UI", 9))
        self.option_add("*selectBackground", ACCENT_BLUE)
        self.option_add("*selectForeground", "#ffffff")
        
        # Ensure Combobox dropdown listbox has dark background and crisp white text everywhere
        self.option_add("*TCombobox*Listbox.background", BG_CARD)
        self.option_add("*TCombobox*Listbox.foreground", "#ffffff")
        self.option_add("*TCombobox*Listbox.selectBackground", ACCENT_BLUE)
        self.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
        self.option_add("*TCombobox*Listbox.font", ("Segoe UI", 9))
        self.option_add("*ComboboxListbox*background", BG_CARD)
        self.option_add("*ComboboxListbox*foreground", "#ffffff")
        self.option_add("*ComboboxListbox*selectBackground", ACCENT_BLUE)
        self.option_add("*ComboboxListbox*selectForeground", "#ffffff")
        self.option_add("*ComboboxListbox*font", ("Segoe UI", 9))
        self.option_add("*Listbox.background", BG_CARD)
        self.option_add("*Listbox.foreground", "#ffffff")
        self.option_add("*Entry.background", BG_CARD)
        self.option_add("*Entry.foreground", "#ffffff")
        self.option_add("*Entry.insertBackground", "#ffffff")

        # 2. Modern Fluent Windows 11 dark theme using sv_ttk
        has_sv = False
        try:
            import sv_ttk
            sv_ttk.set_theme("dark")
            has_sv = True
        except Exception:
            pass

        self.style = ttk.Style(self)
        if not has_sv:
            try: self.style.theme_use("clam")
            except Exception: pass
            
        self.style.configure(".", background=BG_DARK, foreground=FG_MAIN, font=("Segoe UI", 9))
        self.style.configure("TFrame", background=BG_DARK)
        self.style.configure("Card.TFrame", background=BG_CARD, relief="flat")
        self.style.configure("CardLight.TFrame", background=BG_CARD_LIGHT, relief="flat")
        self.style.configure("Panel.TFrame", background=BG_PANEL, relief="flat")
        
        self.style.configure("TLabel", background=BG_DARK, foreground=FG_MAIN)
        self.style.configure("Card.TLabel", background=BG_CARD, foreground=FG_MAIN)
        self.style.configure("CardLight.TLabel", background=BG_CARD_LIGHT, foreground=FG_MAIN)
        self.style.configure("Panel.TLabel", background=BG_PANEL, foreground=FG_MAIN)
        self.style.configure("Muted.TLabel", background=BG_DARK, foreground=FG_MUTED)
        self.style.configure("CardMuted.TLabel", background=BG_CARD, foreground=FG_MUTED)
        
        self.style.configure("Header.TLabel", font=("Segoe UI", 11, "bold"), foreground=ACCENT_GOLD, background=BG_DARK)
        self.style.configure("Title.TLabel", font=("Segoe UI", 13, "bold"), foreground=FG_MAIN, background=BG_CARD)
        self.style.configure("StatGold.TLabel", font=("Segoe UI", 10, "bold"), foreground=ACCENT_GOLD, background=BG_DARK)
        
        self.style.configure("TLabelframe", background=BG_DARK, foreground=ACCENT_GOLD, relief="groove")
        self.style.configure("TLabelframe.Label", background=BG_DARK, foreground=ACCENT_GOLD, font=("Segoe UI", 9, "bold"))
        self.style.configure("Card.TLabelframe", background=BG_CARD, foreground=ACCENT_GOLD, relief="groove")
        self.style.configure("Card.TLabelframe.Label", background=BG_CARD, foreground=ACCENT_GOLD, font=("Segoe UI", 9, "bold"))
        
        # High-contrast Buttons
        self.style.configure("TButton", background=BG_CARD, foreground="#ffffff", borderwidth=1, focuscolor="none", font=("Segoe UI", 9))
        self.style.map("TButton", background=[("active", BG_CARD_LIGHT), ("pressed", BG_DARK)], foreground=[("active", "#ffffff"), ("pressed", FG_MUTED)])
        
        self.style.configure("Accent.TButton", background=ACCENT_GOLD, foreground="#000000", font=("Segoe UI", 9, "bold"))
        self.style.map("Accent.TButton", background=[("active", "#f39c12"), ("pressed", "#d68910")], foreground=[("active", "#000000"), ("pressed", "#000000")])
        
        self.style.configure("Danger.TButton", background=ACCENT_RED, foreground="#ffffff", font=("Segoe UI", 9, "bold"))
        self.style.map("Danger.TButton", background=[("active", "#c0392b"), ("pressed", "#962d22")], foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])
        
        self.style.configure("Success.TButton", background=ACCENT_GREEN, foreground="#000000", font=("Segoe UI", 9, "bold"))
        self.style.map("Success.TButton", background=[("active", "#27ae60"), ("pressed", "#1e8449")], foreground=[("active", "#000000"), ("pressed", "#000000")])
        
        # Tabs / Notebook
        self.style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=BG_PANEL, foreground=FG_MUTED, padding=(14, 8), font=("Segoe UI", 9, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", BG_CARD), ("active", "#252b3d")], foreground=[("selected", ACCENT_GOLD), ("active", FG_MAIN)])
        
        # Treeview
        self.style.configure("Treeview", background=BG_PANEL, fieldbackground=BG_PANEL, foreground="#ffffff", rowheight=40, borderwidth=0, font=("Segoe UI", 9))
        self.style.map("Treeview", background=[("selected", "#1a365d")], foreground=[("selected", "#00e5ff")])
        self.style.configure("Treeview.Heading", background=BG_CARD, foreground=ACCENT_GOLD, font=("Segoe UI", 9, "bold"), borderwidth=1)
        
        # Modern High-Contrast Entries & Comboboxes (Completely eliminates white-on-white!)
        self.style.configure("TEntry", fieldbackground=BG_CARD, background=BG_CARD, foreground="#ffffff", insertcolor="#ffffff")
        self.style.map("TEntry", fieldbackground=[("disabled", BG_PANEL), ("!disabled", BG_CARD)], foreground=[("disabled", FG_MUTED), ("!disabled", "#ffffff")])
        
        self.style.configure("TCombobox", fieldbackground=BG_CARD, background=BG_CARD, foreground="#ffffff", selectbackground=ACCENT_BLUE, selectforeground="#ffffff", arrowcolor=ACCENT_GOLD)
        self.style.map("TCombobox",
            fieldbackground=[("readonly", BG_CARD), ("disabled", BG_PANEL), ("active", BG_CARD_LIGHT), ("!disabled", BG_CARD)],
            background=[("readonly", BG_CARD), ("disabled", BG_PANEL), ("active", BG_CARD_LIGHT), ("!disabled", BG_CARD)],
            foreground=[("readonly", "#ffffff"), ("disabled", FG_MUTED), ("active", "#ffffff"), ("!disabled", "#ffffff")],
            selectbackground=[("readonly", ACCENT_BLUE), ("!disabled", ACCENT_BLUE)],
            selectforeground=[("readonly", "#ffffff"), ("!disabled", "#ffffff")],
            arrowcolor=[("disabled", FG_MUTED), ("active", "#ffffff"), ("!disabled", ACCENT_GOLD)]
        )

    def _load_all_databases(self):
        self._icon_index = {}
        if os.path.isdir(ICONS_DIR):
            for root, _, files in os.walk(ICONS_DIR):
                for f in files:
                    full_p = os.path.join(root, f)
                    lower_f = f.lower()
                    if lower_f not in self._icon_index:
                        self._icon_index[lower_f] = full_p
                    base_no_ext = os.path.splitext(lower_f)[0]
                    if base_no_ext not in self._icon_index:
                        self._icon_index[base_no_ext] = full_p

        if os.path.exists(ICON_MAP_PATH):
            with open(ICON_MAP_PATH, "r", encoding="utf-8") as f:
                self.icon_map = json.load(f)
        if os.path.exists(MATERIALS_DB_PATH):
            with open(MATERIALS_DB_PATH, "r", encoding="utf-8") as f:
                self.materials_db = json.load(f)
        if os.path.exists(EQUIPMENT_DB_PATH):
            with open(EQUIPMENT_DB_PATH, "r", encoding="utf-8") as f:
                self.equipment_db = json.load(f)
        self.decals_map = {}
        if os.path.exists(DECALS_DB_PATH):
            with open(DECALS_DB_PATH, "r", encoding="utf-8") as f:
                self.decals_db = json.load(f)
                for d in self.decals_db:
                    self.decals_map[d["id"]] = d
                    self.decals_map[d["id"].replace("_P", "")] = d
                    self.decals_map[f"{d['id'].replace('_P', '')}_P"] = d
        self.armor_sets = []
        self.armor_set_by_item_id = {}
        if os.path.exists(ARMOR_SETS_PATH):
            with open(ARMOR_SETS_PATH, "r", encoding="utf-8") as f:
                self.armor_sets = json.load(f)
                for s in self.armor_sets:
                    for t in s.get("tiers", []):
                        for slot in ["head", "body", "legs"]:
                            p = t.get(slot)
                            if p and "id" in p:
                                self.armor_set_by_item_id[p["id"]] = (s, t, p)
                                self.armor_set_by_item_id[f"{p['id']}_G"] = (s, t, p)
                        wp = t.get("weapon")
                        if wp and "id" in wp:
                            self.armor_set_by_item_id[wp["id"]] = (s, t, wp)
                            self.armor_set_by_item_id[f"{wp['id']}_G"] = (s, t, wp)
        if os.path.exists(SHROOMS_BEASTS_DB_PATH):
            with open(SHROOMS_BEASTS_DB_PATH, "r", encoding="utf-8") as f:
                self.shrooms_beasts_db = json.load(f)

    def get_photo(self, rel_path, size=(28, 28), preserve_aspect=False):
        if not rel_path:
            return None
        key = (rel_path, size, preserve_aspect)
        if key in self.img_cache:
            return self.img_cache[key]
            
        clean_rel = str(rel_path).replace("\\", "/")
        found_path = None
        
        # 1. Fast O(1) index lookup
        clean_base = os.path.basename(clean_rel).lower()
        clean_stem = os.path.splitext(clean_base)[0]
        idx = getattr(self, "_icon_index", {})
        found_path = idx.get(clean_base) or idx.get(clean_stem)
        
        # 2. Check icon_map if not found directly
        if not found_path and hasattr(self, "icon_map"):
            mapped = self.icon_map.get("gear_icons", {}).get(clean_rel) or \
                     self.icon_map.get("gear_cards", {}).get(clean_rel) or \
                     self.icon_map.get("materials_cards", {}).get(clean_rel) or \
                     self.icon_map.get("materials_thumbs", {}).get(clean_rel) or \
                     self.icon_map.get("decals_icons", {}).get(clean_rel) or \
                     self.icon_map.get("equipment_thumbs", {}).get(clean_rel)
            if mapped:
                mapped_base = os.path.basename(mapped.replace("\\", "/")).lower()
                mapped_stem = os.path.splitext(mapped_base)[0]
                found_path = idx.get(mapped_base) or idx.get(mapped_stem)
                
        # 3. Direct filesystem fallback
        if not found_path:
            if os.path.isabs(clean_rel) and os.path.exists(clean_rel):
                found_path = clean_rel
            else:
                for sub in ["", "cards", "sets", "all_official", "armor", "weapons", "materials", "decals", "shrooms", "gear", "thumbs"]:
                    for ext in ["", ".png", ".jpg", ".jpeg", ".webp"]:
                        p = os.path.join(ICONS_DIR, sub, clean_rel + ext)
                        if os.path.exists(p) and not os.path.isdir(p):
                            found_path = p
                            break
                    if found_path:
                        break
                        
        if found_path:
            try:
                img = Image.open(found_path).convert("RGBA")
                if preserve_aspect:
                    max_w, max_h = size
                    w, h = img.size
                    ratio = min(max_w / max(1, w), max_h / max(1, h))
                    target_size = (max(1, int(w * ratio)), max(1, int(h * ratio)))
                else:
                    target_size = size
                img = img.resize(target_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.img_cache[key] = photo
                return photo
            except Exception:
                pass
        return None

    def _auto_save(self):
        """Immediately writes changes to disk so modifications in the GUI are instantly live in the game."""
        if self.save_json and self.save_path:
            save_to_file(self.save_json, self.save_path, version=self.version)

    def _notify(self, title_en, title_es, msg_en, msg_es, kind="info"):
        """Displays dialog and status updates in the user's selected language (EN or ES)."""
        is_en = i18n.get_language() == "en"
        title = title_en if is_en else title_es
        msg = msg_en if is_en else msg_es
        first_line = msg.splitlines()[0].replace("¡", "").replace("!", "")
        self.status_var.set(first_line)
        if kind == "info":
            messagebox.showinfo(title, msg)
        elif kind == "warning":
            messagebox.showwarning(title, msg)
        elif kind == "error":
            messagebox.showerror(title, msg)

    def _build_ui(self):
        # 1. Top Cyberpunk Save File & Action Bar
        top_frame = tk.Frame(self, bg=BG_PANEL, padx=14, pady=8)
        top_frame.pack(fill="x", padx=10, pady=(6, 2))
        
        self.lbl_file = tk.Label(top_frame, text=t("save_file"), font=("Segoe UI", 9, "bold"), fg=ACCENT_GOLD, bg=BG_PANEL)
        self.lbl_file.pack(side="left", padx=(0, 8))
        
        self.path_entry = ttk.Entry(top_frame)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        if self.save_path:
            self.path_entry.insert(0, self.save_path)
            
        self.browse_btn = ttk.Button(top_frame, text=t("browse"), command=self.browse_save)
        self.browse_btn.pack(side="left", padx=2)
        
        self.reload_btn = ttk.Button(top_frame, text=t("reload"), command=lambda: self.load_save(self.path_entry.get()))
        self.reload_btn.pack(side="left", padx=2)
        
        self.backup_btn = ttk.Button(top_frame, text=t("backup"), command=self.create_manual_backup)
        self.backup_btn.pack(side="left", padx=2)
        
        self.btn_sets_hud = ttk.Button(top_frame, text=t("armor_sets"), style="Accent.TButton", command=self._open_armor_set_viewer)
        self.btn_sets_hud.pack(side="left", padx=(6, 2))
        
        self.btn_rnd_hud = ttk.Button(top_frame, text=t("rnd_analyzer"), command=self._open_smart_analyzer)
        self.btn_rnd_hud.pack(side="left", padx=2)
        
        self.btn_update_hud = ttk.Button(top_frame, text=t("updates"), command=self._check_app_updates)
        self.btn_update_hud.pack(side="left", padx=2)
        
        # Language Switcher (Español / English)
        self.lbl_lang = tk.Label(top_frame, text=t("lang_label"), font=("Segoe UI", 9, "bold"), fg=ACCENT_GOLD, bg=BG_PANEL)
        self.lbl_lang.pack(side="left", padx=(6, 2))
        
        cur_lang_str = "English" if i18n.get_language() == "en" else "Español"
        self.lang_var = tk.StringVar(value=cur_lang_str)
        self.lang_cb = ttk.Combobox(top_frame, textvariable=self.lang_var, values=["Español", "English"], state="readonly", width=8)
        self.lang_cb.pack(side="left", padx=(0, 4))
        self.lang_cb.bind("<<ComboboxSelected>>", self._on_language_changed)
        
        self.save_btn = ttk.Button(top_frame, text=t("save_game"), style="Accent.TButton", command=self.save_current)
        self.save_btn.pack(side="left", padx=(6, 0))

        # 2. Player Status Cyberpunk HUD Dashboard
        self.dashboard_frame = tk.Frame(self, bg=BG_CARD, padx=14, pady=8, relief="flat", highlightbackground=BG_CARD_LIGHT, highlightthickness=1)
        self.dashboard_frame.pack(fill="x", padx=10, pady=4)
        
        self.player_avatar_lbl = tk.Label(self.dashboard_frame, bg=BG_CARD, image=self.get_photo("all-rounder", (38, 38)) or "")
        self.player_avatar_lbl.pack(side="left", padx=(0, 10))
        
        info_subframe = tk.Frame(self.dashboard_frame, bg=BG_CARD)
        info_subframe.pack(side="left", fill="y")
        
        self.player_name_lbl = tk.Label(info_subframe, text="Luchador: ---", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg=BG_CARD)
        self.player_name_lbl.pack(anchor="w")
        
        self.player_meta_lbl = tk.Label(info_subframe, text="UID: --- | Rango Base: -- | 🏆 TDM: --- | Bolsa: -- slots", font=("Segoe UI", 8), fg=FG_MUTED, bg=BG_CARD)
        self.player_meta_lbl.pack(anchor="w")

        # Currency Badges on the right of Dashboard
        curr_subframe = tk.Frame(self.dashboard_frame, bg=BG_CARD)
        curr_subframe.pack(side="right", padx=5)
        
        self.hud_dm_lbl = tk.Label(curr_subframe, text="💎 0 DM", font=("Segoe UI", 9, "bold"), fg=ACCENT_PINK, bg=BG_CARD, compound="left", image=self.get_photo("dm", (20, 20)) or "")
        self.hud_dm_lbl.pack(side="left", padx=8)
        
        self.hud_kc_lbl = tk.Label(curr_subframe, text="🪙 0 KC", font=("Segoe UI", 9, "bold"), fg=ACCENT_GOLD, bg=BG_CARD, compound="left", image=self.get_photo("kc", (20, 20)) or "")
        self.hud_kc_lbl.pack(side="left", padx=8)
        
        self.hud_spl_lbl = tk.Label(curr_subframe, text="⚡ 0 SPL", font=("Segoe UI", 9, "bold"), fg=ACCENT_CYAN, bg=BG_CARD, compound="left", image=self.get_photo("spl", (20, 20)) or "")
        self.hud_spl_lbl.pack(side="left", padx=8)
        
        self.hud_bl_lbl = tk.Label(curr_subframe, text="🩸 0 BL", font=("Segoe UI", 9, "bold"), fg=ACCENT_RED, bg=BG_CARD, compound="left", image=self.get_photo("bloodnium", (20, 20)) or "")
        self.hud_bl_lbl.pack(side="left", padx=8)
        
        self.hud_re_lbl = tk.Label(curr_subframe, text="♻️ 0 RE", font=("Segoe UI", 9, "bold"), fg=ACCENT_GREEN, bg=BG_CARD, compound="left", image=self.get_photo("re_point", (20, 20)) or "")
        self.hud_re_lbl.pack(side="left", padx=8)
        
        self.hud_bp_lbl = tk.Label(curr_subframe, text="📋 0/1370 (0%)", font=("Segoe UI", 9, "bold"), fg=ACCENT_GOLD, bg=BG_CARD, compound="left", image=self.get_photo("blueprint", (20, 20)) or "")
        self.hud_bp_lbl.pack(side="left", padx=8)

        # 3. Main Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=4)
        
        # TAB 1: CURRENCIES
        self.tab_currencies = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_currencies, text=t("tab_currencies"), image=self.get_photo("dm", (18, 18)) or "", compound="left")
        self._build_currencies_tab()
        
        # TAB 2: FIGHTERS
        self.tab_fighters = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_fighters, text=t("tab_fighters"), image=self.get_photo("all-rounder", (18, 18)) or "", compound="left")
        self._build_fighters_tab()
        
        # TAB 3: MATERIALS
        self.tab_materials = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_materials, text=t("tab_materials"), image=self.get_photo("special_steel", (18, 18)) or "", compound="left")
        self._build_materials_tab()
        
        # TAB 4: DECALS
        self.tab_decals = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_decals, text=t("tab_decals"), image=self.get_photo("decal_p", (18, 18)) or "", compound="left")
        self._build_decals_tab()
        
        # TAB 5: BLUEPRINTS
        self.tab_blueprints = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_blueprints, text=t("tab_blueprints"), image=self.get_photo("blueprint", (18, 18)) or "", compound="left")
        self._build_blueprints_tab()
        
        # TAB 6: MASTERY
        self.tab_mastery = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_mastery, text=t("tab_mastery"), image=self.get_photo("weapon", (18, 18)) or "", compound="left")
        self._build_mastery_tab()
        
        # TAB 7: TOWER & MASTER UNLOCKS
        self.tab_tower = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_tower, text=t("tab_tower"), image=self.get_photo("re_point", (18, 18)) or "", compound="left")
        self._build_tower_tab()
        
        # TAB 8: ENCYCLOPEDIA & ADVANCED
        self.tab_advanced = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_advanced, text=t("tab_advanced"), image=self.get_photo("reversal_metal", (18, 18)) or "", compound="left")
        self._build_advanced_tab()

        # 4. Bottom Status Bar
        self.status_var = tk.StringVar(value="Listo.")
        status_bar = tk.Label(self, textvariable=self.status_var, font=("Segoe UI", 9), fg=FG_MUTED, bg=BG_DARK, padx=12, pady=4, anchor="w")
        status_bar.pack(side="bottom", fill="x")

    # ================= TAB 1: CURRENCIES & VIP =================
    def _build_currencies_tab(self):
        self.tab_currencies.columnconfigure(0, weight=1, uniform="tab1")
        self.tab_currencies.columnconfigure(1, weight=1, uniform="tab1")
        self.tab_currencies.rowconfigure(0, weight=1, uniform="tab1_row")
        self.tab_currencies.rowconfigure(1, weight=1, uniform="tab1_row")
        self.tab_currencies.rowconfigure(2, weight=0)
        
        # Card 1 (Top-Left): Currencies
        box_curr = ttk.LabelFrame(self.tab_currencies, text=t("curr_box_title"), padding=12)
        box_curr.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        
        entries = [
            (t("dm_lbl"), "dm_var", "dm"),
            (t("kc_lbl"), "kc_var", "kc"),
            (t("spl_lbl"), "spl_var", "spl"),
            (t("bl_lbl"), "bl_var", "bloodnium"),
            (t("re_lbl"), "re_var", "re_point"),
        ]
        
        for idx, (lbl_text, var_name, icon_name) in enumerate(entries):
            row = ttk.Frame(box_curr)
            row.pack(fill="x", pady=3)
            ico = self.get_photo(icon_name, (20, 20))
            ttk.Label(row, text=f" {lbl_text}", image=ico or "", compound="left", font=("Segoe UI", 9, "bold")).pack(side="left")
            var = tk.StringVar(value="0")
            setattr(self, var_name, var)
            ent = ttk.Entry(row, textvariable=var, width=14, font=("Segoe UI", 9, "bold"), justify="right")
            ent.pack(side="right")
            
        btn_max_all = ttk.Button(box_curr, text=t("max_all_curr_btn"), style="Accent.TButton", command=self.max_all_currencies)
        btn_max_all.pack(fill="x", pady=(10, 2))

        # Card 2 (Top-Right): Waiting Room Upgrades
        box_wr = ttk.LabelFrame(self.tab_currencies, text=t("wr_box_title"), padding=12)
        box_wr.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        
        upgrades = [
            (t("bank_lvl_lbl"), "safe_lvl_var"),
            (t("tank_lvl_lbl"), "tank_lvl_var"),
            (t("player_rank_lbl"), "rank_var"),
        ]
        for lbl_t, var_n in upgrades:
            r = ttk.Frame(box_wr)
            r.pack(fill="x", pady=4)
            ttk.Label(r, text=lbl_t, font=("Segoe UI", 9)).pack(side="left")
            v = tk.StringVar(value="100")
            setattr(self, var_n, v)
            ttk.Entry(r, textvariable=v, width=8, justify="center").pack(side="right")
            
        wr_btn_f = ttk.Frame(box_wr)
        wr_btn_f.pack(fill="x", pady=(10, 2))
        btn_apply_base = ttk.Button(wr_btn_f, text=t("apply_wr_btn"), style="Accent.TButton", command=self._apply_waiting_room_facilities)
        btn_apply_base.pack(side="left", fill="x", expand=True, padx=(0, 3))
        btn_max_base = ttk.Button(wr_btn_f, text=t("max_wr_btn"), command=self._max_waiting_room_facilities)
        btn_max_base.pack(side="left", fill="x", expand=True, padx=(3, 0))
        
        ttk.Label(box_wr, text=t("wr_hint"), font=("Segoe UI", 8), foreground=FG_MUTED, wraplength=280).pack(fill="x", pady=(6, 0))

        # Card 3 (Bottom-Left): VIP Royal Express
        box_vip = ttk.LabelFrame(self.tab_currencies, text=t("vip_box_title"), padding=12)
        box_vip.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        
        self.vip_status_lbl = ttk.Label(box_vip, text=t("vip_inactive"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD)
        self.vip_status_lbl.pack(anchor="w", pady=(0, 2))
        
        ttk.Label(box_vip, text=t("vip_safe_note", "⚠️ Máximo 30 días activo para evitar errores en el ascensor.\nPuedes almacenar hasta 99 pases en reserva."), font=("Segoe UI", 8), foreground=FG_MUTED).pack(anchor="w", pady=(0, 4))

        vip_f = ttk.Frame(box_vip)
        vip_f.pack(fill="x", pady=4)
        ttk.Label(vip_f, text=t("vip_days_lbl")).pack(side="left", padx=2)
        self.vip_days_var = tk.StringVar(value="30")
        cb_vip_days = ttk.Combobox(vip_f, textvariable=self.vip_days_var, values=["90", "60", "30", "15", "7", "1"], state="readonly", width=6)
        cb_vip_days.pack(side="left", padx=4)
        ttk.Button(vip_f, text=t("activate_vip_btn"), style="Accent.TButton", command=self._activate_custom_vip).pack(side="left", padx=4)
        ttk.Button(vip_f, text=t("deactivate_vip_btn", "❌ Cancelar"), command=self._deactivate_vip_action).pack(side="left", padx=4)
        
        vip_quick = ttk.Frame(box_vip)
        vip_quick.pack(fill="x", pady=4)
        ttk.Button(vip_quick, text=t("vip_30d_btn", "🎫 30 Días (+99 Reserva)"), style="Accent.TButton", command=lambda: self._set_vip_entry_and_act(30, passes=99)).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(vip_quick, text=t("vip_1d_btn", "🎟️ 1 Día (+99 Reserva)"), command=lambda: self._set_vip_entry_and_act(1, passes=99)).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(vip_quick, text=t("vip_stock_passes", "📦 +99 Pases Reserva"), command=lambda: self._set_vip_entry_and_act(30, passes=99)).pack(side="left", fill="x", expand=True, padx=2)


        # Card 4 (Bottom-Right): Account Perks & Death Bag Expansion
        box_perks = ttk.LabelFrame(self.tab_currencies, text=t("account_perks_title"), padding=12)
        box_perks.grid(row=1, column=1, sticky="nsew", padx=6, pady=6)
        
        # Death Bag Expansion
        ttk.Label(box_perks, text=t("tw_bag_title"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        bag_f = ttk.Frame(box_perks)
        bag_f.pack(fill="x", pady=2)
        ttk.Label(bag_f, text=t("tw_bag_cap_lbl")).pack(side="left", padx=4)
        self.bag_slots_var = tk.StringVar(value="50")
        cb_bag = ttk.Combobox(bag_f, textvariable=self.bag_slots_var, values=["20", "25", "30", "35", "40", "45", "50", "60", "70"], state="readonly", width=8)
        cb_bag.pack(side="left", padx=4)
        btn_expand_bag = ttk.Button(bag_f, text=t("tw_bag_btn"), style="Accent.TButton", command=self._expand_bag_action)
        btn_expand_bag.pack(side="left", padx=4)
        
        # Free Continues
        ttk.Separator(box_perks, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(box_perks, text=t("tw_cont_title"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        cont_f = ttk.Frame(box_perks)
        cont_f.pack(fill="x", pady=2)
        ttk.Label(cont_f, text=t("tw_cont_lbl")).pack(side="left", padx=4)
        self.free_cont_var = tk.StringVar(value="999")
        ttk.Entry(cont_f, textvariable=self.free_cont_var, width=8, justify="center").pack(side="left", padx=4)
        btn_set_cont = ttk.Button(cont_f, text=t("tw_cont_btn"), style="Accent.TButton", command=self._set_continues_action)
        btn_set_cont.pack(side="left", padx=4)

        # Row 2 (Footer): Account Profile & Metadata
        box_acct = ttk.LabelFrame(self.tab_currencies, text=t("account_summary_title"), padding=10)
        box_acct.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=6, pady=(4, 6))
        
        acct_f = ttk.Frame(box_acct)
        acct_f.pack(fill="x")
        self.acct_uid_lbl = ttk.Label(acct_f, text="UID: --- | Steam ID: ---", font=("Segoe UI", 9, "bold"), foreground=ACCENT_CYAN)
        self.acct_uid_lbl.pack(side="left", padx=(4, 16))
        self.acct_playtime_lbl = ttk.Label(acct_f, text="⏱️ Horas: ---", font=("Segoe UI", 9), foreground=FG_MUTED)
        self.acct_playtime_lbl.pack(side="left", padx=(0, 16))
        self.acct_streak_lbl = ttk.Label(acct_f, text="🔥 Racha Login: ---", font=("Segoe UI", 9), foreground=ACCENT_GOLD)
        self.acct_streak_lbl.pack(side="left", padx=(0, 12))
        btn_max_streak = ttk.Button(acct_f, text=t("max_streak_btn"), command=self._max_login_streak_action)
        btn_max_streak.pack(side="right", padx=4)

    def _apply_waiting_room_facilities(self):
        if not self.save_json:
            return
        try:
            b_lvl = max(1, min(int(self.safe_lvl_var.get().strip() or 1), 100))
            t_lvl = max(1, min(int(self.tank_lvl_var.get().strip() or 1), 100))
            p_rnk = max(1, min(int(self.rank_var.get().strip() or 1), 130))
        except ValueError:
            b_lvl, t_lvl, p_rnk = 100, 100, 100
            
        self.safe_lvl_var.set(str(b_lvl))
        self.tank_lvl_var.set(str(t_lvl))
        self.rank_var.set(str(p_rnk))
        
        modifiers.upgrade_waiting_room(self.save_json, bank_level=b_lvl, tank_level=t_lvl)
        modifiers.set_player_rank(self.save_json, rank=p_rnk)
        pts = modifiers.get_rank_points_for_rank(p_rnk)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Facilities Updated", "Instalaciones Actualizadas",
            f"KC Bank set to Level {b_lvl}, SPL Tank to Level {t_lvl}.\nPlayer Rank set to {p_rnk} ({pts:,} points synced).",
            f"Banco de KC establecido al Nivel {b_lvl}, Tanque de SPL al Nivel {t_lvl}.\nRango de Jugador establecido a {p_rnk} ({pts:,} puntos sincronizados)."
        )

    def _max_waiting_room_facilities(self):
        self.safe_lvl_var.set("100")
        self.tank_lvl_var.set("100")
        self.rank_var.set("100")
        if self.save_json:
            modifiers.upgrade_waiting_room(self.save_json, bank_level=100, tank_level=100)
            modifiers.set_player_rank(self.save_json, rank=100)
            pts = modifiers.get_rank_points_for_rank(100)
            self._auto_save()
            self.refresh_all_views()
            self._notify(
                "Facilities Maximized", "Instalaciones Maximizadas",
                f"KC Bank and SPL Tank upgraded to Max Level 100!\nPlayer Rank set to 100 ({pts:,} points synchronized)!",
                f"¡Banco de KC y Tanque de SPL mejorados al Nivel Máximo 100!\n¡Rango de Jugador establecido a 100 ({pts:,} puntos sincronizados)!"
            )

    def _max_login_streak_action(self):
        if not self.save_json:
            return
        modifiers.max_login_streak(self.save_json, streak=365)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Login Streak", "Racha de Conexión",
            "Login streak set to 365 consecutive days!",
            "¡Racha de inicio de sesión establecida a 365 días consecutivos!"
        )

    def _set_vip_entry_and_act(self, days, passes=99):
        self.vip_days_var.set(str(days))
        self._activate_custom_vip(passes=passes)

    def _activate_custom_vip(self, passes=99):
        if not self.save_json:
            return
        try:
            days = min(90, max(1, int(self.vip_days_var.get())))
        except ValueError:
            days = 30
        self.vip_days_var.set(str(days))
        modifiers.set_vip_pass(self.save_json, days=days, passes=passes, oneday_passes=99)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "VIP Activated", "VIP Activado",
            f"Royal Express Pass activated for {days} days (+{passes} 30-day passes in stock)!\n\n✨ Friendship fixed to 1 (prevents elevator cutscene/voice hang) and duration 100% safe.",
            f"¡Pase Royal Express activado por {days} días (+{passes} pases de 30 días en reserva)!\n\n✨ Amistad fijada en 1 (soluciona el cuelgue de voz/animación en el ascensor) y duración 100% segura."
        )

    def _deactivate_vip_action(self):
        if not self.save_json:
            return
        modifiers.deactivate_vip_pass(self.save_json)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "VIP Deactivated", "VIP Desactivado",
            "Royal Express Pass has been deactivated.",
            "¡Pase Royal Express desactivado correctamente!"
        )

            # ================= TAB 2: FIGHTERS FREEZER =================
    def _build_fighters_tab(self):
        paned = ttk.PanedWindow(self.tab_fighters, orient="horizontal")
        paned.pack(fill="both", expand=True)
        
        left_box = ttk.LabelFrame(paned, text=t("f_freezer_title"), padding=10)
        paned.add(left_box, weight=2)
        
        # Fighter Freezer Slot Reordering Buttons Toolbar (Top of left_box, ALWAYS VISIBLE!)
        reorder_f = ttk.Frame(left_box)
        reorder_f.pack(fill="x", pady=(0, 2))
        ttk.Button(reorder_f, text=t("f_move_up"), style="Accent.TButton", command=self._move_fighter_up_action).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(reorder_f, text=t("f_move_down"), style="Accent.TButton", command=self._move_fighter_down_action).pack(side="left", fill="x", expand=True, padx=2)
        
        # Fighter Creation & Management Toolbar
        manage_f = ttk.Frame(left_box)
        manage_f.pack(fill="x", pady=(0, 6))
        ttk.Button(manage_f, text=t("f_create_btn"), style="Success.TButton", command=self._create_new_fighter_dialog).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(manage_f, text=t("f_clone_btn"), command=self._clone_fighter_action).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(manage_f, text=t("f_delete_btn"), command=self._delete_fighter_action).pack(side="left", fill="x", expand=True, padx=2)
        
        tree_container = ttk.Frame(left_box)
        tree_container.pack(fill="both", expand=True, pady=2)
        
        f_scroll = ttk.Scrollbar(tree_container, orient="vertical")
        self.fighters_tree = ttk.Treeview(tree_container, columns=("num", "lvl", "state"), show="tree headings", height=14, yscrollcommand=f_scroll.set)
        f_scroll.config(command=self.fighters_tree.yview)
        self.fighters_tree.heading("#0", text=t("f_col_name"))
        self.fighters_tree.heading("num", text=t("f_col_num"))
        self.fighters_tree.heading("lvl", text=t("f_col_lvl"))
        self.fighters_tree.heading("state", text=t("f_col_state"))
        
        self.fighters_tree.column("#0", width=180)
        self.fighters_tree.column("num", width=35, anchor="center")
        self.fighters_tree.column("lvl", width=55, anchor="center")
        self.fighters_tree.column("state", width=80, anchor="center")
        
        f_scroll.pack(side="right", fill="y")
        self.fighters_tree.pack(side="left", fill="both", expand=True)
        self.fighters_tree.bind("<<TreeviewSelect>>", self._on_fighter_select)
        
        right_container = ttk.LabelFrame(paned, text=t("f_tech_sheet"), padding=4)
        paned.add(right_container, weight=3)
        
        scroll_right = ScrollableFrame(right_container)
        scroll_right.pack(fill="both", expand=True)
        right_box = scroll_right.content
        
        # Fighter Top Profile
        prof_f = ttk.Frame(right_box)
        prof_f.pack(fill="x", pady=2)
        
        self.f_class_icon_lbl = ttk.Label(prof_f)
        self.f_class_icon_lbl.pack(side="left", padx=(0, 10))
        
        f_meta = ttk.Frame(prof_f)
        f_meta.pack(side="left")
        
        self.f_title_lbl = ttk.Label(f_meta, text=t("f_select_prompt"), font=("Segoe UI", 13, "bold"), foreground=ACCENT_GOLD)
        self.f_title_lbl.pack(anchor="w")
        
        self.f_sub_lbl = ttk.Label(f_meta, text="Clase: --- | Nivel: --- | Rango: Tier ---", font=("Segoe UI", 9), foreground=FG_MUTED)
        self.f_sub_lbl.pack(anchor="w")
        
        # Identity and Configuration Grid

        id_frame = ttk.LabelFrame(right_box, text=t("f_id_config"), padding=8)
        id_frame.pack(fill="x", pady=4)
        
        # Row 0: Name and Class
        ttk.Label(id_frame, text=t("f_lbl_name")).grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.f_name_entry_var = tk.StringVar()
        ttk.Entry(id_frame, textvariable=self.f_name_entry_var, width=16).grid(row=0, column=1, padx=4, pady=3, sticky="w")
        
        ttk.Label(id_frame, text=t("f_lbl_class")).grid(row=0, column=2, sticky="w", padx=4, pady=3)
        self.f_class_select_var = tk.StringVar(value="BAL (All-Rounder)")
        classes_opts = [
            "BAL (All-Rounder)", "BRE (Striker)", "DEF (Defender)", "TEC (Attacker)",
            "SHT (Shooter)", "COL (Collector)", "SKI (Skill Master)", "LUK (Lucky Star)"
        ]
        cb_cls = ttk.Combobox(id_frame, textvariable=self.f_class_select_var, values=classes_opts, state="readonly", width=18)
        cb_cls.grid(row=0, column=3, padx=4, pady=3, sticky="w")
        
        # Row 1: Grade (Tier) and Level
        ttk.Label(id_frame, text=t("f_lbl_grade")).grid(row=1, column=0, sticky="w", padx=4, pady=3)
        self.f_grade_select_var = tk.StringVar(value="5")
        cb_grd = ttk.Combobox(id_frame, textvariable=self.f_grade_select_var, values=["1", "2", "3", "4", "5", "6"], state="readonly", width=6)
        cb_grd.grid(row=1, column=1, padx=4, pady=3, sticky="w")
        
        ttk.Label(id_frame, text=t("f_lbl_level")).grid(row=1, column=2, sticky="w", padx=4, pady=3)
        self.f_lvl_select_var = tk.StringVar(value="125")
        ttk.Entry(id_frame, textvariable=self.f_lvl_select_var, width=8, justify="center").grid(row=1, column=3, padx=4, pady=3, sticky="w")
        
        # Row 2: HP Actual and MINGO Bag Bonus
        ttk.Label(id_frame, text=t("f_lbl_hp_cur")).grid(row=2, column=0, sticky="w", padx=4, pady=3)
        self.f_hp_current_var = tk.StringVar(value="15000")
        ttk.Entry(id_frame, textvariable=self.f_hp_current_var, width=10, justify="center").grid(row=2, column=1, padx=4, pady=3, sticky="w")
        
        ttk.Label(id_frame, text="Bono MINGO (0-3):").grid(row=2, column=2, sticky="w", padx=4, pady=3)
        self.f_bag_select_var = tk.StringVar(value="3")
        cb_fbag = ttk.Combobox(id_frame, textvariable=self.f_bag_select_var, values=["0", "1", "2", "3"], state="readonly", width=6)
        cb_fbag.grid(row=2, column=3, padx=4, pady=3, sticky="w")
        
        # Row 3: Character Model / Appearance
        ttk.Label(id_frame, text=t("f_lbl_model")).grid(row=3, column=0, sticky="w", padx=4, pady=3)
        self.f_model_select_var = tk.StringVar(value="Female 1 (BODY_FEMALE_001)")
        self.f_model_opts = [
            f"Female {i} (BODY_FEMALE_{i:03d})" for i in range(1, 9)
        ] + [
            f"Male {i} (BODY_MALE_{i:03d})" for i in range(1, 9)
        ]
        cb_model = ttk.Combobox(id_frame, textvariable=self.f_model_select_var, values=self.f_model_opts, state="readonly", width=26)
        cb_model.grid(row=3, column=1, columnspan=3, padx=4, pady=3, sticky="w")
        
        # Row 4: Real In-Game Capacity indicator
        self.f_real_bag_lbl = ttk.Label(id_frame, text="🎒 Capacidad Real: Calculando...", foreground=ACCENT_GOLD, font=("Segoe UI", 9, "bold"))
        self.f_real_bag_lbl.grid(row=4, column=0, columnspan=4, sticky="w", padx=4, pady=3)

        
        # Stats Form Grid (3 columns for perfect balance)
        stats_frame = ttk.LabelFrame(right_box, text=t("f_base_stats_box"), padding=8)
        stats_frame.pack(fill="x", pady=4)
        
        self.f_stats_vars = {}
        stat_names = [
            ("hp", t("f_hp_vit")),
            ("stm", t("f_stm_res")),
            ("str", t("f_str_pow")),
            ("dex", t("f_dex_agi")),
            ("vit", t("f_vit_def")),
            ("luk", t("f_luk_luck")),
        ]
        
        for idx, (k, label) in enumerate(stat_names):
            r = idx // 3
            c = (idx % 3) * 2
            ttk.Label(stats_frame, text=label).grid(row=r, column=c, sticky="w", padx=4, pady=4)
            v = tk.StringVar(value="30")
            self.f_stats_vars[k] = v
            ttk.Entry(stats_frame, textvariable=v, width=6, justify="center").grid(row=r, column=c+1, padx=4, pady=4)
            
        # Equipped Decals Preview Frame (8 slots for Grade 6 Tier 8)
        self.f_decals_frame = ttk.LabelFrame(right_box, text=t("f_equipped_decals_box"), padding=8)
        self.f_decals_frame.pack(fill="x", pady=4)
        self.f_decal_slots_lbls = []
        for slot_idx in range(8):
            lbl = ttk.Label(self.f_decals_frame, text=f"{t('f_slot_prefix')} {slot_idx+1}: {t('f_slot_empty')}", font=("Segoe UI", 8), compound="left")
            r = slot_idx % 4
            c = slot_idx // 4
            lbl.grid(row=r, column=c, sticky="w", padx=6, pady=2)
            self.f_decal_slots_lbls.append(lbl)

        # Quick Fighter Actions
        act_frame = ttk.Frame(right_box)
        act_frame.pack(fill="x", pady=6)
        
        btn_save_f = ttk.Button(act_frame, text=t("f_apply_btn"), style="Accent.TButton", command=self._save_fighter_changes)
        btn_save_f.pack(side="left", padx=3, fill="x", expand=True)
        
        btn_revive = ttk.Button(act_frame, text=t("f_revive_btn"), style="Success.TButton", command=self.revive_current_fighter)
        btn_revive.pack(side="left", padx=3, fill="x", expand=True)
        
        btn_max_fighter = ttk.Button(act_frame, text=t("f_max_stats_btn"), command=self.max_current_fighter)
        btn_max_fighter.pack(side="left", padx=3, fill="x", expand=True)

        # Engine Mod: Death Bag Capacity in masters.db
        bag_mod_box = ttk.LabelFrame(right_box, text=t("db_mod_box_title"), padding=8)
        bag_mod_box.pack(fill="x", pady=4)
        
        self.f_bag_db_status_lbl = ttk.Label(bag_mod_box, text="...", font=("Segoe UI", 8))
        self.f_bag_db_status_lbl.pack(anchor="w", pady=2)
        
        bag_btn_row = ttk.Frame(bag_mod_box)
        bag_btn_row.pack(fill="x", pady=2)
        
        btn_expand_bag = ttk.Button(bag_btn_row, text=t("db_expand_btn"), style="Accent.TButton", command=self._expand_deathbag_masters_action)
        btn_expand_bag.pack(side="left", padx=2, fill="x", expand=True)
        
        btn_restore_bag = ttk.Button(bag_btn_row, text=t("db_restore_btn"), command=self._restore_deathbag_masters_action)
        btn_restore_bag.pack(side="left", padx=2, fill="x", expand=True)

        # Meta Decal Presets for Fighters
        decal_preset_box = ttk.LabelFrame(right_box, text=t("f_presets_box"), padding=8)
        decal_preset_box.pack(fill="x", pady=6)
        
        preset_r = ttk.Frame(decal_preset_box)
        preset_r.pack(fill="x", pady=2)
        ttk.Label(preset_r, text="Preset:").pack(side="left", padx=2)
        self.decal_preset_var = tk.StringVar(value="Tengoku God Climber (Pisos 51F - 350F+)")
        preset_names = [
            "Tengoku God Climber (Pisos 51F - 350F+)",
            "Tirador KAMAS Definitivo (Full Shooter Meta)",
            "Destructor Melee (Mayal / Machete / Katana)",
            "Pesadilla de Defensa TDM (Invulnerable Tank)"
        ]
        cb_preset = ttk.Combobox(preset_r, textvariable=self.decal_preset_var, values=preset_names, state="readonly", width=38)
        cb_preset.pack(side="left", padx=4, fill="x", expand=True)
        
        btn_equip_preset = ttk.Button(decal_preset_box, text=t("f_preset_btn"), style="Accent.TButton", command=self._equip_decal_preset_action)
        btn_equip_preset.pack(fill="x", pady=2)
        
        btn_apply_preset = ttk.Button(decal_preset_box, text=t("f_inject_preset_btn"), command=self._apply_decal_preset_action)
        btn_apply_preset.pack(fill="x", pady=2)

    def _on_fighter_select(self, event):
        sel = self.fighters_tree.selection()
        if not sel:
            return
        node = sel[0]
        tree_idx = getattr(self, "_tree_node_to_tree_idx", {}).get(node, 0)
        save_idx = getattr(self, "_tree_node_to_save_idx", {}).get(node, 0)
        self.current_fighter_tree_idx = tree_idx
        self.current_fighter_idx = save_idx
        
        if not self.save_json:
            return
            
        fighters = modifiers.get_all_fighters_info(self.save_json)
        if save_idx < len(fighters):
            f = fighters[save_idx]
            name = f.get("name", f"Luchador #{tree_idx+1}")
            cls_name = f.get("class_name", "All-Rounder")
            cls_code = f.get("class", "BAL")
            grade = f.get("grade", 1)
            lvl = f.get("level", 1)
            hp_cur = f.get("hp", 1000)
            bag = f.get("bag", 20)

            
            self.f_title_lbl.config(text=name)
            is_en = (i18n.get_language() == "en")
            if is_en:
                self.f_sub_lbl.config(text=f"Class: {cls_name} ({cls_code}) | Grade: Tier {grade} ★ | Level: {lvl}")
            else:
                self.f_sub_lbl.config(text=f"Clase: {cls_name} ({cls_code}) | Grado: Tier {grade} ★ | Nivel: {lvl}")
            
            cls_icon_filename = FIGHTER_CLASSES.get(cls_code, ("", "all-rounder.png"))[1]
            ico = self.get_photo(cls_icon_filename, (48, 48)) or self.get_photo("all-rounder", (48, 48))
            self.f_class_icon_lbl.config(image=ico or "")
            self.tree_images["fighter_hero"] = ico
            
            self.f_name_entry_var.set(name)
            self.f_class_select_var.set(f"{cls_code} ({cls_name})")
            self.f_grade_select_var.set(str(grade))
            self.f_lvl_select_var.set(str(lvl))
            self.f_hp_current_var.set(str(hp_cur))
            mingo_bag = min(3, max(0, int(f.get("bag", 0))))
            self.f_bag_select_var.set(str(mingo_bag))
            
            # Select current character model
            body_val = f.get("body", "BODY_FEMALE_001")
            for opt in getattr(self, "f_model_opts", []):
                if body_val in opt:
                    self.f_model_select_var.set(opt)
                    break
            
            # Calculate real in-game bag capacity
            db_st = modifiers.get_deathbag_masters_status()
            vip_active = bool(self.save_json.get("soul", {}).get("vip", {}).get("flag", 0))
            vip_bonus = db_st.get("vip_bonus", 10) if vip_active else 0
            base_slots = db_st.get("min_bag", 20)
            total_slots = base_slots + mingo_bag + vip_bonus
            vip_txt = f" + VIP: +{vip_bonus}" if vip_bonus > 0 else ""
            if hasattr(self, "f_real_bag_lbl"):
                self.f_real_bag_lbl.config(
                    text=f"🎒 Total Real en Juego: {total_slots} slots (Base: {base_slots} + MINGO: +{mingo_bag}{vip_txt})"
                )
            self._refresh_deathbag_db_status()
            
            self.f_stats_vars["hp"].set(str(f.get("hp_pts", 20)))
            self.f_stats_vars["stm"].set(str(f.get("stm", 20)))
            self.f_stats_vars["str"].set(str(f.get("str", 20)))
            self.f_stats_vars["dex"].set(str(f.get("dex", 20)))
            self.f_stats_vars["vit"].set(str(f.get("vit", 20)))
            self.f_stats_vars["luk"].set(str(f.get("luk", 20)))
            
            # Update equipped decals preview (up to 8 slots)
            cid = f.get("cid", "")
            body_uid = modifiers.get_player_uid(self.save_json)
            eq_list = self.save_json.get("soul", {}).get("skl", {}).get("eqskl", {}).get(body_uid, [])
            fighter_eq = [e for e in eq_list if e.get("cid") == cid]
            for s_idx in range(len(self.f_decal_slots_lbls)):
                matching = [e for e in fighter_eq if e.get("slot") == s_idx]
                if matching:
                    did = matching[0].get("sklid", "")
                    d_info = self.decals_map.get(did, {})
                    d_name = d_info.get("name_es") or d_info.get("name_en") or did
                    art_rel = self._find_decal_art(did)
                    d_thumb = self.get_photo(art_rel, (28, 28), preserve_aspect=True)
                    self.f_decal_slots_lbls[s_idx].config(text=f" Espacio {s_idx+1}: {d_name} ({did})", image=d_thumb or "", foreground=ACCENT_GOLD)
                    self.tree_images[f"eq_decal_{s_idx}"] = d_thumb
                else:
                    self.f_decal_slots_lbls[s_idx].config(text=f" Espacio {s_idx+1}: [Vacío]", image="", foreground=FG_MUTED)

    def _move_fighter_up_action(self):
        if not self.save_json:
            return
        idx = getattr(self, "current_fighter_idx", 0)
        if idx <= 0:
            return
        if modifiers.move_fighter_up(self.save_json, idx):
            self._auto_save()
            new_idx = idx - 1
            self.current_fighter_idx = new_idx
            self.current_fighter_tree_idx = new_idx
            self.refresh_all_views()

    def _move_fighter_down_action(self):
        if not self.save_json:
            return
        idx = getattr(self, "current_fighter_idx", 0)
        children = self.fighters_tree.get_children()
        if idx >= len(children) - 1:
            return
        if modifiers.move_fighter_down(self.save_json, idx):
            self._auto_save()
            new_idx = idx + 1
            self.current_fighter_idx = new_idx
            self.current_fighter_tree_idx = new_idx
            self.refresh_all_views()


    def _select_fighter_tree_index(self, target_idx):
        children = self.fighters_tree.get_children()
        if 0 <= target_idx < len(children):
            self.fighters_tree.selection_set(children[target_idx])
            self.fighters_tree.see(children[target_idx])
            self._on_fighter_select(None)

    def _create_new_fighter_dialog(self):
        if not self.save_json:
            return
        uid = modifiers.get_player_uid(self.save_json)
        fighters = self.save_json.get("bodyuser", {}).get(uid, [])
        if len(fighters) >= 10:
            messagebox.showwarning(
                "Congelador Lleno" if i18n.get_language() == "es" else "Freezer Full",
                t("f_freezer_full_msg")
            )
            return
        CreateFighterDialog(self, self.save_json, on_created_cb=self._on_fighter_created_or_modified)

    def _on_fighter_created_or_modified(self):
        self._auto_save()
        uid = modifiers.get_player_uid(self.save_json)
        total_f = len(self.save_json.get("bodyuser", {}).get(uid, []))
        self.current_fighter_idx = max(0, total_f - 1)
        self.current_fighter_tree_idx = max(0, total_f - 1)
        self.refresh_all_views()


    def _clone_fighter_action(self):
        if not self.save_json:
            return
        uid = modifiers.get_player_uid(self.save_json)
        fighters = self.save_json.get("bodyuser", {}).get(uid, [])
        if len(fighters) >= 10:
            messagebox.showwarning(
                "Congelador Lleno" if i18n.get_language() == "es" else "Freezer Full",
                t("f_freezer_full_msg")
            )
            return
        save_idx = getattr(self, "current_fighter_idx", 0)
        chr_chrs = self.save_json.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])
        orig_name = chr_chrs[save_idx].get("name", "Luchador") if save_idx < len(chr_chrs) else "Luchador"
        
        is_en = (i18n.get_language() == "en")
        title = "Clone Fighter" if is_en else "Clonar Luchador"
        prompt = t("f_clone_prompt")
        default_name = f"{orig_name} (Clone)" if is_en else f"{orig_name} (Copia)"
        new_name = simpledialog.askstring(title, prompt, initialvalue=default_name)
        if not new_name:
            return
            
        ok, res = modifiers.clone_fighter(self.save_json, save_idx, new_name=new_name.strip())
        if not ok:
            messagebox.showerror("Error", str(res))
            return
            
        self._auto_save()
        total_f = len(self.save_json.get("bodyuser", {}).get(uid, []))
        self.current_fighter_idx = max(0, total_f - 1)
        self.current_fighter_tree_idx = max(0, total_f - 1)
        self.refresh_all_views()
        self._notify(
            "Fighter Cloned", "Luchador Clonado",
            f"Fighter '{orig_name}' successfully cloned as '{new_name}' with identical armors, weapons, deathbag items, stats and decals!\nSaved automatically.",
            f"¡Luchador '{orig_name}' clonado exitosamente como '{new_name}' con sus armaduras, armas, bolsa, estadísticas y calcomanías idénticas!\nGuardado automáticamente."
        )


    def _delete_fighter_action(self):
        if not self.save_json:
            return
        uid = modifiers.get_player_uid(self.save_json)
        fighters = self.save_json.get("bodyuser", {}).get(uid, [])
        if len(fighters) <= 1:
            messagebox.showwarning(
                "Aviso",
                t("f_delete_only_one_err")
            )
            return
            
        save_idx = getattr(self, "current_fighter_idx", 0)
        tree_idx = getattr(self, "current_fighter_tree_idx", 0)
        chr_chrs = self.save_json.get("soul", {}).get("chr", {}).get("chrs", {}).get(uid, [])
        f_name = chr_chrs[save_idx].get("name", "Luchador") if save_idx < len(chr_chrs) else "Luchador"
        
        if save_idx < len(chr_chrs) and chr_chrs[save_idx].get("state") == "USE":
            messagebox.showwarning(
                "Aviso",
                t("f_delete_in_use_err")
            )
            return
            
        confirm = messagebox.askyesno(
            t("f_delete_btn"),
            t("f_delete_confirm", name=f_name)
        )
        if not confirm:
            return
            
        ok, res = modifiers.delete_fighter(self.save_json, save_idx)
        if not ok:
            messagebox.showerror("Error", str(res))
            return
            
        self._auto_save()
        self.current_fighter_tree_idx = max(0, tree_idx - 1)
        self.refresh_all_views()
        self._notify(
            "Fighter Deleted", "Luchador Eliminado",
            f"Fighter '{f_name}' permanently removed from Freezer.\nSaved automatically.",
            f"¡Luchador '{f_name}' eliminado permanentemente del congelador.\nGuardado automáticamente."
        )

    def _save_fighter_changes(self):

        if not self.save_json:
            return
        idx = getattr(self, "current_fighter_idx", 0)
        name = self.f_name_entry_var.get()
        cls_str = self.f_class_select_var.get().split()[0]
        model_val = self.f_model_select_var.get() if hasattr(self, "f_model_select_var") else None
        try:
            grade = int(self.f_grade_select_var.get())
            lvl = int(self.f_lvl_select_var.get())
            hp_val = int(self.f_hp_current_var.get())
            bag_val = int(self.f_bag_select_var.get())
            php = int(self.f_stats_vars["hp"].get())
            pstm = int(self.f_stats_vars["stm"].get())
            pstr = int(self.f_stats_vars["str"].get())
            pdex = int(self.f_stats_vars["dex"].get())
            pvit = int(self.f_stats_vars["vit"].get())
            pluk = int(self.f_stats_vars["luk"].get())
        except ValueError:
            messagebox.showerror(t("error"), t("err_num_fields"))
            return
            
        modifiers.update_fighter(
            self.save_json, idx,
            name=name, clazz=cls_str, grade=grade, lvl=lvl, hp=hp_val,
            str_stat=pstr, dex=pdex, vit=pvit, stm=pstm, luk=pluk, bag=bag_val,
            param_hp=php, param_stm=pstm, param_str=pstr, param_dex=pdex, param_vit=pvit, param_luk=pluk,
            body_model=model_val
        )
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Fighter Updated", "Luchador Actualizado",
            f"Custom changes applied to {name} (Fighter #{idx+1})!\nSaved automatically.",
            f"¡Se han aplicado los cambios personalizados a {name} (Luchador #{idx+1})!\nGuardado automáticamente."
        )


    def revive_current_fighter(self):
        if not self.save_json:
            return
        modifiers.revive_all_fighters(self.save_json)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Fighters Revived", "Luchadores Revividos",
            "All fighters revived to 100% HP and death status removed!",
            "¡Se ha restaurado la vida al 100% y se ha eliminado el estado de muerte de todos los luchadores!"
        )

    def max_current_fighter(self):
        if not self.save_json:
            return
        modifiers.max_fighter_level_and_stats(self.save_json, fighter_index=self.current_fighter_idx, level=247)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Fighter Maximized", "Luchador Maximizado",
            f"Fighter #{self.current_fighter_idx+1} upgraded to Level 247 with maxed stats!",
            f"¡Luchador #{self.current_fighter_idx+1} mejorado a Nivel 247 con todos sus stats al tope!"
        )

    def _apply_decal_preset_action(self):
        if not self.save_json:
            return
        sel = self.decal_preset_var.get()
        key = "tengoku_climber"
        if "KAMAS" in sel: key = "kamas_god"
        elif "Melee" in sel: key = "melee_melter"
        elif "TDM" in sel: key = "tdm_defense"
        
        name, count = modifiers.apply_decal_preset_to_inventory(self.save_json, preset_key=key, count=5)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Decal Preset Added", "Preset de Calcomanías Añadido",
            f"Added x5 Premium copies of all {count} decals from preset:\n\n⭐ {name}\n\nReady to equip at Uncle Death's Grill!",
            f"¡Se han añadido x5 copias Premium de las {count} calcomanías del preset:\n\n⭐ {name}\n\n¡Listas para equipar en el Grill del Tío Death!"
        )

    def _equip_decal_preset_action(self):
        if not self.save_json:
            return
        fighters = modifiers.get_all_fighters_info(self.save_json)
        idx = getattr(self, "current_fighter_idx", 0)
        if idx >= len(fighters):
            return
        f_info = fighters[idx]
        cid = f_info.get("cid")
        sel = self.decal_preset_var.get()
        key = "tengoku_climber"
        if "KAMAS" in sel: key = "kamas_god"
        elif "Melee" in sel: key = "melee_melter"
        elif "TDM" in sel: key = "tdm_defense"
        
        name, count = modifiers.equip_decal_preset_on_fighter(self.save_json, cid, preset_key=key)
        self._auto_save()
        self.refresh_all_views()
        self.status_var.set(f"Preset '{name}' ({count}).")
        messagebox.showinfo(
            t("mb_preset_equipped_title"),
            t("mb_preset_equipped_msg", count=count, name=name, fighter=f_info.get('name', 'Luchador'))
        )

    def _refresh_deathbag_db_status(self):
        if not hasattr(self, "f_bag_db_status_lbl"):
            return
        st = modifiers.get_deathbag_masters_status()
        if not st.get("exists"):
            self.f_bag_db_status_lbl.config(text=t("db_mod_status_missing"), foreground=FG_MUTED)
        elif st.get("is_modded"):
            min_b = st.get("min_bag", 60)
            vip_b = st.get("vip_bonus", 10)
            self.f_bag_db_status_lbl.config(
                text=t("db_mod_status_active", base=min_b, total=min_b + vip_b),
                foreground=ACCENT_GREEN
            )
        else:
            self.f_bag_db_status_lbl.config(
                text=t("db_mod_status_vanilla"),
                foreground=FG_MUTED
            )

    def _expand_deathbag_masters_action(self):
        target = simpledialog.askinteger(
            t("db_expand_title"),
            t("db_expand_prompt"),
            initialvalue=60,
            minvalue=30,
            maxvalue=100,
            parent=self
        )
        if not target:
            return
        try:
            res = modifiers.expand_deathbag_capacity(target_capacity=target, vip_bonus=10)
            self._refresh_deathbag_db_status()
            if hasattr(self, "current_fighter_idx"):
                self._on_fighter_select(None)
            messagebox.showinfo(
                t("db_expand_success_title"),
                t("db_expand_success_msg", target=target, vip=target + 10, path=res['db_path'])
            )
        except Exception as e:
            messagebox.showerror("Error", f"masters.db:\n{e}")

    def _restore_deathbag_masters_action(self):
        if not messagebox.askyesno(
            t("db_restore_title"),
            t("db_restore_prompt"),
            parent=self
        ):
            return
        try:
            res = modifiers.restore_deathbag_capacity()
            self._refresh_deathbag_db_status()
            if hasattr(self, "current_fighter_idx"):
                self._on_fighter_select(None)
            messagebox.showinfo(
                t("db_restore_success_title"),
                t("db_restore_success_msg", path=res['db_path'])
            )
        except Exception as e:
            messagebox.showerror("Error", f"masters.db:\n{e}")

    def max_all_currencies(self):
        if not self.save_json:
            return
        modifiers.max_all_currencies(self.save_json)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Currencies Maximized", "Divisas Maximizadas",
            "Death Metals (99,999), Kill Coins, SPLithium, Bloodnium, and RE Points maxed out!",
            "¡Se han establecido Death Metals (99,999), Kill Coins, SPLithium, Sangrenio y Puntos RE al límite máximo!"
        )

    # ================= TAB 3: MATERIALS R&D (106) =================
    def _build_materials_tab(self):
        paned = ttk.PanedWindow(self.tab_materials, orient="horizontal")
        paned.pack(fill="both", expand=True)
        
        left_box = ttk.Frame(paned)
        paned.add(left_box, weight=3)
        
        # Row 1: Search, Category, Stock Filter, Rarity, Actions
        ctrl_frame = ttk.Frame(left_box)
        ctrl_frame.pack(fill="x", pady=2)
        
        ttk.Label(ctrl_frame, text=t("mat_search")).pack(side="left", padx=2)
        self.mat_search_var = tk.StringVar()
        self.mat_search_var.trace_add("write", lambda *args: self.filter_materials_list())
        ttk.Entry(ctrl_frame, textvariable=self.mat_search_var, width=12).pack(side="left", padx=2)
        
        is_en = (i18n.get_language() == "en")
        ttk.Label(ctrl_frame, text=t("mat_cat_lbl")).pack(side="left", padx=(4, 1))
        self.mat_cat_var = tk.StringVar(value="All" if is_en else "Todos")
        if is_en:
            cats = [
                "All",
                "Aluminum",
                "Copper",
                "Iron & Steel",
                "Oil",
                "Wood",
                "Cloth & Fibers",
                "D.O.D. ARMS (Metals)",
                "WAR ENSEMBLE (Metals)",
                "CANDLE WOLF (Metals)",
                "M.I.L.K. (Metals)",
                "Boss Metals",
                "Jackals & Tengoku Materials",
                "Steroids / Rostest (Fighters)",
                "🍄 Mushrooms & Beasts"
            ]
        else:
            cats = [
                "Todos",
                "Aluminio (Aluminum)",
                "Cobre (Copper)",
                "Hierro y Acero (Iron & Steel)",
                "Petróleo y Aceites (Oil)",
                "Maderas (Wood)",
                "Textiles y Fibras (Cloth)",
                "D.O.D. ARMS (Metals)",
                "WAR ENSEMBLE (Metals)",
                "CANDLE WOLF (Metals)",
                "M.I.L.K. (Metals)",
                "Metales de Jefes (Boss Metals)",
                "Materiales Jackals y Tengoku",
                "Esteroides / Rostest (Luchadores)",
                "🍄 Setas y Criaturas"
            ]
        cb_cat = ttk.Combobox(ctrl_frame, textvariable=self.mat_cat_var, values=cats, state="readonly", width=24)
        cb_cat.pack(side="left", padx=2)
        cb_cat.bind("<<ComboboxSelected>>", lambda e: self.filter_materials_list())

        ttk.Label(ctrl_frame, text=t("mat_stock_lbl")).pack(side="left", padx=(4, 1))
        self.mat_stock_filter_var = tk.StringVar(value=t("mat_all"))
        cb_stock = ttk.Combobox(ctrl_frame, textvariable=self.mat_stock_filter_var, values=[t("mat_all"), t("mat_in_stock"), t("mat_low_stock"), t("mat_out_stock")], state="readonly", width=14)
        cb_stock.pack(side="left", padx=2)
        cb_stock.bind("<<ComboboxSelected>>", lambda e: self.filter_materials_list())

        ttk.Label(ctrl_frame, text=t("mat_rarity_lbl")).pack(side="left", padx=(4, 1))
        self.mat_rarity_filter_var = tk.StringVar(value=t("decal_all"))
        cb_mrarity = ttk.Combobox(ctrl_frame, textvariable=self.mat_rarity_filter_var, values=[t("decal_all"), "1★", "2★", "3★", "4★", "5★", "6★", "7★", "8★"], state="readonly", width=6)
        cb_mrarity.pack(side="left", padx=2)
        cb_mrarity.bind("<<ComboboxSelected>>", lambda e: self.filter_materials_list())
        
        btn_open_storage = ttk.Button(ctrl_frame, text="📦 Coin Locker", command=self._open_storage_manager)
        btn_open_storage.pack(side="right", padx=1)

        btn_all_mat = ttk.Button(ctrl_frame, text="✨ Max Stock (x100)" if is_en else "✨ Stock Máximo (x100)", style="Accent.TButton", command=self.max_all_materials_preset)
        btn_all_mat.pack(side="right", padx=1)

        # Row 2: Pisos de la Torre (Wiki Tower Sections Quick Bar)
        ctrl_frame_floors = ttk.Frame(left_box)
        ctrl_frame_floors.pack(fill="x", pady=2)
        
        ttk.Label(ctrl_frame_floors, text=t("mat_floors_lbl"), font=("Segoe UI", 8, "bold"), foreground=ACCENT_GOLD).pack(side="left", padx=2)
        self.mat_floor_filter = tk.StringVar(value="TODOS")
        
        floor_buttons = [
            ("🌐 All" if is_en else "🌐 Todos", "TODOS"),
            ("🏢 1F-10F (DOD)", "1_10"),
            ("🏭 11F-20F (WE)", "11_20"),
            ("🏰 21F-30F (CW)", "21_30"),
            ("🏟️ 31F-40F (MILK)", "31_40"),
            ("🌌 41F-50F (Battle)", "41_50"),
            ("👑 51F+ (Tengoku)", "51_PLUS")
        ]
        for btn_text, mode in floor_buttons:
            ttk.Button(ctrl_frame_floors, text=btn_text, command=lambda m=mode: self._set_mat_floor_filter(m)).pack(side="left", padx=1)
        
        # Materials Treeview
        mat_tree_frame = ttk.Frame(left_box)
        mat_tree_frame.pack(fill="both", expand=True, pady=4)
        mat_scroll = ttk.Scrollbar(mat_tree_frame, orient="vertical")
        self.mat_tree = ttk.Treeview(mat_tree_frame, columns=("stock", "rarity", "category", "id"), show="tree headings", height=16, yscrollcommand=mat_scroll.set)
        mat_scroll.config(command=self.mat_tree.yview)
        self.mat_tree.heading("#0", text=t("decal_col_icon"))
        self.mat_tree.heading("stock", text=t("bp_col_storage"))
        self.mat_tree.heading("rarity", text=t("decal_col_rare"))
        self.mat_tree.heading("category", text=t("decal_col_type"))
        self.mat_tree.heading("id", text=t("wm_col_code"))
        
        self.mat_tree.column("#0", width=280)
        self.mat_tree.column("stock", width=90, anchor="center")
        self.mat_tree.column("rarity", width=70, anchor="center")
        self.mat_tree.column("category", width=130)
        self.mat_tree.column("id", width=120)
        
        mat_scroll.pack(side="right", fill="y")
        self.mat_tree.pack(side="left", fill="both", expand=True)
        self.mat_tree.bind("<<TreeviewSelect>>", self._on_mat_select)
        self.mat_tree.bind("<Double-1>", self._edit_selected_material_count)
        
        self.mat_tree.tag_configure("tag_in_stock", foreground=ACCENT_GOLD)
        self.mat_tree.tag_configure("tag_out_of_stock", foreground=FG_MUTED)
        
        # Right Material Card (Wiki Showcase)
        mat_card_container = ttk.LabelFrame(paned, text=t("mat_card_title"), padding=4)
        paned.add(mat_card_container, weight=2)
        scroll_mat = ScrollableFrame(mat_card_container)
        scroll_mat.pack(fill="both", expand=True)
        self.mat_card = scroll_mat.content
        
        self.mat_art_lbl = ttk.Label(self.mat_card)
        self.mat_art_lbl.pack(pady=6)
        
        self.mat_title_lbl = ttk.Label(self.mat_card, text=t("mat_select_prompt"), font=("Segoe UI", 12, "bold"), foreground=ACCENT_GOLD, wraplength=260, justify="center")
        self.mat_title_lbl.pack(pady=2)
        
        self.mat_type_lbl = ttk.Label(self.mat_card, text="---", font=("Segoe UI", 9), foreground=FG_MUTED)
        self.mat_type_lbl.pack(pady=2)
        
        self.mat_stock_lbl = ttk.Label(self.mat_card, text=t("mat_none_in_storage"), font=("Segoe UI", 10, "bold"), foreground=ACCENT_CYAN)
        self.mat_stock_lbl.pack(pady=4)
        
        self.mat_desc_lbl = ttk.Label(self.mat_card, text=t("mat_desc_default"), font=("Segoe UI", 9), foreground=FG_MUTED, wraplength=260, justify="center")
        self.mat_desc_lbl.pack(pady=6)
        
        # Quantity controls
        qty_f = ttk.Frame(self.mat_card)
        qty_f.pack(pady=4)
        ttk.Label(qty_f, text=t("mat_set_qty_lbl")).pack(side="left", padx=2)
        self.mat_qty_entry_var = tk.StringVar(value="50")
        ttk.Entry(qty_f, textvariable=self.mat_qty_entry_var, width=6, justify="center").pack(side="left", padx=4)
        ttk.Button(qty_f, text=t("mat_set_btn"), style="Accent.TButton", command=self._set_selected_mat_qty).pack(side="left", padx=2)
        
        quick_m_box = ttk.Frame(self.mat_card)
        quick_m_box.pack(fill="x", pady=4)
        ttk.Button(quick_m_box, text="+10", command=lambda: self._quick_add_material_qty(10)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(quick_m_box, text="+50", command=lambda: self._quick_add_material_qty(50)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(quick_m_box, text="+100", command=lambda: self._quick_add_material_qty(100)).pack(side="left", fill="x", expand=True, padx=1)

        # Capacity expansion frame
        cap_frame = ttk.LabelFrame(self.mat_card, text=t("mat_locker_cap_title"), padding=8)
        cap_frame.pack(fill="x", pady=(10, 0))
        
        self.mat_cap_indicator_lbl = ttk.Label(cap_frame, text="Almacén: 0 / 0 casillas", font=("Segoe UI", 9, "bold"))
        self.mat_cap_indicator_lbl.pack(anchor="w", pady=2)
        
        exp_row1 = ttk.Frame(cap_frame)
        exp_row1.pack(fill="x", pady=2)
        ttk.Button(exp_row1, text=t("mat_expand_500"), command=lambda: self._expand_coin_locker_add(500)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(exp_row1, text=t("mat_expand_1000"), command=lambda: self._expand_coin_locker_add(1000)).pack(side="left", fill="x", expand=True, padx=1)
        
        exp_row2 = ttk.Frame(cap_frame)
        exp_row2.pack(fill="x", pady=2)
        ttk.Button(exp_row2, text=t("mat_expand_max"), command=lambda: self._expand_coin_locker(6000)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(exp_row2, text=t("mat_expand_custom"), style="Accent.TButton", command=self._expand_coin_locker_custom).pack(side="left", fill="x", expand=True, padx=1)

    def _get_mat_photo_key(self, itemid, name_en):
        if hasattr(self, "icon_map") and "materials_thumbs" in self.icon_map:
            thumb_rel = self.icon_map["materials_thumbs"].get(itemid)
            if thumb_rel and os.path.exists(os.path.join(ICONS_DIR, thumb_rel)):
                return thumb_rel
        clean_en = name_en.lower().replace(" ", "_").replace("-", "_").replace("'", "").replace(".", "")
        for candidate in [f"thumbs/materials/mat_{itemid.lower()}.png", f"{clean_en}_box", f"{clean_en}_itembox", clean_en, itemid.lower()]:
            if self.get_photo(candidate, (36, 36)):
                return candidate
        if "alumi" in itemid.lower(): return "materials/aluminum_scraps.png"
        elif "copper" in itemid.lower(): return "materials/clump_of_copper_scraps.png"
        elif "iron" in itemid.lower(): return "materials/iron_scraps.png"
        elif "oil" in itemid.lower(): return "materials/waste_oil.png"
        elif "wood" in itemid.lower(): return "materials/veneer_plank.png"
        elif "fiber" in itemid.lower(): return "materials/cotton.png"
        elif "diy" in itemid.lower(): return "materials/dod_arms_purple_metal.png"
        elif "spo" in itemid.lower(): return "materials/war_ensemble_purple_metal.png"
        elif "fan" in itemid.lower(): return "materials/candle_wolf_purple_metal.png"
        elif "mil" in itemid.lower(): return "materials/m.i.l.k._purple_metal.png"
        return "materials/special_steel.png"

    def _on_mat_select(self, event):
        sel = self.mat_tree.selection()
        if not sel:
            return
        node = sel[0]
        full_title = self.mat_tree.item(node, "text").strip()
        vals = self.mat_tree.item(node, "values")
        stock_str = vals[0]
        stars = vals[1]
        cat = vals[2]
        itemid = vals[3]
        
        self.current_mat_selection = (itemid, full_title, cat)
        self.mat_title_lbl.config(text=full_title)
        self.mat_type_lbl.config(text=t("mat_cat_info", cat=cat, rare=stars, id=itemid))
        if stock_str != "-":
            self.mat_stock_lbl.config(text=t("mat_in_storage", qty=stock_str), foreground=ACCENT_GOLD)
        else:
            self.mat_stock_lbl.config(text=t("mat_none_in_storage"), foreground=FG_MUTED)
        
        desc = t("mat_desc_default")
        for m in self.materials_db:
            if m["itemid"] == itemid:
                desc = i18n.get_item_desc(m) or desc
                break
        self.mat_desc_lbl.config(text=desc)
        
        name_en = full_title.split("(")[-1].replace(")", "").strip() if "(" in full_title else full_title
        clean_slug = name_en.lower().replace(" ", "_").replace("-", "_").replace("'", "")
        
        # Check if selection is a Special Mushroom or Beast
        special_icon = None
        for mid, mname, icon_f in SPECIAL_MUSHROOMS:
            if mid == itemid:
                special_icon = icon_f
                break
        if not special_icon:
            for bid, bname, icon_b in SPECIAL_BEASTS:
                if bid == itemid:
                    special_icon = icon_b
                    break

        if special_icon:
            photo = self.get_photo(special_icon, size=(220, 220), preserve_aspect=True)
        else:
            card_rel = self.icon_map.get("materials_cards", {}).get(itemid) if hasattr(self, "icon_map") else None
            photo = self.get_photo(card_rel, size=(280, 140), preserve_aspect=True) if card_rel else None
            if not photo:
                photo = self.get_photo(f"{clean_slug}_itembox", size=(280, 140), preserve_aspect=True) or self.get_photo(clean_slug, size=(140, 140), preserve_aspect=True)
            if not photo:
                photo = self.get_photo(self._get_mat_photo_key(itemid, name_en), size=(140, 140), preserve_aspect=True)
            
        self.mat_art_lbl.config(image=photo or "")
        self.tree_images["mat_preview"] = photo

    def _set_selected_mat_qty(self):
        if not self.current_mat_selection or not self.save_json:
            return
        itemid, name, cat = self.current_mat_selection
        try:
            qty = int(self.mat_qty_entry_var.get())
        except ValueError:
            qty = 50
        modifiers.add_material_to_storage(self.save_json, itemid, count=qty)
        self._auto_save()
        self.filter_materials_list()
        self.status_var.set(f"Añadido {qty} u. de {name} a tu Almacén.")

    def _quick_add_material_qty(self, delta):
        if not self.current_mat_selection or not self.save_json:
            return
        itemid, name, cat = self.current_mat_selection
        modifiers.add_material_to_storage(self.save_json, itemid, count=delta)
        self._auto_save()
        self.filter_materials_list()
        self.status_var.set(f"Añadido {delta} u. de {name} a tu Almacén.")

    def _edit_selected_material_count(self, event):
        sel = self.mat_tree.selection()
        if not sel:
            return
        node = sel[0]
        vals = self.mat_tree.item(node, "values")
        itemid = vals[3]
        name = self.mat_tree.item(node, "text").strip()
        
        new_cnt = simpledialog.askinteger("Cantidad de Material", f"Ingresa las unidades para añadir a tu Almacén:\n{name} ({itemid})", initialvalue=50, minvalue=1, maxvalue=500)
        if new_cnt is not None:
            modifiers.add_material_to_storage(self.save_json, itemid, count=new_cnt)
            self._auto_save()
            self.filter_materials_list()
            self.status_var.set(f"Añadido {new_cnt} u. de {name} a tu Almacén.")

    def max_all_materials_preset(self):
        if not self.save_json:
            return
        modifiers.add_all_materials_to_storage(self.save_json, count=100)
        self._auto_save()
        self.filter_materials_list()
        self._notify(
            "Storage Stocked", "Almacén Abastecido",
            "100 units of ALL 108 R&D materials deposited into Coin Locker!",
            "¡Se han depositado 100 unidades de TODOS los 108 materiales de R&D en tu Almacén!"
        )

    def _expand_coin_locker_add(self, amount):
        if not self.save_json:
            return
        current_cap = len(self.save_json.get("soul", {}).get("cl", []))
        self._expand_coin_locker(current_cap + amount)

    def _expand_coin_locker_custom(self):
        if not self.save_json:
            return
        cl_items = self.save_json.get("soul", {}).get("cl", [])
        current_cap = len(cl_items)
        occupied_count = len([x for x in cl_items if x.get("type", -1) != -1 or x.get("eid", "") != ""])
        prompt_txt = t("mat_locker_custom_prompt", cur=current_cap, occ=occupied_count)
        target = simpledialog.askinteger(
            "🚀 " + t("mat_locker_cap_title"),
            prompt_txt,
            initialvalue=max(occupied_count + 200, 6000),
            minvalue=max(occupied_count, 100),
            maxvalue=50000,
            parent=self
        )
        if target and target != current_cap:
            self._expand_coin_locker(target)

    def _expand_coin_locker(self, target_capacity):
        if not self.save_json:
            return
        cl_items = self.save_json.get("soul", {}).get("cl", [])
        current_cap = len(cl_items)
        occupied_count = len([x for x in cl_items if x.get("type", -1) != -1 or x.get("eid", "") != ""])
        if target_capacity < occupied_count:
            messagebox.showwarning(
                t("mat_locker_limit_title"),
                t("mat_locker_limit_msg", occ=occupied_count)
            )
            return
        if target_capacity == current_cap:
            return
        old_c, new_c = modifiers.expand_storage_capacity(self.save_json, target_capacity=target_capacity)
        self._auto_save()
        self.status_var.set(t("mat_locker_status_bar", old=old_c, new=new_c))
        self.refresh_all_views()
        messagebox.showinfo(
            t("mat_locker_updated_title"),
            t("mat_locker_updated_msg", old=old_c, new=new_c, occ=occupied_count)
        )

    def _set_mat_floor_filter(self, mode):
        self.mat_floor_filter.set(mode)
        self.filter_materials_list()

    @staticmethod
    def _match_material_category(cat_filter, item_cat):
        if not cat_filter or cat_filter in ("Todos", "All"):
            return True
        fl = cat_filter.lower()
        cl = item_cat.lower()
        
        if "steroid" in fl or "esteroide" in fl or "rostest" in fl:
            return ("esteroide" in cl or "steroid" in cl or "rostest" in cl)
        if "aluminum" in fl or "aluminio" in fl:
            return "alumin" in cl
        if "copper" in fl or "cobre" in fl:
            return ("cobre" in cl or "copper" in cl)
        if "iron" in fl or "hierro" in fl or "steel" in fl or "acero" in fl:
            return ("hierro" in cl or "iron" in cl)
        if "oil" in fl or "petr" in fl or "aceite" in fl:
            return ("petr" in cl or "oil" in cl or "aceite" in cl)
        if "wood" in fl or "mader" in fl:
            return ("mader" in cl or "wood" in cl)
        if "cloth" in fl or "textil" in fl or "fiber" in fl or "fibra" in fl:
            return ("textil" in cl or "cloth" in cl or "fibra" in cl)
        if "d.o.d" in fl or "dod" in fl:
            return ("d.o.d" in cl or "dod" in cl)
        if "war" in fl:
            return "war" in cl
        if "candle" in fl:
            return "candle" in cl
        if "m.i.l.k" in fl or "milk" in fl:
            return ("m.i.l.k" in cl or "milk" in cl)
        if "boss" in fl or "jefe" in fl:
            return ("boss" in cl or "jefe" in cl)
        if "jackal" in fl or "tengoku" in cl:
            return ("jackal" in cl or "tengoku" in cl)
            
        c_key = cat_filter.lower().split()[0].replace("(", "").replace(")", "")
        return c_key in cl

    @staticmethod
    def _localize_material_category(cat_str):
        cl = cat_str.lower()
        if "esteroide" in cl or "rostest" in cl:
            return "Steroids / Rostest (Fighters)"
        if "alumin" in cl:
            return "Aluminum"
        if "cobre" in cl or "copper" in cl:
            return "Copper"
        if "hierro" in cl or "iron" in cl:
            return "Iron & Steel"
        if "petr" in cl or "oil" in cl:
            return "Oil"
        if "mader" in cl or "wood" in cl:
            return "Wood"
        if "textil" in cl or "cloth" in cl:
            return "Cloth & Fibers"
        if "boss" in cl or "jefe" in cl:
            return "Boss Metals"
        if "jackal" in cl or "tengoku" in cl:
            return "Jackals & Tengoku Materials"
        return cat_str

    def filter_materials_list(self):
        self.mat_tree.delete(*self.mat_tree.get_children())
            
        query = self.mat_search_var.get().lower().strip() if hasattr(self, "mat_search_var") else ""
        query_tokens = query.split() if query else []
        cat_filter = self.mat_cat_var.get() if hasattr(self, "mat_cat_var") else "Todos"

        stock_filter = self.mat_stock_filter_var.get() if hasattr(self, "mat_stock_filter_var") else "Todo"
        rarity_filter = self.mat_rarity_filter_var.get() if hasattr(self, "mat_rarity_filter_var") else "Todas"
        floor_filter = self.mat_floor_filter.get() if hasattr(self, "mat_floor_filter") else "TODOS"
        
        # Get live stock from save
        stock_map = {}
        if self.save_json:
            try:
                stock_map = modifiers.analyze_storage_stock(self.save_json).get("stock_by_id", {})
            except Exception:
                stock_map = {}
                
        first_row = None
        is_en = (i18n.get_language() == "en")
        
        # 1. R&D Materials from masters.db
        if "🍄" not in cat_filter:
            for m in self.materials_db:
                name_es = m.get("name_es", m.get("name", ""))
                name_en = m.get("name_en", "")
                cat = m.get("category", "Materiales")
                r = m.get("rarity", 1)
                stars = "★" * r
                itemid = m.get("itemid", "")
                cnt = stock_map.get(itemid, 0)
                
                # Category filter
                if not self._match_material_category(cat_filter, cat):
                    continue
                    
                # Stock filter
                if ("En Stock" in stock_filter or "In Stock" in stock_filter) and cnt <= 0:
                    continue
                elif ("Stock Bajo" in stock_filter or "Low Stock" in stock_filter) and (cnt <= 0 or cnt >= 10):
                    continue
                elif ("Agotado" in stock_filter or "Out of Stock" in stock_filter) and cnt > 0:
                    continue

                # Rarity filter
                if rarity_filter not in ("Todas", "All"):
                    try:
                        req_r = int(rarity_filter.replace("★", "").strip())
                        if r != req_r:
                            continue
                    except ValueError:
                        pass

                # Floor filter (Tower Section)
                if floor_filter != "TODOS":
                    cat_lower = cat.lower()
                    match_floor = False
                    if floor_filter == "1_10" and (r in (1, 2) or "d.o.d" in cat_lower):
                        match_floor = True
                    elif floor_filter == "11_20" and (r == 3 or "war" in cat_lower):
                        match_floor = True
                    elif floor_filter == "21_30" and (r == 4 or "candle" in cat_lower):
                        match_floor = True
                    elif floor_filter == "31_40" and (r == 5 or "m.i.l.k" in cat_lower):
                        match_floor = True
                    elif floor_filter == "41_50" and (r == 6):
                        match_floor = True
                    elif floor_filter == "51_PLUS" and (r in (7, 8) or "tengoku" in cat_lower or "jackals" in cat_lower):
                        match_floor = True
                    if not match_floor:
                        continue

                # Query search with smart multi-word matching & Tier aliases (e.g. "mdf t2 wood", "t2 wood", "tier 2")
                if query_tokens:
                    searchable = f"{name_es} {name_en} {cat} {self._localize_material_category(cat)} {itemid} t{r} tier {r} tier{r} {r}★ {r}star {name_en.replace('.', '')} {name_es.replace('.', '')}".lower()
                    if not all(token in searchable for token in query_tokens):
                        continue

                    
                stock_str = f"{cnt} pcs." if is_en and cnt > 0 else (f"{cnt} u." if cnt > 0 else "-")
                tag = "tag_in_stock" if cnt > 0 else "tag_out_of_stock"
                    
                if is_en:
                    display_title = f"{name_en} ({name_es})" if name_es and name_en != name_es else (name_en or name_es)
                    cat_display = self._localize_material_category(cat)
                else:
                    display_title = f"{name_es} ({name_en})" if name_en and name_en != name_es else (name_es or name_en)
                    cat_display = cat
                icon_k = self._get_mat_photo_key(itemid, name_en or name_es)
                thumb = self.get_photo(icon_k, size=(36, 36), preserve_aspect=True)
                node_id = self.mat_tree.insert(
                    "",
                    "end",
                    text=f" {display_title}",
                    image=thumb or "",
                    values=(stock_str, stars, cat_display, itemid),
                    tags=(tag,)
                )
                self.tree_images[node_id] = thumb
                if not first_row:
                    first_row = node_id
                    
        # 2. Shrooms and Beasts (Tower Exploration)
        if (cat_filter in ["Todos", "All"] or "🍄" in cat_filter) and floor_filter == "TODOS" and rarity_filter in ("Todas", "All"):
            for mid, mname, icon_f in SPECIAL_MUSHROOMS:
                cnt = stock_map.get(mid, 0)
                if ("En Stock" in stock_filter or "In Stock" in stock_filter) and cnt <= 0:
                    continue
                elif ("Stock Bajo" in stock_filter or "Low Stock" in stock_filter) and (cnt <= 0 or cnt >= 10):
                    continue
                elif ("Agotado" in stock_filter or "Out of Stock" in stock_filter) and cnt > 0:
                    continue
                if query_tokens:
                    searchable = f"{mname} {mid} mushroom seta shroom".lower()
                    if not all(token in searchable for token in query_tokens):
                        continue
                stock_str = f"{cnt} pcs." if i18n.get_language() == "en" and cnt > 0 else (f"{cnt} u." if cnt > 0 else "-")
                tag = "tag_in_stock" if cnt > 0 else "tag_out_of_stock"
                thumb = self.get_photo(icon_f, size=(36, 36), preserve_aspect=True) or self.get_photo("01_heartshroom_1", size=(36, 36), preserve_aspect=True)
                node_id = self.mat_tree.insert(
                    "",
                    "end",
                    text=f" {mname}",
                    image=thumb or "",
                    values=(stock_str, "★★★", "Special Shrooms" if i18n.get_language() == "en" else "Setas Especiales", mid),
                    tags=(tag,)
                )
                self.tree_images[node_id] = thumb
                if not first_row:
                    first_row = node_id
                    
            for bid, bname, icon_b in SPECIAL_BEASTS:
                cnt = stock_map.get(bid, 0)
                if ("En Stock" in stock_filter or "In Stock" in stock_filter) and cnt <= 0:
                    continue
                elif ("Stock Bajo" in stock_filter or "Low Stock" in stock_filter) and (cnt <= 0 or cnt >= 10):
                    continue
                elif ("Agotado" in stock_filter or "Out of Stock" in stock_filter) and cnt > 0:
                    continue
                if query_tokens:
                    searchable = f"{bname} {bid} beast criatura".lower()
                    if not all(token in searchable for token in query_tokens):
                        continue

                stock_str = f"{cnt} pcs." if i18n.get_language() == "en" and cnt > 0 else (f"{cnt} u." if cnt > 0 else "-")
                tag = "tag_in_stock" if cnt > 0 else "tag_out_of_stock"
                thumb = self.get_photo(icon_b, size=(36, 36), preserve_aspect=True) or self.get_photo("snails", size=(36, 36), preserve_aspect=True)
                beast_cat = "Golden Beasts" if i18n.get_language() == "en" else "Criaturas Doradas"
                node_id = self.mat_tree.insert(
                    "",
                    "end",
                    text=f" {bname}",
                    image=thumb or "",
                    values=(stock_str, "★★★★", beast_cat, bid),
                    tags=(tag,)
                )
                self.tree_images[node_id] = thumb
                if not first_row:
                    first_row = node_id
                    
        if first_row:
            self.mat_tree.selection_set(first_row)
            self._on_mat_select(None)

    # ================= TAB 4: OFFICIAL DECALS (626) =================
    def _build_decals_tab(self):
        paned = ttk.PanedWindow(self.tab_decals, orient="horizontal")
        paned.pack(fill="both", expand=True)
        
        left_box = ttk.Frame(paned)
        paned.add(left_box, weight=3)
        
        # Row 1: Search, Rarity, Type, Possession, Bulk Unlock
        ctrl_frame = ttk.Frame(left_box)
        ctrl_frame.pack(fill="x", pady=2)
        
        ttk.Label(ctrl_frame, text=t("decal_search")).pack(side="left", padx=2)
        self.decal_search_var = tk.StringVar()
        self.decal_search_var.trace_add("write", lambda *args: self.filter_decals_list())
        ttk.Entry(ctrl_frame, textvariable=self.decal_search_var, width=13).pack(side="left", padx=2)
        
        ttk.Label(ctrl_frame, text=t("decal_rare_lbl")).pack(side="left", padx=(4, 1))
        self.decal_rarity_filter_var = tk.StringVar(value=t("decal_all"))
        cb_rarity = ttk.Combobox(ctrl_frame, textvariable=self.decal_rarity_filter_var, values=[t("decal_all"), "1★", "2★", "3★", "4★", "5★"], state="readonly", width=6)
        cb_rarity.pack(side="left", padx=2)
        cb_rarity.bind("<<ComboboxSelected>>", lambda e: self.filter_decals_list())

        ttk.Label(ctrl_frame, text=t("decal_type_lbl")).pack(side="left", padx=(4, 1))
        self.decal_type_filter_var = tk.StringVar(value=t("decal_all"))
        cb_dtype = ttk.Combobox(ctrl_frame, textvariable=self.decal_type_filter_var, values=[t("decal_all"), t("decal_premium"), t("decal_standard")], state="readonly", width=12)
        cb_dtype.pack(side="left", padx=2)
        cb_dtype.bind("<<ComboboxSelected>>", lambda e: self.filter_decals_list())

        ttk.Label(ctrl_frame, text=t("decal_poss_lbl")).pack(side="left", padx=(4, 1))
        self.decal_poss_filter_var = tk.StringVar(value=t("decal_all"))
        cb_dposs = ttk.Combobox(ctrl_frame, textvariable=self.decal_poss_filter_var, values=[t("decal_all"), t("decal_owned"), t("decal_missing")], state="readonly", width=14)
        cb_dposs.pack(side="left", padx=2)
        cb_dposs.bind("<<ComboboxSelected>>", lambda e: self.filter_decals_list())

        btn_meta = ttk.Button(ctrl_frame, text=t("decal_pack_meta"), command=self.add_meta_decals_preset)
        btn_meta.pack(side="right", padx=1)

        btn_all_p = ttk.Button(ctrl_frame, text=t("decal_unlock_all"), style="Accent.TButton", command=self.unlock_all_decals_preset)
        btn_all_p.pack(side="right", padx=1)

        self.decal_unlock_qty_var = tk.StringVar(value="3")
        ttk.Entry(ctrl_frame, textvariable=self.decal_unlock_qty_var, width=3, justify="center").pack(side="right", padx=1)
        ttk.Label(ctrl_frame, text=t("decal_copies_lbl")).pack(side="right", padx=(2, 0))

        # Row 2: Eventos / Colaboraciones Quick Buttons Bar
        ctrl_frame_events = ttk.Frame(left_box)
        ctrl_frame_events.pack(fill="x", pady=2)
        
        ttk.Label(ctrl_frame_events, text=t("decal_events_lbl"), font=("Segoe UI", 8, "bold"), foreground=ACCENT_GOLD).pack(side="left", padx=2)
        self.decal_event_filter = tk.StringVar(value="TODOS")
        
        decal_event_buttons = [
            (t("decal_event_all"), "TODOS"),
            ("💥 World of Tanks", "WOT"),
            ("⚔️ No More Heroes", "NMH"),
            ("🎯 Killer7", "KILLER7"),
            ("🌀 Gravity Rush", "GRAVITY_RUSH"),
            ("🗼 Tengoku & Meta", "TENGOKU_META")
        ]
        for btn_text, mode in decal_event_buttons:
            ttk.Button(ctrl_frame_events, text=btn_text, command=lambda m=mode: self._set_decal_event_filter(m)).pack(side="left", padx=1)

        # Row 3: Estilos de Juego Tácticos Quick Buttons Bar
        ctrl_frame_styles = ttk.Frame(left_box)
        ctrl_frame_styles.pack(fill="x", pady=2)
        
        ttk.Label(ctrl_frame_styles, text=t("decal_styles_lbl"), font=("Segoe UI", 8, "bold"), foreground=ACCENT_CYAN).pack(side="left", padx=2)
        self.decal_style_filter = tk.StringVar(value="TODOS")
        
        decal_style_buttons = [
            (t("decal_style_all"), "TODOS"),
            ("⚔️ Addicts", "ADDICTS"),
            (t("decal_style_crit"), "CRIT_DMG"),
            (t("decal_style_tank"), "TANK_DEF"),
            (t("decal_style_vamp"), "VAMP_SURV"),
            (t("decal_style_farm"), "FARM_QOL"),
            (t("decal_style_sets"), "SETS")
        ]
        for btn_text, mode in decal_style_buttons:
            ttk.Button(ctrl_frame_styles, text=btn_text, command=lambda m=mode: self._set_decal_style_filter(m)).pack(side="left", padx=1)

        # Treeview with columns
        decal_tree_frame = ttk.Frame(left_box)
        decal_tree_frame.pack(fill="both", expand=True, pady=4)
        decal_scroll = ttk.Scrollbar(decal_tree_frame, orient="vertical")
        self.decals_tree = ttk.Treeview(decal_tree_frame, columns=("stars", "id", "premium", "count"), show="tree headings", height=16, yscrollcommand=decal_scroll.set)
        decal_scroll.config(command=self.decals_tree.yview)
        self.decals_tree.heading("#0", text=t("decal_col_icon"))
        self.decals_tree.heading("stars", text=t("decal_col_rare"))
        self.decals_tree.heading("id", text=t("decal_col_id"))
        self.decals_tree.heading("premium", text=t("decal_col_type"))
        self.decals_tree.heading("count", text=t("decal_col_qty"))
        
        self.decals_tree.column("#0", width=300)
        self.decals_tree.column("stars", width=65, anchor="center")
        self.decals_tree.column("id", width=160)
        self.decals_tree.column("premium", width=85, anchor="center")
        self.decals_tree.column("count", width=70, anchor="center")
        
        decal_scroll.pack(side="right", fill="y")
        self.decals_tree.pack(side="left", fill="both", expand=True)
        self.decals_tree.bind("<<TreeviewSelect>>", self._on_decal_select)
        self.decals_tree.bind("<Double-1>", self._edit_selected_decal_count)
        
        decal_card_container = ttk.LabelFrame(paned, text=t("decal_card_title"), padding=4)
        paned.add(decal_card_container, weight=2)
        scroll_decal = ScrollableFrame(decal_card_container)
        scroll_decal.pack(fill="both", expand=True)
        self.decal_card = scroll_decal.content
        
        self.decal_art_lbl = ttk.Label(self.decal_card)
        self.decal_art_lbl.pack(pady=10)
        
        self.decal_title_lbl = ttk.Label(self.decal_card, text=t("decal_select_prompt"), font=("Segoe UI", 12, "bold"), wraplength=240, justify="center")
        self.decal_title_lbl.pack(pady=4)
        
        self.decal_type_lbl = ttk.Label(self.decal_card, text="---", font=("Segoe UI", 9), foreground=ACCENT_GOLD)
        self.decal_type_lbl.pack(pady=2)
        
        self.decal_desc_lbl = ttk.Label(self.decal_card, text="---", font=("Segoe UI", 9), foreground=FG_MUTED, wraplength=240, justify="center")
        self.decal_desc_lbl.pack(pady=10)
        
        qty_box = ttk.Frame(self.decal_card)
        qty_box.pack(pady=4)
        ttk.Label(qty_box, text=t("decal_copies_edit_lbl")).pack(side="left", padx=4)
        self.decal_qty_var = tk.StringVar(value="0")
        ttk.Entry(qty_box, textvariable=self.decal_qty_var, width=6, justify="center").pack(side="left", padx=4)
        ttk.Button(qty_box, text=t("decal_set_btn"), style="Accent.TButton", command=self._update_current_decal_qty).pack(side="left", padx=4)
        
        d_quick = ttk.Frame(self.decal_card)
        d_quick.pack(fill="x", pady=2)
        ttk.Button(d_quick, text=t("decal_plus1"), width=3, command=lambda: self._quick_add_decal(1)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(d_quick, text=t("decal_plus5"), width=3, command=lambda: self._quick_add_decal(5)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(d_quick, text=t("decal_zero"), width=3, command=lambda: self._quick_add_decal(-999)).pack(side="left", fill="x", expand=True, padx=1)

    def _find_decal_art(self, decal_id):
        if not hasattr(self, "_decal_disk_map"):
            decals_dir = os.path.join(ICONS_DIR, "decals")
            self._decal_disk_map = {}
            if os.path.isdir(decals_dir):
                for f in os.listdir(decals_dir):
                    self._decal_disk_map[f.lower()] = f

        special_aliases = {
            "SKL_STMNUP_02": "golden_heart.png",
            "SKL_STMNUP_02_P": "golden_heart_p.png",
            "SKL_WHITEFEATHER": "skl_snowwhite.png",
            "SKL_WHITEFEATHER_P": "skl_snowwhite_p.png",
        }
        if decal_id in special_aliases:
            return f"decals/{special_aliases[decal_id]}"

        if hasattr(self, "icon_map") and "decals_icons" in self.icon_map:
            mapped = self.icon_map["decals_icons"].get(decal_id) or self.icon_map["decals_icons"].get(decal_id.replace("_P", ""))
            if mapped and self.get_photo(mapped, size=(24, 24)):
                return mapped

        is_p = decal_id.endswith("_P")
        clean = decal_id.lower().replace("skl_", "").replace("_p", "")
        
        info = self.decals_map.get(decal_id, {})
        name_en = info.get("name_en", "")
        slug = name_en.lower().replace(" ", "_").replace("-", "_").replace("'", "").replace(":", "") if name_en else ""

        exact_candidates = []
        if is_p:
            exact_candidates += [
                f"{decal_id.lower()}.png",
                f"skl_{clean}_p.png",
                f"{clean}_p.png",
            ]
            if slug:
                exact_candidates += [f"{slug}_p.png", f"skl_{slug}_p.png", f"{slug}.png"]
        else:
            exact_candidates += [
                f"{decal_id.lower()}.png",
                f"skl_{clean}.png",
                f"{clean}.png",
            ]
            if slug:
                exact_candidates += [f"{slug}.png", f"skl_{slug}.png"]

        for c in exact_candidates:
            if c in self._decal_disk_map:
                return f"decals/{self._decal_disk_map[c]}"

        for c in [f"skl_{clean}.png", f"{clean}.png"]:
            if c in self._decal_disk_map:
                return f"decals/{self._decal_disk_map[c]}"

        return "decals/decal_p.png" if is_p else "decals/decal_std.png"

    def _on_decal_select(self, event):
        sel = self.decals_tree.selection()
        if not sel:
            return
        node = sel[0]
        text = self.decals_tree.item(node, "text").strip()
        vals = self.decals_tree.item(node, "values")
        stars_str = vals[0]
        did = vals[1]
        dtype = vals[2]
        cnt_raw = str(vals[3]).replace("x", "").replace("-", "0").strip()
        cnt = int(cnt_raw) if cnt_raw.isdigit() else 0
        
        self.current_decal_selection = did
        self.decal_qty_var.set(str(cnt))
        self.decal_title_lbl.config(text=f"{text}\n({did}) • {stars_str}")
        self.decal_type_lbl.config(text=t("decal_type_and_owned", type=dtype, cnt=cnt))
        
        info = self.decals_map.get(did) or self.decals_map.get(did.replace("_P", "")) or {}
        desc = i18n.get_item_desc(info) or ("Official Combat Skill Decal" if i18n.get_language() == "en" else "Calcomanía Oficial de Combate")
        self.decal_desc_lbl.config(text=desc)
        
        art_rel = self._find_decal_art(did)
        photo = self.get_photo(art_rel, size=(160, 160), preserve_aspect=True)
        if not photo:
            photo = self.get_photo("decal_p" if did.endswith("_P") else "decal_std", size=(140, 140), preserve_aspect=True)
        self.decal_art_lbl.config(image=photo or "")
        self.tree_images["decal_preview"] = photo

    def _update_current_decal_qty(self):
        if not self.current_decal_selection or not self.save_json:
            return
        did = self.current_decal_selection
        try:
            val = int(self.decal_qty_var.get())
        except ValueError:
            val = 0
        modifiers.add_or_update_decals(self.save_json, [did], count=val, premium=did.endswith("_P"))
        self.filter_decals_list()
        self._auto_save()
        self.status_var.set(f"Cantidad de {did} actualizada a x{val} y guardada.")

    def _quick_add_decal(self, delta):
        try:
            cur = int(self.decal_qty_var.get())
        except ValueError:
            cur = 0
        self.decal_qty_var.set(str(max(0, cur + delta)))
        self._update_current_decal_qty()

    def add_meta_decals_preset(self):
        if not self.save_json:
            return
        modifiers.add_top_meta_decals(self.save_json, count=5)
        self.filter_decals_list()
        self._auto_save()
        self.status_var.set(t("mb_meta_decals_title"))
        messagebox.showinfo(t("mb_meta_decals_title"), t("mb_meta_decals_msg"))

    def unlock_all_decals_preset(self):
        if not self.save_json:
            return
        try:
            qty = int(self.decal_unlock_qty_var.get())
        except ValueError:
            qty = 3
        modifiers.unlock_all_decals(self.save_json, count=qty, premium=True)
        self.filter_decals_list()
        self._auto_save()
        self.status_var.set(f"{t('mb_all_decals_title')} (x{qty})")
        messagebox.showinfo(t("mb_all_decals_title"), t("mb_all_decals_msg", qty=qty))

    def _set_decal_event_filter(self, mode):
        self.decal_event_filter.set(mode)
        self.filter_decals_list()

    def _set_decal_style_filter(self, mode):
        self.decal_style_filter.set(mode)
        self.filter_decals_list()

    def filter_decals_list(self):
        self.decals_tree.delete(*self.decals_tree.get_children())
            
        query = self.decal_search_var.get().lower().strip() if hasattr(self, "decal_search_var") else ""
        rarity_filter = self.decal_rarity_filter_var.get() if hasattr(self, "decal_rarity_filter_var") else "Todas"
        type_filter = self.decal_type_filter_var.get() if hasattr(self, "decal_type_filter_var") else "Todas"
        poss_filter = self.decal_poss_filter_var.get() if hasattr(self, "decal_poss_filter_var") else "Todas"
        event_filter = self.decal_event_filter.get() if hasattr(self, "decal_event_filter") else "TODOS"
        style_filter = self.decal_style_filter.get() if hasattr(self, "decal_style_filter") else "TODOS"
        
        psskl_counts = {}
        if self.save_json:
            psskl_list = self.save_json.get("soul", {}).get("skl", {}).get("psskl", [])
            for item in psskl_list:
                psskl_counts[item.get("sklid", "")] = item.get("cnt", 0)
                
        first_row = None
        all_ids = set([d["id"] for d in self.decals_db]) | set(psskl_counts.keys())
        
        for did in sorted(all_ids):
            is_p = did.endswith("_P")
            cnt = psskl_counts.get(did, 0)
            info = self.decals_map.get(did) or self.decals_map.get(did.replace("_P", "")) or {}
            
            # 1. Type filter
            if "Premium" in type_filter and not is_p:
                continue
            elif ("Estándar" in type_filter or "Standard" in type_filter) and is_p:
                continue
                
            # 2. Possession filter
            if ("Poseídas" in poss_filter or "Possessed" in poss_filter) and cnt <= 0:
                continue
            elif ("Faltantes" in poss_filter or "Missing" in poss_filter) and cnt > 0:
                continue

            # 3. Rarity filter
            d_rarity = info.get("rarity", 1 if not is_p else 3)
            if rarity_filter not in ("Todas", "All"):
                try:
                    req_stars = int(rarity_filter.replace("★", "").strip())
                    if d_rarity != req_stars:
                        continue
                except ValueError:
                    pass

            name_es = info.get("name_es", did.replace("SKL_", "").replace("_", " "))
            name_en = info.get("name_en", "")
            desc_es = info.get("desc_es", "")
            desc_en = info.get("desc_en", "")
            full_txt = f"{did} {name_en} {name_es} {desc_en} {desc_es}".lower()

            # 4. Event / Collab filter
            if event_filter != "TODOS":
                if event_filter == "WOT":
                    if not any(k in full_txt for k in ["wot", "world of tanks", "tiger ii", "t-34", "sklatrol_wot"]):
                        continue
                elif event_filter == "NMH":
                    if not any(k in full_txt for k in ["travis", "sylvia", "shinobu", "bad girl", "nmh", "beam katana", "heroes"]):
                        continue
                elif event_filter == "KILLER7":
                    if not any(k in full_txt for k in ["garcian", "dan smith", "kaede", "kevin", "coyote", "mask de smith", "con smith", "killer7", "harman"]):
                        continue
                elif event_filter == "GRAVITY_RUSH":
                    if not any(k in full_txt for k in ["kat", "raven", "gravity rush", "dusty"]):
                        continue
                elif event_filter == "TENGOKU_META":
                    if not any(k in full_txt for k in ["ultimate fighter", "golden gym", "serial killer", "joker", "super heavy tank", "king of the wolves", "tengoku"]):
                        continue

            # 5. Playstyle filter
            if style_filter != "TODOS":
                if style_filter == "ADDICTS":
                    if not ("addict" in full_txt or "fanático" in full_txt or "_atkup_" in did.lower()):
                        continue
                elif style_filter == "CRIT_DMG":
                    if not any(k in full_txt for k in ["one shot one kill", "critical", "crítico", "bull", "barbarian", "clover", "five-leaf clover"]):
                        continue
                elif style_filter == "TANK_DEF":
                    if not any(k in full_txt for k in ["tank", "diamond", "poison eater", "defender", "iron wall", "gourmand"]):
                        continue
                elif style_filter == "VAMP_SURV":
                    if not any(k in full_txt for k in ["vampire", "vampiro", "super long tail", "mosquito", "golden heart", "heart"]):
                        continue
                elif style_filter == "FARM_QOL":
                    if not any(k in full_txt for k in ["treasure hunter", "marathon", "rich man", "express pass", "lucky shot", "oriental medicine"]):
                        continue
                elif style_filter == "SETS":
                    if not any(k in full_txt for k in ["cosplayer", "clay figurine", "combat diver", "happy wheeler"]):
                        continue

            # 6. Search query
            if query:
                if query not in full_txt:
                    continue
                    
            if i18n.get_language() == "en":
                display_name = f"{name_en} ({name_es})" if name_es and name_en != name_es else (name_en or name_es)
                std_txt = "STANDARD"
            else:
                display_name = f"{name_es} ({name_en})" if name_en and name_en != name_es else (name_es or name_en)
                std_txt = "ESTÁNDAR"
            stars_str = f"{d_rarity}★"
            art_rel = self._find_decal_art(did)
            thumb = self.get_photo(art_rel, size=(36, 36), preserve_aspect=True)
            node_id = self.decals_tree.insert("", "end", text=f" {display_name}", image=thumb or "", values=(stars_str, did, "PREMIUM" if is_p else std_txt, f"x{cnt}" if cnt > 0 else "-"))
            self.tree_images[node_id] = thumb
            if not first_row:
                first_row = node_id
                
        if first_row:
            self.decals_tree.selection_set(first_row)
            self._on_decal_select(None)

    def _edit_selected_decal_count(self, event):
        sel = self.decals_tree.selection()
        if not sel:
            return
        node = sel[0]
        vals = self.decals_tree.item(node, "values")
        did = vals[1]
        curr_raw = str(vals[3]).replace("x", "").replace("-", "0").strip()
        curr_cnt = int(curr_raw) if curr_raw.isdigit() else 0
        
        new_cnt = simpledialog.askinteger("Cantidad de Calcomanías", f"Ingresa la cantidad para:\n{did}\n(0 a 99):", initialvalue=curr_cnt, minvalue=0, maxvalue=99)
        if new_cnt is not None:
            modifiers.add_or_update_decals(self.save_json, [did], count=new_cnt, premium=did.endswith("_P"))
            self.filter_decals_list()
            self._auto_save()

    # ================= TAB 5: BLUEPRINTS / CHOKUFUNSHA R&D (1,370) =================
    def _get_item_wiki_meta(self, item):
        itemid = item["id"]
        raw_type = item.get("raw_type", "")
        is_en = (i18n.get_language() == "en")
        
        # 1. Slot (Wiki-style)
        if raw_type == "PTTP_HEAD" or "_HEAD_" in itemid:
            slot = "🪖 Helmet" if is_en else "🪖 Casco"
            slot_key = "head"
        elif raw_type == "PTTP_BODY" or "_TOPS_" in itemid:
            slot = "👕 Body" if is_en else "👕 Pecho"
            slot_key = "chest"
        elif raw_type in ("PTTP_PANTS", "PTTP_LEGS") or "_BTM_" in itemid:
            slot = "👖 Pants" if is_en else "👖 Piernas"
            slot_key = "legs"
        else:
            slot = "⚔️ Weapon" if is_en else "⚔️ Arma"
            slot_key = "weapon"
            
        # 2. Faction (Wiki-style)
        if "PT_DIY" in itemid:
            faction = "🔨 D.O.D. ARMS"
            faction_key = "DOD"
        elif "PT_MIL" in itemid:
            faction = "🎖️ WAR ENSEMBLE"
            faction_key = "MIL"
        elif "PT_FAN" in itemid:
            faction = "🕯️ CANDLE WOLF"
            faction_key = "FAN"
        elif "PT_SPO" in itemid:
            faction = "🥛 M.I.L.K."
            faction_key = "SPO"
        elif any(k in itemid for k in ["PT_TBR", "TENGOKU", "WHITE", "NAPALM", "THUNDER", "WIND"]):
            faction = "⚡ 4 FORCEMEN & TENGOKU"
            faction_key = "FORCEMEN"
        elif any(k in itemid for k in ["PT_JAC", "PT_JCL", "JACKAL"]):
            faction = "🕶️ JACKALS"
            faction_key = "JACKAL"
        elif "PT_REC" in itemid:
            faction = "♻️ RE (Recycler)" if is_en else "♻️ RE (Reciclador)"
            faction_key = "RE"
        elif any(k in itemid for k in ["PT_SPE", "PT_GAS"]):
            faction = "🎭 Special / Event" if is_en else "🎭 Especial / Evento"
            faction_key = "SPE"
        else:
            orig = item.get("faction", "")
            if "WAR" in orig:
                faction = "🎖️ WAR ENSEMBLE"
                faction_key = "MIL"
            elif "CANDLE" in orig:
                faction = "🕯️ CANDLE WOLF"
                faction_key = "FAN"
            elif "D.O.D" in orig:
                faction = "🔨 D.O.D. ARMS"
                faction_key = "DOD"
            elif "M.I.L.K" in orig or "MILK" in orig:
                faction = "🥛 M.I.L.K."
                faction_key = "SPO"
            else:
                faction = "⚔️ General / Other" if is_en else "⚔️ General / Otras"
                faction_key = "GEN"
                
        # 3. Set Code / Series
        clean_set = ""
        m = re.search(r"PT_([A-Z]+)_(?:HEAD|TOPS|BTM)_(\d+)", itemid)
        if m:
            clean_set = f"{m.group(1)}_{m.group(2)}"
            
        return slot, slot_key, faction, faction_key, clean_set

    def _get_weapon_damage_type(self, item):
        itemid = item["id"].lower()
        name = f"{item.get('name_en','')} {item.get('name_es','')}".lower()
        full = f"{itemid} {name}"
        
        # Elemental first
        if any(k in full for k in ["flamethrower", "fire", "fuego", "flame", "torch", "antorcha", "lanzallamas"]):
            return "FIRE"
        if any(k in full for k in ["electric", "electricidad", "static", "massager", "masajeador", "stun", "shock", "lightning", "rayo"]):
            return "ELECTRIC"
        if any(k in full for k in ["poison", "veneno", "toxin", "claw", "garra"]):
            return "POISON"
            
        # Physical
        if any(k in full for k in ["kamas", "rifle", "sniper", "francotirador", "nail", "clavos", "magnum", "pistol", "gun", "crossbow", "ballesta", "shotgun", "escopeta", "pitching", "béisbol", "bow", "arco", "rocket", "harpoon", "arpon"]):
            return "PIERCE"
        if any(k in full for k in ["machete", "sword", "espada", "katana", "cleaver", "cuchilla", "saber", "sable", "saw", "sierra", "pickaxe", "picahielo", "knife", "cuchillo", "scythe", "guadaña", "sickle", "hoz", "axe", "hacha", "dagger", "daga", "blade"]):
            return "SLASH"
        if any(k in full for k in ["hammer", "martillo", "bat", "bate", "iron", "plancha", "club", "palo", "bowling", "bolos", "flail", "mayal", "boxing", "boxeo", "wrench", "llave", "pipe", "tubo", "fist", "puño"]):
            return "BLUNT"
            
        return "OTHER"

    def _build_blueprints_tab(self):
        paned = ttk.PanedWindow(self.tab_blueprints, orient="horizontal")
        paned.pack(fill="both", expand=True)
        
        left_box = ttk.Frame(paned)
        paned.add(left_box, weight=3)
        
        # Row 1: Search + Slot + Faction
        ctrl_frame = ttk.Frame(left_box)
        ctrl_frame.pack(fill="x", pady=3)
        
        ttk.Label(ctrl_frame, text=t("bp_search")).pack(side="left", padx=2)
        self.bp_search_var = tk.StringVar()
        self.bp_search_var.trace_add("write", lambda *args: self.filter_blueprints_list())
        ttk.Entry(ctrl_frame, textvariable=self.bp_search_var, width=15).pack(side="left", padx=2)
        
        ttk.Label(ctrl_frame, text=t("bp_slot_lbl")).pack(side="left", padx=(6, 2))
        self.bp_cat_combo_var = tk.StringVar(value=t("bp_slot_all"))
        cb_bp_cat = ttk.Combobox(ctrl_frame, textvariable=self.bp_cat_combo_var, values=[t("bp_slot_all"), t("bp_slot_helmets"), t("bp_slot_bodies"), t("bp_slot_legs"), t("bp_slot_weapons")], state="readonly", width=11)
        cb_bp_cat.pack(side="left", padx=2)
        cb_bp_cat.bind("<<ComboboxSelected>>", lambda e: self.filter_blueprints_list())
        
        ttk.Label(ctrl_frame, text=t("bp_faction_lbl")).pack(side="left", padx=(6, 2))
        self.bp_faction_var = tk.StringVar(value=t("bp_fac_all"))
        factions_list = [
            t("bp_fac_all"),
            t("bp_fac_dod"),
            t("bp_fac_we"),
            t("bp_fac_cw"),
            t("bp_fac_milk"),
            t("bp_fac_44ce"),
            t("bp_fac_jackals"),
            t("bp_fac_re"),
            t("bp_fac_spe"),
            t("bp_fac_gen")
        ]
        cb_faction = ttk.Combobox(ctrl_frame, textvariable=self.bp_faction_var, values=factions_list, state="readonly", width=18)
        cb_faction.pack(side="left", padx=2)
        cb_faction.bind("<<ComboboxSelected>>", lambda e: self.filter_blueprints_list())
        
        btn_sets_viewer = ttk.Button(ctrl_frame, text=t("bp_view_sets_btn"), style="Accent.TButton", command=self._open_armor_set_viewer)
        btn_sets_viewer.pack(side="right", padx=3)
        
        # Row 2: Possession Filter + Level + Actions
        ctrl_frame2 = ttk.Frame(left_box)
        ctrl_frame2.pack(fill="x", pady=3)
        
        ttk.Label(ctrl_frame2, text=t("bp_poss_lbl")).pack(side="left", padx=2)
        self.bp_possession_filter_var = tk.StringVar(value=t("bp_poss_all"))
        poss_list = [
            t("bp_poss_all"),
            t("bp_poss_storage"),
            t("bp_poss_shop"),
            t("bp_poss_rnd"),
            t("bp_poss_locked")
        ]
        cb_poss = ttk.Combobox(ctrl_frame2, textvariable=self.bp_possession_filter_var, values=poss_list, state="readonly", width=18)
        cb_poss.pack(side="left", padx=2)
        cb_poss.bind("<<ComboboxSelected>>", lambda e: self.filter_blueprints_list())

        ttk.Label(ctrl_frame2, text=t("bp_dmg_lbl")).pack(side="left", padx=(4, 2))
        self.bp_dmg_type_var = tk.StringVar(value=t("bp_dmg_all"))
        dmg_list = [
            t("bp_dmg_all"),
            t("bp_dmg_slash"),
            t("bp_dmg_blunt"),
            t("bp_dmg_pierce"),
            t("bp_dmg_fire"),
            t("bp_dmg_elec"),
            t("bp_dmg_poison")
        ]
        cb_dmg = ttk.Combobox(ctrl_frame2, textvariable=self.bp_dmg_type_var, values=dmg_list, state="readonly", width=15)
        cb_dmg.pack(side="left", padx=2)
        cb_dmg.bind("<<ComboboxSelected>>", lambda e: self.filter_blueprints_list())
        
        ttk.Label(ctrl_frame2, text=t("bp_unlock_all_lbl")).pack(side="left", padx=(6, 2))
        self.bp_unlock_all_lvl_var = tk.StringVar(value="+19")
        cb_bp_all_lvl = ttk.Combobox(ctrl_frame2, textvariable=self.bp_unlock_all_lvl_var, values=["+19", "+24", "+4", "+3", "+2", "+1"], width=5, state="readonly")
        cb_bp_all_lvl.pack(side="left", padx=1)
        
        btn_all_bp = ttk.Button(ctrl_frame2, text=t("bp_unlock_all_btn"), style="Accent.TButton", command=self.unlock_all_blueprints_preset)
        btn_all_bp.pack(side="right", padx=2)
        
        btn_repair_bps = ttk.Button(ctrl_frame2, text=t("bp_repair_btn"), command=self._repair_blueprints_action)
        btn_repair_bps.pack(side="right", padx=2)
        
        # Row 3: Collabs & Quick Events Filter Bar
        ctrl_frame3 = ttk.Frame(left_box)
        ctrl_frame3.pack(fill="x", pady=2)
        
        ttk.Label(ctrl_frame3, text=t("bp_collabs_lbl"), font=("Segoe UI", 8, "bold"), foreground=ACCENT_GOLD).pack(side="left", padx=2)
        self.bp_collab_filter = tk.StringVar(value="TODOS")
        
        collab_buttons = [
            (t("bp_collab_all"), "TODOS"),
            ("💥 World of Tanks", "WOT"),
            ("⚔️ No More Heroes", "NMH"),
            ("🏆 TDM Seasons", "TDM"),
            (t("bp_collab_re"), "RE"),
            ("💀 4 Forcemen", "44CE")
        ]
        for btn_text, mode in collab_buttons:
            ttk.Button(ctrl_frame3, text=btn_text, command=lambda m=mode: self._set_collab_filter(m)).pack(side="left", padx=1)
        
        # Treeview with columns
        cols = ("slot", "faction", "status", "storage", "bag", "id")
        bp_tree_frame = ttk.Frame(left_box)
        bp_tree_frame.pack(fill="both", expand=True, pady=4)
        bp_scroll = ttk.Scrollbar(bp_tree_frame, orient="vertical")
        self.bp_tree = ttk.Treeview(bp_tree_frame, columns=cols, show="tree headings", height=16, yscrollcommand=bp_scroll.set)
        bp_scroll.config(command=self.bp_tree.yview)
        self.bp_tree.heading("#0", text=t("bp_col_item"))
        self.bp_tree.heading("slot", text=t("bp_col_slot"))
        self.bp_tree.heading("faction", text=t("bp_col_faction"))
        self.bp_tree.heading("status", text=t("bp_col_status"))
        self.bp_tree.heading("storage", text=t("bp_col_storage"))
        self.bp_tree.heading("bag", text=t("bp_col_bag"))
        self.bp_tree.heading("id", text=t("bp_col_id"))
        
        self.bp_tree.column("#0", width=260)
        self.bp_tree.column("slot", width=85, anchor="center")
        self.bp_tree.column("faction", width=125)
        self.bp_tree.column("status", width=110, anchor="center")
        self.bp_tree.column("storage", width=80, anchor="center")
        self.bp_tree.column("bag", width=70, anchor="center")
        self.bp_tree.column("id", width=125)
        
        bp_scroll.pack(side="right", fill="y")
        self.bp_tree.pack(side="left", fill="both", expand=True)
        self.bp_tree.bind("<<TreeviewSelect>>", self._on_bp_select)
        
        # Tags styling
        self.bp_tree.tag_configure("tag_uncapped", foreground="#ff79c6")
        self.bp_tree.tag_configure("tag_shop", foreground=ACCENT_GOLD)
        self.bp_tree.tag_configure("tag_remodel", foreground=ACCENT_BLUE)
        self.bp_tree.tag_configure("tag_locked", foreground=FG_MUTED)

        # Right Equipment Blueprint Card (Wiki Showcase)
        bp_card_container = ttk.LabelFrame(paned, text=t("bp_card_title"), padding=4)
        paned.add(bp_card_container, weight=2)
        scroll_bp = ScrollableFrame(bp_card_container)
        scroll_bp.pack(fill="both", expand=True)
        self.bp_card = scroll_bp.content
        
        self.bp_art_lbl = ttk.Label(self.bp_card)
        self.bp_art_lbl.pack(pady=4)
        
        self.bp_title_lbl = ttk.Label(self.bp_card, text=t("bp_select_prompt"), font=("Segoe UI", 12, "bold"), foreground=ACCENT_GOLD, wraplength=260, justify="center")
        self.bp_title_lbl.pack(pady=2)
        
        self.bp_faction_lbl = ttk.Label(self.bp_card, text="---", font=("Segoe UI", 9), foreground=FG_MUTED)
        self.bp_faction_lbl.pack(pady=1)
        
        self.bp_status_lbl = ttk.Label(self.bp_card, text="Estado: ---", font=("Segoe UI", 10, "bold"), foreground=ACCENT_CYAN)
        self.bp_status_lbl.pack(pady=2)
        
        self.bp_stats_lbl = ttk.Label(self.bp_card, text="Estadísticas Base: ---", font=("Segoe UI", 9), foreground=FG_MAIN, wraplength=260, justify="center")
        self.bp_stats_lbl.pack(pady=3)
        
        self.bp_set_btn = ttk.Button(self.bp_card, text=t("bp_view_set_btn"), command=self._open_selected_piece_set)
        self.bp_set_btn.pack(pady=3)
        
        # Individual Actions Box
        indiv_box = ttk.LabelFrame(self.bp_card, text=t("bp_indiv_actions_title"), padding=8)
        indiv_box.pack(fill="x", pady=4)
        
        act_r1 = ttk.Frame(indiv_box)
        act_r1.pack(fill="x", pady=2)
        ttk.Label(act_r1, text=t("bp_lvl_lbl")).pack(side="left", padx=2)
        self.bp_single_lvl_var = tk.StringVar(value="+4")
        cb_slvl = ttk.Combobox(act_r1, textvariable=self.bp_single_lvl_var, values=["+4", "+3", "+2", "+1", "+0 (Plano)", "+19", "+24"], width=9, state="readonly")
        cb_slvl.pack(side="left", padx=2)
        self.cb_single_lvl = cb_slvl
        self.btn_unlock_shop = ttk.Button(act_r1, text=t("bp_unlock_shop_btn"), style="Accent.TButton", command=self._unlock_single_bp_shop)
        self.btn_unlock_shop.pack(side="left", padx=2, fill="x", expand=True)
        
        act_r1b = ttk.Frame(indiv_box)
        act_r1b.pack(fill="x", pady=2)
        self.btn_send_rnd = ttk.Button(act_r1b, text=t("bp_send_rnd_btn"), command=self._send_single_bp_to_rnd)
        self.btn_send_rnd.pack(fill="x", expand=True)

        
        act_r2 = ttk.Frame(indiv_box)
        act_r2.pack(fill="x", pady=2)
        ttk.Button(act_r2, text=t("bp_send_storage_btn"), command=self._deliver_single_bp_to_storage).pack(side="left", padx=2, fill="x", expand=True)
        
        act_r3 = ttk.Frame(indiv_box)
        act_r3.pack(fill="x", pady=2)
        ttk.Button(act_r3, text=t("bp_deposit_kit_btn"), style="Accent.TButton", command=self._deposit_crafting_kit_for_selected_bp).pack(fill="x", expand=True)

        self.bp_evolve_lbl = ttk.Label(indiv_box, text="", font=("Segoe UI", 9, "bold"), wraplength=260, justify="center")
        self.bp_evolve_lbl.pack(fill="x", pady=(4, 2))
        
        self.btn_evolve_tier = ttk.Button(indiv_box, text=t("bp_evolve_tier_btn"), style="Accent.TButton", command=self._evolve_selected_bp_to_next_tier)

        # Endgame Sets Injector Box
        is_en = (i18n.get_language() == "en")
        endgame_box = ttk.LabelFrame(self.bp_card, text=t("bp_endgame_box_title"), padding=8)
        endgame_box.pack(fill="x", pady=4)
        
        self.endgame_set_var = tk.StringVar(value="44CE White Steel (D.O.D. Arms)")
        set_choices = [
            "44CE White Steel (D.O.D. Arms)",
            "44CE Red Napalm (War Ensemble)",
            "44CE Black Thunder (Candle Wolf)",
            "44CE Pale Wind (M.I.L.K.)",
            "Jackals Sets v1 / v2 / v3" if is_en else "Sets Jackals v1 / v2 / v3",
            "Tengoku Legendary Weapons (51F+)" if is_en else "Armas Legendarias de Tengoku (51F+)"
        ]
        cb_endgame = ttk.Combobox(endgame_box, textvariable=self.endgame_set_var, values=set_choices, state="readonly", width=28)
        cb_endgame.pack(fill="x", pady=2)
        ttk.Button(endgame_box, text=t("bp_inject_set_btn"), style="Accent.TButton", command=self._inject_endgame_set_action).pack(fill="x", pady=2)

        # Global Equipment Modifiers Box
        global_gear_box = ttk.LabelFrame(self.bp_card, text=t("bp_mass_actions_title"), padding=8)
        global_gear_box.pack(fill="x", pady=4)
        
        ttk.Button(global_gear_box, text=t("bp_inf_dur_btn"), command=self._set_infinite_durability_action).pack(fill="x", pady=2)
        ttk.Button(global_gear_box, text=t("bp_inf_ammo_btn"), command=self._set_massive_ammo_action).pack(fill="x", pady=2)
        ttk.Button(global_gear_box, text=t("bp_upg_all19_btn"), command=lambda: self._upgrade_all_gear_max_lvl_action(19)).pack(fill="x", pady=2)
        ttk.Button(global_gear_box, text=t("bp_upg_all24_btn"), command=lambda: self._upgrade_all_gear_max_lvl_action(24)).pack(fill="x", pady=2)

    def _find_equipment_art(self, ptid):
        if hasattr(self, "icon_map"):
            if "gear_icons" in self.icon_map and ptid in self.icon_map["gear_icons"]:
                return self.icon_map["gear_icons"][ptid]
            if "gear_cards" in self.icon_map and ptid in self.icon_map["gear_cards"]:
                return self.icon_map["gear_cards"][ptid]
            if "equipment_thumbs" in self.icon_map and ptid in self.icon_map["equipment_thumbs"]:
                return self.icon_map["equipment_thumbs"][ptid]
        clean = ptid.lower().replace("pt_", "").replace("_001", "").replace("_01", "")
        for folder in ["weapons", "armor", "cards", "sets", "all_official", "gear"]:
            p = os.path.join(ICONS_DIR, folder, f"{ptid.lower()}.png")
            if os.path.exists(p):
                return f"{folder}/{ptid.lower()}.png"
            p_clean = os.path.join(ICONS_DIR, folder, f"{clean}.png")
            if os.path.exists(p_clean):
                return f"{folder}/{clean}.png"
        return "weapon" if ("WP" in ptid or "ARM" in ptid) else "blueprint"

    def _on_bp_select(self, event):
        sel = self.bp_tree.selection()
        if not sel:
            return
        node = sel[0]
        full_title = self.bp_tree.item(node, "text").strip()
        vals = self.bp_tree.item(node, "values")
        slot = vals[0]
        faction = vals[1]
        status = vals[2]
        storage_str = vals[3]
        bag_str = vals[4]
        ptid = vals[5]
        
        self.current_bp_selection = ptid
        self.bp_title_lbl.config(text=f"{full_title}\n({ptid})")
        if "+19" in status or "Uncapped" in status or "Destope" in status:
            self.bp_status_lbl.config(text=t("bp_status_info", status=status, storage=storage_str, bag=bag_str), foreground="#ff79c6")
        else:
            self.bp_status_lbl.config(text=t("bp_status_info", status=status, storage=storage_str, bag=bag_str), foreground=ACCENT_CYAN)
        
        # Check if this item belongs to an armor set
        lookup_id = ptid
        if lookup_id not in self.armor_set_by_item_id and lookup_id.endswith("_G"):
            lookup_id = lookup_id[:-2]
            
        if lookup_id in self.armor_set_by_item_id:
            set_obj, tier_obj, piece_obj = self.armor_set_by_item_id[lookup_id]
            set_title = get_set_name(set_obj)
            self.bp_set_btn.config(text=f"{t('bp_view_set_btn')}: {set_title}", state="normal")
            if "def" in piece_obj:
                self.bp_stats_lbl.config(text=t("bp_base_def", def_b=piece_obj.get('def', '-'), def_4=piece_obj.get('def_plus4', '-'), dur=piece_obj.get('durability', '-')))
            elif "atk" in piece_obj:
                self.bp_stats_lbl.config(text=t("bp_base_atk", atk_b=piece_obj.get('atk', '-'), atk_4=piece_obj.get('atk_plus4', '-'), dur=piece_obj.get('durability', '-')))
            else:
                self.bp_stats_lbl.config(text=f"{t('bp_view_set_btn')}: {set_title}")
        else:
            self.bp_set_btn.config(text=t("bp_no_set"), state="disabled")
            self.bp_stats_lbl.config(text="Pieza individual de equipamiento o arma" if i18n.get_language() == "es" else "Single equipment piece or weapon")
            
        # Dynamic evolution / uncapping handling
        item_meta = next((item for item in self.equipment_db if item["id"] == ptid), None)
        can_uncap = item_meta.get("can_uncap", True) if item_meta else True
        nextptid = item_meta.get("nextptid", "") if item_meta else ""
        is_en = (i18n.get_language() == "en")
        
        if hasattr(self, "cb_single_lvl") and hasattr(self, "bp_evolve_lbl"):
            if can_uncap:
                uncap_vals = ["+19 (In R&D)", "+19 (Shop Max)", "+4", "+3", "+2", "+1", "+0 (Blueprint)"] if is_en else ["+19 (En I+D)", "+19 (Tienda Máx)", "+4", "+3", "+2", "+1", "+0 (Plano)"]
                self.cb_single_lvl.config(values=uncap_vals)
                self.bp_single_lvl_var.set("+19 (In R&D)" if is_en else "+19 (En I+D)")
                self.bp_evolve_lbl.config(
                    text="⭐ Final Tier: Ready in R&D to Uncap to +19!" if is_en else "⭐ Tier Final: ¡Listo en I+D para Destope a +19!",
                    foreground="#ff79c6"
                )
                if hasattr(self, "btn_evolve_tier"):
                    self.btn_evolve_tier.pack_forget()
            else:
                evolve_vals = ["+4 (In R&D)", "+4 (Shop Max)", "+3", "+2", "+1", "+0 (Blueprint)"] if is_en else ["+4 (En I+D)", "+4 (Tienda Máx)", "+3", "+2", "+1", "+0 (Plano)"]
                self.cb_single_lvl.config(values=evolve_vals)
                self.bp_single_lvl_var.set("+4 (In R&D)" if is_en else "+4 (En I+D)")

                nxt_meta = next((item for item in self.equipment_db if item["id"] == nextptid), None)
                nxt_name = (nxt_meta.get("name_en") if is_en else nxt_meta.get("name_es")) or nextptid
                self.bp_evolve_lbl.config(
                    text=f"🔄 Evolves at +4 to: {nxt_name}" if is_en else f"🔄 Evoluciona a Nvl +4 a: {nxt_name}",
                    foreground=ACCENT_CYAN
                )
                if hasattr(self, "btn_evolve_tier"):
                    is_nxt_uncap = nxt_meta.get("can_uncap", False) if nxt_meta else False
                    if is_nxt_uncap:
                        btn_txt = f"⚡ Desbloquear {nxt_name} (+19 en I+D)" if not is_en else f"⚡ Unlock {nxt_name} (+19 in R&D)"
                    else:
                        btn_txt = f"🔄 Evolucionar a {nxt_name} (+4)" if not is_en else f"🔄 Evolve to {nxt_name} (+4)"
                    self.btn_evolve_tier.config(text=btn_txt)
                    self.btn_evolve_tier.pack(fill="x", pady=(2, 4))
            
        card_art = None
        if hasattr(self, "icon_map") and "gear_cards" in self.icon_map:
            card_art = self.icon_map["gear_cards"].get(ptid)
        if not card_art:
            card_art = self._find_equipment_art(ptid)
            
        photo = self.get_photo(card_art, size=(280, 140), preserve_aspect=True) or \
                self.get_photo(self._find_equipment_art(ptid), size=(280, 140), preserve_aspect=True) or \
                self.get_photo("blueprint", size=(100, 100), preserve_aspect=True)
        self.bp_art_lbl.config(image=photo or "")
        self.tree_images["bp_preview"] = photo

    def _open_selected_piece_set(self):
        ptid = self.current_bp_selection
        if not ptid:
            return
        lookup_id = ptid
        if lookup_id not in self.armor_set_by_item_id and lookup_id.endswith("_G"):
            lookup_id = lookup_id[:-2]
        if lookup_id not in self.armor_set_by_item_id:
            return
        set_obj, tier_obj, piece_obj = self.armor_set_by_item_id[lookup_id]
        tier_num = tier_obj.get("tier_num", tier_obj.get("tier", 1))
        ArmorSetViewerDialog(self, self.save_json, self.armor_sets, initial_set_id=set_obj["id"], initial_tier=tier_num)

    def _open_armor_set_viewer(self):
        if not self.armor_sets:
            messagebox.showwarning(t("notice"), t("mb_armor_sets_missing"))
            return
        ArmorSetViewerDialog(self, self.save_json, self.armor_sets)

    def _open_smart_analyzer(self):
        if not self.save_json:
            messagebox.showwarning(t("notice"), t("mb_load_save_first"))
            return
        SmartInventoryAnalyzerDialog(self, self.save_json, on_modified_cb=self.refresh_all_views)

    def _open_storage_manager(self):
        if not self.save_json:
            messagebox.showwarning(t("notice"), t("mb_load_save_first"))
            return
        InventoryViewerDialog(self, self.save_json, self.equipment_db, self.materials_db, getattr(self, "shrooms_beasts_db", None))

    def _check_app_updates(self):
        updater.check_updates_background(self, silent=False)

    def _on_language_changed(self, event=None):
        val = self.lang_var.get()
        new_lang = "en" if "Eng" in val else "es"
        if new_lang != i18n.get_language():
            i18n.set_language(new_lang)
            self._refresh_all_language_texts()

    def _refresh_all_language_texts(self):
        """Dynamically re-applies all translated titles and strings across the UI and rebuilds tabs."""
        self.title(t("app_title"))
        if hasattr(self, "lbl_file"): self.lbl_file.config(text=t("save_file"))
        if hasattr(self, "browse_btn"): self.browse_btn.config(text=t("browse"))
        if hasattr(self, "reload_btn"): self.reload_btn.config(text=t("reload"))
        if hasattr(self, "backup_btn"): self.backup_btn.config(text=t("backup"))
        if hasattr(self, "btn_sets_hud"): self.btn_sets_hud.config(text=t("armor_sets"))
        if hasattr(self, "btn_rnd_hud"): self.btn_rnd_hud.config(text=t("rnd_analyzer"))
        if hasattr(self, "btn_update_hud"): self.btn_update_hud.config(text=t("updates"))
        if hasattr(self, "save_btn"): self.save_btn.config(text=t("save_game"))
        if hasattr(self, "lbl_lang"): self.lbl_lang.config(text=t("lang_label"))
        
        # Notebook Tab titles
        if hasattr(self, "notebook"):
            if hasattr(self, "tab_currencies"): self.notebook.tab(self.tab_currencies, text=t("tab_currencies"))
            if hasattr(self, "tab_fighters"): self.notebook.tab(self.tab_fighters, text=t("tab_fighters"))
            if hasattr(self, "tab_materials"): self.notebook.tab(self.tab_materials, text=t("tab_materials"))
            if hasattr(self, "tab_decals"): self.notebook.tab(self.tab_decals, text=t("tab_decals"))
            if hasattr(self, "tab_blueprints"): self.notebook.tab(self.tab_blueprints, text=t("tab_blueprints"))
            if hasattr(self, "tab_mastery"): self.notebook.tab(self.tab_mastery, text=t("tab_mastery"))
            if hasattr(self, "tab_tower"): self.notebook.tab(self.tab_tower, text=t("tab_tower"))
            if hasattr(self, "tab_advanced"): self.notebook.tab(self.tab_advanced, text=t("tab_advanced"))

        # Rebuild tab contents to instantiate translated widgets
        active_tab_idx = 0
        if hasattr(self, "notebook") and self.notebook.tabs():
            try:
                active_tab_idx = self.notebook.index(self.notebook.select())
            except Exception:
                active_tab_idx = 0

        for tab_frame in [
            getattr(self, "tab_currencies", None),
            getattr(self, "tab_fighters", None),
            getattr(self, "tab_materials", None),
            getattr(self, "tab_decals", None),
            getattr(self, "tab_blueprints", None),
            getattr(self, "tab_mastery", None),
            getattr(self, "tab_tower", None),
            getattr(self, "tab_advanced", None)
        ]:
            if tab_frame:
                for widget in tab_frame.winfo_children():
                    widget.destroy()

        if hasattr(self, "tab_currencies"): self._build_currencies_tab()
        if hasattr(self, "tab_fighters"): self._build_fighters_tab()
        if hasattr(self, "tab_materials"): self._build_materials_tab()
        if hasattr(self, "tab_decals"): self._build_decals_tab()
        if hasattr(self, "tab_blueprints"): self._build_blueprints_tab()
        if hasattr(self, "tab_mastery"): self._build_mastery_tab()
        if hasattr(self, "tab_tower"): self._build_tower_tab()
        if hasattr(self, "tab_advanced"): self._build_advanced_tab()

        if hasattr(self, "notebook") and self.notebook.tabs():
            try:
                self.notebook.select(active_tab_idx)
            except Exception:
                pass

        self.refresh_all_views()

    def _unlock_single_bp_shop(self):
        if not self.current_bp_selection or not self.save_json:
            return
        ptid = self.current_bp_selection
        val = str(self.bp_single_lvl_var.get())
        if "Tienda" in val or "Shop" in val:
            lvl = 20 if ("19" in val or "24" in val) else 5
            display_lvl = 19 if ("19" in val or "24" in val) else 4
        elif "19" in val or "24" in val:
            lvl = 19
            display_lvl = 19
        elif "4" in val:
            lvl = 4 if ("I+D" in val or "R&D" in val) else 5
            display_lvl = 4
        elif "3" in val:
            lvl = 4
            display_lvl = 3
        elif "2" in val:
            lvl = 3
            display_lvl = 2
        elif "1" in val:
            lvl = 2
            display_lvl = 1
        elif "0" in val:
            lvl = 1
            display_lvl = 0
        else:
            lvl = 19
            display_lvl = 19
        next_unlocked = modifiers.unlock_single_blueprint(self.save_json, ptid, level=lvl, unlock_next_tier=True)
        self._auto_save()
        self.filter_blueprints_list()
        
        is_en = (i18n.get_language() == "en")
        item_meta = next((item for item in self.equipment_db if item["id"] == ptid), None)
        cur_name = (item_meta.get("name_en") if is_en else item_meta.get("name_es")) if item_meta else ptid
        
        lvl_str = f"+{display_lvl} (Destope)" if display_lvl >= 19 else f"+{display_lvl}"
        lvl_str_en = f"+{display_lvl} (Uncapped)" if display_lvl >= 19 else f"+{display_lvl}"
        
        if next_unlocked:
            nxt_meta = next((item for item in self.equipment_db if item["id"] == next_unlocked), None)
            nxt_name = (nxt_meta.get("name_en") if is_en else nxt_meta.get("name_es")) if nxt_meta else next_unlocked
            self._notify(
                "Blueprint & Next Tier in R&D!", "¡Plano y Siguiente Tier en I+D!",
                f"{cur_name} registered at Level {lvl_str_en} in Chokufunsha!\n\n✨ Reached Level +4: Unlocked next tier in R&D (Development):\n🔨 {nxt_name} [{next_unlocked}]",
                f"¡{cur_name} registrado al Nivel {lvl_str} en Chokufunsha!\n\n✨ Alcanzó Nivel +4: ¡Se ha desbloqueado el siguiente tier en I+D (Desarrollo):\n🔨 {nxt_name} [{next_unlocked}]!"
            )
        else:
            self._notify(
                "Blueprint Unlocked", "Plano Desbloqueado",
                f"Blueprint {cur_name} unlocked at Level {lvl_str_en} in Chokufunsha Shop!\nSaved automatically.",
                f"¡Plano {cur_name} registrado al Nivel {lvl_str} en Chokufunsha!\nGuardado automáticamente."
            )

    def _send_single_bp_to_rnd(self):
        if not self.current_bp_selection or not self.save_json:
            return
        ptid = self.current_bp_selection
        val = str(self.bp_single_lvl_var.get())
        if "+0" in val or "Plano" in val or "Blueprint" in val:
            target_lvl = 0
        elif "+24" in val or "+19" in val:
            target_lvl = 19
        elif "+4" in val:
            target_lvl = 4
        elif "+3" in val:
            target_lvl = 3
        elif "+2" in val:
            target_lvl = 2
        elif "+1" in val:
            target_lvl = 1
        else:
            target_lvl = 0
            
        modifiers.send_blueprint_to_rnd(self.save_json, ptid, target_level=target_lvl)
        self._auto_save()
        self.filter_blueprints_list()
        
        is_en = (i18n.get_language() == "en")
        item_meta = next((item for item in self.equipment_db if item["id"] == ptid), None)
        cur_name = (item_meta.get("name_en") if is_en else item_meta.get("name_es")) if item_meta else ptid
        
        if target_lvl == 0:
            self._notify(
                "Blueprint Sent to R&D!", "¡Plano Enviado a I+D!",
                f"{cur_name} [{ptid}] is now available in Chokufunsha R&D to develop with materials!\nSaved automatically.",
                f"¡{cur_name} [{ptid}] está ahora disponible en el I+D de Chokufunsha para desarrollarlo con materiales!\nGuardado automáticamente."
            )
        else:
            prev_str = f"+{target_lvl-1} (Uncapped)" if target_lvl >= 19 else f"+{target_lvl-1}"
            next_str = f"+{target_lvl} (Uncapped)" if target_lvl >= 19 else f"+{target_lvl}"
            prev_str_es = f"+{target_lvl-1} (Destope)" if target_lvl >= 19 else f"+{target_lvl-1}"
            next_str_es = f"+{target_lvl} (Destope)" if target_lvl >= 19 else f"+{target_lvl}"
            self._notify(
                "Item Set in R&D!", "¡Objeto Configurado en I+D!",
                f"{cur_name} [{ptid}] registered at Level {prev_str}.\n\n🔨 Ready in Chokufunsha R&D to research Level {next_str}!\nSaved automatically.",
                f"¡{cur_name} [{ptid}] registrado al Nivel {prev_str_es}.\n\n🔨 ¡Listo en el I+D de Chokufunsha para investigar el Nivel {next_str_es}!\nGuardado automáticamente."
            )

    def _evolve_selected_bp_to_next_tier(self):

        if not self.current_bp_selection or not self.save_json:
            return
        ptid = self.current_bp_selection
        item_meta = next((item for item in self.equipment_db if item["id"] == ptid), None)
        if not item_meta:
            return
        nextptid = item_meta.get("nextptid", "")
        if not nextptid:
            return
            
        nxt_meta = next((item for item in self.equipment_db if item["id"] == nextptid), None)
        is_nxt_uncap = nxt_meta.get("can_uncap", False) if nxt_meta else False
        modifiers.unlock_single_blueprint(self.save_json, ptid, level=4, unlock_next_tier=True)
        if is_nxt_uncap:
            modifiers.send_blueprint_to_rnd(self.save_json, nextptid, target_level=19)
        self._auto_save()
        self.filter_blueprints_list()
        
        is_en = (i18n.get_language() == "en")
        cur_name = item_meta.get("name_en") if is_en else item_meta.get("name_es")
        nxt_name = (nxt_meta.get("name_en") if is_en else nxt_meta.get("name_es")) if nxt_meta else nextptid
        
        self._notify(
            "Tier in R&D Ready!", "¡Tier Listo en I+D!",
            f"Equipped R&D evolved from {cur_name} (+4)!\n\nSuccessfully unlocked next tier in Chokufunsha R&D:\n🔨 {nxt_name} [{nextptid}]",
            f"¡R&D evolucionado desde {cur_name} (+4)!\n\n¡Se ha desbloqueado con éxito el siguiente tier en I+D (Desarrollo) de Chokufunsha:\n🔨 {nxt_name} [{nextptid}]!"
        )


    def _deliver_single_bp_to_storage(self):
        if not self.current_bp_selection or not self.save_json:
            return
        ptid = self.current_bp_selection
        val = str(self.bp_single_lvl_var.get())
        if "24" in val or "19" in val:
            lvl = 20
            plus = 19
        elif "4" in val:
            lvl = 5
            plus = 4
        elif "3" in val:
            lvl = 4
            plus = 3
        elif "2" in val:
            lvl = 3
            plus = 2
        elif "1" in val:
            lvl = 2
            plus = 1
        elif "0" in val:
            lvl = 1
            plus = 0
        else:
            lvl = 20
            plus = 19
        modifiers.add_equipment_to_storage(self.save_json, ptid, count=1, lvl=lvl, dur=999999 if plus >= 19 else 50000)
        self._auto_save()
        self.filter_blueprints_list()
        plus_str = f"+{plus} (Destope)" if plus >= 19 else f"+{plus}"
        plus_str_en = f"+{plus} (Uncapped)" if plus >= 19 else f"+{plus}"
        self._notify(
            "Item Delivered", "Objeto Entregado",
            f"Delivered 1 unit of {ptid} ({plus_str_en}, 100% Durability) to Coin Locker!\nSaved automatically.",
            f"¡Se ha entregado 1 unidad de {ptid} ({plus_str}, 100% Durabilidad) en tu Almacén!\nGuardado automáticamente."
        )

    def _set_collab_filter(self, mode):
        if hasattr(self, "bp_collab_filter"):
            self.bp_collab_filter.set(mode)
            self.filter_blueprints_list()

    def _deposit_crafting_kit_for_selected_bp(self):
        if not self.current_bp_selection or not self.save_json:
            messagebox.showwarning(t("notice"), t("mb_select_bp_first"))
            return
        ptid = self.current_bp_selection
        
        item_meta = None
        for item in self.equipment_db:
            if item["id"] == ptid:
                item_meta = item
                break
                
        name_lbl = (item_meta.get("name_es") or item_meta.get("name_en") or ptid) if item_meta else ptid
        raw_fac = (item_meta.get("faction") or "").upper() if item_meta else ""
        
        fac_code = "DIY"
        if "WAR" in raw_fac: fac_code = "MIL"
        elif "CANDLE" in raw_fac: fac_code = "FAN"
        elif "MILK" in raw_fac or "M.I.L.K" in raw_fac: fac_code = "SPO"
        
        tier_num = 1
        m_tier = re.search(r"_0*(\d)$", ptid)
        if m_tier:
            tier_num = min(4, max(1, int(m_tier.group(1))))
        elif item_meta and item_meta.get("rarity"):
            tier_num = min(4, max(1, item_meta["rarity"]))
            
        tier_metals = {
            1: f"ITMT_STONE_{fac_code}_1",
            2: f"ITMT_STONE_{fac_code}_2",
            3: f"ITMT_STONE_{fac_code}_3",
            4: f"ITMT_STONE_{fac_code}_4",
        }
        
        tier_mats = {
            1: ["ITMT_IRON_1", "ITMT_COPPER_1", "ITMT_ALUMI_1", "ITMT_OIL_1", "ITMT_WOOD_1"],
            2: ["ITMT_IRON_2", "ITMT_COPPER_2", "ITMT_ALUMI_2", "ITMT_OIL_2", "ITMT_WOOD_2"],
            3: ["ITMT_IRON_3", "ITMT_COPPER_3", "ITMT_ALUMI_3", "ITMT_OIL_3", "ITMT_WOOD_3"],
            4: ["ITMT_IRON_4", "ITMT_COPPER_4", "ITMT_ALUMI_4", "ITMT_OIL_4", "ITMT_WOOD_4"],
        }
        
        target_mats = [tier_metals.get(tier_num, f"ITMT_STONE_{fac_code}_1")] + tier_mats.get(tier_num, tier_mats[1])
        
        for mid in target_mats:
            modifiers.add_material_to_storage(self.save_json, mid, count=10)
            
        self._auto_save()
        self.filter_materials_list()
        self.status_var.set(t("mb_craft_kit_status", tier=tier_num, name=name_lbl))
        messagebox.showinfo(t("mb_craft_kit_title"), t("mb_craft_kit_msg", tier=tier_num, name=name_lbl))

    def unlock_all_blueprints_preset(self):
        if not self.save_json:
            return
        val = str(self.bp_unlock_all_lvl_var.get())
        if "24" in val: lvl = 24
        elif "19" in val: lvl = 19
        elif "4" in val: lvl = 4
        elif "3" in val: lvl = 3
        elif "2" in val: lvl = 2
        elif "1" in val: lvl = 1
        else: lvl = 19
        modifiers.unlock_all_blueprints(self.save_json, level=lvl)
        self._auto_save()
        self.filter_blueprints_list()
        self._notify(
            "Blueprints Unlocked", "Planos Desbloqueados",
            f"All 1,370 weapon and armor blueprints unlocked at Level +{lvl} in Chokufunsha!",
            f"¡Todos los 1,370 planos de armas y armaduras han sido desbloqueados al Nivel +{lvl} en Chokufunsha!"
        )

    def _repair_blueprints_action(self):
        if not self.save_json:
            return
        fixed = modifiers.repair_unlocked_blueprints_states(self.save_json)
        self._auto_save()
        self.filter_blueprints_list()
        self._notify(
            "Blueprints Verified", "Planos Reparados",
            f"Verified and fixed {fixed} blueprints in Chokufunsha to ensure shop availability!",
            f"¡Se han reparado {fixed} planos para asegurar que estén listos para fabricar y comprar en Chokufunsha!"
        )

    def _inject_endgame_set_action(self):
        if not self.save_json:
            return
        sel = self.endgame_set_var.get()
        key = "white_steel"
        if "Red Napalm" in sel: key = "red_napalm"
        elif "Black Thunder" in sel: key = "black_thunder"
        elif "Pale Wind" in sel: key = "pale_wind"
        elif "Jackal" in sel: key = "jackals_gear"
        elif "Tengoku" in sel: key = "tengoku_weapons"
        
        name, added = modifiers.inject_endgame_set(self.save_json, set_key=key, count=1, dur=999999, lvl=20)
        self._auto_save()
        self.filter_blueprints_list()
        self.refresh_all_views()
        self._notify(
            "Endgame Set Injected", "Set Endgame Inyectado",
            f"Added {added} pieces of {name} (+19 Uncapped, 999,999 Durability) to Coin Locker & Shop!",
            f"¡Se han añadido las {added} piezas del set {name} (Nivel +19 Uncapped, Dur 999,999) a tu Almacén y Tienda!"
        )

    def _set_infinite_durability_action(self):
        if not self.save_json:
            return
        cnt = modifiers.set_infinite_durability_all_equipment(self.save_json, target_dur=999999)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Infinite Durability", "Durabilidad Infinita",
            f"Set 999,999 durability on {cnt} weapons and armors across Storage and Bags!\n\nYour equipment will never break.",
            f"¡Se ha establecido durabilidad de 999,999 en {cnt} piezas de armas y armaduras en tu Almacén y Bolsas!\n\n¡Tu equipo nunca se romperá!"
        )

    def _set_massive_ammo_action(self):
        if not self.save_json:
            return
        cnt = modifiers.set_massive_ammo_all_weapons(self.save_json, ammo=9999)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Massive Ammo", "Munición Masiva",
            f"Set 9,999 direct magazine and spare reserve ammo for {cnt} ranged firearms in Storage!",
            f"¡Se han configurado 9,999 balas directas en cargador y reserva para {cnt} armas a distancia en tu Almacén!"
        )

    def _upgrade_all_gear_max_lvl_action(self, target_lvl=19):
        if not self.save_json:
            return
        cnt = modifiers.upgrade_all_equipment_max_level(self.save_json, target_lvl=target_lvl)
        self._auto_save()
        self.filter_blueprints_list()
        self.refresh_all_views()
        is_en = (i18n.get_language() == "en")
        if target_lvl == 19:
            self._notify(
                "All Uncapped Gear in R&D (+19)!", "¡Todo el Equipo Destopado a I+D (+19)!",
                f"Updated {cnt} equipment items in Storage & Bags!\n\n🔨 ALL 377+ uncapped blueprints sent to R&D (+18 in Shop, ready to upgrade to +19)!\nSaved automatically.",
                f"¡Se han actualizado {cnt} piezas de equipo en Almacén y Bolsas!\n\n🔨 ¡Los 377+ planos destopados se enviaron a I+D (+18 en Tienda, listos para subir a +19)!\nGuardado automáticamente."
            )
        else:
            self._notify(
                "All Uncapped Gear Maxed!", "¡Todo el Equipo al Máximo Absoluto!",
                f"Updated {cnt} items! All uncapped gear set to Level +19 in Shop & Storage!\nSaved automatically.",
                f"¡Se han actualizado {cnt} piezas! ¡Todo el equipo destopado se estableció al Máximo en Tienda y Almacén!\nGuardado automáticamente."
            )

    def filter_blueprints_list(self):
        self.bp_tree.delete(*self.bp_tree.get_children())
            
        query = self.bp_search_var.get().lower().strip()
        cat_filter = self.bp_cat_combo_var.get()
        fac_filter = self.bp_faction_var.get()
        poss_filter = self.bp_possession_filter_var.get()
        
        pr_map = modifiers.get_part_research_status(self.save_json) if self.save_json else {}
        storage_gear = modifiers.get_storage_equipment_counts(self.save_json) if self.save_json else {}
        bag_gear = modifiers.get_bag_equipment_counts(self.save_json) if self.save_json else {}
        
        first_row = None
        for item in self.equipment_db:
            bp_id = item["id"]
            name_es = item.get("name_es", item.get("name", ""))
            name_en = item.get("name_en", "")
            slot, slot_key, faction, faction_key, set_code = self._get_item_wiki_meta(item)
            
            # 1. Filter by Slot
            if cat_filter not in ("Todos", "All"):
                if any(k in cat_filter for k in ("Casco", "Helmet")) and slot_key != "head": continue
                elif any(k in cat_filter for k in ("Pecho", "Body")) and slot_key != "chest": continue
                elif any(k in cat_filter for k in ("Pierna", "Leg", "Pant")) and slot_key != "legs": continue
                elif any(k in cat_filter for k in ("Arma", "Weapon")) and slot_key != "weapon": continue
                
            # 2. Filter by Faction
            if fac_filter not in ("Todas", "All"):
                f_target_key = None
                if "D.O.D" in fac_filter: f_target_key = "DOD"
                elif "WAR" in fac_filter: f_target_key = "MIL"
                elif "CANDLE" in fac_filter: f_target_key = "FAN"
                elif "M.I.L.K" in fac_filter or "MILK" in fac_filter: f_target_key = "SPO"
                elif "FORCEMEN" in fac_filter or "TENGOKU" in fac_filter: f_target_key = "FORCEMEN"
                elif "JACKAL" in fac_filter: f_target_key = "JACKAL"
                elif "RE" in fac_filter: f_target_key = "RE"
                elif "Especial" in fac_filter or "Special" in fac_filter: f_target_key = "SPE"
                elif "General" in fac_filter or "Other" in fac_filter or "Otras" in fac_filter: f_target_key = "GEN"
                
                if f_target_key and faction_key != f_target_key:
                    continue
                elif not f_target_key and faction != fac_filter:
                    continue
                
            # 3. Forge status
            is_en = (i18n.get_language() == "en")
            if bp_id in pr_map:
                forge_info = pr_map[bp_id]
                forge_code = forge_info["status"]
                lvl_val = forge_info.get("lvl", 20)
                plus_lvl = lvl_val - 1 if lvl_val > 1 else lvl_val
                if is_en:
                    if forge_code == "STORE_UNCAPPED": forge_status = f"⭐ In Shop (+{plus_lvl} Uncapped)"
                    elif forge_code == "RND_UNCAPPED": forge_status = f"🔨 In R&D (+{plus_lvl} → +{plus_lvl+1})"
                    elif forge_code == "STORE_PLUS4": forge_status = "⭐ In Shop (+4)"
                    elif forge_code == "STORE": forge_status = f"🛒 In Shop (+{forge_info.get('level', 1)})"
                    elif forge_code == "FINISHED_LVL": forge_status = f"🔨 In R&D (+{plus_lvl} → +{plus_lvl+1})"
                    elif forge_code == "REMODEL": forge_status = "🔨 In R&D (Evolution +0)"
                    elif forge_code == "MAP": forge_status = "📜 In R&D (Blueprint +0)"
                    else: forge_status = forge_info.get("label", forge_code)
                else:
                    if forge_code == "STORE_UNCAPPED": forge_status = f"⭐ Tienda (+{plus_lvl} Destope)"
                    elif forge_code == "RND_UNCAPPED": forge_status = f"🔨 En I+D (+{plus_lvl} → +{plus_lvl+1})"
                    else: forge_status = forge_info["label"]

            else:
                forge_status = "❌ Locked" if is_en else "❌ Bloqueado"
                forge_code = "LOCKED"
                
            storage_count = storage_gear.get(bp_id, 0)
            bag_count = bag_gear.get(bp_id, 0)
            
            # 4. Filter by Possession
            if ("Almacén" in poss_filter or "Storage" in poss_filter) and storage_count <= 0:
                continue
            elif ("Desbloqueados" in poss_filter or "Unlocked" in poss_filter) and forge_code not in ("STORE_PLUS4", "STORE_UNCAPPED", "RND_UNCAPPED"):
                continue
            elif ("I+D" in poss_filter or "R&D" in poss_filter) and forge_code not in ("REMODEL", "MAP", "FINISHED_LVL", "RND_UNCAPPED"):
                continue
            elif ("Bloqueados" in poss_filter or "Locked" in poss_filter) and forge_code != "LOCKED":

                continue

            # 4b. Filter by Damage Type (Weapons only)
            dmg_filter = self.bp_dmg_type_var.get() if hasattr(self, "bp_dmg_type_var") else "Todos"
            if dmg_filter not in ("Todos", "All"):
                if slot_key != "weapon":
                    continue
                w_dmg = self._get_weapon_damage_type(item)
                if ("Corte" in dmg_filter or "Slash" in dmg_filter) and w_dmg != "SLASH": continue
                elif ("Golpe" in dmg_filter or "Blunt" in dmg_filter) and w_dmg != "BLUNT": continue
                elif ("Perforación" in dmg_filter or "Pierce" in dmg_filter) and w_dmg != "PIERCE": continue
                elif ("Fuego" in dmg_filter or "Fire" in dmg_filter) and w_dmg != "FIRE": continue
                elif ("Electricidad" in dmg_filter or "Electric" in dmg_filter) and w_dmg != "ELECTRIC": continue
                elif ("Veneno" in dmg_filter or "Poison" in dmg_filter) and w_dmg != "POISON": continue
                
            # 5. Search query (matches name_es, name_en, bp_id, or set_code)
            if query:
                if (query not in bp_id.lower() and 
                    query not in name_es.lower() and 
                    query not in name_en.lower() and
                    query not in set_code.lower()):
                    continue
                    
            # 6. Collab / Event Filter
            collab = self.bp_collab_filter.get() if hasattr(self, "bp_collab_filter") else "TODOS"
            if collab != "TODOS":
                n_en = (name_en or "").lower()
                n_es = (name_es or "").lower()
                b_id = bp_id.lower()
                if collab == "WOT" and "wot" not in n_en and "world of tanks" not in n_en:
                    continue
                elif collab == "NMH" and "beam" not in n_en and "travis" not in n_en and "heroes" not in n_en:
                    continue
                elif collab == "TDM" and "tdm" not in n_en and "_0a" not in b_id:
                    continue
                elif collab == "RE" and " re" not in n_en and "_0b" not in b_id:
                    continue
                elif collab == "44CE" and not any(k in n_en or k in n_es for k in ["white steel", "red napalm", "black thunder", "pale wind", "m2g"]):
                    continue
                    
            if is_en:
                display_title = f"{name_en} ({name_es})" if name_es and name_en != name_es else (name_en or name_es)
            else:
                display_title = f"{name_es} ({name_en})" if name_en and name_en != name_es else (name_es or name_en)
            storage_str = f"{storage_count} pcs." if is_en and storage_count > 0 else (f"{storage_count} u." if storage_count > 0 else "-")
            bag_str = f"{bag_count} pcs." if is_en and bag_count > 0 else (f"{bag_count} u." if bag_count > 0 else "-")
            
            if forge_code in ("STORE_UNCAPPED", "RND_UNCAPPED"):
                tag = "tag_uncapped"
            elif forge_code == "STORE_PLUS4":
                tag = "tag_shop"
            elif forge_code in ("REMODEL", "MAP", "FINISHED_LVL"):
                tag = "tag_remodel"
            else:
                tag = "tag_locked"
            
            art_rel = self._find_equipment_art(bp_id)
            thumb = self.get_photo(art_rel, size=(36, 36), preserve_aspect=True)
            node_id = self.bp_tree.insert(
                "",
                "end",
                text=f" {display_title}",
                image=thumb or "",
                values=(slot, faction, forge_status, storage_str, bag_str, bp_id),
                tags=(tag,)
            )
            self.tree_images[node_id] = thumb
            if not first_row:
                first_row = node_id
                
        if first_row:
            self.bp_tree.selection_set(first_row)
            self._on_bp_select(None)

    # ================= TAB 6: WEAPON MASTERY =================
    def _build_mastery_tab(self):
        top_ctrl = ttk.Frame(self.tab_mastery)
        top_ctrl.pack(fill="x", pady=6)
        
        ttk.Label(top_ctrl, text=t("wm_target_lvl_lbl")).pack(side="left", padx=4)
        self.mastery_target_lvl_var = tk.StringVar(value="20")
        cb_m_lvl = ttk.Combobox(top_ctrl, textvariable=self.mastery_target_lvl_var, values=[str(i) for i in range(1, 21)], width=4, state="readonly")
        cb_m_lvl.pack(side="left", padx=2)
        
        btn_max_m = ttk.Button(top_ctrl, text=t("wm_set_all_btn"), style="Accent.TButton", command=self.max_all_mastery)
        btn_max_m.pack(side="left", padx=6)
        
        m_tree_frame = ttk.Frame(self.tab_mastery)
        m_tree_frame.pack(fill="both", expand=True, pady=4)
        m_scroll = ttk.Scrollbar(m_tree_frame, orient="vertical")
        self.mastery_tree = ttk.Treeview(m_tree_frame, columns=("id", "lvl", "points"), show="tree headings", height=15, yscrollcommand=m_scroll.set)
        m_scroll.config(command=self.mastery_tree.yview)
        self.mastery_tree.heading("#0", text=t("wm_col_type"))
        self.mastery_tree.heading("id", text=t("wm_col_code"))
        self.mastery_tree.heading("lvl", text=t("wm_col_lvl"))
        self.mastery_tree.heading("points", text=t("wm_col_exp"))
        
        self.mastery_tree.column("#0", width=260)
        self.mastery_tree.column("id", width=140)
        self.mastery_tree.column("lvl", width=140, anchor="center")
        self.mastery_tree.column("points", width=180, anchor="center")
        
        m_scroll.pack(side="right", fill="y")
        self.mastery_tree.pack(side="left", fill="both", expand=True)
        self.mastery_tree.bind("<Double-1>", self._edit_mastery_level)

    def filter_mastery_list(self):
        self.mastery_tree.delete(*self.mastery_tree.get_children())
            
        if not self.save_json:
            return
            
        expert_list = self.save_json.get("soul", {}).get("expert", [])
        
        for item in expert_list:
            k = item.get("ptarmtp", "PTARMTP_00")
            lvl = item.get("lvl", 1)
            pts = item.get("abp", 0)
            
            w_name = get_expert_weapon_name(k)
            ico_file = WEAPON_MASTERY_ICONS.get(k, "weapon")
            thumb = self.get_photo(ico_file, (28, 28), preserve_aspect=True) or self.get_photo("weapon", (24, 24))
            lvl_str = t("wm_lvl_val", lvl=lvl)
            node_id = self.mastery_tree.insert("", "end", text=f" {w_name}", image=thumb or "", values=(k, lvl_str, f"{pts:,} ABP"))
            self.tree_images[node_id] = thumb

    def _edit_mastery_level(self, event):
        sel = self.mastery_tree.selection()
        if not sel:
            return
        node = sel[0]
        vals = self.mastery_tree.item(node, "values")
        arm_type = vals[0]
        
        is_en = i18n.get_language() == "en"
        title = "Weapon Mastery Level" if is_en else "Nivel de Maestría"
        prompt = f"Enter level for {arm_type} (1 to 20):" if is_en else f"Ingresa el nivel para {arm_type} (1 a 20):"
        new_lvl = simpledialog.askinteger(title, prompt, minvalue=1, maxvalue=20, initialvalue=20)
        if new_lvl is not None:
            modifiers.set_weapon_mastery(self.save_json, arm_type, level=new_lvl)
            self._auto_save()
            self.filter_mastery_list()
            self._notify(
                "Mastery Updated", "Maestría Actualizada",
                f"Mastery for {arm_type} set to Level {new_lvl}!\nSaved automatically.",
                f"¡Maestría de {arm_type} establecida al Nivel {new_lvl}!\nGuardado automáticamente."
            )

    def max_all_mastery(self):
        if not self.save_json:
            return
        try:
            lvl = int(self.mastery_target_lvl_var.get())
        except ValueError:
            lvl = 20
        modifiers.max_all_weapon_mastery(self.save_json, level=lvl)
        self._auto_save()
        self.filter_mastery_list()
        self._notify(
            "Masteries Maximized", "Maestrías Maximizadas",
            f"All 57 weapon masteries set to Level {lvl}!\nSaved automatically.",
            f"¡Todas las 57 maestrías de armas han sido establecidas al Nivel {lvl}!\nGuardado automáticamente."
        )

    # ================= TAB 7: TOWER & MASTER UNLOCKS =================
    def _build_tower_tab(self):
        self.tab_tower.columnconfigure(0, weight=1, uniform="tab7")
        self.tab_tower.columnconfigure(1, weight=1, uniform="tab7")
        self.tab_tower.rowconfigure(0, weight=1)
        self.tab_tower.rowconfigure(1, weight=1)
        
        # Left Panel: Tower, Elevators & Stamps
        box_left = ttk.LabelFrame(self.tab_tower, text=t("tw_left_title"), padding=12)
        box_left.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        
        # 1. Elevators & Map Discovery
        ttk.Label(box_left, text="🗺️ " + t("tw_elev_title", "Ascensores y Mapa Completo"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        ttk.Label(box_left, text=t("tw_elev_sub", "Desbloquea los 61 ascensores, 980 habitaciones, 1,119 escaleras y 122 puertas de la Torre."), font=("Segoe UI", 8), foreground=FG_MUTED).pack(anchor="w", pady=1)
        btn_unlock_elevators = ttk.Button(box_left, text=t("tw_elev_btn", "🗺️ Desbloquear Ascensores y Mapa"), style="Accent.TButton", command=self._unlock_elevators_action)
        btn_unlock_elevators.pack(fill="x", pady=(2, 6))

        # Emergency Rescue
        btn_rescue = ttk.Button(box_left, text="🚨 " + t("tw_rescue_btn", "Rescate a Sala de Espera (Fix Carga)"), command=self._rescue_stuck_fighter_action)
        btn_rescue.pack(fill="x", pady=(0, 8))
        
        # 2. Stamp Rally Perfect
        ttk.Label(box_left, text=t("tw_stamp_title"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        ttk.Label(box_left, text=t("tw_stamp_sub"), font=("Segoe UI", 8), foreground=FG_MUTED).pack(anchor="w", pady=1)
        btn_stamps_perfect = ttk.Button(box_left, text=t("tw_stamp_btn"), style="Accent.TButton", command=self._set_stamps_perfect_action)
        btn_stamps_perfect.pack(fill="x", pady=(2, 8))
        
        # 3. Tower Secret Shop Utilities
        ttk.Separator(box_left, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(box_left, text=t("tw_shop_title"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        btn_reset_shop = ttk.Button(box_left, text=t("tw_shop_btn"), command=self._reset_wandering_shop_action)
        btn_reset_shop.pack(fill="x", pady=2)

        # Right Panel: TDM & Encyclopedia Books
        box_right = ttk.LabelFrame(self.tab_tower, text=t("tw_right_title"), padding=12)
        box_right.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        
        # 4. TDM Rank & Points
        ttk.Label(box_right, text=t("tw_tdm_title"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        tdm_f = ttk.Frame(box_right)
        tdm_f.pack(fill="x", pady=2)
        ttk.Label(tdm_f, text=t("tw_rank_lbl")).pack(side="left", padx=2)
        is_en = i18n.get_language() == "en"
        self.tdm_rank_var = tk.StringVar(value="Diamond I (3,500+ pts)" if is_en else "Diamante I (3,500+ pts)")
        tdm_ranks = [
            "Diamond I (3,500+ pts)" if is_en else "Diamante I (3,500+ pts)",
            "Diamond II (3,200 pts)" if is_en else "Diamante II (3,200 pts)",
            "Diamond III (3,000 pts)" if is_en else "Diamante III (3,000 pts)",
            "Platinum I (2,500 pts)" if is_en else "Platino I (2,500 pts)",
            "Gold I (1,800 pts)" if is_en else "Oro I (1,800 pts)",
            "Silver I (1,200 pts)" if is_en else "Plata I (1,200 pts)",
            "Bronze I (500 pts)" if is_en else "Bronce I (500 pts)"
        ]
        cb_tdm = ttk.Combobox(tdm_f, textvariable=self.tdm_rank_var, values=tdm_ranks, state="readonly", width=26)
        cb_tdm.pack(side="left", padx=2)
        btn_set_tdm = ttk.Button(tdm_f, text=t("tw_apply_btn"), style="Accent.TButton", command=self._set_tdm_rank_action)
        btn_set_tdm.pack(side="left", padx=2)

        # 5. Compendiums & Hub Customization
        ttk.Separator(box_right, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(box_right, text=t("tw_comp_title"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        btn_comp = ttk.Button(box_right, text=t("tw_comp_mats_btn"), style="Accent.TButton", command=self._complete_compendiums_action)
        btn_comp.pack(fill="x", pady=2)
        btn_hub = ttk.Button(box_right, text=t("tw_comp_room_btn"), command=self._unlock_hub_action)
        btn_hub.pack(fill="x", pady=2)
        btn_quests = ttk.Button(box_right, text=t("tw_comp_quests_btn"), style="Accent.TButton", command=self._complete_all_quests_action)
        btn_quests.pack(fill="x", pady=2)
        btn_media = ttk.Button(box_right, text=t("tw_comp_mags_btn"), command=self._unlock_magazines_and_radio_action)
        btn_media.pack(fill="x", pady=2)
        btn_rescue = ttk.Button(box_right, text="🚨 Rescatar Luchador (Fix Carga)" if not is_en else "🚨 Rescue Fighter (Fix Loading)", command=self._rescue_stuck_fighter_action)
        btn_rescue.pack(fill="x", pady=2)

        # Row 1 (Bottom Full-Width): Tower Exploration Records & Combat Stats
        box_playlog = ttk.LabelFrame(self.tab_tower, text=t("tw_playlog_title"), padding=12)
        box_playlog.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)
        
        pl_grid = ttk.Frame(box_playlog)
        pl_grid.pack(fill="both", expand=True)
        pl_grid.columnconfigure(0, weight=1)
        pl_grid.columnconfigure(1, weight=1)
        
        # Left Playlog Actions
        pl_acts = ttk.Frame(pl_grid)
        pl_acts.grid(row=0, column=0, sticky="nsew", padx=8, pady=4)
        
        # Max Floor
        r_fl = ttk.Frame(pl_acts)
        r_fl.pack(fill="x", pady=4)
        ttk.Label(r_fl, text=t("tw_max_floor_lbl"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(side="left", padx=2)
        self.max_floor_var = tk.StringVar(value="40")
        ttk.Entry(r_fl, textvariable=self.max_floor_var, width=8, justify="center").pack(side="left", padx=6)
        btn_set_fl = ttk.Button(r_fl, text=t("tw_set_floor_btn"), style="Accent.TButton", command=self._set_max_floor_action)
        btn_set_fl.pack(side="left", padx=2)
        
        # Disconnections & Penalties Reset
        r_int = ttk.Frame(pl_acts)
        r_int.pack(fill="x", pady=6)
        ttk.Label(r_int, text=t("tw_interrupt_lbl"), font=("Segoe UI", 9)).pack(side="left", padx=2)
        self.interrupt_lbl = ttk.Label(r_int, text="0 penalizaciones", font=("Segoe UI", 9, "bold"), foreground=ACCENT_CYAN)
        self.interrupt_lbl.pack(side="left", padx=6)
        btn_reset_int = ttk.Button(r_int, text=t("tw_reset_interrupt_btn"), command=self._reset_interrupt_action)
        btn_reset_int.pack(side="left", padx=2)
        
        # Right Playlog Stats Display
        pl_stats = ttk.Frame(pl_grid)
        pl_stats.grid(row=0, column=1, sticky="nsew", padx=8, pady=4)
        
        ttk.Label(pl_stats, text=t("tw_stats_title"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=(0, 4))
        
        st_f = ttk.Frame(pl_stats)
        st_f.pack(fill="x")
        st_f.columnconfigure(0, weight=1)
        st_f.columnconfigure(1, weight=1)
        
        self.pl_elev_lbl = ttk.Label(st_f, text="🛗 Ascensores: 0", font=("Segoe UI", 9))
        self.pl_elev_lbl.grid(row=0, column=0, sticky="w", pady=2)
        self.pl_esc_lbl = ttk.Label(st_f, text="🪜 Escaleras: 0", font=("Segoe UI", 9))
        self.pl_esc_lbl.grid(row=0, column=1, sticky="w", pady=2)
        
        self.pl_mats_lbl = ttk.Label(st_f, text="📦 Materiales: 0", font=("Segoe UI", 9))
        self.pl_mats_lbl.grid(row=1, column=0, sticky="w", pady=2)
        self.pl_res_lbl = ttk.Label(st_f, text="🔬 Investigaciones: 0", font=("Segoe UI", 9))
        self.pl_res_lbl.grid(row=1, column=1, sticky="w", pady=2)
        
        self.pl_boss_lbl = ttk.Label(st_f, text="💀 Jefes Vencidos: 0", font=("Segoe UI", 9))
        self.pl_boss_lbl.grid(row=2, column=0, sticky="w", pady=2)
        self.pl_time_lbl = ttk.Label(st_f, text="⏱️ Horas Torre: 0.0 hrs", font=("Segoe UI", 9))
        self.pl_time_lbl.grid(row=2, column=1, sticky="w", pady=2)

    def _complete_all_quests_action(self):
        if not self.save_json:
            return
        cnt = modifiers.complete_all_quests(self.save_json)
        self._auto_save()
        self._notify(
            "Quests Completed", "Misiones Completadas",
            f"Marked {cnt} official quests as completed!\n\nYou can claim hundreds of Death Metals, rare metals, and blueprints from your Rewards Box.",
            f"¡Se han marcado como completadas {cnt} misiones oficiales de la Torre de Barbs!\n\nPuedes recoger cientos de Death Metals, metales raros y planos en tu Buzón de Recompensas."
        )

    def _unlock_magazines_and_radio_action(self):
        if not self.save_json:
            return
        modifiers.unlock_all_magazines(self.save_json)
        modifiers.unlock_all_radio_music(self.save_json)
        self._auto_save()
        self._notify(
            "Collectibles Unlocked", "Coleccionables Desbloqueados",
            "All 36 magazines and Uncle Death comics unlocked! Radio Jukebox enabled with all channels.",
            "¡Se han desbloqueado las 36 revistas y cómics del Tío Death y se ha habilitado la Gramola de Radio con todos los canales!"
        )

    def _rescue_stuck_fighter_action(self):
        if not self.save_json:
            return
        modifiers.reset_floor_to_waiting_room(self.save_json)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Fighter Rescued", "Luchador Rescatado",
            "Fighter safely extracted back to the Waiting Room!\n\nAny stuck floor loading transitions or escalator deadlocks have been cleared.",
            "¡Luchador extraído de forma segura de vuelta a la Sala de Espera!\n\nSe han resuelto los bloqueos de pantalla de carga y transiciones de escalera atascadas."
        )

    def _unlock_elevators_action(self):
        if not self.save_json:
            return
        modifiers.unlock_all_elevators(self.save_json)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Tower & Elevators Fully Unlocked", "Torre y Ascensores Desbloqueados",
            "Full access enabled to all 61 Tower elevators (Floors 1-40, 41-50, and Tengoku 51+)!\n\nAll 980 tower rooms & 1,119 escalators revealed on the Map, 122 gates opened, and Floor 41+ Waiting Room gate unlocked!",
            "¡Acceso completo a los 61 ascensores de la Torre (pisos 1 al 40, 41-50 y Tengoku 51+)!\n\n¡Los 980 cuartos y 1,119 escaleras han sido revelados en el Mapa, 122 puertas desbloqueadas y el portal a Pisos 41+ habilitado en la Sala de Espera!"
        )

    def _set_stamps_perfect_action(self):
        if not self.save_json:
            return
        modifiers.set_all_stamps_perfect(self.save_json)
        self._auto_save()
        self._notify(
            "Stamps in PERFECT", "Sellos en PERFECT",
            "All 40 Stamp Rally stamps marked as PERFECT!\n\nUncle Death Scythe unlocked at Chokufunsha +4 and 1 copy delivered to Storage.",
            "¡Todos los 40 sellos del Stamp Rally marcados en PERFECT!\n\nGuadaña del Tío Death desbloqueada al Nivel +4 en Chokufunsha y 1 unidad entregada en tu Almacén."
        )

    def _set_max_floor_action(self):
        if not self.save_json:
            return
        try:
            fl = int(self.max_floor_var.get())
        except ValueError:
            fl = 40
        modifiers.set_tower_max_floor(self.save_json, max_floor=fl)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Tower Record", "Récord de Torre",
            f"Tower record max floor set to Floor {fl} successfully!",
            f"¡Piso máximo alcanzado establecido al Piso {fl} con éxito!"
        )

    def _reset_interrupt_action(self):
        if not self.save_json:
            return
        old = modifiers.reset_tower_interruptions(self.save_json)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Penalties Cleared", "Penalizaciones Limpiadas",
            f"Cleared {old:,} tower disconnections and penalty counters!\n\nYour fighters are completely protected from disconnections and forced rescue fees.",
            f"¡Se han eliminado {old:,} interrupciones y cierres de la torre!\n\nTus luchadores están completamente protegidos de penalizaciones por desconexión."
        )

    def _expand_bag_action(self):
        if not self.save_json:
            return
        try:
            slots = int(self.bag_slots_var.get())
        except ValueError:
            slots = 50
        modifiers.expand_death_bag(self.save_json, fighter_index=self.current_fighter_idx, slots=slots)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Death Bag Expanded", "Bolsa Expandida",
            f"Current fighter death bag expanded to {slots} slots!",
            f"¡Bolsa del luchador actual ampliada a {slots} casillas!"
        )

    def _set_continues_action(self):
        if not self.save_json:
            return
        try:
            cnt = int(self.free_cont_var.get())
        except ValueError:
            cnt = 999
        modifiers.set_free_continues(self.save_json, count=cnt)
        self._auto_save()
        self._notify(
            "Free Continues", "Continues Establecidos",
            f"Granted {cnt} unlimited free revives directly in the Tower!",
            f"¡Se han otorgado {cnt} revives gratuitos ilimitados en la torre!"
        )

    def _set_tdm_rank_action(self):
        if not self.save_json:
            return
        sel = self.tdm_rank_var.get()
        rank_id = "TDM_RANK_05_03"
        points = 5000
        if any(k in sel for k in ("Diamante II", "Diamond II")): rank_id, points = "TDM_RANK_05_02", 3200
        elif any(k in sel for k in ("Diamante III", "Diamond III")): rank_id, points = "TDM_RANK_05_01", 3000
        elif any(k in sel for k in ("Platino", "Platinum")): rank_id, points = "TDM_RANK_04_03", 2500
        elif any(k in sel for k in ("Oro", "Gold")): rank_id, points = "TDM_RANK_03_03", 1800
        elif any(k in sel for k in ("Plata", "Silver")): rank_id, points = "TDM_RANK_02_03", 1200
        elif any(k in sel for k in ("Bronce", "Bronze")): rank_id, points = "TDM_RANK_01_03", 500
        
        modifiers.set_tdm_rank(self.save_json, rank_id=rank_id, points=points)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "TDM Rank Updated", "Rango TDM Actualizado",
            f"Tokyo Death Metro rank set to {sel} with {points:,} points!",
            f"¡Rango de Tokyo Death Metro establecido a {sel} con {points:,} puntos!"
        )

    def _complete_compendiums_action(self):
        if not self.save_json:
            return
        m_cnt, b_cnt = modifiers.complete_encyclopedia_books(self.save_json)
        self._auto_save()
        self._notify(
            "Compendiums Completed", "Compendios Completados",
            f"All {m_cnt} Mushrooms and {b_cnt} Beasts registered in Uncle Death's Book!\n\nMarked as discovered, eaten, thrown, and cooked.",
            f"¡Se han registrado al 100% las {m_cnt} Setas y {b_cnt} Bestias en el Libro del Tío Death!\n\nMarcadas como descubiertas, comidas, lanzadas y cocinadas."
        )

    def _unlock_hub_action(self):
        if not self.save_json:
            return
        total, unlocked = modifiers.unlock_all_hub_customizations(self.save_json)
        self._auto_save()
        self._notify(
            "Waiting Room Unlocked", "Sala de Espera Desbloqueada",
            f"All {total} Waiting Room themes, floors, and decorations unlocked ({unlocked} newly enabled)!",
            f"¡Se han desbloqueado todas las {total} personalizaciones oficiales de la Sala de Espera ({unlocked} activadas)!"
        )

    def _reset_wandering_shop_action(self):
        if not self.save_json:
            return
        modifiers.reset_wandering_shop_timer(self.save_json)
        self._auto_save()
        self._notify(
            "Secret Shop Reset", "Tienda Reseteada",
            "Chokufunsha wandering shop timer reset! Gyaku-Funsha is ready to trade on designated floors.",
            "¡Se ha reseteado el temporizador de Chokufunsha ambulante!\n\nGyaku-Funsha aparecerá inmediatamente en sus pisos designados."
        )

    # ================= TAB 8: ADVANCED & BACKUPS =================
    def _build_advanced_tab(self):
        self.tab_advanced.columnconfigure(0, weight=1)
        self.tab_advanced.columnconfigure(1, weight=1)
        
        # Left: Backup Manager
        box_bak = ttk.LabelFrame(self.tab_advanced, text=t("bak_title"), padding=12)
        box_bak.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        
        bak_tree_frame = ttk.Frame(box_bak)
        bak_tree_frame.pack(fill="both", expand=True, pady=4)
        bak_scroll = ttk.Scrollbar(bak_tree_frame, orient="vertical")
        self.backups_tree = ttk.Treeview(bak_tree_frame, columns=("date", "size"), show="tree headings", height=12, yscrollcommand=bak_scroll.set)
        bak_scroll.config(command=self.backups_tree.yview)
        self.backups_tree.heading("#0", text=t("bak_col_file"))
        self.backups_tree.heading("date", text=t("bak_col_date"))
        self.backups_tree.heading("size", text=t("bak_col_size"))
        
        self.backups_tree.column("#0", width=220)
        self.backups_tree.column("date", width=140, anchor="center")
        self.backups_tree.column("size", width=80, anchor="center")
        
        bak_scroll.pack(side="right", fill="y")
        self.backups_tree.pack(side="left", fill="both", expand=True)
        
        btn_f = ttk.Frame(box_bak)
        btn_f.pack(fill="x", pady=4)
        ttk.Button(btn_f, text=t("bak_create_btn"), style="Accent.TButton", command=self.create_manual_backup).pack(side="left", padx=2, fill="x", expand=True)
        ttk.Button(btn_f, text=t("bak_restore_btn"), command=self._restore_selected_backup).pack(side="left", padx=2, fill="x", expand=True)
        
        # Right: JSON Tools & Wiki Links
        box_tools = ttk.LabelFrame(self.tab_advanced, text=t("bak_tools_title"), padding=12)
        box_tools.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        
        ttk.Label(box_tools, text=t("bak_json_lbl"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        json_f = ttk.Frame(box_tools)
        json_f.pack(fill="x", pady=4)
        ttk.Button(json_f, text=t("bak_export_json"), command=self.export_json).pack(side="left", padx=2, fill="x", expand=True)
        ttk.Button(json_f, text=t("bak_import_json"), command=self.import_json).pack(side="left", padx=2, fill="x", expand=True)
        
        ttk.Separator(box_tools, orient="horizontal").pack(fill="x", pady=10)
        ttk.Label(box_tools, text=t("bak_links_lbl"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        ttk.Label(box_tools, text=t("bak_links_txt"), font=("Segoe UI", 8), foreground=FG_MUTED).pack(anchor="w", pady=2)

    def refresh_backups_list(self):
        self.backups_tree.delete(*self.backups_tree.get_children())
            
        if not self.save_path:
            return
            
        save_dir = os.path.dirname(self.save_path)
        base_name = os.path.basename(self.save_path)
        
        found_backups = {}
        for bdir in [save_dir, save_io.PROJECT_BACKUPS_DIR]:
            if os.path.isdir(bdir):
                for f in os.listdir(bdir):
                    if f.startswith(base_name) and f.endswith(".bak"):
                        fp = os.path.join(bdir, f)
                        if f not in found_backups:
                            st = os.stat(fp)
                            found_backups[f] = (fp, st.st_size, st.st_mtime)
                            
        for f, (fp, sz, mt) in sorted(found_backups.items(), key=lambda x: x[1][2], reverse=True):
            mtime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mt))
            thumb = self.get_photo("reversal_metal", (20, 20))
            node_id = self.backups_tree.insert("", "end", text=f" {f}", image=thumb or "", values=(mtime_str, f"{sz // 1024} KB"))
            self.tree_images[node_id] = thumb

    def _restore_selected_backup(self):
        sel = self.backups_tree.selection()
        if not sel:
            messagebox.showwarning(t("notice"), t("mb_select_backup_restore"))
            return
        node = sel[0]
        bak_name = self.backups_tree.item(node, "text").strip()
        
        # Check both directories
        save_dir = os.path.dirname(self.save_path)
        bak_path = os.path.join(save_dir, bak_name)
        if not os.path.exists(bak_path):
            bak_path = os.path.join(save_io.PROJECT_BACKUPS_DIR, bak_name)
            
        if not os.path.exists(bak_path):
            messagebox.showerror(t("error"), t("mb_backup_not_found", name=bak_name))
            return
        
        if messagebox.askyesno(t("mb_confirm_restore_title"), t("mb_confirm_restore_msg", name=bak_name)):
            try:
                save_io.restore_backup(bak_path, self.save_path)
                self.load_save(self.save_path)
                messagebox.showinfo(t("mb_restore_success_title"), t("mb_restore_success_msg"))
            except Exception as e:
                messagebox.showerror(t("error"), t("mb_restore_error", err=e))

    # ================= GENERAL APP LOGIC =================
    def browse_save(self):
        f = filedialog.askopenfilename(
            title="Seleccionar archivo de guardado de LET IT DIE" if i18n.get_language() == "es" else "Select LET IT DIE save file",
            filetypes=[("LET IT DIE Save", "*.sav"), ("All files", "*.*")],
            initialdir=os.path.dirname(self.save_path) if self.save_path else None
        )
        if f:
            self.save_path = f
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, f)
            self.load_save(f)

    def load_save(self, path):
        if not os.path.exists(path):
            messagebox.showerror(t("error"), t("mb_file_not_found", path=path))
            return
        try:
            data, ver = decompress_save(path)
            self.save_json = data
            self.version = ver
            self.save_path = path
            self.refresh_all_views()
            self.status_var.set(f"Save loaded: {os.path.basename(path)}" if i18n.get_language() == "en" else f"Partida cargada con éxito: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror(t("error"), t("mb_decompress_error", err=e))

    def refresh_all_views(self):
        if not self.save_json:
            return
            
        # 1. Update HUD & Currencies
        curr = modifiers.get_player_currencies(self.save_json)
        dm = curr.get("dm", 0)
        kc = curr.get("kc", 0)
        spl = curr.get("spl", 0)
        bl = curr.get("bloodnium", 0)
        re_pt = curr.get("re_points", 0)
        
        self.hud_dm_lbl.config(text=f"💎 {dm:,} DM")
        self.hud_kc_lbl.config(text=f"🪙 {kc:,} KC")
        self.hud_spl_lbl.config(text=f"⚡ {spl:,} SPL")
        self.hud_bl_lbl.config(text=f"🩸 {bl:,} BL")
        self.hud_re_lbl.config(text=f"♻️ {re_pt:,} RE")
        
        pr_map = modifiers.get_part_research_status(self.save_json) if self.save_json else {}
        unlocked_bps = sum(1 for v in pr_map.values() if v.get("status") in ("STORE_PLUS4", "REMODEL", "MAP"))
        total_bps = len(self.equipment_db) if self.equipment_db else 1370
        pct_bps = (unlocked_bps / total_bps * 100) if total_bps else 0
        if hasattr(self, "hud_bp_lbl"):
            self.hud_bp_lbl.config(text=f"📋 {unlocked_bps}/{total_bps} ({pct_bps:.0f}%)")
        
        if hasattr(self, "dm_var"): self.dm_var.set(str(dm))
        if hasattr(self, "kc_var"): self.kc_var.set(str(kc))
        if hasattr(self, "spl_var"): self.spl_var.set(str(spl))
        if hasattr(self, "bl_var"): self.bl_var.set(str(bl))
        if hasattr(self, "re_var"): self.re_var.set(str(re_pt))
        
        # Base Upgrades
        base_up = modifiers.get_waiting_room_info(self.save_json)
        if hasattr(self, "safe_lvl_var"): self.safe_lvl_var.set(str(base_up.get("bank_level", 10)))
        if hasattr(self, "tank_lvl_var"): self.tank_lvl_var.set(str(base_up.get("tank_level", 10)))
        if hasattr(self, "rank_var"): self.rank_var.set(str(base_up.get("rank", 100)))
        
        # VIP Status
        vip_info = modifiers.get_vip_status(self.save_json)
        if hasattr(self, "vip_status_lbl"):
            if vip_info.get("active"):
                self.vip_status_lbl.config(text=t("vip_active", days=vip_info.get('days_left', 0), date=vip_info.get('expires_at', '')), foreground=ACCENT_GREEN)
            else:
                self.vip_status_lbl.config(text=t("vip_inactive"), foreground=ACCENT_RED)
            
        # Account Metadata & Login Streak (Tab 1)
        is_en = (i18n.get_language() == "en")
        acct = modifiers.get_account_overview(self.save_json)
        if hasattr(self, "acct_uid_lbl"):
            self.acct_uid_lbl.config(text=f"UID: {acct.get('uid', '---')} | Steam ID: {acct.get('steam_id', '---')}")
        if hasattr(self, "acct_streak_lbl"):
            self.acct_streak_lbl.config(text=f"🔥 Login Streak: {acct.get('login_streak', 1)} days" if is_en else f"🔥 Racha Login: {acct.get('login_streak', 1)} días")
        
        # Tower Playlog & Records (Tab 1 & Tab 7)
        pl = modifiers.get_tower_playlog(self.save_json)
        if hasattr(self, "acct_playtime_lbl"):
            self.acct_playtime_lbl.config(text=f"⏱️ Playtime: {pl.get('playtime_hours', 0.0)} hrs" if is_en else f"⏱️ Horas Jugadas: {pl.get('playtime_hours', 0.0)} hrs")
        if hasattr(self, "max_floor_var"):
            self.max_floor_var.set(str(pl.get("max_floor", 40)))
        if hasattr(self, "interrupt_lbl"):
            self.interrupt_lbl.config(text=f"{pl.get('interruptions', 0):,} penalties" if is_en else f"{pl.get('interruptions', 0):,} penalizaciones")
        if hasattr(self, "pl_elev_lbl"):
            self.pl_elev_lbl.config(text=f"🛗 Elevators: {pl.get('elevators', 0):,}" if is_en else f"🛗 Ascensores: {pl.get('elevators', 0):,}")
        if hasattr(self, "pl_esc_lbl"):
            self.pl_esc_lbl.config(text=f"🪜 Escalators: {pl.get('escalators', 0):,}" if is_en else f"🪜 Escaleras: {pl.get('escalators', 0):,}")
        if hasattr(self, "pl_mats_lbl"):
            self.pl_mats_lbl.config(text=f"📦 Materials: {pl.get('materials_collected', 0):,}" if is_en else f"📦 Materiales: {pl.get('materials_collected', 0):,}")
        if hasattr(self, "pl_res_lbl"):
            self.pl_res_lbl.config(text=f"🔬 Researches: {pl.get('researches', 0):,}" if is_en else f"🔬 Investigaciones: {pl.get('researches', 0):,}")
        if hasattr(self, "pl_boss_lbl"):
            self.pl_boss_lbl.config(text=f"💀 Bosses Defeated: {pl.get('boss_kills', 0):,}" if is_en else f"💀 Jefes Vencidos: {pl.get('boss_kills', 0):,}")
        if hasattr(self, "pl_time_lbl"):
            self.pl_time_lbl.config(text=f"⏱️ Tower Hours: {pl.get('playtime_hours', 0.0)} hrs" if is_en else f"⏱️ Horas Torre: {pl.get('playtime_hours', 0.0)} hrs")
        
        # 2. Update Fighters List (1:1 with in-game Fighter Freezer)
        self.fighters_tree.delete(*self.fighters_tree.get_children())
            
        all_fighters = modifiers.get_all_fighters_info(self.save_json)
        total_f = len(all_fighters)
        self._tree_node_to_save_idx = {}
        self._tree_node_to_tree_idx = {}
        first_f = None
        for idx in range(total_f):
            f = all_fighters[idx]
            slot_num = idx + 1
            name = f.get("name", f"Luchador #{slot_num}")
            cls_name = f.get("class_name", "All-Rounder")
            lvl = f.get("level", 1)
            grade = f.get("grade", 1)
            hp = f.get("hp", 1000)
            state = t("f_state_alive") if hp > 0 else t("f_state_dead")
            lvl_str = f"Lv. {lvl} (G{grade})" if i18n.get_language() == "en" else f"Nv. {lvl} (G{grade})"
            
            cls_code = f.get("class", "BAL")
            cls_icon_filename = FIGHTER_CLASSES.get(cls_code, ("", "all-rounder.png"))[1]
            thumb = self.get_photo(cls_icon_filename, (36, 36), preserve_aspect=True) or self.get_photo("all-rounder", (36, 36), preserve_aspect=True)
            node_id = self.fighters_tree.insert("", "end", text=f" {name} ({cls_name})", image=thumb or "", values=(slot_num, lvl_str, state))
            self.tree_images[node_id] = thumb
            self._tree_node_to_save_idx[node_id] = idx
            self._tree_node_to_tree_idx[node_id] = idx
            if idx == 0:
                first_f = node_id
                
        cur_t_idx = getattr(self, "current_fighter_tree_idx", 0)
        children = self.fighters_tree.get_children()
        if children:
            target_node = children[cur_t_idx] if 0 <= cur_t_idx < len(children) else children[0]
            self.fighters_tree.selection_set(target_node)
            self.fighters_tree.see(target_node)
            self._on_fighter_select(None)
            
        # Active Fighter Info on top HUD
        if all_fighters:
            f0 = next((f for f in all_fighters if f.get("state") == "USE"), all_fighters[0])
            f_prefix = t("hud_fighter")
            r_prefix = t("hud_rank")

            tdm_txt = t("hud_tdm")

            b_prefix = t("hud_bag")
            s_suffix = t("hud_slots")
            self.player_name_lbl.config(text=f"{f_prefix} {f0.get('name', 'Principal')} • {f0.get('class_name', 'All-Rounder')} (Tier {f0.get('grade', 1)} ★)")
            self.player_meta_lbl.config(text=f"UID: {self.save_json.get('soul', {}).get('uid', '---')} | {r_prefix} {base_up.get('rank', 100)} | {tdm_txt} | {b_prefix} {f0.get('bag', 20)} {s_suffix}")
            
        # 3. Filter other lists
        self.filter_materials_list()
        self.filter_decals_list()
        self.filter_blueprints_list()
        self.filter_mastery_list()
        self.refresh_backups_list()
        
        # Storage Capacity gauge in Materials tab
        if hasattr(self, "mat_cap_indicator_lbl"):
            st_info = modifiers.analyze_storage_stock(self.save_json)
            cap = st_info.get("capacity", 2000)
            used = st_info.get("total_items", 0)
            self.mat_cap_indicator_lbl.config(text=t("mat_locker_status", used=used, cap=cap, free=cap - used))

    def create_manual_backup(self):
        if not self.save_path or not os.path.exists(self.save_path):
            messagebox.showwarning(t("notice"), t("mb_no_save_backup"))
            return
        bak_file = save_io.create_backup(self.save_path)
        self.refresh_backups_list()
        self.status_var.set(f"{t('mb_backup_created_title')}: {os.path.basename(bak_file)}")
        messagebox.showinfo(t("mb_backup_created_title"), t("mb_backup_created_msg", file=bak_file))

    def save_current(self):
        if not self.save_json or not self.save_path:
            self._notify("Warning", "Aviso", "No save file loaded to save.", "No hay ninguna partida cargada para guardar.", kind="warning")
            return
        try:
            # Sync currencies from entries
            if hasattr(self, "dm_var"):
                modifiers.set_currencies(
                    self.save_json,
                    dm=int(self.dm_var.get()),
                    kc=int(self.kc_var.get()),
                    spl=int(self.spl_var.get()),
                    bloodnium=int(self.bl_var.get()),
                    re_points=int(self.re_var.get())
                )
            save_io.save_to_file(self.save_json, self.save_path, version=self.version)
            self._notify(
                "Save Successful", "Guardado Exitoso",
                f"Game save successfully re-encrypted and sealed!\n\nAll changes applied to {os.path.basename(self.save_path)}.",
                f"¡Partida guardada y re-encriptada con éxito!\n\nTodos los cambios están aplicados en {os.path.basename(self.save_path)}."
            )
        except PermissionError:
            is_en = i18n.get_language() == "en"
            t_title = "Admin Elevation Required" if is_en else "Permisos de Administrador Requeridos"
            t_msg = (
                "Permission Denied (Error 13).\n\n"
                "The game save file is protected by Windows or Steam folder permissions.\n"
                "Would you like to restart the editor with Administrator privileges to save?"
            ) if is_en else (
                "Permiso Denegado (Error 13).\n\n"
                "El archivo de guardado está protegido por permisos de Windows o Steam.\n"
                "¿Deseas reiniciar el editor con permisos de Administrador para guardar?"
            )
            if messagebox.askyesno(t_title, t_msg):
                import ctypes
                try:
                    target_arg = f'"{self.save_path}"' if self.save_path else ""
                    if getattr(sys, 'frozen', False):
                        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, target_arg, None, 1)
                    else:
                        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}" {target_arg}', None, 1)
                    self.destroy()
                    sys.exit(0)
                except Exception as ex:
                    messagebox.showerror(t("error"), str(ex))
        except Exception as e:
            self._notify("Error Saving", "Error al Guardar", f"Could not save game file:\n{e}", f"No se pudo guardar la partida:\n{e}", kind="error")

    def export_json(self):
        if not self.save_json:
            messagebox.showwarning(t("notice"), t("mb_load_save_first"))
            return
        out_p = os.path.join(BASE_DIR, "save_decompressed.json")
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(self.save_json, f, indent=2, ensure_ascii=False)
        self.status_var.set(t("mb_export_json_success", path=out_p))
        messagebox.showinfo(t("notice"), t("mb_export_json_success", path=out_p))

    def import_json(self):
        in_p = os.path.join(BASE_DIR, "save_decompressed.json")
        if not os.path.exists(in_p):
            messagebox.showerror(t("error"), t("mb_file_not_found", path=in_p))
            return
        try:
            with open(in_p, "r", encoding="utf-8") as f:
                self.save_json = json.load(f)
            self.refresh_all_views()
            self._auto_save()
            self.status_var.set(t("mb_import_json_success"))
            messagebox.showinfo(t("notice"), t("mb_import_json_success"))
        except Exception as e:
            messagebox.showerror(t("error"), t("mb_import_json_error", err=e))


if __name__ == "__main__":
    app = CompleteSaveEditorGUI()
    app.mainloop()
