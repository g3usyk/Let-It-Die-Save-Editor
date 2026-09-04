# -*- coding: utf-8 -*-
"""
Tower & Master Unlocks Tab Mixin for LET IT DIE Save Editor.
"""

import tkinter as tk
from tkinter import ttk

import modifiers
import i18n
from i18n import t
from ui.theme import ACCENT_GOLD, ACCENT_CYAN, FG_MUTED


class TowerTabMixin:
    """Provides methods for constructing and handling the Tower & Master Unlocks Tab."""

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
        btn_unlock_elevators.pack(fill="x", pady=(2, 4))
        
        # 1b. Skip Tutorial & Unlock Waiting Room / Fighter Freezer
        btn_unlock_tutorial = ttk.Button(box_left, text=t("tw_tut_btn", "🎓 Desbloquear Sala y Congelador"), command=self._unlock_tutorial_action)
        btn_unlock_tutorial.pack(fill="x", pady=(0, 8))
        
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

    def _unlock_tutorial_action(self):
        if not self.save_json:
            return
        modifiers.unlock_tutorial_and_waiting_room(self.save_json)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Waiting Room & Freezer Unlocked", "Sala de Espera y Congelador Desbloqueados",
            "Tutorial completed and Waiting Room fully unlocked!\n\n• Fighter Freezer (Kiwako Seto): Unlocked\n• Chokufunsha Shop & Mushroom Club: Unlocked\n• Naomi Detox Quests & Direct Hell VIP Elevator: Unlocked\n• Player safely returned to Waiting Room",
            "¡Tutorial completado y Sala de Espera completamente desbloqueada!\n\n• Congelador de Luchadores (Kiwako Seto): Desbloqueado\n• Tienda Chokufunsha y Club Setas: Desbloqueados\n• Mostrador de Misiones y Ascensor VIP: Desbloqueados\n• Jugador posicionado de forma segura en la Sala de Espera"
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
