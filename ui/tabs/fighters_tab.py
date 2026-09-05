# -*- coding: utf-8 -*-
"""
Fighters Freezer Tab Mixin for LET IT DIE Save Editor.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import modifiers
import i18n
from i18n import t
from ui.theme import (
    BG_CARD, BG_DARK, BG_PANEL, FG_MAIN, FG_MUTED,
    ACCENT_GOLD, ACCENT_GREEN, ACCENT_CYAN, ACCENT_RED,
)
from ui.components import ScrollableFrame, ImageCombobox
from ui.dialogs import CreateFighterDialog, FighterModelGalleryDialog, get_fighter_model_art
from game_data import FIGHTER_CLASSES


class FightersTabMixin:
    """Provides methods for constructing and handling the Fighter Freezer Tab."""

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
        
        # Unlock Freezer (Skip Tutorial) Button
        self.btn_unlock_freezer = ttk.Button(
            left_box,
            text=t("f_tut_btn", "🎓 Desbloquear Congelador (Saltar Tutorial)"),
            command=self._unlock_freezer_action
        )
        self.btn_unlock_freezer.pack(fill="x", pady=(0, 4))
        
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
        
        self.fighters_scroll = scroll_right = ScrollableFrame(right_container)
        scroll_right.pack(fill="both", expand=True)
        right_box = scroll_right.content
        
        # Fighter Top Profile
        prof_f = ttk.Frame(right_box)
        prof_f.pack(fill="x", pady=2)
        
        self.f_model_hero_lbl = ttk.Label(prof_f, cursor="hand2")
        self.f_model_hero_lbl.pack(side="left", padx=(0, 10))
        self.f_model_hero_lbl.bind("<Button-1>", lambda e: self._open_fighter_model_gallery())
        
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
        self.f_model_items = [
            (opt, get_fighter_model_art(opt)) for opt in self.f_model_opts
        ]
        
        model_row = ttk.Frame(id_frame)
        model_row.grid(row=3, column=1, columnspan=3, padx=4, pady=3, sticky="w")
        
        self.cb_f_model = ImageCombobox(
            model_row,
            values_with_icons=self.f_model_items,
            textvariable=self.f_model_select_var,
            get_photo_cb=self.get_photo,
            width=270
        )
        self.cb_f_model.pack(side="left", padx=(0, 8))
        self.cb_f_model.bind("<<ComboboxSelected>>", lambda e: self._update_fighter_model_preview())
        
        is_en = (i18n.get_language() == "en")
        btn_gallery = ttk.Button(model_row, text="🖼️ " + ("Gallery" if is_en else "Galería"), style="Accent.TButton", command=self._open_fighter_model_gallery)
        btn_gallery.pack(side="left")
        
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
            self._update_fighter_model_preview()
            
            # Calculate real in-game bag capacity
            db_st = modifiers.get_deathbag_masters_status(save_path=getattr(self, "save_path", None))
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

    def _update_fighter_model_preview(self):
        sel_val = self.f_model_select_var.get() if hasattr(self, "f_model_select_var") else ""
        art_rel = get_fighter_model_art(sel_val)
        
        # 1. Sync ImageCombobox display
        if hasattr(self, "cb_f_model"):
            self.cb_f_model.set(sel_val)
            
        # 2. Hero portrait in profile header
        if hasattr(self, "f_model_hero_lbl"):
            photo_hero = self.get_photo(art_rel, size=(54, 66), preserve_aspect=True)
            self.f_model_hero_lbl.config(image=photo_hero or "")
            self.tree_images["f_model_hero"] = photo_hero

    def _open_fighter_model_gallery(self):
        cur = self.f_model_select_var.get() if hasattr(self, "f_model_select_var") else ""
        def on_picked(full_opt, code):
            if hasattr(self, "f_model_select_var"):
                self.f_model_select_var.set(full_opt)
            if hasattr(self, "cb_f_model"):
                self.cb_f_model.set(full_opt)
            self._update_fighter_model_preview()
        FighterModelGalleryDialog(self, current_model=cur, on_select_cb=on_picked)

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

    def _unlock_freezer_action(self):
        if not self.save_json:
            return
        modifiers.unlock_tutorial_and_waiting_room(self.save_json)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Freezer Unlocked", "Congelador Desbloqueado",
            "Tutorial completed! Kiwako Seto's Fighter Freezer and all Waiting Room facilities are now fully accessible.",
            "¡Tutorial completado! El Congelador de Kiwako Seto y las instalaciones de la Sala de Espera ya están 100% accesibles."
        )

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
        st = modifiers.get_deathbag_masters_status(save_path=getattr(self, "save_path", None))
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
            res = modifiers.expand_deathbag_capacity(target_capacity=target, vip_bonus=10, save_path=getattr(self, "save_path", None))
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
            res = modifiers.restore_deathbag_capacity(save_path=getattr(self, "save_path", None))
            self._refresh_deathbag_db_status()
            if hasattr(self, "current_fighter_idx"):
                self._on_fighter_select(None)
            messagebox.showinfo(
                t("db_restore_success_title"),
                t("db_restore_success_msg", path=res['db_path'])
            )
        except Exception as e:
            messagebox.showerror("Error", f"masters.db:\n{e}")
