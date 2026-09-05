# -*- coding: utf-8 -*-
"""
Decals Tab Mixin for LET IT DIE Save Editor.
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

if getattr(sys, "frozen", False):
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    mei_dir = getattr(sys, "_MEIPASS", exe_dir)
    BASE_DIR = exe_dir if os.path.isdir(os.path.join(exe_dir, "icons")) else mei_dir
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

ICONS_DIR = os.path.join(BASE_DIR, "icons")


class DecalsTabMixin:
    """Provides methods for constructing and handling the Official Decals Tab."""

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
        self.decals_scroll = scroll_decal = ScrollableFrame(decal_card_container)
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
