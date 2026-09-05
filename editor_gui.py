# -*- coding: utf-8 -*-
"""
LET IT DIE (Offline) - Deep Save Editor Pro v4.0.1 (Master Cyberpunk Encyclopedia Edition)
Complete Visual Redesign matching ArmorSetViewerDialog quality standard across all tabs.
Modular architecture with tab mixins in ui/tabs.
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
from ui.dialogs import (
    SmartInventoryAnalyzerDialog,
    InventoryViewerDialog,
    ArmorSetViewerDialog,
    CreateFighterDialog
)
from ui.components import setup_mousewheel_dispatcher
from game_data import SPECIAL_MUSHROOMS, SPECIAL_BEASTS, WEAPON_CATEGORIES, FIGHTER_CLASSES

# Tab Mixins
from ui.tabs import (
    CurrenciesTabMixin,
    FightersTabMixin,
    MaterialsTabMixin,
    DecalsTabMixin,
    BlueprintsTabMixin,
    MasteryTabMixin,
    TowerTabMixin,
    AdvancedTabMixin,
)


class CompleteSaveEditorGUI(
    tk.Tk,
    CurrenciesTabMixin,
    FightersTabMixin,
    MaterialsTabMixin,
    DecalsTabMixin,
    BlueprintsTabMixin,
    MasteryTabMixin,
    TowerTabMixin,
    AdvancedTabMixin,
):
    """Deep Save Editor Pro main window combining all functional tabs via mixin classes."""

    def __init__(self):
        super().__init__()
        self.title("LET IT DIE (Offline) - Deep Save Editor Pro v4.0.1 (Master Cyberpunk Edition)")
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
        setup_mousewheel_dispatcher(self)
        
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
        
        # Modern High-Contrast Entries & Comboboxes
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

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=4)
        self.notebook.bind("<<NotebookTabChanged>>", self._on_notebook_tab_changed)
        
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

    # ================= GENERAL NAVIGATION & DIALOGS =================
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

    def _on_notebook_tab_changed(self, event=None):
        # Notebook tab changed - mousewheel routing is handled cleanly by the global dispatcher
        pass

    # ================= LANGUAGE HANDLING =================
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

            # Normalize empty associative arrays ({}) to lists
            modifiers.repair_save_list_structures(self.save_json)

            # Auto-sanitize currencies and facilities against C++ out-of-bounds corruption (> level 99)
            repaired_curr, fixes_curr = modifiers.repair_and_sanitize_currencies(self.save_json)
            if repaired_curr:
                print(f"[Auto-Repair] Currencies sanitized: {fixes_curr}")

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
            body_val = f.get("body", "BODY_FEMALE_001")
            model_art = f"all_official/{body_val.lower()}.png"
            thumb = self.get_photo(model_art, (32, 36), preserve_aspect=True) or \
                    self.get_photo(cls_icon_filename, (36, 36), preserve_aspect=True) or \
                    self.get_photo("all-rounder", (36, 36), preserve_aspect=True)
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
            cap = st_info.get("total_slots", st_info.get("capacity", 2000))
            used = st_info.get("used_slots", st_info.get("total_items", 0))
            self.mat_cap_indicator_lbl.config(text=t("mat_locker_status", used=used, cap=cap, free=max(0, cap - used)))

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
            def _parse_safe_int(val, default=0):
                if val is None:
                    return default
                s = str(val).replace(",", "").replace(".", "").replace(" ", "").strip()
                try:
                    return int(s)
                except ValueError:
                    return default

            # Sync currencies from entries
            if hasattr(self, "dm_var"):
                modifiers.set_currencies(
                    self.save_json,
                    dm=_parse_safe_int(self.dm_var.get()),
                    kc=_parse_safe_int(self.kc_var.get()),
                    spl=_parse_safe_int(self.spl_var.get()),
                    bloodnium=_parse_safe_int(self.bl_var.get()),
                    re_points=_parse_safe_int(self.re_var.get())
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
