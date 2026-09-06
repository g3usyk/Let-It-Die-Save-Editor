# -*- coding: utf-8 -*-
"""
Blueprints & Chokufunsha R&D Tab Mixin for LET IT DIE Save Editor.
"""

import os
import sys
import re
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import modifiers
import i18n
from i18n import t, get_set_name
from ui.theme import ACCENT_GOLD, ACCENT_CYAN, ACCENT_BLUE, FG_MAIN, FG_MUTED
from ui.components import ScrollableFrame
from ui.dialogs import ArmorSetViewerDialog

if getattr(sys, "frozen", False):
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    mei_dir = getattr(sys, "_MEIPASS", exe_dir)
    BASE_DIR = exe_dir if os.path.isdir(os.path.join(exe_dir, "icons")) else mei_dir
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

ICONS_DIR = os.path.join(BASE_DIR, "icons")


class BlueprintsTabMixin:
    """Provides methods for constructing and handling the Blueprints / R&D Tab."""

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
        self.blueprints_scroll = scroll_bp = ScrollableFrame(bp_card_container)
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
        cb_slvl = ttk.Combobox(act_r1, textvariable=self.bp_single_lvl_var, values=["+4", "+3", "+2", "+1", "+0 (Plano)", "+19"], width=9, state="readonly")
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
        ttk.Button(global_gear_box, text=t("bp_upg_all24_btn"), command=lambda: self._upgrade_all_gear_max_lvl_action(20)).pack(fill="x", pady=2)

        # Chokufunsha Shop Tier Suppression Mod Box
        shop_tiers_box = ttk.LabelFrame(self.bp_card, text=t("bp_shop_tiers_mod_title"), padding=8)
        shop_tiers_box.pack(fill="x", pady=4)

        ttk.Label(shop_tiers_box, text=t("bp_shop_tiers_mod_desc"), wraplength=260, justify="left", foreground=FG_MUTED, font=("Segoe UI", 8)).pack(fill="x", pady=(0, 4))
        self.bp_shop_tiers_status_lbl = ttk.Label(shop_tiers_box, text=t("bp_shop_tiers_inactive_status"), font=("Segoe UI", 9, "bold"), foreground=FG_MUTED, wraplength=260)
        self.bp_shop_tiers_status_lbl.pack(fill="x", pady=(0, 4))

        st_btn_row = ttk.Frame(shop_tiers_box)
        st_btn_row.pack(fill="x", pady=2)
        ttk.Button(st_btn_row, text=t("bp_shop_tiers_enable_btn"), style="Accent.TButton", command=self._enable_all_shop_tiers_action).pack(fill="x", pady=1)
        ttk.Button(st_btn_row, text=t("bp_shop_tiers_restore_btn"), command=self._restore_shop_tiers_action).pack(fill="x", pady=1)

        self._refresh_shop_tiers_status()

    def _find_equipment_art(self, ptid):
        if hasattr(self, "icon_map"):
            if "gear_icons" in self.icon_map:
                if ptid in self.icon_map["gear_icons"]:
                    return self.icon_map["gear_icons"][ptid]
                if ptid.endswith("_G") and ptid[:-2] in self.icon_map["gear_icons"]:
                    return self.icon_map["gear_icons"][ptid[:-2]]
            if "gear_cards" in self.icon_map and ptid in self.icon_map["gear_cards"]:
                return self.icon_map["gear_cards"][ptid]
            if "equipment_thumbs" in self.icon_map and ptid in self.icon_map["equipment_thumbs"]:
                return self.icon_map["equipment_thumbs"][ptid]

        clean = ptid.lower().replace("pt_", "").replace("_001", "").replace("_01", "")
        candidates = [
            f"{ptid.lower()}.png",
            f"{ptid.lower()[:-2]}.png" if ptid.lower().endswith("_g") else None,
            f"thumb_{ptid.lower()}.png",
            f"{clean}.png"
        ]
        candidates = [c for c in candidates if c]

        # Check AssetManager manifest
        if hasattr(self, "asset_manager") and getattr(self.asset_manager, "manifest", None):
            for c in candidates:
                c_low = c.lower()
                if c_low in self.asset_manager.manifest:
                    return self.asset_manager.manifest[c_low]

        search_roots = [ICONS_DIR, getattr(getattr(self, "asset_manager", None), "cache_dir", "")]
        for base in search_roots:
            if not base or not os.path.isdir(base):
                continue
            for folder in ["all_official", "weapons", "armor", "cards", "sets", "gear", "thumbs"]:
                p = os.path.join(base, folder, f"{ptid.lower()}.png")
                if os.path.exists(p):
                    return f"{folder}/{ptid.lower()}.png"
                if ptid.lower().endswith("_g"):
                    p_base = os.path.join(base, folder, f"{ptid.lower()[:-2]}.png")
                    if os.path.exists(p_base):
                        return f"{folder}/{ptid.lower()[:-2]}.png"
                p_thumb = os.path.join(base, folder, f"thumb_{ptid.lower()}.png")
                if os.path.exists(p_thumb):
                    return f"{folder}/thumb_{ptid.lower()}.png"
                p_clean = os.path.join(base, folder, f"{clean}.png")
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
                uncap_vals = [
                    "+19 (In R&D)", "+19 (Shop Max)", "+18", "+17", "+16", "+15", "+14", "+13",
                    "+12", "+11", "+10", "+9", "+8", "+7", "+6", "+5", "+4", "+3", "+2", "+1", "+0 (Blueprint)"
                ] if is_en else [
                    "+19 (En I+D)", "+19 (Tienda Máx)", "+18", "+17", "+16", "+15", "+14", "+13",
                    "+12", "+11", "+10", "+9", "+8", "+7", "+6", "+5", "+4", "+3", "+2", "+1", "+0 (Plano)"
                ]
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

                if nextptid:
                    nxt_meta = next((item for item in self.equipment_db if item["id"] == nextptid), None)
                    nxt_name = ((nxt_meta.get("name_en") if is_en else nxt_meta.get("name_es")) if nxt_meta else "") or nextptid
                    self.bp_evolve_lbl.config(
                        text=f"🔄 Evolves at +4 to: {nxt_name}" if is_en else f"🔄 Evoluciona a Nvl +4 a: {nxt_name}",
                        foreground=ACCENT_CYAN
                    )
                    if hasattr(self, "btn_evolve_tier"):
                        is_nxt_uncap = nxt_meta.get("can_uncap", False) if nxt_meta else False
                        btn_txt = t("bp_evolve_to_uncapped", name=nxt_name) if is_nxt_uncap else t("bp_evolve_to_next", name=nxt_name)
                        self.btn_evolve_tier.config(text=btn_txt)
                        self.btn_evolve_tier.pack(fill="x", pady=(2, 4))
                else:
                    self.bp_evolve_lbl.config(
                        text="⭐ Max Tier: +4" if is_en else "⭐ Tier Máximo: +4",
                        foreground=ACCENT_CYAN
                    )
                    if hasattr(self, "btn_evolve_tier"):
                        self.btn_evolve_tier.pack_forget()
            
        card_art = None
        if hasattr(self, "icon_map") and "gear_cards" in self.icon_map:
            card_art = self.icon_map["gear_cards"].get(ptid)
        if not card_art:
            card_art = self._find_equipment_art(ptid)
            
        self.set_widget_image(self.bp_art_lbl, card_art or self._find_equipment_art(ptid), size=(280, 140), preserve_aspect=True, fallback="blueprint")

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

    def _parse_selected_level(self, val_str):
        val = str(val_str).strip()
        is_shop_max = ("tienda máx" in val.lower() or "tienda max" in val.lower() or "shop max" in val.lower())
        is_rnd = ("i+d" in val.lower() or "r&d" in val.lower())
        m = re.search(r"\+?(\d+)", val)
        lvl_num = int(m.group(1)) if m else 0
        return lvl_num, is_shop_max, is_rnd

    def _unlock_single_bp_shop(self):
        if not self.current_bp_selection or not self.save_json:
            return
        ptid = self.current_bp_selection
        item_meta = next((item for item in self.equipment_db if item["id"] == ptid), None)
        can_uncap = item_meta.get("can_uncap", True) if item_meta else True
        
        lvl_num, is_shop_max, is_rnd = self._parse_selected_level(self.bp_single_lvl_var.get())
        if is_shop_max or lvl_num in (20, 24, 25):
            api_lvl = 20 if can_uncap else 5
            display_lvl = 19 if can_uncap else 4
        else:
            api_lvl = lvl_num
            display_lvl = lvl_num

        next_unlocked = modifiers.unlock_single_blueprint(self.save_json, ptid, level=api_lvl, unlock_next_tier=True)
        self._auto_save()
        self.filter_blueprints_list()
        
        is_en = (i18n.get_language() == "en")
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
        lvl_num, _, _ = self._parse_selected_level(val)
        
        if "+0" in val or "plano" in val.lower() or "blueprint" in val.lower() or lvl_num <= 0:
            target_lvl = 0
        elif lvl_num in (19, 20, 24, 25):
            target_lvl = 19
        else:
            target_lvl = lvl_num
            
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
            prev_num = target_lvl - 1
            prev_str = f"+{prev_num} (Uncapped)" if prev_num >= 19 else f"+{prev_num}"
            prev_str_es = f"+{prev_num} (Destope)" if prev_num >= 19 else f"+{prev_num}"
            next_str = f"+{target_lvl} (Uncapped)" if target_lvl >= 19 else f"+{target_lvl}"
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
        item_meta = next((item for item in self.equipment_db if item["id"] == ptid), None)
        can_uncap = item_meta.get("can_uncap", True) if item_meta else True
        
        lvl_num, _, _ = self._parse_selected_level(self.bp_single_lvl_var.get())
        if lvl_num >= 19:
            lvl = 20 if can_uncap else 5
            plus = 19 if can_uncap else 4
        elif lvl_num <= 0:
            lvl = 1
            plus = 0
        else:
            lvl = min(20 if can_uncap else 5, lvl_num + 1)
            plus = min(19 if can_uncap else 4, lvl_num)
            
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

    def _refresh_shop_tiers_status(self):
        if not hasattr(self, "bp_shop_tiers_status_lbl"):
            return
        status = modifiers.get_shop_tier_mod_status()
        if status.get("active"):
            count = status.get("modified_count", 0)
            self.bp_shop_tiers_status_lbl.config(
                text=t("bp_shop_tiers_active_status", count=count),
                foreground=ACCENT_GOLD
            )
        else:
            self.bp_shop_tiers_status_lbl.config(
                text=t("bp_shop_tiers_inactive_status"),
                foreground=FG_MUTED
            )

    def _enable_all_shop_tiers_action(self):
        res = modifiers.enable_all_shop_tiers()
        self._refresh_shop_tiers_status()
        if res.get("success"):
            cnt = res.get("modified_count", 0)
            self._notify(
                "Shop Mod Active!", "¡Mod Tienda Activado!",
                f"All {cnt} equipment evolution tiers (Tiers 1 to 4) unlocked in Chokufunsha Shop!\nYou can now purchase any tier directly from the store.",
                f"¡Los {cnt} tiers de evolución (Tiers 1 al 4) ahora están desbloqueados en la Tienda Chokufunsha!\nPuedes comprar cualquier tier directamente en la tienda."
            )
        else:
            messagebox.showerror(t("notice"), f"Error: {res.get('reason')}")

    def _restore_shop_tiers_action(self):
        res = modifiers.restore_shop_tier_progression()
        self._refresh_shop_tiers_status()
        if res.get("success"):
            self._notify(
                "Progression Restored", "Progresión Restaurada",
                "Standard Chokufunsha tier progression restored.\nOnly the latest researched tier will be displayed in the store.",
                "Progresión estándar de Chokufunsha restaurada.\nSólo se mostrará el último tier investigado en la tienda."
            )
        else:
            messagebox.showerror(t("notice"), f"Error: {res.get('reason')}")

    def unlock_all_blueprints_preset(self):
        if not self.save_json:
            return
        val = str(self.bp_unlock_all_lvl_var.get())
        lvl_num, _, _ = self._parse_selected_level(val)
        if lvl_num in (19, 20, 24, 25):
            lvl = 19
        elif lvl_num > 0:
            lvl = lvl_num
        else:
            lvl = 19
        modifiers.unlock_all_blueprints(self.save_json, level=lvl, enable_shop_tiers=False)
        self._refresh_shop_tiers_status()
        self._auto_save()
        self.filter_blueprints_list()
        self._notify(
            "Blueprints Unlocked", "Planos Desbloqueados",
            f"All weapon and armor blueprints unlocked at Level +{lvl} in Chokufunsha!\nAll lower tiers (Tier 1-4) are available in the store.",
            f"¡Todos los planos de armas y armaduras han sido desbloqueados al Nivel +{lvl} en Chokufunsha!\nTodos los tiers inferiores (Tier 1 al 4) están disponibles en la tienda."
        )

    def _repair_blueprints_action(self):
        if not self.save_json:
            return
        fixed = modifiers.repair_unlocked_blueprints_states(self.save_json)
        clamped_bp, clamped_st = modifiers.clamp_all_equipment_authentic_levels(self.save_json)
        self._auto_save()
        self.filter_blueprints_list()
        self._notify(
            "Blueprints Verified", "Planos Reparados",
            f"Verified and fixed {fixed} blueprints in Chokufunsha!\nAudited and clamped {clamped_bp} uncap blueprints to authentic +19 (level 15) and {clamped_st} storage items.",
            f"¡Se han verificado {fixed} planos en Chokufunsha!\nSe auditaron y ajustaron {clamped_bp} planos de destope al auténtico +19 (nivel 15) y {clamped_st} objetos del alijo."
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
        
        name, added = modifiers.inject_endgame_set(self.save_json, set_key=key, count=1, dur=50000, lvl=20)
        self._auto_save()
        self.filter_blueprints_list()
        self.refresh_all_views()
        self._notify(
            "Endgame Set Injected", "Set Endgame Inyectado",
            f"Added {added} pieces of {name} (+19 Uncapped, 100% Durability) to Coin Locker & Shop!",
            f"¡Se han añadido las {added} piezas del set {name} (Nivel +19 Uncapped, Durabilidad 100%) a tu Almacén y Tienda!"
        )

    def _set_infinite_durability_action(self):
        if not self.save_json:
            return
        cnt = modifiers.set_infinite_durability_all_equipment(self.save_json, target_dur=50000)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "100% Durability Restored", "Durabilidad al 100% Restaurada",
            f"Restored 100% authentic durability on {cnt} weapons and armors across Storage and Bags!\n\nYour equipment is in factory-fresh condition.",
            f"¡Se ha restaurado la durabilidad al 100% auténtico en {cnt} piezas de armas y armaduras en tu Almacén y Bolsas!\n\n¡Tu equipo está en estado impecable!"
        )

    def _set_massive_ammo_action(self):
        if not self.save_json:
            return
        cnt = modifiers.set_massive_ammo_all_weapons(self.save_json, ammo=None)
        self._auto_save()
        self.refresh_all_views()
        self._notify(
            "Max Ammo Refilled", "Munición al Máximo Recargada",
            f"Refilled authentic full magazine and reserve ammo for {cnt} ranged firearms in Storage and Bags!\nCleaned any erroneous ammo on melee weapons.",
            f"¡Se ha recargado el cargador y la reserva máxima auténtica para {cnt} armas de fuego en Almacén y Bolsas!\nSe limpió cualquier munición errónea en armas cuerpo a cuerpo."
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
                "All Uncapped Gear in Shop (+19)!", "¡Todo el Equipo Destopado en Tienda (+19)!",
                f"Updated {cnt} items! All uncapped gear unlocked at Level +19 directly in Chokufunsha Shop & Storage!\nSaved automatically.",
                f"¡Se han actualizado {cnt} piezas! ¡Todo el equipo destopado se desbloqueó al Nivel +19 directamente en la Tienda Chokufunsha y Almacén!\nGuardado automáticamente."
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
            if not thumb and art_rel:
                self.set_tree_item_image(self.bp_tree, node_id, art_rel, size=(36, 36), preserve_aspect=True, fallback="weapon" if ("WP" in bp_id or "ARM" in bp_id) else "blueprint")
            if not first_row:
                first_row = node_id
                
        if first_row:
            self.bp_tree.selection_set(first_row)
            self._on_bp_select(None)
