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

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "icons")
ICON_ICO_PATH = os.path.join(ICONS_DIR, "app_icon.ico")
ICON_PNG_PATH = os.path.join(ICONS_DIR, "app_icon.png")
ICON_MAP_PATH = os.path.join(BASE_DIR, "icon_map.json")
MATERIALS_DB_PATH = os.path.join(BASE_DIR, "all_materials_db.json")
EQUIPMENT_DB_PATH = os.path.join(BASE_DIR, "all_equipment_encyclopedia.json")
DECALS_DB_PATH = os.path.join(BASE_DIR, "all_decals_encyclopedia.json")
ARMOR_SETS_PATH = os.path.join(BASE_DIR, "armor_sets_encyclopedia.json")

# Premium Cyberpunk Dark Theme Color Palette
BG_DARK = "#0d0f17"        # Ultra deep dark space background
BG_PANEL = "#151824"       # Clean dark slate panel
BG_CARD = "#1c2030"        # Elevated card surface
BG_CARD_LIGHT = "#252b40"  # Highlighted card surface
BG_CARD_HOVER = "#2f3650"  # Interactive hover
FG_MAIN = "#f0f2f5"        # Crisp white text
FG_MUTED = "#9aa0b4"       # Subtle soft secondary text
ACCENT_GOLD = "#f5b041"    # Royal gold accent
ACCENT_CYAN = "#00e5ff"    # Bright cyber cyan
ACCENT_BLUE = "#3498db"    # Clean sky blue
ACCENT_GREEN = "#2ecc71"   # Success emerald
ACCENT_RED = "#e74c3c"     # Danger crimson
ACCENT_PURPLE = "#bb86fc"  # Cyberpunk neon purple
ACCENT_PINK = "#ff4081"    # Death Metal vibrant magenta

from game_data import SPECIAL_MUSHROOMS, SPECIAL_BEASTS, WEAPON_CATEGORIES, FIGHTER_CLASSES
WEAPON_MASTERY_ICONS = {wt: img for wt, nm, img in WEAPON_CATEGORIES}

EXPERT_WEAPON_NAMES = {
    "PTARMTP_00": "Manos Desnudas / Fists",
    "PTARMTP_01": "Machete / Machete (DOD ARMS)",
    "PTARMTP_02": "Martillo / Hammer (DOD ARMS)",
    "PTARMTP_03": "Plancha / Iron (DOD ARMS)",
    "PTARMTP_04": "Pistola de Clavos / Nail Gun (DOD ARMS)",
    "PTARMTP_05": "Sierra Circular / Buzzsaw (DOD ARMS)",
    "PTARMTP_06": "Picahielo / Pickaxe (DOD ARMS)",
    "PTARMTP_07": "Palo de Golf / Golf Club (WAR ENSEMBLE)",
    "PTARMTP_08": "Cuchillo de Caza / Hunting Knife (WAR ENSEMBLE)",
    "PTARMTP_09": "Hacha de Batalla / Battle Axe (CANDLE WOLF)",
    "PTARMTP_10": "Espada Larga / Longsword (CANDLE WOLF)",
    "PTARMTP_11": "Maza de Guerra / Flail (CANDLE WOLF)",
    "PTARMTP_12": "Cuchillo Arrojadizo / Shuriken",
    "PTARMTP_13": "Lanza / Spear (CANDLE WOLF)",
    "PTARMTP_14": "Vara de Trueno / Thunder Rod (CANDLE WOLF)",
    "PTARMTP_15": "Guantelete / Claws (WAR ENSEMBLE)",
    "PTARMTP_16": "Pistola Magnum / Magnum (WAR ENSEMBLE)",
    "PTARMTP_17": "Fusil de Asalto KAMAS / Assault Rifle (WAR ENSEMBLE)",
    "PTARMTP_18": "Escopeta / Shotgun (WAR ENSEMBLE)",
    "PTARMTP_19": "Fusil Francotirador / Sniper Rifle (WAR ENSEMBLE)",
    "PTARMTP_20": "Lanzacohetes / Rocket Launcher (WAR ENSEMBLE)",
    "PTARMTP_21": "Fuegos Artificiales / Fireworks (DOD ARMS)",
    "PTARMTP_22": "Motosierra / Chainsaw (DOD ARMS)",
    "PTARMTP_23": "Motor Psycho / Motor Psycho (WAR ENSEMBLE)",
    "PTARMTP_24": "Taladro / Drill Arm (DOD ARMS)",
    "PTARMTP_25": "Katana Masamune / Katana (CANDLE WOLF)",
    "PTARMTP_26": "Bate de Béisbol / Baseball Bat (M.I.L.K.)",
    "PTARMTP_27": "Palo de Hockey / Hockey Stick (M.I.L.K.)",
    "PTARMTP_28": "Bolas de Bolos / Bowling Ball (M.I.L.K.)",
    "PTARMTP_29": "Estatua Shishimai / Shishimai",
    "PTARMTP_30": "Espada Cortante / Cleaver Saber (WAR ENSEMBLE)",
    "PTARMTP_31": "Lanzallamas / Flamethrower (DOD ARMS)",
    "PTARMTP_32": "Arma Taser / Taser Gun (DOD ARMS)",
    "PTARMTP_33": "Pala / Shovel (DOD ARMS)",
    "PTARMTP_34": "Pistola de Dardos / Crossbow (CANDLE WOLF)",
    "PTARMTP_35": "Lanza de Dragón / Dragon Buster (CANDLE WOLF)",
    "PTARMTP_36": "Vara Eléctrica / Stun Rod (M.I.L.K.)",
    "PTARMTP_37": "Palo de Madera / Timber (DOD ARMS)",
    "PTARMTP_38": "Bate de Pitching / Pitching Machine (M.I.L.K.)",
    "PTARMTP_39": "Guantelete de Boxeo / Boxing Glove (M.I.L.K.)",
    "PTARMTP_40": "Maza de Clavos / Spiked Bat (M.I.L.K.)",
    "PTARMTP_41": "Espada Láser / Beam Katana (NO MORE HEROES)",
    "PTARMTP_42": "Pistola de Bengala / Flare Gun (WAR ENSEMBLE)",
    "PTARMTP_43": "Espadón / Greatsword (CANDLE WOLF)",
    "PTARMTP_44": "Yo-yo de Combate / Yo-yo (DOD ARMS)",
    "PTARMTP_45": "Látigo / Whip (M.I.L.K.)",
    "PTARMTP_46": "Maza Pesada / Heavy Mace (TENGOKU)",
    "PTARMTP_47": "Cuchillo Mariposa / Butterfly Knife",
    "PTARMTP_48": "Nunchaku / Nunchaku (WAR ENSEMBLE)",
    "PTARMTP_50": "Pistola de Plasma / Plasma Pistol (TENGOKU)",
    "PTARMTP_51": "Espada Electromagnética / EMP Saber (TENGOKU)",
    "PTARMTP_52": "Lanzador EMP / EMP Launcher (TENGOKU)",
    "PTARMTP_53": "Fusil Láser TDM / Laser Rifle TDM",
    "PTARMTP_54": "Maza Pesada TDM / Heavy Mace TDM",
    "PTARMTP_55": "Masajeador TDM / Massager (44CE White Steel)",
    "PTARMTP_56": "Lanzador de Púas / Spike Launcher (44CE Red Napalm)",
    "PTARMTP_57": "Espada de Energía / Energy Sword (44CE Black Thunder)",
    "PTARMTP_58": "Pistola de Veneno / Poison Gun (44CE Pale Wind)",
    "PTARMTP_59": "Esquís de Combate / Ski Blades (TENGOKU)",
    "PTARMTP_62": "Arma Jackal X / Jackal X Blaster",
    "PTARMTP_63": "Arma Jackal Y / Jackal Y Saber",
    "PTARMTP_64": "Arma Jackal Z / Jackal Z Yo-yo"
}

class CompleteSaveEditorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LET IT DIE (Offline) - Deep Save Editor Pro v3.5 (Master Cyberpunk Edition)")
        self.geometry("1280x920")
        self.minsize(1080, 760)
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

    def get_photo(self, rel_path, size=(28, 28), preserve_aspect=False):
        if not rel_path:
            return None
        key = (rel_path, size, preserve_aspect)
        if key in self.img_cache:
            return self.img_cache[key]
            
        clean_rel = str(rel_path).replace("\\", "/")
        subdirs = ["", "cards", "sets", "all_official", "armor", "weapons", "materials", "decals", "shrooms", "gear", "thumbs"]
        found_path = None
        
        # 1. Direct path or subdirs with common extensions
        extensions = ["", ".png", ".jpg", ".jpeg", ".webp"]
        for sub in subdirs:
            for ext in extensions:
                p = os.path.join(ICONS_DIR, sub, clean_rel + ext)
                if os.path.exists(p) and not os.path.isdir(p):
                    found_path = p
                    break
            if found_path:
                break
                
        # 2. Check icon_map if available
        if not found_path and hasattr(self, "icon_map"):
            mapped = self.icon_map.get("gear_icons", {}).get(clean_rel) or \
                     self.icon_map.get("gear_cards", {}).get(clean_rel) or \
                     self.icon_map.get("materials_cards", {}).get(clean_rel) or \
                     self.icon_map.get("materials_thumbs", {}).get(clean_rel) or \
                     self.icon_map.get("decals_icons", {}).get(clean_rel) or \
                     self.icon_map.get("equipment_thumbs", {}).get(clean_rel)
            if mapped:
                mapped_clean = mapped.replace("\\", "/")
                for sub in subdirs:
                    for ext in extensions:
                        p = os.path.join(ICONS_DIR, sub, mapped_clean + ext)
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

    def _build_ui(self):
        # 1. Top Cyberpunk Save File & Action Bar
        top_frame = tk.Frame(self, bg=BG_PANEL, padx=14, pady=8)
        top_frame.pack(fill="x", padx=10, pady=(6, 2))
        
        lbl_file = tk.Label(top_frame, text="PARTIDA (.sav):", font=("Segoe UI", 9, "bold"), fg=ACCENT_GOLD, bg=BG_PANEL)
        lbl_file.pack(side="left", padx=(0, 8))
        
        self.path_entry = ttk.Entry(top_frame)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        if self.save_path:
            self.path_entry.insert(0, self.save_path)
            
        browse_btn = ttk.Button(top_frame, text="📁 Examinar...", command=self.browse_save)
        browse_btn.pack(side="left", padx=2)
        
        reload_btn = ttk.Button(top_frame, text="🔄 Recargar", command=lambda: self.load_save(self.path_entry.get()))
        reload_btn.pack(side="left", padx=2)
        
        backup_btn = ttk.Button(top_frame, text="🛡️ Backup", command=self.create_manual_backup)
        backup_btn.pack(side="left", padx=2)
        
        btn_sets_hud = ttk.Button(top_frame, text="👘 Sets de Armadura", style="Accent.TButton", command=self._open_armor_set_viewer)
        btn_sets_hud.pack(side="left", padx=(6, 2))
        
        btn_rnd_hud = ttk.Button(top_frame, text="🧠 Analizador I+D", command=self._open_smart_analyzer)
        btn_rnd_hud.pack(side="left", padx=2)
        
        btn_update_hud = ttk.Button(top_frame, text="⚡ Actualizaciones", command=self._check_app_updates)
        btn_update_hud.pack(side="left", padx=2)
        
        save_btn = ttk.Button(top_frame, text="💾 GUARDAR PARTIDA", style="Accent.TButton", command=self.save_current)
        save_btn.pack(side="left", padx=(8, 0))

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
        self.notebook.add(self.tab_currencies, text=" Monedas y VIP ", image=self.get_photo("dm", (18, 18)) or "", compound="left")
        self._build_currencies_tab()
        
        # TAB 2: FIGHTERS
        self.tab_fighters = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_fighters, text=" Luchadores (Congelador) ", image=self.get_photo("all-rounder", (18, 18)) or "", compound="left")
        self._build_fighters_tab()
        
        # TAB 3: MATERIALS
        self.tab_materials = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_materials, text=" Materiales y Forja (106) ", image=self.get_photo("special_steel", (18, 18)) or "", compound="left")
        self._build_materials_tab()
        
        # TAB 4: DECALS
        self.tab_decals = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_decals, text=" Calcomanías (626) ", image=self.get_photo("decal_p", (18, 18)) or "", compound="left")
        self._build_decals_tab()
        
        # TAB 5: BLUEPRINTS
        self.tab_blueprints = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_blueprints, text=" Planos Chokufunsha (1,370) ", image=self.get_photo("blueprint", (18, 18)) or "", compound="left")
        self._build_blueprints_tab()
        
        # TAB 6: MASTERY
        self.tab_mastery = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_mastery, text=" Maestría de Armas ", image=self.get_photo("weapon", (18, 18)) or "", compound="left")
        self._build_mastery_tab()
        
        # TAB 7: TOWER & MASTER UNLOCKS
        self.tab_tower = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_tower, text=" Desbloqueos Maestros y Torre ", image=self.get_photo("re_point", (18, 18)) or "", compound="left")
        self._build_tower_tab()
        
        # TAB 8: ENCYCLOPEDIA & ADVANCED
        self.tab_advanced = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_advanced, text=" Enciclopedia y Respaldos ", image=self.get_photo("reversal_metal", (18, 18)) or "", compound="left")
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
        
        # Card 1 (Top-Left): Currencies
        box_curr = ttk.LabelFrame(self.tab_currencies, text="💰 Recursos y Divisas Principales", padding=12)
        box_curr.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        
        entries = [
            ("Metales de Muerte (DM):", "dm_var", "dm"),
            ("Monedas Kill Coins (KC):", "kc_var", "kc"),
            ("Litio SPLithium (SPL):", "spl_var", "spl"),
            ("Sangrenio (Bloodnium):", "bl_var", "bloodnium"),
            ("Puntos de Reciclaje (RE):", "re_var", "re_point"),
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
            
        btn_max_all = ttk.Button(box_curr, text="⭐ MAXIMIZAR TODAS LAS DIVISAS AL TOPE", style="Accent.TButton", command=self.max_all_currencies)
        btn_max_all.pack(fill="x", pady=(10, 2))

        # Card 2 (Top-Right): Waiting Room Upgrades
        box_wr = ttk.LabelFrame(self.tab_currencies, text="🏦 Mejoras de Instalaciones de la Sala de Espera", padding=12)
        box_wr.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        
        upgrades = [
            ("Nivel del Banco de KC (1-10):", "safe_lvl_var"),
            ("Nivel del Tanque de SPL (1-10):", "tank_lvl_var"),
            ("Rango de Jugador (1-100):", "rank_var"),
        ]
        for lbl_t, var_n in upgrades:
            r = ttk.Frame(box_wr)
            r.pack(fill="x", pady=5)
            ttk.Label(r, text=lbl_t, font=("Segoe UI", 9)).pack(side="left")
            v = tk.StringVar(value="10")
            setattr(self, var_n, v)
            ttk.Entry(r, textvariable=v, width=8, justify="center").pack(side="right")
            
        btn_max_base = ttk.Button(box_wr, text="🏦 Maximizar Banco y Tanque (Nivel 10)", command=self._max_waiting_room_facilities)
        btn_max_base.pack(fill="x", pady=(18, 2))

        # Card 3 (Bottom-Left): VIP Royal Express
        box_vip = ttk.LabelFrame(self.tab_currencies, text="👑 Pase Expreso Royal VIP", padding=12)
        box_vip.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        
        self.vip_status_lbl = ttk.Label(box_vip, text="Estado: Inactivo", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD)
        self.vip_status_lbl.pack(anchor="w", pady=(0, 4))
        
        vip_f = ttk.Frame(box_vip)
        vip_f.pack(fill="x", pady=4)
        ttk.Label(vip_f, text="Días de Pase VIP:").pack(side="left", padx=2)
        self.vip_days_var = tk.StringVar(value="30")
        ttk.Entry(vip_f, textvariable=self.vip_days_var, width=8, justify="center").pack(side="left", padx=4)
        ttk.Button(vip_f, text="👑 Activar VIP", style="Accent.TButton", command=self._activate_custom_vip).pack(side="left", padx=4)
        
        vip_quick = ttk.Frame(box_vip)
        vip_quick.pack(fill="x", pady=4)
        ttk.Button(vip_quick, text="30 Días", command=lambda: self._set_vip_entry_and_act(30)).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(vip_quick, text="90 Días", command=lambda: self._set_vip_entry_and_act(90)).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(vip_quick, text="1 Año", command=lambda: self._set_vip_entry_and_act(365)).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(vip_quick, text="10 Años", command=lambda: self._set_vip_entry_and_act(3650)).pack(side="left", fill="x", expand=True, padx=2)

        # Card 4 (Bottom-Right): TDM Mystery Bags
        box_mb = ttk.LabelFrame(self.tab_currencies, text="🌈 Bolsas Misteriosas TDM (Mystery Bags)", padding=12)
        box_mb.grid(row=1, column=1, sticky="nsew", padx=6, pady=6)
        
        self.mystery_status_lbl = ttk.Label(box_mb, text="🌈 Arcoíris: 0 | ⚪ Platino: 0 | 🟡 Oro: 0 | 🔘 Plata: 0 | 🟤 Cobre: 0", font=("Segoe UI", 9))
        self.mystery_status_lbl.pack(anchor="w", pady=(0, 4))
        
        mb_f = ttk.Frame(box_mb)
        mb_f.pack(fill="x", pady=4)
        ttk.Label(mb_f, text="Rareza:").pack(side="left", padx=2)
        self.mystery_type_var = tk.StringVar(value="RAINBOW")
        cb_mtype = ttk.Combobox(mb_f, textvariable=self.mystery_type_var, values=["RAINBOW", "PLATINUM", "GOLD", "SILVER", "COPPER", "TODAS"], width=10, state="readonly")
        cb_mtype.pack(side="left", padx=2)
        
        ttk.Label(mb_f, text="Cant:").pack(side="left", padx=2)
        self.mystery_qty_var = tk.StringVar(value="10")
        ttk.Entry(mb_f, textvariable=self.mystery_qty_var, width=5, justify="center").pack(side="left", padx=2)
        ttk.Button(mb_f, text="➕ Añadir Bolsas", style="Accent.TButton", command=self._add_custom_mystery_bags).pack(side="left", padx=4)
        
        mb_quick = ttk.Frame(box_mb)
        mb_quick.pack(fill="x", pady=4)
        ttk.Button(mb_quick, text="+10 Arcoíris", command=lambda: self._quick_add_mystery("RAINBOW", 10)).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(mb_quick, text="+50 Arcoíris", command=lambda: self._quick_add_mystery("RAINBOW", 50)).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(mb_quick, text="Pack Todas (x10)", command=lambda: self._quick_add_mystery("TODAS", 10)).pack(side="left", fill="x", expand=True, padx=2)

    def _max_waiting_room_facilities(self):
        self.safe_lvl_var.set("10")
        self.tank_lvl_var.set("10")
        self.rank_var.set("100")
        if self.save_json:
            modifiers.upgrade_waiting_room(self.save_json, bank_level=10, tank_level=10)
            modifiers.set_player_rank(self.save_json, rank=100)
            self._auto_save()
            self.refresh_all_views()
            messagebox.showinfo("Instalaciones Maximizadas", "¡Banco de KC y Tanque de SPL mejorados al Nivel Máximo 10!")

    def _set_vip_entry_and_act(self, days):
        self.vip_days_var.set(str(days))
        self._activate_custom_vip()

    def _activate_custom_vip(self):
        if not self.save_json:
            return
        try:
            days = int(self.vip_days_var.get())
        except ValueError:
            days = 30
        end_ts = modifiers.activate_vip_express_pass(self.save_json, days=days)
        self._auto_save()
        self.refresh_all_views()
        self.status_var.set(f"¡Pase Royal Express VIP activado por {days} días!")
        messagebox.showinfo("VIP Activado", f"¡Pase Royal Express activado con éxito por {days} días!\n\nAscensor VIP Gratuito, 10 slots de bolsa extra y seguro de TDM garantizado.")

    def _add_custom_mystery_bags(self):
        if not self.save_json:
            return
        r_type = self.mystery_type_var.get()
        try:
            qty = int(self.mystery_qty_var.get())
        except ValueError:
            qty = 10
            
        if r_type == "TODAS":
            modifiers.add_all_mystery_bags(self.save_json, count_each=qty)
            self._auto_save()
            self.refresh_all_views()
            self.status_var.set(f"¡Añadidas x{qty} bolsas de cada rareza!")
            messagebox.showinfo("Bolsas Añadidas", f"¡Se han añadido x{qty} Bolsas Misteriosas de cada rareza!\n\nDisponibles directamente en el Buzón de Recompensas (Rewards Box) de tu Sala de Espera y en el Metro.")
        elif r_type == "RAINBOW":
            total = modifiers.add_rainbow_bags(self.save_json, count=qty)
            self._auto_save()
            self.refresh_all_views()
            self.status_var.set(f"¡Añadidas x{qty} Bolsas Arcoíris TDM (Total: {total})!")
            messagebox.showinfo("Bolsas Arcoíris Añadidas", f"¡Se han añadido x{qty} Bolsas Arcoíris (Rainbow Bags)!\n\nDisponibles directamente en el Buzón de Recompensas.")
        else:
            soul = self.save_json.setdefault("soul", {})
            mbags = soul.setdefault("mysterybag", {})
            b_list = mbags.setdefault(r_type, [])
            now = int(time.time())
            for i in range(qty):
                b_list.append({"rarity": r_type, "cntgen": f"MYSTERYBAG_GEN_{r_type}_{now % 1000 + i + 1}"})
            modifiers.send_present_to_reward_box(self.save_json, p_type="LOSTBAG", num=qty, kind=f"MYSTERYBAG_{r_type}", val0=r_type)
            self._auto_save()
            self.refresh_all_views()
            self.status_var.set(f"¡Añadidas x{qty} Bolsas {r_type} TDM!")
            messagebox.showinfo("Bolsas Añadidas", f"¡Se han añadido x{qty} Bolsas {r_type}!\n\nDisponibles directamente en el Buzón de Recompensas de tu Sala de Espera.")

    def _quick_add_mystery(self, rarity, count):
        self.mystery_type_var.set(rarity)
        self.mystery_qty_var.set(str(count))
        self._add_custom_mystery_bags()

    # ================= TAB 2: FIGHTERS STUDIO =================
    def _build_fighters_tab(self):
        paned = ttk.PanedWindow(self.tab_fighters, orient="horizontal")
        paned.pack(fill="both", expand=True)
        
        left_box = ttk.LabelFrame(paned, text="Luchadores en el Congelador (Fighter Freezer)", padding=10)
        paned.add(left_box, weight=2)
        
        self.fighters_tree = ttk.Treeview(left_box, columns=("num", "lvl", "state"), show="tree headings", height=14)
        self.fighters_tree.heading("#0", text="Luchador / Clase")
        self.fighters_tree.heading("num", text="#")
        self.fighters_tree.heading("lvl", text="Nivel")
        self.fighters_tree.heading("state", text="Estado")
        
        self.fighters_tree.column("#0", width=180)
        self.fighters_tree.column("num", width=35, anchor="center")
        self.fighters_tree.column("lvl", width=55, anchor="center")
        self.fighters_tree.column("state", width=80, anchor="center")
        
        self.fighters_tree.pack(fill="both", expand=True, pady=4)
        self.fighters_tree.bind("<<TreeviewSelect>>", self._on_fighter_select)
        
        right_box = ttk.LabelFrame(paned, text="Ficha Técnica del Luchador", padding=14)
        paned.add(right_box, weight=3)
        
        # Fighter Top Profile
        prof_f = ttk.Frame(right_box)
        prof_f.pack(fill="x", pady=2)
        
        self.f_class_icon_lbl = ttk.Label(prof_f)
        self.f_class_icon_lbl.pack(side="left", padx=(0, 10))
        
        f_meta = ttk.Frame(prof_f)
        f_meta.pack(side="left")
        
        self.f_title_lbl = ttk.Label(f_meta, text="Selecciona un luchador", font=("Segoe UI", 13, "bold"), foreground=ACCENT_GOLD)
        self.f_title_lbl.pack(anchor="w")
        
        self.f_sub_lbl = ttk.Label(f_meta, text="Clase: --- | Nivel: --- | Rango: Tier ---", font=("Segoe UI", 9), foreground=FG_MUTED)
        self.f_sub_lbl.pack(anchor="w")
        
        # Identity and Configuration Grid
        id_frame = ttk.LabelFrame(right_box, text="Identidad y Configuración del Luchador", padding=8)
        id_frame.pack(fill="x", pady=4)
        
        # Row 0: Name and Class
        ttk.Label(id_frame, text="Nombre:").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.f_name_entry_var = tk.StringVar()
        ttk.Entry(id_frame, textvariable=self.f_name_entry_var, width=16).grid(row=0, column=1, padx=4, pady=3, sticky="w")
        
        ttk.Label(id_frame, text="Clase:").grid(row=0, column=2, sticky="w", padx=4, pady=3)
        self.f_class_select_var = tk.StringVar(value="BAL (All-Rounder)")
        classes_opts = [
            "BAL (All-Rounder)", "BRE (Striker)", "DEF (Defender)", "TEC (Attacker)",
            "SHT (Shooter)", "COL (Collector)", "SKI (Skill Master)", "LUK (Lucky Star)"
        ]
        cb_cls = ttk.Combobox(id_frame, textvariable=self.f_class_select_var, values=classes_opts, state="readonly", width=18)
        cb_cls.grid(row=0, column=3, padx=4, pady=3, sticky="w")
        
        # Row 1: Grade (Tier) and Level
        ttk.Label(id_frame, text="Grado (Tier ★):").grid(row=1, column=0, sticky="w", padx=4, pady=3)
        self.f_grade_select_var = tk.StringVar(value="5")
        cb_grd = ttk.Combobox(id_frame, textvariable=self.f_grade_select_var, values=["1", "2", "3", "4", "5", "6"], state="readonly", width=6)
        cb_grd.grid(row=1, column=1, padx=4, pady=3, sticky="w")
        
        ttk.Label(id_frame, text="Nivel (1-247):").grid(row=1, column=2, sticky="w", padx=4, pady=3)
        self.f_lvl_select_var = tk.StringVar(value="125")
        ttk.Entry(id_frame, textvariable=self.f_lvl_select_var, width=8, justify="center").grid(row=1, column=3, padx=4, pady=3, sticky="w")
        
        # Row 2: HP Actual and Bag Slots
        ttk.Label(id_frame, text="Salud HP Actual:").grid(row=2, column=0, sticky="w", padx=4, pady=3)
        self.f_hp_current_var = tk.StringVar(value="15000")
        ttk.Entry(id_frame, textvariable=self.f_hp_current_var, width=10, justify="center").grid(row=2, column=1, padx=4, pady=3, sticky="w")
        
        ttk.Label(id_frame, text="Bolsa (Slots):").grid(row=2, column=2, sticky="w", padx=4, pady=3)
        self.f_bag_select_var = tk.StringVar(value="50")
        cb_fbag = ttk.Combobox(id_frame, textvariable=self.f_bag_select_var, values=["20", "25", "30", "35", "40", "45", "50", "60"], state="readonly", width=6)
        cb_fbag.grid(row=2, column=3, padx=4, pady=3, sticky="w")
        
        # Stats Form Grid (3 columns for perfect balance)
        stats_frame = ttk.LabelFrame(right_box, text="Nivel de Atributos Base (Puntos de Estadística 1 a 35)", padding=8)
        stats_frame.pack(fill="x", pady=4)
        
        self.f_stats_vars = {}
        stat_names = [
            ("hp", "HP (Vitalidad):"),
            ("stm", "STM (Resistencia):"),
            ("str", "STR (Fuerza):"),
            ("dex", "DEX (Destreza):"),
            ("vit", "VIT (Defensa):"),
            ("luk", "LUK (Suerte):"),
        ]
        
        for idx, (k, label) in enumerate(stat_names):
            r = idx // 3
            c = (idx % 3) * 2
            ttk.Label(stats_frame, text=label).grid(row=r, column=c, sticky="w", padx=4, pady=4)
            v = tk.StringVar(value="30")
            self.f_stats_vars[k] = v
            ttk.Entry(stats_frame, textvariable=v, width=6, justify="center").grid(row=r, column=c+1, padx=4, pady=4)
            
        # Equipped Decals Preview Frame
        self.f_decals_frame = ttk.LabelFrame(right_box, text="🏷️ Calcomanías Equipadas en este Luchador", padding=8)
        self.f_decals_frame.pack(fill="x", pady=4)
        self.f_decal_slots_lbls = []
        for slot_idx in range(5):
            lbl = ttk.Label(self.f_decals_frame, text=f"Espacio {slot_idx+1}: Vacío", font=("Segoe UI", 8), compound="left")
            lbl.pack(anchor="w", pady=1)
            self.f_decal_slots_lbls.append(lbl)

        # Quick Fighter Actions
        act_frame = ttk.Frame(right_box)
        act_frame.pack(fill="x", pady=6)
        
        btn_save_f = ttk.Button(act_frame, text="💾 APLICAR CAMBIOS AL LUCHADOR", style="Accent.TButton", command=self._save_fighter_changes)
        btn_save_f.pack(side="left", padx=3, fill="x", expand=True)
        
        btn_revive = ttk.Button(act_frame, text="💖 Revivir al 100%", style="Success.TButton", command=self.revive_current_fighter)
        btn_revive.pack(side="left", padx=3, fill="x", expand=True)
        
        btn_max_fighter = ttk.Button(act_frame, text="⭐ Maximizar Stats (Lv 247)", command=self.max_current_fighter)
        btn_max_fighter.pack(side="left", padx=3, fill="x", expand=True)

        # Meta Decal Presets for Fighters
        decal_preset_box = ttk.LabelFrame(right_box, text="⚡ Presets de Calcomanías Meta (8 Slots)", padding=8)
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
        
        btn_equip_preset = ttk.Button(decal_preset_box, text="🥋 EQUIPAR PRESET DIRECTO EN ESTE LUCHADOR", style="Accent.TButton", command=self._equip_decal_preset_action)
        btn_equip_preset.pack(fill="x", pady=2)
        
        btn_apply_preset = ttk.Button(decal_preset_box, text="📦 Inyectar Set al Inventario (x5 cada una)", command=self._apply_decal_preset_action)
        btn_apply_preset.pack(fill="x", pady=2)

    def _on_fighter_select(self, event):
        sel = self.fighters_tree.selection()
        if not sel:
            return
        node = sel[0]
        vals = self.fighters_tree.item(node, "values")
        num_str = vals[0]
        idx = int(num_str) - 1
        self.current_fighter_idx = idx
        
        if not self.save_json:
            return
            
        fighters = modifiers.get_all_fighters_info(self.save_json)
        if idx < len(fighters):
            f = fighters[idx]
            name = f.get("name", f"Luchador #{idx+1}")
            cls_name = f.get("class_name", "All-Rounder")
            cls_code = f.get("class", "BAL")
            grade = f.get("grade", 1)
            lvl = f.get("level", 1)
            hp_cur = f.get("hp", 1000)
            bag = f.get("bag", 20)
            
            self.f_title_lbl.config(text=name)
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
            self.f_bag_select_var.set(str(bag))
            
            self.f_stats_vars["hp"].set(str(f.get("hp_pts", 20)))
            self.f_stats_vars["stm"].set(str(f.get("stm", 20)))
            self.f_stats_vars["str"].set(str(f.get("str", 20)))
            self.f_stats_vars["dex"].set(str(f.get("dex", 20)))
            self.f_stats_vars["vit"].set(str(f.get("vit", 20)))
            self.f_stats_vars["luk"].set(str(f.get("luk", 20)))
            
            # Update equipped decals preview
            cid = f.get("cid", "")
            eq_list = self.save_json.get("soul", {}).get("skl", {}).get("eqskl", {}).get(list(self.save_json.get("bodyuser", {}).keys())[0] if self.save_json.get("bodyuser") else "", [])
            fighter_eq = [e for e in eq_list if e.get("cid") == cid]
            for s_idx in range(5):
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

    def _save_fighter_changes(self):
        if not self.save_json:
            return
        idx = getattr(self, "current_fighter_idx", 0)
        name = self.f_name_entry_var.get()
        cls_str = self.f_class_select_var.get().split()[0]
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
            messagebox.showerror("Error", "Por favor ingresa números válidos en los campos numéricos.")
            return
            
        modifiers.update_fighter(
            self.save_json, idx,
            name=name, clazz=cls_str, grade=grade, lvl=lvl, hp=hp_val,
            str_stat=pstr, dex=pdex, vit=pvit, stm=pstm, luk=pluk, bag=bag_val,
            param_hp=php, param_stm=pstm, param_str=pstr, param_dex=pdex, param_vit=pvit, param_luk=pluk
        )
        self._auto_save()
        self.refresh_all_views()
        self.status_var.set(f"Cambios guardados para {name} (Luchador #{idx+1}).")
        messagebox.showinfo("Luchador Actualizado", f"¡Se han aplicado los cambios personalizados a {name}!\nGuardado automáticamente.")

    def revive_current_fighter(self):
        if not self.save_json:
            return
        modifiers.revive_all_fighters(self.save_json)
        self._auto_save()
        self.refresh_all_views()
        self.status_var.set("¡Todos los luchadores han sido revividos al 100% de salud!")
        messagebox.showinfo("Luchadores Revividos", "¡Se ha restaurado la vida al 100% y se ha eliminado el estado de muerte de todos los luchadores!")

    def max_current_fighter(self):
        if not self.save_json:
            return
        modifiers.max_fighter_level_and_stats(self.save_json, fighter_index=self.current_fighter_idx, level=247)
        self._auto_save()
        self.refresh_all_views()
        self.status_var.set(f"Luchador #{self.current_fighter_idx+1} maximizado con éxito.")
        messagebox.showinfo("Luchador Maximizado", f"¡Luchador #{self.current_fighter_idx+1} mejorado a Nivel 247 con todos sus stats al tope!")

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
        self.status_var.set(f"Preset '{name}' aplicado (x5 de cada calcomanía).")
        messagebox.showinfo("Preset de Calcomanías Aplicado", f"¡Se han añadido x5 copias Premium de las {count} calcomanías del preset:\n\n⭐ {name}\n\n¡Listas para equipar en el Grill del Tío Death!")

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
        self.status_var.set(f"Preset '{name}' equipado en {f_info.get('name', 'Luchador')} ({count} calcomanías).")
        messagebox.showinfo(
            "Preset Equipado con Éxito",
            f"¡Se han equipado directamente {count} calcomanías del preset:\n\n"
            f"⭐ {name}\n\n"
            f"en los espacios de combate de {f_info.get('name', 'Luchador')}!\n"
            f"Guardado automáticamente."
        )

    def max_all_currencies(self):
        if not self.save_json:
            return
        modifiers.max_all_currencies(self.save_json)
        self._auto_save()
        self.refresh_all_views()
        self.status_var.set("¡Todas las divisas maximizadas al tope!")
        messagebox.showinfo("Divisas Maximizadas", "¡Se han establecido Death Metals (9,999), Kill Coins, SPLithium, Bloodnium y Puntos RE al límite máximo!")

    # ================= TAB 3: MATERIALS R&D (106) =================
    def _build_materials_tab(self):
        paned = ttk.PanedWindow(self.tab_materials, orient="horizontal")
        paned.pack(fill="both", expand=True)
        
        left_box = ttk.Frame(paned)
        paned.add(left_box, weight=3)
        
        # Row 1: Search, Category, Stock Filter, Rarity, Actions
        ctrl_frame = ttk.Frame(left_box)
        ctrl_frame.pack(fill="x", pady=2)
        
        ttk.Label(ctrl_frame, text="🔍 Buscar:").pack(side="left", padx=2)
        self.mat_search_var = tk.StringVar()
        self.mat_search_var.trace_add("write", lambda *args: self.filter_materials_list())
        ttk.Entry(ctrl_frame, textvariable=self.mat_search_var, width=12).pack(side="left", padx=2)
        
        ttk.Label(ctrl_frame, text="Categoría:").pack(side="left", padx=(4, 1))
        self.mat_cat_var = tk.StringVar(value="Todos")
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
        cb_cat = ttk.Combobox(ctrl_frame, textvariable=self.mat_cat_var, values=cats, state="readonly", width=18)
        cb_cat.pack(side="left", padx=2)
        cb_cat.bind("<<ComboboxSelected>>", lambda e: self.filter_materials_list())

        ttk.Label(ctrl_frame, text="Stock:").pack(side="left", padx=(4, 1))
        self.mat_stock_filter_var = tk.StringVar(value="Todo")
        cb_stock = ttk.Combobox(ctrl_frame, textvariable=self.mat_stock_filter_var, values=["Todo", "📦 En Stock (> 0)", "⚠️ Stock Bajo (< 10)", "❌ Agotado (0)"], state="readonly", width=14)
        cb_stock.pack(side="left", padx=2)
        cb_stock.bind("<<ComboboxSelected>>", lambda e: self.filter_materials_list())

        ttk.Label(ctrl_frame, text="Rareza:").pack(side="left", padx=(4, 1))
        self.mat_rarity_filter_var = tk.StringVar(value="Todas")
        cb_mrarity = ttk.Combobox(ctrl_frame, textvariable=self.mat_rarity_filter_var, values=["Todas", "1★", "2★", "3★", "4★", "5★", "6★", "7★", "8★"], state="readonly", width=6)
        cb_mrarity.pack(side="left", padx=2)
        cb_mrarity.bind("<<ComboboxSelected>>", lambda e: self.filter_materials_list())
        
        btn_open_storage = ttk.Button(ctrl_frame, text="📦 Coin Locker", command=self._open_storage_manager)
        btn_open_storage.pack(side="right", padx=1)

        btn_all_mat = ttk.Button(ctrl_frame, text="✨ Stock Máximo (x100)", style="Accent.TButton", command=self.max_all_materials_preset)
        btn_all_mat.pack(side="right", padx=1)

        # Row 2: Pisos de la Torre (Wiki Tower Sections Quick Bar)
        ctrl_frame_floors = ttk.Frame(left_box)
        ctrl_frame_floors.pack(fill="x", pady=2)
        
        ttk.Label(ctrl_frame_floors, text="🗼 Pisos Torre:", font=("Segoe UI", 8, "bold"), foreground=ACCENT_GOLD).pack(side="left", padx=2)
        self.mat_floor_filter = tk.StringVar(value="TODOS")
        
        floor_buttons = [
            ("🌐 Todos", "TODOS"),
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
        self.mat_tree = ttk.Treeview(left_box, columns=("stock", "rarity", "category", "id"), show="tree headings", height=16)
        self.mat_tree.heading("#0", text="Icono / Nombre Oficial del Material (ES / EN)")
        self.mat_tree.heading("stock", text="En Almacén")
        self.mat_tree.heading("rarity", text="Rareza")
        self.mat_tree.heading("category", text="Tipo")
        self.mat_tree.heading("id", text="Código ID")
        
        self.mat_tree.column("#0", width=280)
        self.mat_tree.column("stock", width=90, anchor="center")
        self.mat_tree.column("rarity", width=70, anchor="center")
        self.mat_tree.column("category", width=130)
        self.mat_tree.column("id", width=120)
        
        self.mat_tree.pack(fill="both", expand=True, pady=4)
        self.mat_tree.bind("<<TreeviewSelect>>", self._on_mat_select)
        self.mat_tree.bind("<Double-1>", self._edit_selected_material_count)
        
        self.mat_tree.tag_configure("tag_in_stock", foreground=ACCENT_GOLD)
        self.mat_tree.tag_configure("tag_out_of_stock", foreground=FG_MUTED)
        
        # Right Material Card (Wiki Showcase)
        self.mat_card = ttk.LabelFrame(paned, text="Ficha Oficial de Material R&D", padding=12)
        paned.add(self.mat_card, weight=2)
        
        self.mat_art_lbl = ttk.Label(self.mat_card)
        self.mat_art_lbl.pack(pady=6)
        
        self.mat_title_lbl = ttk.Label(self.mat_card, text="Selecciona un material", font=("Segoe UI", 12, "bold"), foreground=ACCENT_GOLD, wraplength=260, justify="center")
        self.mat_title_lbl.pack(pady=2)
        
        self.mat_type_lbl = ttk.Label(self.mat_card, text="---", font=("Segoe UI", 9), foreground=FG_MUTED)
        self.mat_type_lbl.pack(pady=2)
        
        self.mat_stock_lbl = ttk.Label(self.mat_card, text="📦 En tu Almacén: --", font=("Segoe UI", 10, "bold"), foreground=ACCENT_CYAN)
        self.mat_stock_lbl.pack(pady=4)
        
        self.mat_desc_lbl = ttk.Label(self.mat_card, text="Selecciona cualquier material para ver su icono oficial y gestionar existencias para Chokufunsha.", font=("Segoe UI", 9), foreground=FG_MUTED, wraplength=260, justify="center")
        self.mat_desc_lbl.pack(pady=6)
        
        # Quantity controls
        qty_f = ttk.Frame(self.mat_card)
        qty_f.pack(pady=4)
        ttk.Label(qty_f, text="Añadir / Establecer:").pack(side="left", padx=2)
        self.mat_qty_entry_var = tk.StringVar(value="50")
        ttk.Entry(qty_f, textvariable=self.mat_qty_entry_var, width=6, justify="center").pack(side="left", padx=4)
        ttk.Button(qty_f, text="Establecer", style="Accent.TButton", command=self._set_selected_mat_qty).pack(side="left", padx=2)
        
        quick_m_box = ttk.Frame(self.mat_card)
        quick_m_box.pack(fill="x", pady=4)
        ttk.Button(quick_m_box, text="+10", command=lambda: self._quick_add_material_qty(10)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(quick_m_box, text="+50", command=lambda: self._quick_add_material_qty(50)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(quick_m_box, text="+100", command=lambda: self._quick_add_material_qty(100)).pack(side="left", fill="x", expand=True, padx=1)

        # Capacity expansion frame
        cap_frame = ttk.LabelFrame(self.mat_card, text="Capacidad del Coin Locker", padding=8)
        cap_frame.pack(fill="x", pady=(10, 0))
        
        self.mat_cap_indicator_lbl = ttk.Label(cap_frame, text="Almacén: 0 / 0 casillas", font=("Segoe UI", 9, "bold"))
        self.mat_cap_indicator_lbl.pack(anchor="w", pady=2)
        
        exp_row = ttk.Frame(cap_frame)
        exp_row.pack(fill="x", pady=2)
        ttk.Button(exp_row, text="Ampliación +500", command=lambda: self._expand_coin_locker(500)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(exp_row, text="Ampliación +1000", command=lambda: self._expand_coin_locker(1000)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(exp_row, text="Al Máximo (2,000)", style="Accent.TButton", command=lambda: self._expand_coin_locker(2000)).pack(side="left", fill="x", expand=True, padx=1)

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
        self.mat_type_lbl.config(text=f"Categoría: {cat} | Rareza: {stars} ({itemid})")
        if stock_str != "-":
            self.mat_stock_lbl.config(text=f"📦 En tu Almacén: {stock_str}", foreground=ACCENT_GOLD)
        else:
            self.mat_stock_lbl.config(text="📦 En tu Almacén: 0 u. (No tienes)", foreground=FG_MUTED)
        
        desc = "Material oficial de R&D para fabricar y mejorar armas y armaduras en Chokufunsha."
        for m in self.materials_db:
            if m["itemid"] == itemid:
                if m.get("desc_es"): desc = m["desc_es"]
                elif m.get("desc_en"): desc = m["desc_en"]
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
        self.status_var.set("¡Todos los 106 materiales de forja abastecidos a 100 u. en tu Almacén!")
        messagebox.showinfo("Almacén Abastecido", "¡Se han depositado 100 unidades de TODOS los 106 materiales de R&D en tu Almacén!")

    def _expand_coin_locker(self, target_capacity):
        if not self.save_json:
            return
        old_c, new_c = modifiers.expand_coin_locker_capacity(self.save_json, target_capacity=target_capacity)
        self._auto_save()
        self.status_var.set(f"Almacén ampliado de {old_c:,} a {new_c:,} casillas.")
        self.refresh_all_views()
        messagebox.showinfo(
            "Capacidad Ampliada",
            f"¡Almacén ampliado con éxito!\n\n"
            f"• Capacidad anterior: {old_c:,} casillas\n"
            f"• Nueva capacidad: {new_c:,} casillas\n\n"
            f"Se ha sincronizado masters.db (COINLOCKER_EXPAND_LIMIT_COUNT = {new_c}) y soul.cl.\n"
            f"Guardado automáticamente."
        )

    def _set_mat_floor_filter(self, mode):
        self.mat_floor_filter.set(mode)
        self.filter_materials_list()

    def filter_materials_list(self):
        for row in self.mat_tree.get_children():
            self.mat_tree.delete(row)
            
        query = self.mat_search_var.get().lower().strip() if hasattr(self, "mat_search_var") else ""
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
        
        # 1. R&D Materials from masters.db
        if cat_filter != "🍄 Setas y Criaturas":
            for m in self.materials_db:
                name_es = m.get("name_es", m.get("name", ""))
                name_en = m.get("name_en", "")
                cat = m.get("category", "Materiales")
                r = m.get("rarity", 1)
                stars = "★" * r
                itemid = m.get("itemid", "")
                cnt = stock_map.get(itemid, 0)
                
                # Category filter
                if cat_filter != "Todos" and cat != cat_filter:
                    continue
                    
                # Stock filter
                if stock_filter == "📦 En Stock (> 0)" and cnt <= 0:
                    continue
                elif stock_filter == "⚠️ Stock Bajo (< 10)" and (cnt <= 0 or cnt >= 10):
                    continue
                elif stock_filter == "❌ Agotado (0)" and cnt > 0:
                    continue

                # Rarity filter
                if rarity_filter != "Todas":
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

                # Query search
                if query and (query not in name_es.lower() and query not in name_en.lower() and query not in cat.lower() and query not in itemid.lower()):
                    continue
                    
                stock_str = f"{cnt} u." if cnt > 0 else "-"
                tag = "tag_in_stock" if cnt > 0 else "tag_out_of_stock"
                    
                display_title = f"{name_es} ({name_en})" if name_en and name_en != name_es else name_es
                icon_k = self._get_mat_photo_key(itemid, name_en or name_es)
                thumb = self.get_photo(icon_k, size=(36, 36), preserve_aspect=True)
                node_id = self.mat_tree.insert(
                    "",
                    "end",
                    text=f" {display_title}",
                    image=thumb or "",
                    values=(stock_str, stars, cat, itemid),
                    tags=(tag,)
                )
                self.tree_images[node_id] = thumb
                if not first_row:
                    first_row = node_id
                    
        # 2. Shrooms and Beasts (Tower Exploration)
        if cat_filter in ["Todos", "🍄 Setas y Criaturas"] and floor_filter == "TODOS" and rarity_filter == "Todas":
            for mid, mname, icon_f in SPECIAL_MUSHROOMS:
                cnt = stock_map.get(mid, 0)
                if stock_filter == "📦 En Stock (> 0)" and cnt <= 0:
                    continue
                elif stock_filter == "⚠️ Stock Bajo (< 10)" and (cnt <= 0 or cnt >= 10):
                    continue
                elif stock_filter == "❌ Agotado (0)" and cnt > 0:
                    continue
                if query and query not in mname.lower() and query not in mid.lower():
                    continue
                stock_str = f"{cnt} u." if cnt > 0 else "-"
                tag = "tag_in_stock" if cnt > 0 else "tag_out_of_stock"
                thumb = self.get_photo(icon_f, size=(36, 36), preserve_aspect=True) or self.get_photo("01_heartshroom_1", size=(36, 36), preserve_aspect=True)
                node_id = self.mat_tree.insert(
                    "",
                    "end",
                    text=f" {mname}",
                    image=thumb or "",
                    values=(stock_str, "★★★", "Setas Especiales", mid),
                    tags=(tag,)
                )
                self.tree_images[node_id] = thumb
                if not first_row:
                    first_row = node_id
                    
            for bid, bname, icon_b in SPECIAL_BEASTS:
                cnt = stock_map.get(bid, 0)
                if stock_filter == "📦 En Stock (> 0)" and cnt <= 0:
                    continue
                elif stock_filter == "⚠️ Stock Bajo (< 10)" and (cnt <= 0 or cnt >= 10):
                    continue
                elif stock_filter == "❌ Agotado (0)" and cnt > 0:
                    continue
                if query and query not in bname.lower() and query not in bid.lower():
                    continue
                stock_str = f"{cnt} u." if cnt > 0 else "-"
                tag = "tag_in_stock" if cnt > 0 else "tag_out_of_stock"
                thumb = self.get_photo(icon_b, size=(36, 36), preserve_aspect=True) or self.get_photo("snails", size=(36, 36), preserve_aspect=True)
                node_id = self.mat_tree.insert(
                    "",
                    "end",
                    text=f" {bname}",
                    image=thumb or "",
                    values=(stock_str, "★★★★", "Criaturas Doradas", bid),
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
        
        ttk.Label(ctrl_frame, text="🔍 Buscar:").pack(side="left", padx=2)
        self.decal_search_var = tk.StringVar()
        self.decal_search_var.trace_add("write", lambda *args: self.filter_decals_list())
        ttk.Entry(ctrl_frame, textvariable=self.decal_search_var, width=13).pack(side="left", padx=2)
        
        ttk.Label(ctrl_frame, text="Rareza:").pack(side="left", padx=(4, 1))
        self.decal_rarity_filter_var = tk.StringVar(value="Todas")
        cb_rarity = ttk.Combobox(ctrl_frame, textvariable=self.decal_rarity_filter_var, values=["Todas", "1★", "2★", "3★", "4★", "5★"], state="readonly", width=6)
        cb_rarity.pack(side="left", padx=2)
        cb_rarity.bind("<<ComboboxSelected>>", lambda e: self.filter_decals_list())

        ttk.Label(ctrl_frame, text="Tipo:").pack(side="left", padx=(4, 1))
        self.decal_type_filter_var = tk.StringVar(value="Todas")
        cb_dtype = ttk.Combobox(ctrl_frame, textvariable=self.decal_type_filter_var, values=["Todas", "Premium (_P)", "Estándar"], state="readonly", width=12)
        cb_dtype.pack(side="left", padx=2)
        cb_dtype.bind("<<ComboboxSelected>>", lambda e: self.filter_decals_list())

        ttk.Label(ctrl_frame, text="Posesión:").pack(side="left", padx=(4, 1))
        self.decal_poss_filter_var = tk.StringVar(value="Todas")
        cb_dposs = ttk.Combobox(ctrl_frame, textvariable=self.decal_poss_filter_var, values=["Todas", "📦 Poseídas (> 0)", "❌ Faltantes (0)"], state="readonly", width=14)
        cb_dposs.pack(side="left", padx=2)
        cb_dposs.bind("<<ComboboxSelected>>", lambda e: self.filter_decals_list())

        btn_meta = ttk.Button(ctrl_frame, text="🏆 Pack Meta", command=self.add_meta_decals_preset)
        btn_meta.pack(side="right", padx=1)

        btn_all_p = ttk.Button(ctrl_frame, text="✨ Desbloquear Todas", style="Accent.TButton", command=self.unlock_all_decals_preset)
        btn_all_p.pack(side="right", padx=1)

        self.decal_unlock_qty_var = tk.StringVar(value="3")
        ttk.Entry(ctrl_frame, textvariable=self.decal_unlock_qty_var, width=3, justify="center").pack(side="right", padx=1)
        ttk.Label(ctrl_frame, text="Copias:").pack(side="right", padx=(2, 0))

        # Row 2: Eventos / Colaboraciones Quick Buttons Bar
        ctrl_frame_events = ttk.Frame(left_box)
        ctrl_frame_events.pack(fill="x", pady=2)
        
        ttk.Label(ctrl_frame_events, text="🎯 Eventos:", font=("Segoe UI", 8, "bold"), foreground=ACCENT_GOLD).pack(side="left", padx=2)
        self.decal_event_filter = tk.StringVar(value="TODOS")
        
        decal_event_buttons = [
            ("🌐 Todas", "TODOS"),
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
        
        ttk.Label(ctrl_frame_styles, text="⚡ Estilos:", font=("Segoe UI", 8, "bold"), foreground=ACCENT_CYAN).pack(side="left", padx=2)
        self.decal_style_filter = tk.StringVar(value="TODOS")
        
        decal_style_buttons = [
            ("Todos", "TODOS"),
            ("⚔️ Addicts", "ADDICTS"),
            ("💥 Crítico", "CRIT_DMG"),
            ("🛡️ Tanque", "TANK_DEF"),
            ("🩸 Vampiro", "VAMP_SURV"),
            ("📦 Farmeo", "FARM_QOL"),
            ("🎭 Sets", "SETS")
        ]
        for btn_text, mode in decal_style_buttons:
            ttk.Button(ctrl_frame_styles, text=btn_text, command=lambda m=mode: self._set_decal_style_filter(m)).pack(side="left", padx=1)

        # Treeview with columns
        self.decals_tree = ttk.Treeview(left_box, columns=("stars", "id", "premium", "count"), show="tree headings", height=16)
        self.decals_tree.heading("#0", text="Icono / Nombre Oficial en Español e Inglés")
        self.decals_tree.heading("stars", text="Rareza")
        self.decals_tree.heading("id", text="ID Calcomanía")
        self.decals_tree.heading("premium", text="Tipo")
        self.decals_tree.heading("count", text="Cantidad")
        
        self.decals_tree.column("#0", width=300)
        self.decals_tree.column("stars", width=65, anchor="center")
        self.decals_tree.column("id", width=160)
        self.decals_tree.column("premium", width=85, anchor="center")
        self.decals_tree.column("count", width=70, anchor="center")
        
        self.decals_tree.pack(fill="both", expand=True, pady=4)
        self.decals_tree.bind("<<TreeviewSelect>>", self._on_decal_select)
        self.decals_tree.bind("<Double-1>", self._edit_selected_decal_count)
        
        self.decal_card = ttk.LabelFrame(paned, text="Tarjeta de Arte Oficial (Full HD)", padding=12)
        paned.add(self.decal_card, weight=2)
        
        self.decal_art_lbl = ttk.Label(self.decal_card)
        self.decal_art_lbl.pack(pady=10)
        
        self.decal_title_lbl = ttk.Label(self.decal_card, text="Selecciona una calcomanía", font=("Segoe UI", 12, "bold"), wraplength=240, justify="center")
        self.decal_title_lbl.pack(pady=4)
        
        self.decal_type_lbl = ttk.Label(self.decal_card, text="---", font=("Segoe UI", 9), foreground=ACCENT_GOLD)
        self.decal_type_lbl.pack(pady=2)
        
        self.decal_desc_lbl = ttk.Label(self.decal_card, text="Selecciona cualquier calcomanía de la lista para ver su ilustración original in-game en alta definición y sus efectos.", font=("Segoe UI", 9), foreground=FG_MUTED, wraplength=240, justify="center")
        self.decal_desc_lbl.pack(pady=10)
        
        qty_box = ttk.Frame(self.decal_card)
        qty_box.pack(pady=4)
        ttk.Label(qty_box, text="Cantidad:").pack(side="left", padx=4)
        self.decal_qty_var = tk.StringVar(value="0")
        ttk.Entry(qty_box, textvariable=self.decal_qty_var, width=6, justify="center").pack(side="left", padx=4)
        ttk.Button(qty_box, text="Actualizar", style="Accent.TButton", command=self._update_current_decal_qty).pack(side="left", padx=4)
        
        d_quick = ttk.Frame(self.decal_card)
        d_quick.pack(fill="x", pady=2)
        ttk.Button(d_quick, text="+1", width=3, command=lambda: self._quick_add_decal(1)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(d_quick, text="+3", width=3, command=lambda: self._quick_add_decal(3)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(d_quick, text="+5", width=3, command=lambda: self._quick_add_decal(5)).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(d_quick, text="+10", width=3, command=lambda: self._quick_add_decal(10)).pack(side="left", fill="x", expand=True, padx=1)

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
        self.decal_type_lbl.config(text=f"Tipo: {dtype} | Poseídas: x{cnt}")
        
        info = self.decals_map.get(did) or self.decals_map.get(did.replace("_P", "")) or {}
        desc = info.get("desc_es") or info.get("desc_en") or "Calcomanía Oficial de Combate"
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
        self.status_var.set("Pack de calcomanías Top Tier Meta añadido (x5).")
        messagebox.showinfo("Pack Meta Añadido", "¡Se han añadido x5 copias de las mejores Calcomanías Meta del juego!\nGuardado automáticamente.")

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
        self.status_var.set(f"¡Todas las calcomanías desbloqueadas (x{qty} normal y x{qty} premium)!")
        messagebox.showinfo("Calcomanías Desbloqueadas", f"¡Se han añadido x{qty} copias de TODAS las 626 calcomanías oficiales del juego a tu inventario!\nGuardado automáticamente.")

    def _set_decal_event_filter(self, mode):
        self.decal_event_filter.set(mode)
        self.filter_decals_list()

    def _set_decal_style_filter(self, mode):
        self.decal_style_filter.set(mode)
        self.filter_decals_list()

    def filter_decals_list(self):
        for row in self.decals_tree.get_children():
            self.decals_tree.delete(row)
            
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
            if type_filter == "Premium (_P)" and not is_p:
                continue
            elif type_filter == "Estándar" and is_p:
                continue
                
            # 2. Possession filter
            if poss_filter == "📦 Poseídas (> 0)" and cnt <= 0:
                continue
            elif poss_filter == "❌ Faltantes (0)" and cnt > 0:
                continue

            # 3. Rarity filter
            d_rarity = info.get("rarity", 1 if not is_p else 3)
            if rarity_filter != "Todas":
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
                    
            display_name = f"{name_es} ({name_en})" if name_en and name_en != name_es else name_es
            stars_str = f"{d_rarity}★"
            art_rel = self._find_decal_art(did)
            thumb = self.get_photo(art_rel, size=(36, 36), preserve_aspect=True)
            node_id = self.decals_tree.insert("", "end", text=f" {display_name}", image=thumb or "", values=(stars_str, did, "PREMIUM" if is_p else "ESTÁNDAR", f"x{cnt}" if cnt > 0 else "-"))
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
        
        # 1. Slot (Wiki-style)
        if raw_type == "PTTP_HEAD" or "_HEAD_" in itemid:
            slot = "🪖 Casco"
            slot_key = "head"
        elif raw_type == "PTTP_BODY" or "_TOPS_" in itemid:
            slot = "👕 Pecho"
            slot_key = "chest"
        elif raw_type in ("PTTP_PANTS", "PTTP_LEGS") or "_BTM_" in itemid:
            slot = "👖 Piernas"
            slot_key = "legs"
        else:
            slot = "⚔️ Arma"
            slot_key = "weapon"
            
        # 2. Faction (Wiki-style)
        if "PT_DIY" in itemid:
            faction = "🔨 D.O.D. ARMS"
            faction_key = "DOD"
        elif "PT_SPO" in itemid:
            faction = "🎖️ WAR ENSEMBLE"
            faction_key = "SPO"
        elif "PT_FAN" in itemid:
            faction = "🕯️ CANDLE WOLF"
            faction_key = "FAN"
        elif "PT_MIL" in itemid:
            faction = "🥛 M.I.L.K."
            faction_key = "MIL"
        elif any(k in itemid for k in ["PT_TBR", "TENGOKU", "WHITE", "NAPALM", "THUNDER", "WIND"]):
            faction = "⚡ 4 FORCEMEN & TENGOKU"
            faction_key = "FORCEMEN"
        elif any(k in itemid for k in ["PT_JAC", "PT_JCL", "JACKAL"]):
            faction = "🕶️ JACKALS"
            faction_key = "JACKAL"
        elif "PT_REC" in itemid:
            faction = "♻️ RE (Reciclador)"
            faction_key = "RE"
        elif any(k in itemid for k in ["PT_SPE", "PT_GAS"]):
            faction = "🎭 Especial / Evento"
            faction_key = "SPE"
        else:
            orig = item.get("faction", "")
            if "WAR" in orig:
                faction = "🎖️ WAR ENSEMBLE"
                faction_key = "SPO"
            elif "CANDLE" in orig:
                faction = "🕯️ CANDLE WOLF"
                faction_key = "FAN"
            elif "D.O.D" in orig:
                faction = "🔨 D.O.D. ARMS"
                faction_key = "DOD"
            elif "M.I.L.K" in orig:
                faction = "🥛 M.I.L.K."
                faction_key = "MIL"
            else:
                faction = "⚔️ General / Otras"
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
        
        ttk.Label(ctrl_frame, text="🔍 Buscar:").pack(side="left", padx=2)
        self.bp_search_var = tk.StringVar()
        self.bp_search_var.trace_add("write", lambda *args: self.filter_blueprints_list())
        ttk.Entry(ctrl_frame, textvariable=self.bp_search_var, width=15).pack(side="left", padx=2)
        
        ttk.Label(ctrl_frame, text="Ranura:").pack(side="left", padx=(6, 2))
        self.bp_cat_combo_var = tk.StringVar(value="Todos")
        cb_bp_cat = ttk.Combobox(ctrl_frame, textvariable=self.bp_cat_combo_var, values=["Todos", "🪖 Cascos", "👕 Pechos", "👖 Piernas", "⚔️ Armas"], state="readonly", width=11)
        cb_bp_cat.pack(side="left", padx=2)
        cb_bp_cat.bind("<<ComboboxSelected>>", lambda e: self.filter_blueprints_list())
        
        ttk.Label(ctrl_frame, text="Facción:").pack(side="left", padx=(6, 2))
        self.bp_faction_var = tk.StringVar(value="Todas")
        factions_list = [
            "Todas",
            "🔨 D.O.D. ARMS",
            "🎖️ WAR ENSEMBLE",
            "🕯️ CANDLE WOLF",
            "🥛 M.I.L.K.",
            "⚡ 4 FORCEMEN & TENGOKU",
            "🕶️ JACKALS",
            "♻️ RE (Reciclador)",
            "🎭 Especial / Evento",
            "⚔️ General / Otras"
        ]
        cb_faction = ttk.Combobox(ctrl_frame, textvariable=self.bp_faction_var, values=factions_list, state="readonly", width=18)
        cb_faction.pack(side="left", padx=2)
        cb_faction.bind("<<ComboboxSelected>>", lambda e: self.filter_blueprints_list())
        
        btn_sets_viewer = ttk.Button(ctrl_frame, text="👘 Visor de Sets por Nivel", style="Accent.TButton", command=self._open_armor_set_viewer)
        btn_sets_viewer.pack(side="right", padx=3)
        
        # Row 2: Possession Filter + Level + Actions
        ctrl_frame2 = ttk.Frame(left_box)
        ctrl_frame2.pack(fill="x", pady=3)
        
        ttk.Label(ctrl_frame2, text="Posesión:").pack(side="left", padx=2)
        self.bp_possession_filter_var = tk.StringVar(value="Todos")
        poss_list = [
            "Todos",
            "📦 En Almacén (> 0)",
            "⭐ Desbloqueados en Tienda (+4)",
            "🔨 En I+D (REMODEL / MAP)",
            "❌ Bloqueados (Faltantes)"
        ]
        cb_poss = ttk.Combobox(ctrl_frame2, textvariable=self.bp_possession_filter_var, values=poss_list, state="readonly", width=18)
        cb_poss.pack(side="left", padx=2)
        cb_poss.bind("<<ComboboxSelected>>", lambda e: self.filter_blueprints_list())

        ttk.Label(ctrl_frame2, text="Daño:").pack(side="left", padx=(4, 2))
        self.bp_dmg_type_var = tk.StringVar(value="Todos")
        dmg_list = [
            "Todos",
            "🗡️ Corte (Slash)",
            "🔨 Golpe (Blunt)",
            "🏹 Perforación (Pierce)",
            "🔥 Fuego (Burn)",
            "⚡ Electricidad (Electric)",
            "🧪 Veneno (Poison)"
        ]
        cb_dmg = ttk.Combobox(ctrl_frame2, textvariable=self.bp_dmg_type_var, values=dmg_list, state="readonly", width=15)
        cb_dmg.pack(side="left", padx=2)
        cb_dmg.bind("<<ComboboxSelected>>", lambda e: self.filter_blueprints_list())
        
        ttk.Label(ctrl_frame2, text="Nivel a desbloquear:").pack(side="left", padx=(6, 2))
        self.bp_unlock_all_lvl_var = tk.StringVar(value="4")
        cb_bp_all_lvl = ttk.Combobox(ctrl_frame2, textvariable=self.bp_unlock_all_lvl_var, values=["1", "2", "3", "4"], width=3, state="readonly")
        cb_bp_all_lvl.pack(side="left", padx=1)
        
        btn_all_bp = ttk.Button(ctrl_frame2, text="🌟 DESBLOQUEAR TODO", style="Accent.TButton", command=self.unlock_all_blueprints_preset)
        btn_all_bp.pack(side="right", padx=2)
        
        btn_repair_bps = ttk.Button(ctrl_frame2, text="🔧 Reparar I+D", command=self._repair_blueprints_action)
        btn_repair_bps.pack(side="right", padx=2)
        
        # Row 3: Collabs & Quick Events Filter Bar
        ctrl_frame3 = ttk.Frame(left_box)
        ctrl_frame3.pack(fill="x", pady=2)
        
        ttk.Label(ctrl_frame3, text="🎯 Eventos:", font=("Segoe UI", 8, "bold"), foreground=ACCENT_GOLD).pack(side="left", padx=2)
        self.bp_collab_filter = tk.StringVar(value="TODOS")
        
        collab_buttons = [
            ("🌐 Todos", "TODOS"),
            ("💥 World of Tanks", "WOT"),
            ("⚔️ No More Heroes", "NMH"),
            ("🏆 TDM Seasons", "TDM"),
            ("♻️ Ediciones RE", "RE"),
            ("💀 4 Forcemen", "44CE")
        ]
        for btn_text, mode in collab_buttons:
            ttk.Button(ctrl_frame3, text=btn_text, command=lambda m=mode: self._set_collab_filter(m)).pack(side="left", padx=1)
        
        # Treeview with columns
        cols = ("slot", "faction", "status", "storage", "bag", "id")
        self.bp_tree = ttk.Treeview(left_box, columns=cols, show="tree headings", height=16)
        self.bp_tree.heading("#0", text="Icono / Nombre Oficial (ES / EN)")
        self.bp_tree.heading("slot", text="Ranura")
        self.bp_tree.heading("faction", text="Facción")
        self.bp_tree.heading("status", text="Estado Forja")
        self.bp_tree.heading("storage", text="Almacén")
        self.bp_tree.heading("bag", text="Bolsa")
        self.bp_tree.heading("id", text="ID Plano")
        
        self.bp_tree.column("#0", width=260)
        self.bp_tree.column("slot", width=85, anchor="center")
        self.bp_tree.column("faction", width=125)
        self.bp_tree.column("status", width=110, anchor="center")
        self.bp_tree.column("storage", width=80, anchor="center")
        self.bp_tree.column("bag", width=70, anchor="center")
        self.bp_tree.column("id", width=125)
        
        self.bp_tree.pack(fill="both", expand=True, pady=4)
        self.bp_tree.bind("<<TreeviewSelect>>", self._on_bp_select)
        
        # Tags styling
        self.bp_tree.tag_configure("tag_shop", foreground=ACCENT_GOLD)
        self.bp_tree.tag_configure("tag_remodel", foreground=ACCENT_BLUE)
        self.bp_tree.tag_configure("tag_locked", foreground=FG_MUTED)

        # Right Equipment Blueprint Card (Wiki Showcase)
        self.bp_card = ttk.LabelFrame(paned, text="Ficha Técnica de Plano Chokufunsha", padding=12)
        paned.add(self.bp_card, weight=2)
        
        self.bp_art_lbl = ttk.Label(self.bp_card)
        self.bp_art_lbl.pack(pady=4)
        
        self.bp_title_lbl = ttk.Label(self.bp_card, text="Selecciona un equipo", font=("Segoe UI", 12, "bold"), foreground=ACCENT_GOLD, wraplength=260, justify="center")
        self.bp_title_lbl.pack(pady=2)
        
        self.bp_faction_lbl = ttk.Label(self.bp_card, text="---", font=("Segoe UI", 9), foreground=FG_MUTED)
        self.bp_faction_lbl.pack(pady=1)
        
        self.bp_status_lbl = ttk.Label(self.bp_card, text="Estado: ---", font=("Segoe UI", 10, "bold"), foreground=ACCENT_CYAN)
        self.bp_status_lbl.pack(pady=2)
        
        self.bp_stats_lbl = ttk.Label(self.bp_card, text="Estadísticas Base: ---", font=("Segoe UI", 9), foreground=FG_MAIN, wraplength=260, justify="center")
        self.bp_stats_lbl.pack(pady=3)
        
        self.bp_set_btn = ttk.Button(self.bp_card, text="👘 Ver Conjunto en Visor de Sets", command=self._open_selected_piece_set)
        self.bp_set_btn.pack(pady=3)
        
        # Individual Actions Box
        indiv_box = ttk.LabelFrame(self.bp_card, text="Acciones Individuales para esta Pieza", padding=8)
        indiv_box.pack(fill="x", pady=4)
        
        act_r1 = ttk.Frame(indiv_box)
        act_r1.pack(fill="x", pady=2)
        ttk.Label(act_r1, text="Nivel:").pack(side="left", padx=2)
        self.bp_single_lvl_var = tk.StringVar(value="4")
        cb_slvl = ttk.Combobox(act_r1, textvariable=self.bp_single_lvl_var, values=["1", "2", "3", "4"], width=3, state="readonly")
        cb_slvl.pack(side="left", padx=2)
        ttk.Button(act_r1, text="⭐ Desbloquear en Tienda", style="Accent.TButton", command=self._unlock_single_bp_shop).pack(side="left", padx=4, fill="x", expand=True)
        
        act_r2 = ttk.Frame(indiv_box)
        act_r2.pack(fill="x", pady=2)
        ttk.Button(act_r2, text="📦 Enviar 1 u. al Almacén", command=self._deliver_single_bp_to_storage).pack(side="left", padx=2, fill="x", expand=True)
        
        act_r3 = ttk.Frame(indiv_box)
        act_r3.pack(fill="x", pady=2)
        ttk.Button(act_r3, text="🛠️ Depositar Kit de Forja (+10 u.)", style="Accent.TButton", command=self._deposit_crafting_kit_for_selected_bp).pack(fill="x", expand=True)

        # Endgame Sets Injector Box
        endgame_box = ttk.LabelFrame(self.bp_card, text="🛡️ Inyector de Sets Endgame", padding=8)
        endgame_box.pack(fill="x", pady=4)
        
        self.endgame_set_var = tk.StringVar(value="44CE White Steel (D.O.D. Arms)")
        set_choices = [
            "44CE White Steel (D.O.D. Arms)",
            "44CE Red Napalm (War Ensemble)",
            "44CE Black Thunder (Candle Wolf)",
            "44CE Pale Wind (M.I.L.K.)",
            "Sets Jackals v1 / v2 / v3",
            "Armas Legendarias de Tengoku (51F+)"
        ]
        cb_endgame = ttk.Combobox(endgame_box, textvariable=self.endgame_set_var, values=set_choices, state="readonly", width=28)
        cb_endgame.pack(fill="x", pady=2)
        ttk.Button(endgame_box, text="🛡️ Inyectar Set Completo al Almacén", style="Accent.TButton", command=self._inject_endgame_set_action).pack(fill="x", pady=2)

        # Global Equipment Modifiers Box
        global_gear_box = ttk.LabelFrame(self.bp_card, text="⚡ Modificadores de Equipamiento", padding=8)
        global_gear_box.pack(fill="x", pady=4)
        
        ttk.Button(global_gear_box, text="✨ Durabilidad Infinita (999,999) en Todo", command=self._set_infinite_durability_action).pack(fill="x", pady=2)
        ttk.Button(global_gear_box, text="🔫 Munición Masiva (9,999) en Armas", command=self._set_massive_ammo_action).pack(fill="x", pady=2)
        ttk.Button(global_gear_box, text="⭐ Subir Todo a Nivel +19 (Uncapped)", command=self._upgrade_all_gear_max_lvl_action).pack(fill="x", pady=2)

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
        self.bp_faction_lbl.config(text=f"{slot} • {faction}")
        self.bp_status_lbl.config(text=f"Forja: {status} | Almacén: {storage_str} | Bolsa: {bag_str}")
        
        # Check if this item belongs to an armor set
        lookup_id = ptid
        if lookup_id not in self.armor_set_by_item_id and lookup_id.endswith("_G"):
            lookup_id = lookup_id[:-2]
            
        if lookup_id in self.armor_set_by_item_id:
            set_obj, tier_obj, piece_obj = self.armor_set_by_item_id[lookup_id]
            set_title = set_obj.get("name_es") or set_obj.get("name_en", "")
            self.bp_set_btn.config(text=f"👘 Ver Conjunto: {set_title}", state="normal")
            if "def" in piece_obj:
                self.bp_stats_lbl.config(text=f"Defensa Base: {piece_obj.get('def', '-')} (Def+4: {piece_obj.get('def_plus4', '-')}) | Durabilidad: {piece_obj.get('durability', '-')}")
            elif "atk" in piece_obj:
                self.bp_stats_lbl.config(text=f"Ataque Base: {piece_obj.get('atk', '-')} (Atk+4: {piece_obj.get('atk_plus4', '-')}) | Durabilidad: {piece_obj.get('durability', '-')}")
            else:
                self.bp_stats_lbl.config(text=f"Conjunto: {set_title}")
        else:
            self.bp_set_btn.config(text="👘 No pertenece a un conjunto", state="disabled")
            self.bp_stats_lbl.config(text="Pieza individual de equipamiento o arma")
            
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
            messagebox.showwarning("Aviso", "No se encontró la enciclopedia de sets de armadura.")
            return
        ArmorSetViewerDialog(self, self.save_json, self.armor_sets)

    def _open_smart_analyzer(self):
        if not self.save_json:
            messagebox.showwarning("Aviso", "Carga una partida primero.")
            return
        SmartInventoryAnalyzerDialog(self, self.save_json, on_modified_cb=self.refresh_all_views)

    def _open_storage_manager(self):
        if not self.save_json:
            messagebox.showwarning("Aviso", "Carga una partida primero.")
            return
        StorageManagerDialog(self, self.save_json, on_modified_cb=self.refresh_all_views)

    def _check_app_updates(self):
        updater.check_updates_background(self, silent=False)

    def _unlock_single_bp_shop(self):
        if not self.current_bp_selection or not self.save_json:
            return
        ptid = self.current_bp_selection
        try:
            lvl = int(self.bp_single_lvl_var.get())
        except ValueError:
            lvl = 4
        modifiers.unlock_single_blueprint(self.save_json, ptid, level=lvl)
        self._auto_save()
        self.filter_blueprints_list()
        self.status_var.set(f"Plano {ptid} desbloqueado al Nivel +{lvl} en Chokufunsha.")
        messagebox.showinfo("Plano Desbloqueado", f"¡Plano {ptid} registrado al Nivel +{lvl} en Chokufunsha!\nGuardado automáticamente.")

    def _deliver_single_bp_to_storage(self):
        if not self.current_bp_selection or not self.save_json:
            return
        ptid = self.current_bp_selection
        try:
            lvl = int(self.bp_single_lvl_var.get())
        except ValueError:
            lvl = 4
        modifiers.add_equipment_to_storage(self.save_json, ptid, count=1, lvl=lvl, dur=50000)
        self._auto_save()
        self.filter_blueprints_list()
        self.status_var.set(f"Enviada 1 u. de {ptid} al Almacén (Nivel +{lvl}).")
        messagebox.showinfo("Objeto Entregado", f"¡Se ha entregado 1 unidad de {ptid} al 100% de durabilidad en tu Almacén!\nGuardado automáticamente.")

    def _set_collab_filter(self, mode):
        if hasattr(self, "bp_collab_filter"):
            self.bp_collab_filter.set(mode)
            self.filter_blueprints_list()

    def _deposit_crafting_kit_for_selected_bp(self):
        if not self.current_bp_selection or not self.save_json:
            messagebox.showwarning("Aviso", "Selecciona una pieza o plano primero.")
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
        if "WAR" in raw_fac: fac_code = "SPO"
        elif "CANDLE" in raw_fac: fac_code = "FAN"
        elif "MILK" in raw_fac or "M.I.L.K" in raw_fac: fac_code = "MIL"
        
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
        self.status_var.set(f"¡Kit de forja (+10 u. de metales y materiales Tier {tier_num}) depositado para {name_lbl}!")
        messagebox.showinfo("Kit de Forja Depositado", f"¡Se han añadido 10 unidades de metales oficiales y materiales Tier {tier_num} a tu Almacén para forjar:\n{name_lbl}!\nGuardado automáticamente.")

    def unlock_all_blueprints_preset(self):
        if not self.save_json:
            return
        try:
            lvl = int(self.bp_unlock_all_lvl_var.get())
        except ValueError:
            lvl = 4
        modifiers.unlock_all_blueprints(self.save_json, level=lvl)
        self._auto_save()
        self.filter_blueprints_list()
        self.status_var.set(f"¡Todos los 1,370 planos desbloqueados al Nivel +{lvl} en Chokufunsha!")
        messagebox.showinfo("Planos Desbloqueados", f"¡Todos los 1,370 planos han sido desbloqueados al Nivel +{lvl} en Chokufunsha!\nGuardado automáticamente.")

    def _repair_blueprints_action(self):
        if not self.save_json:
            return
        fixed = modifiers.repair_unlocked_blueprints_states(self.save_json)
        self._auto_save()
        self.filter_blueprints_list()
        self.status_var.set(f"¡Se han reparado {fixed} planos en Chokufunsha!")
        messagebox.showinfo("Planos Reparados", f"¡Se han reparado {fixed} planos para asegurar que estén listos para fabricar y comprar en Chokufunsha!")

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
        
        name, added = modifiers.inject_endgame_set(self.save_json, set_key=key, count=1, dur=999999, lvl=5)
        self._auto_save()
        self.filter_blueprints_list()
        self.refresh_all_views()
        self.status_var.set(f"Set '{name}' inyectado ({added} piezas con durabilidad 999k).")
        messagebox.showinfo("Set Endgame Inyectado", f"¡Se han añadido las {added} piezas del set:\n\n🛡️ {name}\n\nCon durabilidad de 999,999 y nivel máximo en tu Almacén y Chokufunsha!")

    def _set_infinite_durability_action(self):
        if not self.save_json:
            return
        cnt = modifiers.set_infinite_durability_all_equipment(self.save_json, target_dur=999999)
        self._auto_save()
        self.refresh_all_views()
        self.status_var.set(f"¡Durabilidad infinita (999k) aplicada a {cnt} piezas de equipo!")
        messagebox.showinfo("Durabilidad Infinita", f"¡Se ha establecido durabilidad de 999,999 en {cnt} piezas de armas y armaduras en tu Almacén y Bolsas!\n\n¡Tu equipo nunca se romperá!")

    def _set_massive_ammo_action(self):
        if not self.save_json:
            return
        cnt = modifiers.set_massive_ammo_all_weapons(self.save_json, ammo=9999)
        self._auto_save()
        self.refresh_all_views()
        self.status_var.set(f"¡Munición masiva (9,999 balas) aplicada a {cnt} armas!")
        messagebox.showinfo("Munición Masiva", f"¡Se han configurado 9,999 balas directas en cargador y reserva para {cnt} armas a distancia en tu Almacén!")

    def _upgrade_all_gear_max_lvl_action(self):
        if not self.save_json:
            return
        cnt = modifiers.upgrade_all_equipment_max_level(self.save_json, target_lvl=19)
        self._auto_save()
        self.refresh_all_views()
        self.status_var.set(f"¡{cnt} piezas de equipo mejoradas a Nivel +19 (Uncapped)!")
        messagebox.showinfo("Equipo al Máximo", f"¡Se han mejorado {cnt} piezas de armas y armaduras a Nivel +19 (Uncapped de Tengoku) en tu Almacén!")

    def filter_blueprints_list(self):
        for row in self.bp_tree.get_children():
            self.bp_tree.delete(row)
            
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
            if cat_filter != "Todos":
                if cat_filter == "🪖 Cascos" and slot_key != "head": continue
                elif cat_filter == "👕 Pechos" and slot_key != "chest": continue
                elif cat_filter == "👖 Piernas" and slot_key != "legs": continue
                elif cat_filter == "⚔️ Armas" and slot_key != "weapon": continue
                
            # 2. Filter by Faction
            if fac_filter != "Todas" and faction != fac_filter:
                continue
                
            # 3. Forge status
            if bp_id in pr_map:
                forge_info = pr_map[bp_id]
                forge_status = forge_info["label"]
                forge_code = forge_info["status"]
            else:
                forge_status = "❌ Bloqueado"
                forge_code = "LOCKED"
                
            storage_count = storage_gear.get(bp_id, 0)
            bag_count = bag_gear.get(bp_id, 0)
            
            # 4. Filter by Possession
            if poss_filter == "📦 En Almacén (> 0)" and storage_count <= 0:
                continue
            elif poss_filter == "⭐ Desbloqueados en Tienda (+4)" and forge_code != "STORE_PLUS4":
                continue
            elif poss_filter == "🔨 En I+D (REMODEL / MAP)" and forge_code not in ("REMODEL", "MAP"):
                continue
            elif poss_filter == "❌ Bloqueados (Faltantes)" and forge_code != "LOCKED":
                continue

            # 4b. Filter by Damage Type (Weapons only)
            dmg_filter = self.bp_dmg_type_var.get() if hasattr(self, "bp_dmg_type_var") else "Todos"
            if dmg_filter != "Todos":
                if slot_key != "weapon":
                    continue
                w_dmg = self._get_weapon_damage_type(item)
                if "Corte" in dmg_filter and w_dmg != "SLASH": continue
                elif "Golpe" in dmg_filter and w_dmg != "BLUNT": continue
                elif "Perforación" in dmg_filter and w_dmg != "PIERCE": continue
                elif "Fuego" in dmg_filter and w_dmg != "FIRE": continue
                elif "Electricidad" in dmg_filter and w_dmg != "ELECTRIC": continue
                elif "Veneno" in dmg_filter and w_dmg != "POISON": continue
                
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
                    
            display_title = f"{name_es} ({name_en})" if name_en and name_en != name_es else name_es
            storage_str = f"{storage_count} u." if storage_count > 0 else "-"
            bag_str = f"{bag_count} u." if bag_count > 0 else "-"
            
            tag = "tag_shop" if forge_code == "STORE_PLUS4" else ("tag_remodel" if forge_code in ("REMODEL", "MAP") else "tag_locked")
            
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
        
        ttk.Label(top_ctrl, text="Nivel Deseado:").pack(side="left", padx=4)
        self.mastery_target_lvl_var = tk.StringVar(value="20")
        cb_m_lvl = ttk.Combobox(top_ctrl, textvariable=self.mastery_target_lvl_var, values=[str(i) for i in range(1, 21)], width=4, state="readonly")
        cb_m_lvl.pack(side="left", padx=2)
        
        btn_max_m = ttk.Button(top_ctrl, text="⭐ Establecer TODAS las Maestrías", style="Accent.TButton", command=self.max_all_mastery)
        btn_max_m.pack(side="left", padx=6)
        
        self.mastery_tree = ttk.Treeview(self.tab_mastery, columns=("id", "lvl", "points"), show="tree headings", height=15)
        self.mastery_tree.heading("#0", text="Tipo de Arma")
        self.mastery_tree.heading("id", text="Código Interno")
        self.mastery_tree.heading("lvl", text="Nivel de Maestría")
        self.mastery_tree.heading("points", text="Puntos de Experiencia (EXP)")
        
        self.mastery_tree.column("#0", width=260)
        self.mastery_tree.column("id", width=140)
        self.mastery_tree.column("lvl", width=140, anchor="center")
        self.mastery_tree.column("points", width=180, anchor="center")
        
        self.mastery_tree.pack(fill="both", expand=True, pady=4)
        self.mastery_tree.bind("<Double-1>", self._edit_mastery_level)

    def filter_mastery_list(self):
        for row in self.mastery_tree.get_children():
            self.mastery_tree.delete(row)
            
        if not self.save_json:
            return
            
        expert_list = self.save_json.get("soul", {}).get("expert", [])
        
        for item in expert_list:
            k = item.get("ptarmtp", "PTARMTP_00")
            lvl = item.get("lvl", 1)
            pts = item.get("abp", 0)
            
            name_es = EXPERT_WEAPON_NAMES.get(k, f"Arma Especial ({k})")
            ico_file = WEAPON_MASTERY_ICONS.get(k, "weapon")
            thumb = self.get_photo(ico_file, (28, 28), preserve_aspect=True) or self.get_photo("weapon", (24, 24))
            node_id = self.mastery_tree.insert("", "end", text=f" {name_es}", image=thumb or "", values=(k, f"Nivel {lvl} / 20", f"{pts:,} ABP"))
            self.tree_images[node_id] = thumb

    def _edit_mastery_level(self, event):
        sel = self.mastery_tree.selection()
        if not sel:
            return
        node = sel[0]
        vals = self.mastery_tree.item(node, "values")
        arm_type = vals[0]
        
        new_lvl = simpledialog.askinteger("Nivel de Maestría", f"Ingresa el nivel para {arm_type} (1 a 20):", minvalue=1, maxvalue=20, initialvalue=20)
        if new_lvl is not None:
            modifiers.set_weapon_mastery(self.save_json, arm_type, level=new_lvl)
            self._auto_save()
            self.filter_mastery_list()
            self.status_var.set(f"Maestría de {arm_type} establecida al Nivel {new_lvl}.")
            messagebox.showinfo("Maestría Actualizada", f"Maestría de {arm_type} establecida al Nivel {new_lvl}.\nGuardado automáticamente.")

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
        self.status_var.set(f"Todas las maestrías de armas establecidas al Nivel {lvl}.")
        messagebox.showinfo("Éxito", f"¡Todas las 57 maestrías de armas han sido establecidas al Nivel {lvl}!\nGuardado automáticamente.")

    # ================= TAB 7: TOWER & MASTER UNLOCKS =================
    def _build_tower_tab(self):
        self.tab_tower.columnconfigure(0, weight=1, uniform="tab7")
        self.tab_tower.columnconfigure(1, weight=1, uniform="tab7")
        self.tab_tower.rowconfigure(0, weight=1)
        
        # Left Panel: Tower, Elevators & Stamps
        box_left = ttk.LabelFrame(self.tab_tower, text="Torre de Barbs, Ascensores y Stamp Rally", padding=12)
        box_left.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        
        # 1. Elevators
        ttk.Label(box_left, text="🛗 Ascensores y Pisos de la Torre (1 al 51+ Tengoku)", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        ttk.Label(box_left, text="Desbloquea el acceso directo a todos los pisos del 1 al 40, Battle Royale 41-50 y Tengoku.", font=("Segoe UI", 8), foreground=FG_MUTED).pack(anchor="w", pady=1)
        btn_unlock_elevators = ttk.Button(box_left, text="🛗 Desbloquear TODOS los Ascensores y Pisos", style="Accent.TButton", command=self._unlock_elevators_action)
        btn_unlock_elevators.pack(fill="x", pady=(2, 8))
        
        # 2. Stamp Rally Perfect
        ttk.Label(box_left, text="🎯 Stamp Rally 100% Perfecto (Sellos del Tío Death)", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        ttk.Label(box_left, text="Marca todos los sellos de la Torre en PERFECT. Desbloquea la Guadaña del Tío Death.", font=("Segoe UI", 8), foreground=FG_MUTED).pack(anchor="w", pady=1)
        btn_stamps_perfect = ttk.Button(box_left, text="⭐ Completar Sellos en PERFECT (Desbloquea Guadaña)", style="Accent.TButton", command=self._set_stamps_perfect_action)
        btn_stamps_perfect.pack(fill="x", pady=(2, 8))
        
        # 3. Death Bag Expansion
        ttk.Label(box_left, text="🎒 Expansión de la Bolsa de la Muerte", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        bag_f = ttk.Frame(box_left)
        bag_f.pack(fill="x", pady=2)
        ttk.Label(bag_f, text="Capacidad de Slots:").pack(side="left", padx=4)
        self.bag_slots_var = tk.StringVar(value="50")
        cb_bag = ttk.Combobox(bag_f, textvariable=self.bag_slots_var, values=["20", "25", "30", "35", "40", "45", "50", "60"], state="readonly", width=8)
        cb_bag.pack(side="left", padx=4)
        btn_expand_bag = ttk.Button(bag_f, text="🎒 Expandir Bolsa", command=self._expand_bag_action)
        btn_expand_bag.pack(side="left", padx=4)
        
        # 4. Free Continues
        ttk.Separator(box_left, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(box_left, text="♾️ Revives / Continues Gratuitos Ilimitados", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        cont_f = ttk.Frame(box_left)
        cont_f.pack(fill="x", pady=2)
        ttk.Label(cont_f, text="Continues Gratis:").pack(side="left", padx=4)
        self.free_cont_var = tk.StringVar(value="999")
        ttk.Entry(cont_f, textvariable=self.free_cont_var, width=8, justify="center").pack(side="left", padx=4)
        btn_set_cont = ttk.Button(cont_f, text="♾️ Establecer Continues", command=self._set_continues_action)
        btn_set_cont.pack(side="left", padx=4)

        # 4b. Tower Secret Shop & Death Boxes Utilities
        ttk.Separator(box_left, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(box_left, text="🛒 Tienda Secreta y Cajas de Muerte", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        btn_reset_shop = ttk.Button(box_left, text="🛒 Resetear Cooldown Tienda Gyaku-Funsha", command=self._reset_wandering_shop_action)
        btn_reset_shop.pack(fill="x", pady=2)
        btn_open_boxes = ttk.Button(box_left, text="📦 Abrir Inmediatamente Cajas de Muerte (Lost Bags)", command=self._open_deathboxes_action)
        btn_open_boxes.pack(fill="x", pady=2)

        # Right Panel: TDM, Rewards Box & Encyclopedia Books
        box_right = ttk.LabelFrame(self.tab_tower, text="Tokyo Death Metro, Buzón y Compendios", padding=12)
        box_right.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        
        # 5. TDM Rank & Points
        ttk.Label(box_right, text="🏆 Rango y Puntuación TDM (Tokyo Death Metro)", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        tdm_f = ttk.Frame(box_right)
        tdm_f.pack(fill="x", pady=2)
        ttk.Label(tdm_f, text="Rango:").pack(side="left", padx=2)
        self.tdm_rank_var = tk.StringVar(value="Diamante I (Diamond I - 3,500+ pts)")
        tdm_ranks = [
            "Diamante I (Diamond I - 3,500+ pts)",
            "Diamante II (Diamond II - 3,200 pts)",
            "Diamante III (Diamond III - 3,000 pts)",
            "Platino I (Platinum I - 2,500 pts)",
            "Oro I (Gold I - 1,800 pts)",
            "Plata I (Silver I - 1,200 pts)",
            "Bronce I (Bronze I - 500 pts)"
        ]
        cb_tdm = ttk.Combobox(tdm_f, textvariable=self.tdm_rank_var, values=tdm_ranks, state="readonly", width=28)
        cb_tdm.pack(side="left", padx=2)
        btn_set_tdm = ttk.Button(tdm_f, text="🏆 Aplicar", style="Accent.TButton", command=self._set_tdm_rank_action)
        btn_set_tdm.pack(side="left", padx=2)
        
        # 6. Rewards Box Injector (soul.present)
        ttk.Label(box_right, text="📬 Inyector a la Caja de Recompensas (Rewards Box)", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=(8, 2))
        ttk.Label(box_right, text="Envía recursos directamente a tu buzón para acumularlos sin límite de capacidad.", font=("Segoe UI", 8), foreground=FG_MUTED).pack(anchor="w", pady=1)
        
        p_cust = ttk.Frame(box_right)
        p_cust.pack(fill="x", pady=4)
        ttk.Label(p_cust, text="Recurso:").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.rb_type_var = tk.StringVar(value="Kill Coins (MONEY)")
        cb_rb_t = ttk.Combobox(p_cust, textvariable=self.rb_type_var, values=["Kill Coins (MONEY)", "Litio SPLithium (SPL)", "Metales de Muerte (DM)"], state="readonly", width=22)
        cb_rb_t.grid(row=0, column=1, padx=2, pady=2)
        
        ttk.Label(p_cust, text="Cantidad:").grid(row=1, column=0, sticky="w", padx=2, pady=2)
        self.rb_qty_var = tk.StringVar(value="1000000")
        ttk.Entry(p_cust, textvariable=self.rb_qty_var, width=12, justify="center").grid(row=1, column=1, padx=2, pady=2, sticky="w")
        ttk.Button(p_cust, text="📬 Enviar Regalo al Buzón", style="Accent.TButton", command=self._send_custom_reward_box).grid(row=1, column=2, padx=4, pady=2)

        # 7. Compendiums & Hub Customization
        ttk.Separator(box_right, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(box_right, text="📖 Compendios y Personalización de Sala", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        btn_comp = ttk.Button(box_right, text="📖 Completar Compendios del Tío Death (63 Setas + 24 Bestias)", style="Accent.TButton", command=self._complete_compendiums_action)
        btn_comp.pack(fill="x", pady=2)
        btn_hub = ttk.Button(box_right, text="🎨 Desbloquear Todas las Personalizaciones de Sala de Espera (113)", command=self._unlock_hub_action)
        btn_hub.pack(fill="x", pady=2)
        btn_quests = ttk.Button(box_right, text="🎖️ Completar Todas las Misiones Oficiales (232 Quests)", style="Accent.TButton", command=self._complete_all_quests_action)
        btn_quests.pack(fill="x", pady=2)
        btn_media = ttk.Button(box_right, text="📻 Desbloquear Colección de Revistas (36) y Radio Jukebox", command=self._unlock_magazines_and_radio_action)
        btn_media.pack(fill="x", pady=2)

    def _complete_all_quests_action(self):
        if not self.save_json:
            return
        cnt = modifiers.complete_all_quests(self.save_json)
        self._auto_save()
        self.status_var.set(f"¡{cnt} misiones oficiales completadas!")
        messagebox.showinfo("Misiones Completadas", f"¡Se han marcado como completadas {cnt} misiones oficiales de la Torre de Barbs!\n\nPuedes recoger cientos de Death Metals, metales raros y planos en tu Buzón de Recompensas.")

    def _unlock_magazines_and_radio_action(self):
        if not self.save_json:
            return
        modifiers.unlock_all_magazines(self.save_json)
        modifiers.unlock_all_radio_music(self.save_json)
        self._auto_save()
        self.status_var.set("¡Todas las 36 revistas y música de radio desbloqueadas!")
        messagebox.showinfo("Coleccionables Desbloqueados", "¡Se han desbloqueado las 36 revistas y cómics del Tío Death y se ha habilitado la Gramola de Radio con todos los canales!")

    def _unlock_elevators_action(self):
        if not self.save_json:
            return
        modifiers.unlock_all_elevators(self.save_json)
        self._auto_save()
        self.status_var.set("¡Todos los pisos y ascensores desbloqueados!")
        messagebox.showinfo("Ascensores Desbloqueados", "¡Se ha habilitado el acceso completo a todos los pisos de la Torre de Barbs (1 al 51+ Tengoku) y ascensores gratuitos!")

    def _set_stamps_perfect_action(self):
        if not self.save_json:
            return
        modifiers.set_all_stamps_perfect(self.save_json)
        self._auto_save()
        self.status_var.set("¡Todos los sellos marcados en PERFECT y Guadaña desbloqueada!")
        messagebox.showinfo("Sellos en PERFECT", "¡Todos los 40 sellos del Stamp Rally marcados en PERFECT!\n\nGuadaña del Tío Death desbloqueada al Nivel +4 en Chokufunsha y 1 unidad entregada en tu Almacén.")

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
        self.status_var.set(f"Bolsa expandida a {slots} slots.")
        messagebox.showinfo("Bolsa Expandida", f"¡Bolsa del luchador actual ampliada a {slots} casillas!")

    def _set_continues_action(self):
        if not self.save_json:
            return
        try:
            cnt = int(self.free_cont_var.get())
        except ValueError:
            cnt = 999
        modifiers.set_free_continues(self.save_json, count=cnt)
        self._auto_save()
        self.status_var.set(f"Continues gratis establecidos a {cnt}.")
        messagebox.showinfo("Continues Establecidos", f"¡Se han otorgado {cnt} revives gratuitos ilimitados en la torre!")

    def _set_tdm_rank_action(self):
        if not self.save_json:
            return
        sel = self.tdm_rank_var.get()
        rank_id = "TDM_RANK_05_03"
        points = 5000
        if "Diamante II" in sel: rank_id, points = "TDM_RANK_05_02", 3200
        elif "Diamante III" in sel: rank_id, points = "TDM_RANK_05_01", 3000
        elif "Platino" in sel: rank_id, points = "TDM_RANK_04_03", 2500
        elif "Oro" in sel: rank_id, points = "TDM_RANK_03_03", 1800
        elif "Plata" in sel: rank_id, points = "TDM_RANK_02_03", 1200
        elif "Bronce" in sel: rank_id, points = "TDM_RANK_01_03", 500
        
        modifiers.set_tdm_rank(self.save_json, rank_id=rank_id, points=points)
        self._auto_save()
        self.refresh_all_views()
        self.status_var.set(f"Rango TDM establecido a {sel}.")
        messagebox.showinfo("Rango TDM Actualizado", f"¡Rango de Tokyo Death Metro establecido a {sel} con {points:,} puntos!")

    def _send_custom_reward_box(self):
        if not self.save_json:
            return
        t_sel = self.rb_type_var.get()
        try:
            qty = int(self.rb_qty_var.get())
        except ValueError:
            qty = 1000000
            
        p_type = "MONEY"
        if "SPL" in t_sel: p_type = "SPL"
        elif "DM" in t_sel: p_type = "DM"
        
        modifiers.send_present_to_reward_box(self.save_json, p_type=p_type, num=qty)
        self._auto_save()
        self.status_var.set(f"Enviado {qty:,} de {t_sel} al Buzón de Recompensas.")
        messagebox.showinfo("Regalo Enviado", f"¡Se han enviado {qty:,} {t_sel} directamente a tu Buzón de Recompensas en la Sala de Espera!")

    def _complete_compendiums_action(self):
        if not self.save_json:
            return
        m_cnt, b_cnt = modifiers.complete_encyclopedia_books(self.save_json)
        self._auto_save()
        self.status_var.set("¡Compendios del Tío Death completados (63 Setas, 24 Bestias)!")
        messagebox.showinfo("Compendios Completados", "¡Se han registrado al 100% las 63 Setas y 24 Bestias en el Libro del Tío Death!\n\nMarcadas como descubiertas, comidas, lanzadas y cocinadas.")

    def _unlock_hub_action(self):
        if not self.save_json:
            return
        total, unlocked = modifiers.unlock_all_hub_customizations(self.save_json)
        self._auto_save()
        self.status_var.set(f"¡{unlocked} decoraciones de Sala de Espera desbloqueadas!")
        messagebox.showinfo("Sala de Espera Desbloqueada", f"¡Se han desbloqueado todas las {total} personalizaciones oficiales de la Sala de Espera!\n\nIncluye todos los suelos, fuentes, postes, banderas y skins temáticas de temporada (Primavera, Verano, Otoño, Invierno y WOT).")

    def _open_deathboxes_action(self):
        if not self.save_json:
            return
        count = modifiers.instant_open_deathboxes(self.save_json)
        self._auto_save()
        self.status_var.set(f"¡{count} Cajas de Muerte listas para abrir!")
        messagebox.showinfo("Cajas de Muerte Desbloqueadas", f"¡Se ha eliminado el temporizador de {count} cajas de muerte / bolsas perdidas!\n\nYa puedes recogerlas al instante en tu Sala de Espera.")

    def _reset_wandering_shop_action(self):
        if not self.save_json:
            return
        modifiers.reset_wandering_shop_timer(self.save_json)
        self._auto_save()
        self.status_var.set("¡Tienda ambulante Gyaku-Funsha reseteada con éxito!")
        messagebox.showinfo("Tienda Reseteada", "¡Se ha reseteado el temporizador de Chokufunsha ambulante!\n\nLa tienda secreta reaparecerá de inmediato al entrar en un piso de tienda en la Torre de Barbs.")

    # ================= TAB 8: ADVANCED & BACKUPS =================
    def _build_advanced_tab(self):
        self.tab_advanced.columnconfigure(0, weight=1)
        self.tab_advanced.columnconfigure(1, weight=1)
        
        # Left: Backup Manager
        box_bak = ttk.LabelFrame(self.tab_advanced, text="🛡️ Gestor de Respaldos de Seguridad (.bak)", padding=12)
        box_bak.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        
        self.backups_tree = ttk.Treeview(box_bak, columns=("date", "size"), show="tree headings", height=12)
        self.backups_tree.heading("#0", text="Archivo de Respaldo")
        self.backups_tree.heading("date", text="Fecha de Creación")
        self.backups_tree.heading("size", text="Tamaño")
        
        self.backups_tree.column("#0", width=220)
        self.backups_tree.column("date", width=140, anchor="center")
        self.backups_tree.column("size", width=80, anchor="center")
        
        self.backups_tree.pack(fill="both", expand=True, pady=4)
        
        btn_f = ttk.Frame(box_bak)
        btn_f.pack(fill="x", pady=4)
        ttk.Button(btn_f, text="🛡️ Crear Nuevo Respaldo", style="Accent.TButton", command=self.create_manual_backup).pack(side="left", padx=2, fill="x", expand=True)
        ttk.Button(btn_f, text="🔄 Restaurar Respaldo", command=self._restore_selected_backup).pack(side="left", padx=2, fill="x", expand=True)
        
        # Right: JSON Tools & Wiki Links
        box_tools = ttk.LabelFrame(self.tab_advanced, text="🛠️ Herramientas Avanzadas y Enlaces Oficiales", padding=12)
        box_tools.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        
        ttk.Label(box_tools, text="Exportar / Importar Partida en JSON legible:", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        json_f = ttk.Frame(box_tools)
        json_f.pack(fill="x", pady=4)
        ttk.Button(json_f, text="📤 Exportar a JSON", command=self.export_json).pack(side="left", padx=2, fill="x", expand=True)
        ttk.Button(json_f, text="📥 Importar desde JSON", command=self.import_json).pack(side="left", padx=2, fill="x", expand=True)
        
        ttk.Separator(box_tools, orient="horizontal").pack(fill="x", pady=10)
        ttk.Label(box_tools, text="Enlaces y Recursos de la Comunidad:", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        ttk.Label(box_tools, text="• Wiki Oficial: letitdie.wiki.gg\n• Forja y R&D: Chokufunsha Complete DB\n• Calculadora de Daño y Stats", font=("Segoe UI", 8), foreground=FG_MUTED).pack(anchor="w", pady=2)

    def refresh_backups_list(self):
        for row in self.backups_tree.get_children():
            self.backups_tree.delete(row)
            
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
            messagebox.showwarning("Aviso", "Selecciona un respaldo para restaurar.")
            return
        node = sel[0]
        bak_name = self.backups_tree.item(node, "text").strip()
        
        # Check both directories
        save_dir = os.path.dirname(self.save_path)
        bak_path = os.path.join(save_dir, bak_name)
        if not os.path.exists(bak_path):
            bak_path = os.path.join(save_io.PROJECT_BACKUPS_DIR, bak_name)
            
        if not os.path.exists(bak_path):
            messagebox.showerror("Error", f"No se encontró el archivo de respaldo:\n{bak_name}")
            return
        
        if messagebox.askyesno("Confirmar Restauración", f"¿Estás seguro de restaurar el respaldo:\n{bak_name}?\n\nSobrescribirá tu archivo .sav actual."):
            try:
                save_io.restore_backup(bak_path, self.save_path)
                self.load_save(self.save_path)
                messagebox.showinfo("Respaldo Restaurado", "¡Partida restaurada con éxito desde el respaldo seleccionado!")
            except Exception as e:
                messagebox.showerror("Error", f"Error al restaurar respaldo:\n{e}")

    # ================= GENERAL APP LOGIC =================
    def browse_save(self):
        f = filedialog.askopenfilename(
            title="Seleccionar archivo de guardado de LET IT DIE",
            filetypes=[("Archivos de Partida LET IT DIE", "*.sav"), ("Todos los archivos", "*.*")],
            initialdir=os.path.dirname(self.save_path) if self.save_path else None
        )
        if f:
            self.save_path = f
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, f)
            self.load_save(f)

    def load_save(self, path):
        if not os.path.exists(path):
            messagebox.showerror("Error", f"No se encontró el archivo:\n{path}")
            return
        try:
            data, ver = decompress_save(path)
            self.save_json = data
            self.version = ver
            self.save_path = path
            self.refresh_all_views()
            self.status_var.set(f"Partida cargada con éxito: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Error de Carga", f"Error al descompromir la partida:\n{e}")

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
        if vip_info.get("active"):
            self.vip_status_lbl.config(text=f"Estado: ACTIVO • Expira en: {vip_info.get('days_left', 0)} días ({vip_info.get('expires_at', '')})", foreground=ACCENT_GREEN)
        else:
            self.vip_status_lbl.config(text="Estado: INACTIVO (Haz clic abajo para activar)", foreground=ACCENT_RED)
            
        # Mystery Bags
        mb_info = modifiers.get_mystery_bags_summary(self.save_json)
        self.mystery_status_lbl.config(
            text=f"🌈 Arcoíris: {mb_info.get('RAINBOW', 0)} | ⚪ Platino: {mb_info.get('PLATINUM', 0)} | 🟡 Oro: {mb_info.get('GOLD', 0)} | 🔘 Plata: {mb_info.get('SILVER', 0)} | 🟤 Cobre: {mb_info.get('COPPER', 0)}"
        )
        
        # 2. Update Fighters List
        for row in self.fighters_tree.get_children():
            self.fighters_tree.delete(row)
            
        fighters = modifiers.get_all_fighters_info(self.save_json)
        first_f = None
        for idx, f in enumerate(fighters):
            name = f.get("name", f"Luchador #{idx+1}")
            cls_name = f.get("class_name", "All-Rounder")
            lvl = f.get("level", 1)
            grade = f.get("grade", 1)
            hp = f.get("hp", 1000)
            state = "Vivo" if hp > 0 else "Muerto"
            
            cls_code = f.get("class", "BAL")
            cls_icon_filename = FIGHTER_CLASSES.get(cls_code, ("", "all-rounder.png"))[1]
            thumb = self.get_photo(cls_icon_filename, (36, 36), preserve_aspect=True) or self.get_photo("all-rounder", (36, 36), preserve_aspect=True)
            node_id = self.fighters_tree.insert("", "end", text=f" {name} ({cls_name})", image=thumb or "", values=(idx+1, f"Nv. {lvl} (G{grade})", state))
            self.tree_images[node_id] = thumb
            if idx == 0:
                first_f = node_id
                
        if first_f:
            self.fighters_tree.selection_set(first_f)
            self._on_fighter_select(None)
            
        # Active Fighter Info on top HUD
        if fighters:
            f0 = fighters[0]
            self.player_name_lbl.config(text=f"Luchador: {f0.get('name', 'Principal')} • {f0.get('class_name', 'All-Rounder')} (Tier {f0.get('grade', 1)} ★)")
            self.player_meta_lbl.config(text=f"UID: {self.save_json.get('soul', {}).get('uid', '---')} | Rango Base: {base_up.get('rank', 100)} | 🏆 TDM: Diamante | Bolsa: {f0.get('bag', 20)} slots")
            
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
            self.mat_cap_indicator_lbl.config(text=f"Almacén: {used:,} / {cap:,} casillas ocupadas ({cap - used:,} libres)")

    def create_manual_backup(self):
        if not self.save_path or not os.path.exists(self.save_path):
            messagebox.showwarning("Aviso", "No hay ninguna partida cargada para respaldar.")
            return
        bak_file = save_io.backup_save(self.save_path)
        self.refresh_backups_list()
        self.status_var.set(f"Respaldo creado: {os.path.basename(bak_file)}")
        messagebox.showinfo("Respaldo Creado", f"¡Copia de seguridad creada con éxito!\n\n{bak_file}")

    def save_current(self):
        if not self.save_json or not self.save_path:
            messagebox.showwarning("Aviso", "No hay ninguna partida cargada.")
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
            self.status_var.set(f"Partida guardada y sellada con éxito: {os.path.basename(self.save_path)}")
            messagebox.showinfo("Guardado Exitoso", "¡Partida guardada y re-encriptada con éxito!\n\nTodos los cambios están aplicados en el archivo .sav.")
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudo guardar la partida:\n{e}")

    def export_json(self):
        if not self.save_json:
            messagebox.showwarning("Aviso", "Carga una partida primero.")
            return
        out_p = os.path.join(BASE_DIR, "save_decompressed.json")
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(self.save_json, f, indent=2, ensure_ascii=False)
        self.status_var.set(f"Partida exportada a JSON: {out_p}")
        messagebox.showinfo("Exportado", f"Partida exportada a JSON con éxito:\n{out_p}")

    def import_json(self):
        in_p = os.path.join(BASE_DIR, "save_decompressed.json")
        if not os.path.exists(in_p):
            messagebox.showerror("Error", f"No se encontró {in_p}")
            return
        try:
            with open(in_p, "r", encoding="utf-8") as f:
                self.save_json = json.load(f)
            self.refresh_all_views()
            self._auto_save()
            self.status_var.set("Partida importada desde save_decompressed.json")
            messagebox.showinfo("Importado", "¡Partida importada desde JSON y guardada automáticamente!")
        except Exception as e:
            messagebox.showerror("Error de Importación", f"Error al leer JSON:\n{e}")


class SmartInventoryAnalyzerDialog(tk.Toplevel):
    def __init__(self, parent, save_json, on_modified_cb=None):
        super().__init__(parent)
        self.title("🧠 Analizador Inteligente de Inventario y Forja (R&D) - LET IT DIE")
        self.geometry("880x640")
        self.minsize(740, 520)
        self.configure(bg=BG_DARK)
        self.transient(parent)
        self.grab_set()
        
        self.parent = parent
        self.save_json = save_json
        self.on_modified_cb = on_modified_cb
        
        self._build_ui()
        self.refresh_analysis()
        
    def _build_ui(self):
        # Header banner
        header_frame = tk.Frame(self, bg=BG_PANEL, padx=14, pady=10)
        header_frame.pack(fill="x")
        
        title_lbl = tk.Label(
            header_frame,
            text="🧠 Analizador Inteligente de Inventario y Forja (R&D)",
            font=("Segoe UI", 13, "bold"),
            bg=BG_PANEL,
            fg=ACCENT_GOLD
        )
        title_lbl.pack(anchor="w")
        
        sub_lbl = tk.Label(
            header_frame,
            text="Calcula las necesidades exactas de tus recetas activas en I+D para abastecer tu almacén sin saturarlo ni meter cosas de más.",
            font=("Segoe UI", 9),
            bg=BG_PANEL,
            fg=FG_MUTED
        )
        sub_lbl.pack(anchor="w", pady=(2, 6))
        
        # Storage Capacity indicator
        self.cap_lbl = tk.Label(
            header_frame,
            text="Almacén (Coin Locker): Calculando...",
            font=("Segoe UI", 9, "bold"),
            bg=BG_PANEL,
            fg=FG_MAIN
        )
        self.cap_lbl.pack(anchor="w")
        
        self.cap_bar = ttk.Progressbar(header_frame, orient="horizontal", mode="determinate", length=400)
        self.cap_bar.pack(fill="x", pady=(3, 0))
        
        # Metrics summary row
        metrics_frame = tk.Frame(self, bg=BG_DARK, padx=14, pady=8)
        metrics_frame.pack(fill="x")
        
        self.m_recipes_lbl = self._create_metric_card(metrics_frame, "🔨 Recetas Activas", "---", ACCENT_BLUE)
        self.m_needed_lbl = self._create_metric_card(metrics_frame, "📋 Materiales Requeridos", "---", FG_MAIN)
        self.m_deficit_lbl = self._create_metric_card(metrics_frame, "⚠️ Materiales con Déficit", "---", ACCENT_RED)
        self.m_units_lbl = self._create_metric_card(metrics_frame, "📦 Unidades Faltantes", "---", ACCENT_GOLD)
        
        # Table of Materials
        table_frame = tk.Frame(self, bg=BG_DARK, padx=14, pady=4)
        table_frame.pack(fill="both", expand=True)
        
        cols = ("id", "needed", "stock", "deficit", "status")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="tree headings", height=12)
        
        self.tree.heading("#0", text="Material de Forja (Nombre Oficial)")
        self.tree.heading("id", text="ID Ítem")
        self.tree.heading("needed", text="Requerido por Recetas")
        self.tree.heading("stock", text="En Almacén")
        self.tree.heading("deficit", text="Faltante Neto")
        self.tree.heading("status", text="Estado")
        
        self.tree.column("#0", width=280)
        self.tree.column("id", width=140)
        self.tree.column("needed", width=120, anchor="center")
        self.tree.column("stock", width=90, anchor="center")
        self.tree.column("deficit", width=90, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        
        # Scrollbars
        ysb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        ysb.pack(side="right", fill="y")
        
        # Row tags styling
        self.tree.tag_configure("tag_deficit", foreground=ACCENT_RED)
        self.tree.tag_configure("tag_ok", foreground=ACCENT_GREEN)
        
        # Bottom Actions Bar
        action_bar = tk.Frame(self, bg=BG_PANEL, padx=14, pady=10)
        action_bar.pack(fill="x")
        
        btn_supply_needed = ttk.Button(
            action_bar,
            text="⚡ Suministrar Solo Faltantes para I+D (Sin Excesos)",
            style="Accent.TButton",
            command=self._on_supply_missing
        )
        btn_supply_needed.pack(side="left", padx=4)
        
        btn_top_up = ttk.Button(
            action_bar,
            text="⚖️ Top-Up Inteligente (Rellenar hasta X)",
            command=self._on_smart_top_up
        )
        btn_top_up.pack(side="left", padx=4)
        
        btn_refresh = ttk.Button(
            action_bar,
            text="🔄 Actualizar",
            command=self.refresh_analysis
        )
        btn_refresh.pack(side="left", padx=4)
        
        btn_expand_storage = ttk.Button(
            action_bar,
            text="🚀 Ampliar Almacén",
            command=self._on_expand_storage
        )
        btn_expand_storage.pack(side="left", padx=4)
        
        btn_close = ttk.Button(
            action_bar,
            text="Cerrar",
            command=self.destroy
        )
        btn_close.pack(side="right", padx=4)
        
    def _create_metric_card(self, parent, title, initial_val, color):
        card = tk.Frame(parent, bg=BG_CARD, padx=10, pady=6, highlightbackground=BG_PANEL, highlightthickness=1)
        card.pack(side="left", fill="x", expand=True, padx=4)
        
        t_lbl = tk.Label(card, text=title, font=("Segoe UI", 8), bg=BG_CARD, fg=FG_MUTED)
        t_lbl.pack(anchor="w")
        
        v_lbl = tk.Label(card, text=initial_val, font=("Segoe UI", 13, "bold"), bg=BG_CARD, fg=color)
        v_lbl.pack(anchor="w")
        return v_lbl
        
    def refresh_analysis(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
            
        res = modifiers.analyze_active_recipes_materials(self.save_json)
        
        # Storage bar
        used = res["storage_used"]
        tot = res["storage_total"]
        free = res["storage_free"]
        pct = (used / tot * 100) if tot > 0 else 0
        self.cap_lbl.config(text=f"Almacén (Coin Locker): {used:,} / {tot:,} casillas ocupadas ({free:,} libres - {pct:.1f}% lleno)")
        self.cap_bar["maximum"] = tot
        self.cap_bar["value"] = used
        
        # Metrics
        deficit_items = [m for m in res["materials"] if m["deficit"] > 0]
        total_deficit_units = sum(m["deficit"] for m in deficit_items)
        
        self.m_recipes_lbl.config(text=str(res["total_active_recipes"]))
        self.m_needed_lbl.config(text=f"{res['total_materials_needed']} tipos")
        self.m_deficit_lbl.config(text=f"{len(deficit_items)} tipos")
        self.m_units_lbl.config(text=f"{total_deficit_units} u.")
        
        # Populate table
        for m in res["materials"]:
            tag = "tag_deficit" if m["deficit"] > 0 else "tag_ok"
            status_text = f"⚠️ FALTA (-{m['deficit']})" if m["deficit"] > 0 else "✅ OK"
            self.tree.insert(
                "",
                "end",
                text=m["name"],
                values=(m["itemid"], m["needed"], m["stock"], m["deficit"], status_text),
                tags=(tag,)
            )
            
    def _on_supply_missing(self):
        analysis = modifiers.analyze_active_recipes_materials(self.save_json)
        deficit_items = [m for m in analysis["materials"] if m["deficit"] > 0]
        if not deficit_items:
            messagebox.showinfo("Stock Completo", "¡Ya tienes el 100% de los materiales requeridos para todas tus recetas de I+D en el almacén!\nNo es necesario añadir nada más.")
            return
            
        tot_units = sum(m["deficit"] for m in deficit_items)
        if analysis["storage_free"] < tot_units:
            if not messagebox.askyesno("Espacio Limitado", f"El almacén tiene {analysis['storage_free']} casillas libres y se requieren {tot_units} unidades.\n¿Deseas suministrar hasta donde alcance el espacio?"):
                return
                
        added_types, added_units = modifiers.smart_supply_missing_materials(self.save_json)
        self.refresh_analysis()
        if self.on_modified_cb:
            self.on_modified_cb(f"Suministrados {added_units} materiales faltantes ({added_types} tipos) para recetas de I+D.")
        messagebox.showinfo(
            "Forja Abastecida",
            f"¡Abastecimiento Inteligente Completado!\n\n"
            f"• Se inyectaron: {added_units} unidades de {added_types} materiales faltantes.\n"
            f"• Materiales con stock suficiente: 0 unidades añadidas (sin excesos).\n\n"
            f"¡Tus recetas de I+D en Chokufunsha ahora tienen todo lo necesario para fabricarse!"
        )
        
    def _on_smart_top_up(self):
        target = simpledialog.askinteger(
            "Top-Up Inteligente de Almacén",
            "Indica la cantidad objetivo a la que deseas nivelar cada material:\n(Si ya tienes esa cantidad o más, añadirá 0 para no saturar)",
            initialvalue=15,
            minvalue=1,
            maxvalue=99,
            parent=self
        )
        if not target:
            return
            
        added_types, added_units = modifiers.smart_top_up_materials(self.save_json, target_qty=target)
        self.refresh_analysis()
        if self.on_modified_cb:
            self.on_modified_cb(f"Top-Up Inteligente: Nivelados {added_types} materiales a {target} unidades (+{added_units} unidades).")
        messagebox.showinfo(
            "Top-Up Completado",
            f"¡Stock Nivelado con Éxito!\n\n"
            f"• Meta por material: {target} unidades.\n"
            f"• Materiales ajustados: {added_types} tipos.\n"
            f"• Unidades añadidas: {added_units} unidades.\n\n"
            f"Los materiales que ya tenían {target} o más unidades permanecieron intactos."
        )

    def _on_expand_storage(self):
        current_cap = len(self.save_json.get("soul", {}).get("cl", []))
        target = simpledialog.askinteger(
            "🚀 Ampliar Capacidad del Almacén",
            f"Capacidad actual: {current_cap:,} casillas.\n\n"
            "Introduce la nueva capacidad deseada para el almacén:\n"
            "Ejemplos recomendados: 6000, 8000, 10000",
            initialvalue=max(current_cap, 6000),
            minvalue=current_cap,
            maxvalue=20000,
            parent=self
        )
        if not target or target <= current_cap:
            return
            
        old_c, new_c = modifiers.expand_storage_capacity(self.save_json, target_capacity=target)
        self.refresh_analysis()
        if self.on_modified_cb:
            self.on_modified_cb(f"Almacén ampliado de {old_c:,} a {new_c:,} casillas.")
        messagebox.showinfo(
            "Capacidad Ampliada",
            f"¡Almacén ampliado con éxito!\n\n"
            f"• Capacidad anterior: {old_c:,} casillas\n"
            f"• Nueva capacidad: {new_c:,} casillas\n\n"
            f"¡Recuerda hacer clic en 'GUARDAR PARTIDA' en el editor para aplicar los cambios!"
        )

class InventoryViewerDialog(tk.Toplevel):
    """Dialog that displays the complete physical inventory of the player's Coin Locker and Fighter Deathbag."""
    def __init__(self, parent, save_json, equipment_db, materials_db):
        super().__init__(parent)
        self.title("📋 Visor de Inventario Completo en Partida (Almacén y Mochila)")
        self.geometry("960x650")
        self.configure(bg=BG_DARK)
        self.transient(parent)
        self.grab_set()
        
        self.save_json = save_json
        self.equipment_db = {e["id"]: e for e in equipment_db}
        self.materials_db = {m["itemid"]: m for m in materials_db}
        self.parent_app = parent
        self.tree_images = {}
        
        self._build_ui()
        self.refresh_inventory()
        
    def _build_ui(self):
        # Header frame
        header = tk.Frame(self, bg=BG_PANEL, padx=14, pady=10)
        header.pack(fill="x")
        
        ttk.Label(header, text="📦 INVENTARIO ACTUAL EN TU PARTIDA", font=("Segoe UI", 13, "bold"), foreground=ACCENT_GOLD).pack(anchor="w")
        self.cap_lbl = ttk.Label(header, text="Almacén (Coin Locker): Calculando...", font=("Segoe UI", 10))
        self.cap_lbl.pack(anchor="w", pady=(3, 4))
        
        self.cap_bar = ttk.Progressbar(header, orient="horizontal", mode="determinate", length=400)
        self.cap_bar.pack(fill="x")
        
        # Filter and Search row
        filter_frame = tk.Frame(self, bg=BG_DARK, padx=14, pady=8)
        filter_frame.pack(fill="x")
        
        ttk.Label(filter_frame, text="🔍 Buscar:").pack(side="left", padx=2)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_inventory())
        ttk.Entry(filter_frame, textvariable=self.search_var, width=16).pack(side="left", padx=2)
        
        ttk.Label(filter_frame, text="Categoría:").pack(side="left", padx=(10, 2))
        self.cat_filter_var = tk.StringVar(value="Todos")
        cb_cat = ttk.Combobox(
            filter_frame,
            textvariable=self.cat_filter_var,
            values=["Todos", "🔨 Materiales", "⚔️ Armas y Armaduras", "🍄 Setas y Criaturas", "🎒 Mochila / Equipado"],
            state="readonly",
            width=22
        )
        cb_cat.pack(side="left", padx=2)
        cb_cat.bind("<<ComboboxSelected>>", lambda e: self.refresh_inventory())
        
        ttk.Button(filter_frame, text="🔄 Actualizar", command=self.refresh_inventory).pack(side="right", padx=3)
        
        # Treeview
        table_frame = tk.Frame(self, bg=BG_DARK, padx=14, pady=4)
        table_frame.pack(fill="both", expand=True)
        
        cols = ("qty", "loc", "cat", "id")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="tree headings", height=16)
        self.tree.heading("#0", text="Icono / Nombre Oficial en Español e Inglés")
        self.tree.heading("qty", text="Cantidad")
        self.tree.heading("loc", text="Ubicación")
        self.tree.heading("cat", text="Categoría Oficial")
        self.tree.heading("id", text="ID Ítem")
        
        self.tree.column("#0", width=380)
        self.tree.column("qty", width=90, anchor="center")
        self.tree.column("loc", width=120, anchor="center")
        self.tree.column("cat", width=150)
        self.tree.column("id", width=140)
        
        self.tree.tag_configure("tag_material", foreground=ACCENT_GOLD)
        self.tree.tag_configure("tag_gear", foreground=ACCENT_BLUE)
        self.tree.tag_configure("tag_bag", foreground=ACCENT_GREEN)
        
        ysb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        ysb.pack(side="right", fill="y")
        
        # Bottom Bar
        bottom_bar = tk.Frame(self, bg=BG_PANEL, padx=14, pady=8)
        bottom_bar.pack(fill="x")
        
        self.status_lbl = ttk.Label(bottom_bar, text="---", font=("Segoe UI", 9))
        self.status_lbl.pack(side="left")
        
        ttk.Button(bottom_bar, text="Cerrar", command=self.destroy).pack(side="right", padx=2)

    def refresh_inventory(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        if not self.save_json:
            return
            
        cl = self.save_json.get("soul", {}).get("cl", [])
        total_slots = len(cl)
        used_slots = len([c for c in cl if c.get("type") != -1 and c.get("eid")])
        free_slots = max(0, total_slots - used_slots)
        pct = (used_slots / total_slots * 100) if total_slots > 0 else 0
        
        self.cap_lbl.config(
            text=f"Almacén (Coin Locker): {used_slots:,} / {total_slots:,} casillas ocupadas ({free_slots:,} libres - {pct:.1f}% lleno)"
        )
        self.cap_bar["value"] = pct
        
        query = self.search_var.get().lower().strip()
        cat_filter = self.cat_filter_var.get()
        
        # 1. Gather materials and consumable counts from save["item"]["items"]
        items = self.save_json.get("item", {}).get("items", [])
        mat_counts = Counter()
        for it in items:
            mat_counts[it.get("itemid", "")] += 1
            
        # 2. Gather equipment counts from save["part"]["pts"]
        storage_gear, bag_gear = modifiers.get_equipment_inventory_counts(self.save_json)
        
        total_entries = 0
        total_units = 0
        
        # Insert Materials / Consumables
        if cat_filter in ("Todos", "🔨 Materiales", "🍄 Setas y Criaturas"):
            for itemid, qty in mat_counts.items():
                if not itemid or qty <= 0:
                    continue
                info = self.materials_db.get(itemid, {})
                name_es = info.get("name_es", info.get("name", itemid))
                name_en = info.get("name_en", "")
                cat = info.get("category", "Materiales")
                
                is_shroom = "MSR_" in itemid or "MUSH" in itemid or "Setas" in cat
                if cat_filter == "🔨 Materiales" and is_shroom:
                    continue
                elif cat_filter == "🍄 Setas y Criaturas" and not is_shroom:
                    continue
                    
                if query and (query not in name_es.lower() and query not in name_en.lower() and query not in itemid.lower() and query not in cat.lower()):
                    continue
                    
                display_name = f"{name_es} ({name_en})" if name_en and name_en != name_es else name_es
                icon_k = self.parent_app._get_mat_photo_key(itemid, name_en or name_es)
                thumb = self.parent_app.get_photo(icon_k, size=(24, 24))
                
                node = self.tree.insert(
                    "",
                    "end",
                    text=f" {display_name}",
                    image=thumb or "",
                    values=(f"{qty} u.", "📦 Almacén", cat, itemid),
                    tags=("tag_material",)
                )
                self.tree_images[node] = thumb
                total_entries += 1
                total_units += qty
                
        # Insert Storage Equipment
        if cat_filter in ("Todos", "⚔️ Armas y Armaduras"):
            for ptid, qty in storage_gear.items():
                if not ptid or qty <= 0:
                    continue
                info = self.equipment_db.get(ptid, {})
                name_es = info.get("name_es", ptid)
                name_en = info.get("name_en", "")
                cat = info.get("type", "Equipo")
                
                if query and (query not in name_es.lower() and query not in name_en.lower() and query not in ptid.lower() and query not in cat.lower()):
                    continue
                    
                display_name = f"{name_es} ({name_en})" if name_en and name_en != name_es else name_es
                art_rel = self.parent_app._find_equipment_art(ptid)
                thumb = self.parent_app.get_photo(art_rel, size=(24, 24))
                
                node = self.tree.insert(
                    "",
                    "end",
                    text=f" {display_name}",
                    image=thumb or "",
                    values=(f"{qty} u.", "📦 Almacén", cat, ptid),
                    tags=("tag_gear",)
                )
                self.tree_images[node] = thumb
                total_entries += 1
                total_units += qty
                
        # Insert Bag Equipment
        if cat_filter in ("Todos", "🎒 Mochila / Equipado"):
            for ptid, qty in bag_gear.items():
                if not ptid or qty <= 0:
                    continue
                info = self.equipment_db.get(ptid, {})
                name_es = info.get("name_es", ptid)
                name_en = info.get("name_en", "")
                cat = info.get("type", "Equipo")
                
                if query and (query not in name_es.lower() and query not in name_en.lower() and query not in ptid.lower() and query not in cat.lower()):
                    continue
                    
                display_name = f"{name_es} ({name_en})" if name_en and name_en != name_es else name_es
                art_rel = self.parent_app._find_equipment_art(ptid)
                thumb = self.parent_app.get_photo(art_rel, size=(24, 24))
                
                node = self.tree.insert(
                    "",
                    "end",
                    text=f" {display_name}",
                    image=thumb or "",
                    values=(f"{qty} u.", "🎒 Mochila", cat, ptid),
                    tags=("tag_bag",)
                )
                self.tree_images[node] = thumb
                total_entries += 1
                total_units += qty
                
        self.status_lbl.config(
            text=f"Mostrando {total_entries} tipos de objetos distintos ({total_units:,} unidades físicas en total)."
        )

class ArmorSetViewerDialog(tk.Toplevel):
    """Interactive visual dialog to inspect complete armor sets by tier like on letitdie.wiki.gg"""
    def __init__(self, parent, save_json, armor_sets, initial_set_id=None, initial_tier=1):
        super().__init__(parent)
        self.parent_app = parent
        self.save_json = save_json
        self.armor_sets = armor_sets
        self.title("👘 Visor Oficial de Sets y Tiers de Armadura (Wiki.gg)")
        self.geometry("1140x840")
        self.minsize(1020, 720)
        self.configure(bg=BG_DARK)
        self.transient(parent)
        self.grab_set()
        
        self.set_index = 0
        if initial_set_id:
            for idx, s in enumerate(self.armor_sets):
                if s["id"] == initial_set_id:
                    self.set_index = idx
                    break
                    
        self.current_tier_num = max(1, min(initial_tier, 4))
        self.img_refs = []
        
        self._build_ui()
        self.display_current_set()
        
    def _build_ui(self):
        # 1. Header Toolbar
        header = tk.Frame(self, bg=BG_PANEL, padx=14, pady=10)
        header.pack(fill="x")
        
        row1 = ttk.Frame(header)
        row1.pack(fill="x")
        
        ttk.Label(row1, text="👘 CONJUNTO DE ARMADURA:", font=("Segoe UI", 11, "bold"), foreground=ACCENT_GOLD).pack(side="left", padx=(0, 8))
        
        set_names = [f"{s['name_en']} ({s.get('name_es', s['name_en'])}) • {s['faction']}" for s in self.armor_sets]
        self.cb_set_var = tk.StringVar(value=set_names[self.set_index] if self.armor_sets else "")
        cb_sets = ttk.Combobox(row1, textvariable=self.cb_set_var, values=set_names, state="readonly", width=52)
        cb_sets.pack(side="left", padx=4)
        cb_sets.bind("<<ComboboxSelected>>", self._on_set_changed)
        
        self.faction_lbl = ttk.Label(row1, text="", font=("Segoe UI", 10, "bold"))
        self.faction_lbl.pack(side="left", padx=10)
        
        # 2. Tier Selection Tabs
        tier_bar = tk.Frame(self, bg=BG_CARD, padx=10, pady=8)
        tier_bar.pack(fill="x", pady=(2, 4))
        
        ttk.Label(tier_bar, text="Evolución / Nivel:", font=("Segoe UI", 10, "bold"), foreground=FG_MAIN).pack(side="left", padx=(4, 10))
        
        self.tier_buttons = []
        for tnum in [1, 2, 3, 4]:
            tbtn = ttk.Button(
                tier_bar,
                text=f"Tier {tnum}",
                command=lambda tn=tnum: self.switch_tier(tn)
            )
            tbtn.pack(side="left", padx=4)
            self.tier_buttons.append((tnum, tbtn))
            
        # 3. Main Split Content Area
        content_box = ttk.Frame(self)
        content_box.pack(fill="both", expand=True, padx=10, pady=6)
        
        # Left Side: Character Armor Model Showcase
        left_box = ttk.LabelFrame(content_box, text="🧍 Previsualización del Conjunto (Modelo 3D Oficial)", padding=10)
        left_box.pack(side="left", fill="both", expand=False, padx=(0, 6))
        left_box.config(width=340)
        
        self.model_lbl = ttk.Label(left_box, anchor="center")
        self.model_lbl.pack(fill="both", expand=True)
        
        self.model_title_lbl = ttk.Label(left_box, text="", font=("Segoe UI", 11, "bold"), foreground=ACCENT_GOLD, wraplength=320, justify="center")
        self.model_title_lbl.pack(pady=(4, 1))
        
        # Right Side: Piece & Weapon Stat Cards
        right_box = ttk.Frame(content_box)
        right_box.pack(side="right", fill="both", expand=True)
        
        self.piece_cards = {}
        for slot_key, slot_title, emoji in [
            ("head", "🪖 CASCO (Head)", "🪖"),
            ("body", "👕 PECHERA (Body Armor)", "👕"),
            ("legs", "👖 PANTALONES (Legs / Pants)", "👖"),
            ("weapon", "⚔️ ARMA CARACTERÍSTICA (Signature Weapon)", "⚔️")
        ]:
            card_lf = ttk.LabelFrame(right_box, text=slot_title, padding=6)
            card_lf.pack(fill="x", expand=True, pady=3)
            
            # Sub-elements
            inner = ttk.Frame(card_lf)
            inner.pack(fill="x")
            
            icon_lbl = ttk.Label(inner)
            icon_lbl.pack(side="left", padx=(2, 10))
            
            info_col = ttk.Frame(inner)
            info_col.pack(side="left", fill="both", expand=True)
            
            title_lbl = ttk.Label(info_col, text="---", font=("Segoe UI", 10, "bold"), foreground=FG_MAIN)
            title_lbl.pack(anchor="w")
            
            def_dur_lbl = ttk.Label(info_col, text="", font=("Segoe UI", 9, "bold"), foreground=ACCENT_CYAN)
            def_dur_lbl.pack(anchor="w", pady=1)
            
            res_lbl = ttk.Label(info_col, text="", font=("Segoe UI", 8), foreground=FG_MUTED)
            res_lbl.pack(anchor="w", pady=1)
            
            status_lbl = ttk.Label(info_col, text="", font=("Segoe UI", 9))
            status_lbl.pack(anchor="w", pady=1)
            
            # Right side: stat card and action buttons
            action_col = ttk.Frame(inner)
            action_col.pack(side="right", padx=4)
            
            card_img_lbl = ttk.Label(action_col)
            card_img_lbl.pack(pady=2)
            
            btns_row = ttk.Frame(action_col)
            btns_row.pack(fill="x", pady=2)
            
            btn_unlock = ttk.Button(btns_row, text="⭐ Desbloquear +4", style="Accent.TButton", width=16)
            btn_unlock.pack(side="left", padx=2)
            
            btn_add = ttk.Button(btns_row, text="🎁 +1 al Almacén", width=14)
            btn_add.pack(side="left", padx=2)
            
            self.piece_cards[slot_key] = {
                "frame": card_lf,
                "icon_lbl": icon_lbl,
                "title_lbl": title_lbl,
                "def_dur_lbl": def_dur_lbl,
                "res_lbl": res_lbl,
                "status_lbl": status_lbl,
                "card_img_lbl": card_img_lbl,
                "btn_unlock": btn_unlock,
                "btn_add": btn_add,
                "current_pid": None
            }
            
        # 4. Bottom Global Actions
        bottom_bar = tk.Frame(self, bg=BG_PANEL, padx=14, pady=10)
        bottom_bar.pack(fill="x")
        
        btn_unlock_set = ttk.Button(
            bottom_bar,
            text="⭐ Desbloquear Set + Arma Completa (Tier a +4 en Tienda y Almacén)",
            style="Accent.TButton",
            command=self.unlock_current_tier_set
        )
        btn_unlock_set.pack(side="left", padx=4)
        
        btn_add_set = ttk.Button(
            bottom_bar,
            text="🎁 Añadir Set Completo al Almacén (Casco + Pechera + Piernas)",
            command=self.add_current_tier_set_storage
        )
        btn_add_set.pack(side="left", padx=4)
        
        btn_close = ttk.Button(bottom_bar, text="Cerrar", command=self.destroy)
        btn_close.pack(side="right", padx=4)

    def _on_set_changed(self, event=None):
        sel_idx = self.cb_set_var.get()
        for idx, s in enumerate(self.armor_sets):
            label = f"{s['name_en']} ({s.get('name_es', s['name_en'])}) • {s['faction']}"
            if label == sel_idx:
                self.set_index = idx
                break
        self.display_current_set()

    def switch_tier(self, tier_num):
        self.current_tier_num = tier_num
        self.display_current_set()

    def display_current_set(self):
        if not self.armor_sets:
            return
        self.img_refs.clear()
        
        s_obj = self.armor_sets[self.set_index]
        self.faction_lbl.config(text=f"Facción: {s_obj['faction']}")
        
        # Highlight active tier button
        for tnum, btn in self.tier_buttons:
            if tnum == self.current_tier_num:
                btn.configure(style="Accent.TButton")
            else:
                btn.configure(style="TButton")
                
        # Find tier object
        t_obj = None
        for t in s_obj.get("tiers", []):
            if t["tier_num"] == self.current_tier_num:
                t_obj = t
                break
        if not t_obj and s_obj.get("tiers"):
            t_obj = s_obj["tiers"][-1]
            self.current_tier_num = t_obj["tier_num"]
            
        if not t_obj:
            return
            
        # 1. Update character set model
        render_path = t_obj.get("set_render")
        if render_path:
            model_photo = self.parent_app.get_photo(render_path, size=(300, 470))
            if model_photo:
                self.model_lbl.config(image=model_photo, text="")
                self.model_lbl.image = model_photo
                self.img_refs.append(model_photo)
            else:
                self.model_lbl.config(image="", text="[Render Oficial en Proceso]")
        else:
            self.model_lbl.config(image="", text="[Render Oficial en Proceso]")
            
        self.model_title_lbl.config(text=f"{s_obj['name_en']} ({t_obj['tier_name']})")
        
        # 2. Update piece cards
        counts = modifiers.get_equipment_inventory_counts(self.save_json) if self.save_json else ({}, {})
        storage_map, bag_map = counts
        pr_list = self.save_json.get("soul", {}).get("partresearch", {}).get("user", []) if self.save_json else []
        forge_levels = {r.get("ptid"): r.get("lvl", 0) for r in pr_list if isinstance(r, dict)}
        
        for slot_key in ["head", "body", "legs", "weapon"]:
            p = t_obj.get(slot_key)
            card_ui = self.piece_cards[slot_key]
            
            if not p:
                card_ui["frame"].pack_forget()
                continue
                
            card_ui["frame"].pack(fill="x", expand=True, pady=2)
            card_ui["current_pid"] = p["id"]
            
            # Title
            name_str = f"{p['name_es']} ({p['name']})" if p.get('name_es') and p['name_es'] != p['name'] else p['name']
            card_ui["title_lbl"].config(text=f"{name_str}  [{p['id']}]")
            
            if slot_key == "weapon":
                atk_base = p.get("atk", 0)
                atk_plus4 = p.get("atk_plus4", int(atk_base * 1.5))
                dur = p.get("durability", 1400)
                card_ui["def_dur_lbl"].config(text=f"⚔️ Ataque Base: {atk_base} (A +4: ~{atk_plus4})  |  Durabilidad: {dur}", foreground=ACCENT_GOLD)
                card_ui["res_lbl"].config(text="🔥 Arma característica oficial emparejada con este conjunto de armadura.")
                card_ui["btn_unlock"].config(text="⭐ Desbloquear Arma +4")
            else:
                # Def / Dur
                def_base = p.get("def", 0)
                def_plus4 = p.get("def_plus4", 0)
                dur = p.get("durability", 0)
                card_ui["def_dur_lbl"].config(text=f"🛡️ Defensa Base: {def_base} (A +4: {def_plus4})  |  Durabilidad: {dur}", foreground=ACCENT_CYAN)
                
                # Resistances
                res = p.get("resistances", {})
                res_txt = (
                    f"🗡️ Corte: {res.get('slash',0):+d}%   🔨 Golpe: {res.get('blunt',0):+d}%   🏹 Perf: {res.get('pierce',0):+d}%\n"
                    f"🔥 Fuego: {res.get('fire',0):+d}%   ⚡ Elec: {res.get('electric',0):+d}%   🧪 Veneno: {res.get('poison',0):+d}%"
                )
                card_ui["res_lbl"].config(text=res_txt)
                card_ui["btn_unlock"].config(text="⭐ Desbloquear +4")
            
            # Status
            f_lvl = forge_levels.get(p["id"], 0)
            st_cnt = storage_map.get(p["id"], 0)
            bg_cnt = bag_map.get(p["id"], 0)
            
            f_txt = f"⭐ Tienda: Desbloqueado (+{f_lvl})" if f_lvl >= 4 else f"🔨 Tienda: Nivel +{f_lvl}" if f_lvl > 0 else "❌ Tienda: Bloqueado"
            f_color = ACCENT_GOLD if f_lvl >= 4 else ACCENT_BLUE if f_lvl > 0 else FG_MUTED
            
            st_txt = f"📦 Almacén: {st_cnt} u." if st_cnt > 0 else "📦 Almacén: 0 u."
            bg_txt = f"🎒 Mochila: {bg_cnt} u." if bg_cnt > 0 else ""
            full_stat = f"{f_txt}  •  {st_txt}" + (f"  •  {bg_txt}" if bg_txt else "")
            card_ui["status_lbl"].config(text=full_stat, foreground=f_color)
            
            # Icon
            icon_rel = p.get("icon")
            icon_photo = None
            if icon_rel:
                icon_photo = self.parent_app.get_photo(icon_rel, size=(54, 54))
            if not icon_photo:
                icon_photo = self.parent_app.get_photo(self.parent_app._find_equipment_art(p["id"]), size=(54, 54))
            if not icon_photo and hasattr(self.parent_app, "icon_map"):
                mapped = self.parent_app.icon_map.get("gear_icons", {}).get(p["id"])
                if mapped:
                    icon_photo = self.parent_app.get_photo(mapped, size=(54, 54))
            if icon_photo:
                card_ui["icon_lbl"].config(image=icon_photo, text="")
                card_ui["icon_lbl"].image = icon_photo
                self.img_refs.append(icon_photo)
            else:
                card_ui["icon_lbl"].config(image="", text="[Icono]")
                
            # Card image
            card_rel = p.get("card")
            card_photo = None
            if card_rel:
                card_photo = self.parent_app.get_photo(card_rel, size=(180, 85))
            if not card_photo and hasattr(self.parent_app, "icon_map"):
                mapped_card = self.parent_app.icon_map.get("gear_cards", {}).get(p["id"])
                if mapped_card:
                    card_photo = self.parent_app.get_photo(mapped_card, size=(180, 85))
            if card_photo:
                card_ui["card_img_lbl"].config(image=card_photo)
                card_ui["card_img_lbl"].image = card_photo
                card_ui["card_img_lbl"].pack(pady=2)
                self.img_refs.append(card_photo)
            else:
                card_ui["card_img_lbl"].pack_forget()
                
            # Wire buttons
            card_ui["btn_unlock"].config(command=lambda pid=p["id"]: self.unlock_single_piece(pid))
            card_ui["btn_add"].config(command=lambda pid=p["id"]: self.add_single_piece_storage(pid))

    def _auto_save_and_sync(self):
        try:
            if hasattr(self.parent_app, "save_path") and self.parent_app.save_path:
                save_to_file(self.save_json, self.parent_app.save_path, version=getattr(self.parent_app, "version", 1))
                if hasattr(self.parent_app, "status_var"):
                    self.parent_app.status_var.set("¡Partida guardada y actualizada automáticamente!")
        except Exception as e:
            print(f"Auto-save warning: {e}")

    def unlock_single_piece(self, pid):
        if not self.save_json or not pid:
            return
        pr_list = self.save_json.setdefault("soul", {}).setdefault("partresearch", {}).setdefault("user", [])
        existing = {(r.get("ptid"), r.get("lvl")): r for r in pr_list if isinstance(r, dict)}
        
        # 1. Levels 1 to 4 (FINISHED / FINISHED)
        for lvl in range(1, 5):
            key = (pid, lvl)
            if key not in existing:
                pr_list.append({
                    "ptid": pid,
                    "lvl": lvl,
                    "research_type": "FINISHED",
                    "receive_type": "FINISHED",
                    "is_announced": 1,
                    "is_checked": 1,
                    "before_ptid": pid if lvl > 1 else "",
                    "before_lvl": lvl - 1 if lvl > 1 else 0
                })
            else:
                existing[key]["research_type"] = "FINISHED"
                existing[key]["receive_type"] = "FINISHED"
                
        # 2. Level 5 (Completed +4, available to purchase in Chokufunsha with Kill Coins)
        key5 = (pid, 5)
        if key5 not in existing:
            pr_list.append({
                "ptid": pid,
                "lvl": 5,
                "research_type": "FINISHED",
                "receive_type": "CHARGE",
                "is_announced": 1,
                "is_checked": 3,
                "before_ptid": pid,
                "before_lvl": 4
            })
        else:
            existing[key5]["research_type"] = "FINISHED"
            existing[key5]["receive_type"] = "CHARGE"
            existing[key5]["is_checked"] = 3
            
        # 3. Add 1 unit directly to Storage (Coin Locker)
        modifiers.add_equipment_to_storage(self.save_json, pid, count=1, lvl=5, dur=50000)
        self._auto_save_and_sync()
        self.parent_app.filter_blueprints_list()
        self.display_current_set()
        messagebox.showinfo(
            "Plano y Objeto Desbloqueado",
            f"¡El objeto '{pid}' ha sido completamente desbloqueado!\n\n"
            f"1. 🛒 Chokufunsha: Ya está disponible al Nivel +4 para comprar siempre en la tienda.\n"
            f"2. 📦 Almacén: Se ha entregado 1 unidad (Nivel +4, Dur 100%) en tu Almacén.\n"
            f"3. 💾 Partida guardada automáticamente."
        )

    def add_single_piece_storage(self, pid):
        if not self.save_json or not pid:
            return
        modifiers.add_equipment_to_storage(self.save_json, pid, count=1, lvl=5, dur=50000)
        self._auto_save_and_sync()
        self.parent_app.filter_blueprints_list()
        self.display_current_set()
        messagebox.showinfo("Objeto Añadido", f"¡Se ha añadido 1 unidad de '{pid}' (Nvl +4, Dur 100%) a tu Almacén!\nGuardado automáticamente.")

    def unlock_current_tier_set(self):
        if not self.save_json or not self.armor_sets:
            return
        s_obj = self.armor_sets[self.set_index]
        t_obj = next((t for t in s_obj.get("tiers", []) if t["tier_num"] == self.current_tier_num), None)
        if not t_obj:
            return
            
        unlocked = []
        for slot in ["head", "body", "legs", "weapon"]:
            p = t_obj.get(slot)
            if p and p.get("id"):
                pid = p["id"]
                pr_list = self.save_json.setdefault("soul", {}).setdefault("partresearch", {}).setdefault("user", [])
                existing = {(r.get("ptid"), r.get("lvl")): r for r in pr_list if isinstance(r, dict)}
                
                # Levels 1 to 4
                for lvl in range(1, 5):
                    key = (pid, lvl)
                    if key not in existing:
                        pr_list.append({
                            "ptid": pid,
                            "lvl": lvl,
                            "research_type": "FINISHED",
                            "receive_type": "FINISHED",
                            "is_announced": 1,
                            "is_checked": 1,
                            "before_ptid": pid if lvl > 1 else "",
                            "before_lvl": lvl - 1 if lvl > 1 else 0
                        })
                    else:
                        existing[key]["research_type"] = "FINISHED"
                        existing[key]["receive_type"] = "FINISHED"
                        
                # Level 5 (CHARGE / Buyable in store)
                key5 = (pid, 5)
                if key5 not in existing:
                    pr_list.append({
                        "ptid": pid,
                        "lvl": 5,
                        "research_type": "FINISHED",
                        "receive_type": "CHARGE",
                        "is_announced": 1,
                        "is_checked": 3,
                        "before_ptid": pid,
                        "before_lvl": 4
                    })
                else:
                    existing[key5]["research_type"] = "FINISHED"
                    existing[key5]["receive_type"] = "CHARGE"
                    existing[key5]["is_checked"] = 3
                    
                # Add 1 physical unit to Storage
                modifiers.add_equipment_to_storage(self.save_json, pid, count=1, lvl=5, dur=50000)
                unlocked.append(f"{p['name']} ({p.get('name_es', p['name'])})")
                
        self._auto_save_and_sync()
        self.parent_app.filter_blueprints_list()
        self.display_current_set()
        messagebox.showinfo(
            "Set + Arma Completa Desbloqueados",
            f"¡El {s_obj['name_en']} ({t_obj['tier_name']}) y su arma característica han sido desbloqueados!\n\n"
            f"🛒 Tienda Chokufunsha: Las piezas y el arma están listas para comprar al Nivel +4 con Kill Coins.\n"
            f"📦 Almacén: Se ha entregado 1 copia de cada armadura + el arma (Nivel +4, 100% Durabilidad) en tu Almacén.\n"
            f"💾 Partida guardada automáticamente.\n\n"
            + "\n".join([f"• {u}" for u in unlocked])
        )

    def add_current_tier_set_storage(self):
        if not self.save_json or not self.armor_sets:
            return
        s_obj = self.armor_sets[self.set_index]
        t_obj = next((t for t in s_obj.get("tiers", []) if t["tier_num"] == self.current_tier_num), None)
        if not t_obj:
            return
            
        added = []
        for slot in ["head", "body", "legs", "weapon"]:
            p = t_obj.get(slot)
            if p and p.get("id"):
                modifiers.add_equipment_to_storage(self.save_json, p["id"], count=1, lvl=5, dur=50000)
                added.append(f"{p['name']} ({p.get('name_es', p['name'])})")
                
        self._auto_save_and_sync()
        self.parent_app.filter_blueprints_list()
        self.display_current_set()
        messagebox.showinfo(
            "Set + Arma Añadidos al Almacén",
            f"¡Se han añadido al Almacén las 3 piezas del set + el arma característica (Nivel +4, Dur 100%)!\n\n"
            + "\n".join([f"• {a}" for a in added])
            + "\n\nPartida guardada automáticamente."
        )

if __name__ == "__main__":
    app = CompleteSaveEditorGUI()
    app.mainloop()
