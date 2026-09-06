# -*- coding: utf-8 -*-
"""
Materials & R&D Tab Mixin for LET IT DIE Save Editor.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import modifiers
import i18n
from i18n import t
from ui.theme import ACCENT_GOLD, ACCENT_CYAN, FG_MUTED
from ui.components import ScrollableFrame
from game_data import SPECIAL_MUSHROOMS, SPECIAL_BEASTS

if getattr(sys, "frozen", False):
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    mei_dir = getattr(sys, "_MEIPASS", exe_dir)
    BASE_DIR = exe_dir if os.path.isdir(os.path.join(exe_dir, "icons")) else mei_dir
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

ICONS_DIR = os.path.join(BASE_DIR, "icons")


class MaterialsTabMixin:
    """Provides methods for constructing and handling the Materials R&D Tab."""

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
        
        cur_lang = i18n.get_language()
        ttk.Label(ctrl_frame, text=t("mat_cat_lbl")).pack(side="left", padx=(4, 1))
        if cur_lang == "zh":
            self.mat_cat_var = tk.StringVar(value=t("mat_all"))
            cats = [
                t("mat_all"),
                "铝 (Aluminum)",
                "铜 (Copper)",
                "铁与钢 (Iron & Steel)",
                "油与石油 (Oil)",
                "木材 (Wood)",
                "布料与纤维 (Cloth)",
                "D.O.D. ARMS (Metals)",
                "WAR ENSEMBLE (Metals)",
                "CANDLE WOLF (Metals)",
                "M.I.L.K. (Metals)",
                "Boss金属 (Boss Metals)",
                "豺狼与天狱材料 (Jackals & Tengoku)",
                "类固醇 / Rostest (Fighters)",
                "🍄 蘑菇与野兽",
                "🍄 蘑菇 (Mushrooms)",
                "🐸 野兽 (Beasts)"
            ]
        elif cur_lang == "en":
            self.mat_cat_var = tk.StringVar(value="All")
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
                "🍄 Mushrooms & Beasts",
                "🍄 Mushrooms",
                "🐸 Beasts"
            ]
        else:
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
                "🍄 Setas y Criaturas",
                "🍄 Setas (Mushrooms)",
                "🐸 Criaturas (Beasts)"
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

        btn_all_mat = ttk.Button(ctrl_frame, text=t("mat_max_stock_btn"), style="Accent.TButton", command=self.max_all_materials_preset)
        btn_all_mat.pack(side="right", padx=1)

        # Row 2: Pisos de la Torre (Wiki Tower Sections Quick Bar)
        ctrl_frame_floors = ttk.Frame(left_box)
        ctrl_frame_floors.pack(fill="x", pady=2)
        
        ttk.Label(ctrl_frame_floors, text=t("mat_floors_lbl"), font=("Segoe UI", 8, "bold"), foreground=ACCENT_GOLD).pack(side="left", padx=2)
        self.mat_floor_filter = tk.StringVar(value="TODOS")
        
        floor_buttons = [
            (t("mat_floor_all"), "TODOS"),
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
        self.materials_scroll = scroll_mat = ScrollableFrame(mat_card_container)
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
            if thumb_rel:
                return thumb_rel
        clean_en = name_en.lower().replace(" ", "_").replace("-", "_").replace("'", "").replace(".", "")
        candidates = [
            f"thumbs/materials/mat_{itemid.lower()}.png",
            f"{clean_en}_box.png",
            f"{clean_en}_itembox.png",
            f"{clean_en}.png",
            f"{itemid.lower()}.png"
        ]
        if hasattr(self, "asset_manager") and getattr(self.asset_manager, "manifest", None):
            for c in candidates:
                c_low = c.lower()
                if c_low in self.asset_manager.manifest:
                    return self.asset_manager.manifest[c_low]
                c_base = os.path.basename(c_low)
                if c_base in self.asset_manager.manifest:
                    return self.asset_manager.manifest[c_base]

        for candidate in candidates:
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
        
        cnt_raw = str(stock_str).replace("pcs.", "").replace("u.", "").replace("-", "0").strip()
        cnt = int(cnt_raw) if cnt_raw.isdigit() else 0
        
        self.current_mat_selection = (itemid, full_title, cat)
        self.mat_qty_entry_var.set(str(cnt))
        self.mat_title_lbl.config(text=f"{full_title}\n({itemid}) • {stars}")
        self.mat_type_lbl.config(text=t("mat_type_info", cat=cat, count=cnt))
        
        clean_slug = full_title.split("(")[0].strip().lower().replace(" ", "_").replace("-", "_")
        name_en = full_title.split("(")[0].strip()
        
        sb_db = getattr(self, "shrooms_beasts_db", {})
        if itemid in sb_db:
            meta = sb_db[itemid]
            desc = i18n.get_item_desc(meta) or meta.get("desc_es") or meta.get("desc_en", "")
        else:
            meta = next((item for item in self.materials_db if item.get("itemid") == itemid), {})
            desc = i18n.get_item_desc(meta) or meta.get("desc", "")
            
        self.mat_desc_lbl.config(text=desc)
        
        # Check if selection is a Mushroom or Beast
        mat_art_target = None
        if itemid.startswith("MSR_") or itemid.startswith("BST_"):
            mat_art_target = sb_db.get(itemid, {}).get("icon") or f"{itemid.lower()}.png"
        else:
            card_rel = self.icon_map.get("materials_cards", {}).get(itemid) if hasattr(self, "icon_map") else None
            mat_art_target = card_rel or self._get_mat_photo_key(itemid, name_en)

        self.set_widget_image(self.mat_art_lbl, mat_art_target, size=(160, 160), preserve_aspect=True, fallback="materials/special_steel.png")

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
        if not cat_filter or cat_filter in ("Todos", "All", "全部", t("mat_all"), t("decal_all")):
            return True
        fl = cat_filter.lower()
        cl = item_cat.lower()
        
        if "steroid" in fl or "esteroide" in fl or "rostest" in fl or "类固醇" in fl:
            return ("esteroide" in cl or "steroid" in cl or "rostest" in cl)
        if "aluminum" in fl or "aluminio" in fl or "铝" in fl:
            return "alumin" in cl
        if "copper" in fl or "cobre" in fl or "铜" in fl:
            return ("cobre" in cl or "copper" in cl)
        if "iron" in fl or "hierro" in fl or "steel" in fl or "acero" in fl or "铁" in fl or "钢" in fl:
            return ("hierro" in cl or "iron" in cl)
        if "oil" in fl or "petr" in fl or "aceite" in fl or "油" in fl:
            return ("petr" in cl or "oil" in cl or "aceite" in cl)
        if "wood" in fl or "mader" in fl or "木" in fl:
            return ("mader" in cl or "wood" in cl)
        if "cloth" in fl or "textil" in fl or "fiber" in fl or "fibra" in fl or "布" in fl:
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
        if "jackal" in fl or "tengoku" in cl or "豺狼" in fl or "天狱" in cl:
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

    @staticmethod
    def _localize_material_category_zh(cat_str):
        cl = cat_str.lower()
        if "esteroide" in cl or "rostest" in cl or "steroid" in cl:
            return "类固醇 / Rostest"
        if "alumin" in cl:
            return "铝"
        if "cobre" in cl or "copper" in cl:
            return "铜"
        if "hierro" in cl or "iron" in cl:
            return "铁与钢"
        if "petr" in cl or "oil" in cl:
            return "油与石油"
        if "mader" in cl or "wood" in cl:
            return "木材"
        if "textil" in cl or "cloth" in cl or "fiber" in cl or "fibra" in cl:
            return "布料与纤维"
        if "boss" in cl or "jefe" in cl:
            return "Boss金属"
        if "jackal" in cl or "tengoku" in cl:
            return "豺狼与天狱"
        if "d.o.d" in cl or "dod" in cl:
            return "D.O.D. ARMS"
        if "war" in cl:
            return "WAR ENSEMBLE"
        if "candle" in cl:
            return "CANDLE WOLF"
        if "m.i.l.k" in cl or "milk" in cl:
            return "M.I.L.K."
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
        
        # 1. R&D Materials from masters.db
        if "🍄" not in cat_filter and "🐸" not in cat_filter:
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
                if ("> 0" in stock_filter or "En Stock" in stock_filter or "In Stock" in stock_filter or "已拥有" in stock_filter or "有库存" in stock_filter) and cnt <= 0:
                    continue
                elif ("< 10" in stock_filter or "Stock Bajo" in stock_filter or "Low Stock" in stock_filter or "低库存" in stock_filter) and (cnt <= 0 or cnt >= 10):
                    continue
                elif ("(0)" in stock_filter or "Agotado" in stock_filter or "Out of Stock" in stock_filter or "缺货" in stock_filter or "无库存" in stock_filter) and cnt > 0:
                    continue

                # Rarity filter
                if "★" in rarity_filter:
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

                # Query search with smart multi-word matching & Tier aliases
                name_zh = m.get("name_zh", "")
                if query_tokens:
                    searchable = f"{name_es} {name_en} {name_zh} {cat} {self._localize_material_category(cat)} {self._localize_material_category_zh(cat)} {itemid} t{r} tier {r} tier{r} {r}★ {r}star {name_en.replace('.', '')} {name_es.replace('.', '')}".lower()
                    if not all(token in searchable for token in query_tokens):
                        continue

                stock_str = t("inv_unit_str", qty=cnt) if cnt > 0 else "-"
                tag = "tag_in_stock" if cnt > 0 else "tag_out_of_stock"
                    
                cur_lang = i18n.get_language()
                if cur_lang == "es":
                    display_title = f"{name_es} ({name_en})" if name_en and name_en != name_es else (name_es or name_en)
                    cat_display = cat
                elif cur_lang == "en":
                    display_title = f"{name_en} ({name_es})" if name_es and name_en != name_es else (name_en or name_es)
                    cat_display = self._localize_material_category(cat)
                else:
                    display_title = f"{name_zh} ({name_en})" if name_zh and name_en and name_zh != name_en else (name_zh or name_en or name_es)
                    cat_display = self._localize_material_category_zh(cat)
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
                if not thumb and icon_k:
                    self.set_tree_item_image(self.mat_tree, node_id, icon_k, size=(36, 36), preserve_aspect=True)
                if not first_row:
                    first_row = node_id
                    
        # 2. Shrooms and Beasts (Tower Exploration)
        is_shroom_cat = ("🍄" in cat_filter or "🐸" in cat_filter)
        allow_shrooms_floors = (is_shroom_cat or floor_filter == "TODOS")
        show_shrooms = (cat_filter in ["Todos", "All", "全部", t("mat_all"), t("decal_all")] or is_shroom_cat)

        if show_shrooms and allow_shrooms_floors:
            only_shrooms = ("(Mushrooms)" in cat_filter or "(Setas)" in cat_filter or "🍄 蘑菇" in cat_filter or cat_filter == "🍄 Mushrooms")
            only_beasts = ("(Beasts)" in cat_filter or "(Criaturas)" in cat_filter or "🐸 野兽" in cat_filter or cat_filter == "🐸 Beasts")

            sb_db = getattr(self, "shrooms_beasts_db", {})
            if not sb_db:
                sb_path = os.path.join(BASE_DIR, "all_shrooms_beasts_db.json")
                if os.path.exists(sb_path):
                    try:
                        with open(sb_path, "r", encoding="utf-8") as f:
                            self.shrooms_beasts_db = json.load(f)
                            sb_db = self.shrooms_beasts_db
                    except Exception:
                        pass

            sorted_entries = sorted(
                sb_db.items(),
                key=lambda item: (0 if item[1].get("type") == "MUSHROOM" else 1, item[0])
            )

            for itemid, info in sorted_entries:
                item_type = info.get("type", "MUSHROOM")
                if only_shrooms and item_type != "MUSHROOM":
                    continue
                if only_beasts and item_type != "BEAST":
                    continue

                cnt = stock_map.get(itemid, 0)
                if ("> 0" in stock_filter or "En Stock" in stock_filter or "In Stock" in stock_filter or "已拥有" in stock_filter or "有库存" in stock_filter) and cnt <= 0:
                    continue
                elif ("< 10" in stock_filter or "Stock Bajo" in stock_filter or "Low Stock" in stock_filter or "低库存" in stock_filter) and (cnt <= 0 or cnt >= 10):
                    continue
                elif ("(0)" in stock_filter or "Agotado" in stock_filter or "Out of Stock" in stock_filter or "缺货" in stock_filter or "无库存" in stock_filter) and cnt > 0:
                    continue

                r = info.get("rarity", 1)
                if "★" in rarity_filter:
                    try:
                        req_r = int(rarity_filter.replace("★", "").strip())
                        if r != req_r:
                            continue
                    except ValueError:
                        pass

                name_en = info.get("name_en", "")
                name_es = info.get("name_es", "")
                cooked_en = info.get("cooked_name_en", "")
                cooked_es = info.get("cooked_name_es", "")
                cat_es = info.get("category_es", "Setas" if item_type == "MUSHROOM" else "Criaturas")
                cat_en = info.get("category_en", "Mushrooms" if item_type == "MUSHROOM" else "Beasts")
                cur_lang = i18n.get_language()
                if cur_lang == "es":
                    cat_display = cat_es
                elif cur_lang == "en":
                    cat_display = cat_en
                else:
                    cat_display = "蘑菇" if item_type == "MUSHROOM" else "野兽"

                name_zh = info.get("name_zh", "")
                if query_tokens:
                    searchable = f"{name_es} {name_en} {name_zh} {itemid} {item_type} {cat_display} {cooked_en} {cooked_es} mushroom seta shroom beast criatura t{r} tier{r} {r}★ {r}star".lower()
                    if not all(token in searchable for token in query_tokens):
                        continue

                stock_str = t("inv_unit_str", qty=cnt) if cnt > 0 else "-"
                tag = "tag_in_stock" if cnt > 0 else "tag_out_of_stock"
                stars = "★" * r
                if cur_lang == "es":
                    display_title = f"{name_es} ({name_en})" if name_en and name_en != name_es else (name_es or name_en)
                elif cur_lang == "en":
                    display_title = f"{name_en} ({name_es})" if name_es and name_en != name_es else (name_en or name_es)
                else:
                    display_title = f"{name_zh} ({name_en})" if name_zh and name_en and name_zh != name_en else (name_zh or name_en or name_es)

                icon_f = info.get("icon") or f"{itemid.lower()}.png"
                thumb = self.get_photo(icon_f, size=(36, 36), preserve_aspect=True) or self.get_photo(itemid.lower(), size=(36, 36), preserve_aspect=True)

                node_id = self.mat_tree.insert(
                    "",
                    "end",
                    text=f" {display_title}",
                    image=thumb or "",
                    values=(stock_str, stars, cat_display, itemid),
                    tags=(tag,)
                )
                self.tree_images[node_id] = thumb
                if not thumb and icon_f:
                    self.set_tree_item_image(self.mat_tree, node_id, icon_f, size=(36, 36), preserve_aspect=True)
                if not first_row:
                    first_row = node_id
                    
        if first_row:
            self.mat_tree.selection_set(first_row)
            self._on_mat_select(None)
