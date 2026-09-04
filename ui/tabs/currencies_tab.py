# -*- coding: utf-8 -*-
"""
Currencies & VIP Tab Mixin for LET IT DIE Save Editor.
"""

import tkinter as tk
from tkinter import ttk
import modifiers
import i18n
from i18n import t
from ui.theme import (
    BG_CARD, BG_DARK, BG_PANEL, FG_MUTED,
    ACCENT_GOLD, ACCENT_CYAN, ACCENT_GREEN, ACCENT_RED,
)

class CurrenciesTabMixin:
    """Provides methods for constructing and handling the Currencies & VIP Tab."""

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
