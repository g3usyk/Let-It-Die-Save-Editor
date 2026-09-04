# -*- coding: utf-8 -*-
"""
Weapon Mastery Tab Mixin for LET IT DIE Save Editor.
"""

import tkinter as tk
from tkinter import ttk, simpledialog

import modifiers
import i18n
from i18n import t, get_expert_weapon_name
from game_data import WEAPON_CATEGORIES

WEAPON_MASTERY_ICONS = {wt: img for wt, nm, img in WEAPON_CATEGORIES}


class MasteryTabMixin:
    """Provides methods for constructing and handling the Weapon Mastery Tab."""

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
