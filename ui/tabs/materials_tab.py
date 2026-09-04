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

                # Query search with smart multi-word matching & Tier aliases
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
