# -*- coding: utf-8 -*-
import re
import tkinter as tk
from tkinter import ttk, messagebox
import modifiers
from save_io import save_to_file
import i18n
from i18n import t
from ui.theme import *

class ArmorSetViewerDialog(tk.Toplevel):
    """Interactive visual dialog to inspect complete armor sets by tier like on letitdie.wiki.gg"""
    def __init__(self, parent, save_json, armor_sets, initial_set_id=None, initial_tier=1):
        super().__init__(parent)
        self.parent_app = parent
        self.save_json = save_json
        self.armor_sets = armor_sets
        self.title(t("dialog_armor_viewer_title"))
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
        is_en = (i18n.get_language() == "en")
        # 1. Header Toolbar
        header = tk.Frame(self, bg=BG_PANEL, padx=14, pady=10)
        header.pack(fill="x")
        
        row1 = ttk.Frame(header)
        row1.pack(fill="x")
        
        ttk.Label(row1, text=t("dialog_armor_set_label"), font=("Segoe UI", 11, "bold"), foreground=ACCENT_GOLD).pack(side="left", padx=(0, 8))
        
        set_names = [f"{s['name_en']} • {s['faction']}" if is_en else f"{s.get('name_es', s['name_en'])} ({s['name_en']}) • {s['faction']}" for s in self.armor_sets]
        self.cb_set_var = tk.StringVar(value=set_names[self.set_index] if self.armor_sets else "")
        cb_sets = ttk.Combobox(row1, textvariable=self.cb_set_var, values=set_names, state="readonly", width=52)
        cb_sets.pack(side="left", padx=4)
        cb_sets.bind("<<ComboboxSelected>>", self._on_set_changed)
        
        self.faction_lbl = ttk.Label(row1, text="", font=("Segoe UI", 10, "bold"))
        self.faction_lbl.pack(side="left", padx=10)
        
        # 2. Tier Selection Tabs
        tier_bar = tk.Frame(self, bg=BG_CARD, padx=10, pady=8)
        tier_bar.pack(fill="x", pady=(2, 4))
        
        ttk.Label(tier_bar, text=t("dialog_evolution_label"), font=("Segoe UI", 10, "bold"), foreground=FG_MAIN).pack(side="left", padx=(4, 10))
        
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
        left_box = ttk.LabelFrame(content_box, text=t("dialog_preview_title"), padding=10)
        left_box.pack(side="left", fill="both", expand=False, padx=(0, 6))
        left_box.config(width=340)
        
        self.model_lbl = ttk.Label(left_box, anchor="center")
        self.model_lbl.pack(fill="both", expand=True)
        
        self.model_title_lbl = ttk.Label(left_box, text="", font=("Segoe UI", 11, "bold"), foreground=ACCENT_GOLD, wraplength=320, justify="center")
        self.model_title_lbl.pack(pady=(4, 1))
        
        # Right Side: Piece & Weapon Stat Cards
        right_box = ttk.Frame(content_box)
        right_box.pack(side="right", fill="both", expand=True)
        
        slot_defs = [
            ("head", "🪖 HEAD (Helmet)" if is_en else "🪖 CASCO (Head)", "🪖"),
            ("body", "👕 BODY (Chest Armor)" if is_en else "👕 PECHERA (Body Armor)", "👕"),
            ("legs", "👖 LEGS (Pants)" if is_en else "👖 PANTALONES (Legs / Pants)", "👖"),
            ("weapon", "⚔️ SIGNATURE WEAPON" if is_en else "⚔️ ARMA CARACTERÍSTICA (Signature Weapon)", "⚔️")
        ]
        
        self.piece_cards = {}
        for slot_key, slot_title, emoji in slot_defs:
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
            
            btn_unlock = ttk.Button(btns_row, text="⭐ Unlock +4" if is_en else "⭐ Desbloquear +4", style="Accent.TButton", width=16)
            btn_unlock.pack(side="left", padx=2)
            
            btn_add = ttk.Button(btns_row, text="🎁 +1 to Storage" if is_en else "🎁 +1 al Almacén", width=14)
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
        
        ttk.Label(bottom_bar, text="Level:" if is_en else "Nivel:", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(side="left", padx=(4, 2))
        self.gear_target_lvl_var = tk.StringVar(value="+19 (Uncapped)")
        cb_glvl = ttk.Combobox(
            bottom_bar,
            textvariable=self.gear_target_lvl_var,
            values=["+19 (Uncapped)", "+24 (Max Uncapped)", "+4 (Base)"],
            state="readonly",
            width=18
        )
        cb_glvl.pack(side="left", padx=(0, 10))
        
        btn_unlock_set = ttk.Button(
            bottom_bar,
            text="⭐ Unlock Set + Weapon" if is_en else "⭐ Desbloquear Set + Arma",
            style="Accent.TButton",
            command=self.unlock_current_tier_set
        )
        btn_unlock_set.pack(side="left", padx=4)
        
        btn_add_set = ttk.Button(
            bottom_bar,
            text="🎁 Add Set to Storage" if is_en else "🎁 Añadir Set al Almacén",
            command=self.add_current_tier_set_storage
        )
        btn_add_set.pack(side="left", padx=4)
        
        btn_close = ttk.Button(bottom_bar, text="Close" if is_en else "Cerrar", command=self.destroy)
        btn_close.pack(side="right", padx=4)

    def _get_selected_gear_level(self):
        val = self.gear_target_lvl_var.get()
        if "+24" in val:
            return 25, 24
        elif "+4" in val:
            return 5, 4
        return 20, 19

    def _on_set_changed(self, event=None):
        sel_idx = self.cb_set_var.get()
        for idx, s in enumerate(self.armor_sets):
            lbl_es = f"{s.get('name_es', s['name_en'])} ({s['name_en']}) • {s['faction']}"
            lbl_en = f"{s['name_en']} • {s['faction']}"
            if sel_idx in (lbl_es, lbl_en):
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
        is_en = (i18n.get_language() == "en")
        s_name = s_obj['name_en'] if is_en else (s_obj.get('name_es') or s_obj['name_en'])
        self.faction_lbl.config(text=f"Faction: {s_obj['faction']}" if is_en else f"Facción: {s_obj['faction']}")
        
        # Highlight active tier button
        for tnum, btn in self.tier_buttons:
            if tnum == self.current_tier_num:
                btn.configure(style="Accent.TButton")
            else:
                btn.configure(style="TButton")
                
        # Find tier object
        t_obj = None
        for tier_item in s_obj.get("tiers", []):
            if tier_item["tier_num"] == self.current_tier_num:
                t_obj = tier_item
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
                self.model_lbl.config(image="", text="[Official Render In Progress]" if is_en else "[Render Oficial en Proceso]")
        else:
            self.model_lbl.config(image="", text="[Official Render In Progress]" if is_en else "[Render Oficial en Proceso]")
            
        t_name = t_obj.get('tier_name_en', t_obj['tier_name']) if is_en else t_obj['tier_name']
        self.model_title_lbl.config(text=f"{s_name} ({t_name})")
        
        # 2. Update piece cards
        counts = modifiers.get_equipment_inventory_counts(self.save_json) if self.save_json else ({}, {})
        storage_map, bag_map = counts
        pr_list = self.save_json.get("soul", {}).get("partresearch", {}).get("user", []) if self.save_json else []
        forge_levels = {}
        for r in pr_list:
            if isinstance(r, dict) and r.get("research_type") == "FINISHED":
                ptid = r.get("ptid")
                lvl = r.get("lvl", 0)
                if lvl > forge_levels.get(ptid, 0):
                    forge_levels[ptid] = lvl
        
        for slot_key in ["head", "body", "legs", "weapon"]:
            p = t_obj.get(slot_key)
            card_ui = self.piece_cards[slot_key]
            
            if not p:
                card_ui["frame"].pack_forget()
                continue
                
            card_ui["frame"].pack(fill="x", expand=True, pady=2)
            card_ui["current_pid"] = p["id"]
            
            # Title
            if is_en:
                name_str = f"{p['name']} ({p.get('name_es')})" if p.get('name_es') and p.get('name_es') != p['name'] else p['name']
            else:
                name_str = f"{p['name_es']} ({p['name']})" if p.get('name_es') and p['name_es'] != p['name'] else p['name']
            card_ui["title_lbl"].config(text=f"{name_str}  [{p['id']}]")
            
            if slot_key == "weapon":
                atk_base = p.get("atk", 0)
                atk_plus4 = p.get("atk_plus4", int(atk_base * 1.5))
                dur = p.get("durability", 1400)
                card_ui["def_dur_lbl"].config(text=t("dialog_atk_base", atk=atk_base, atk4=atk_plus4, dur=dur), foreground=ACCENT_GOLD)
                card_ui["res_lbl"].config(text=t("dialog_weapon_paired"))
                card_ui["btn_unlock"].config(text="⭐ Unlock Weapon +4" if is_en else "⭐ Desbloquear Arma +4")
            else:
                # Def / Dur
                def_base = p.get("def", 0)
                def_plus4 = p.get("def_plus4", 0)
                dur = p.get("durability", 0)
                card_ui["def_dur_lbl"].config(text=t("dialog_def_base", def_b=def_base, def4=def_plus4, dur=dur), foreground=ACCENT_CYAN)
                
                # Resistances
                res = p.get("resistances", {})
                if is_en:
                    res_txt = (
                        f"🗡️ Slash: {res.get('slash',0):+d}%   🔨 Blunt: {res.get('blunt',0):+d}%   🏹 Pierce: {res.get('pierce',0):+d}%\n"
                        f"🔥 Fire: {res.get('fire',0):+d}%   ⚡ Elec: {res.get('electric',0):+d}%   🧪 Poison: {res.get('poison',0):+d}%"
                    )
                else:
                    res_txt = (
                        f"🗡️ Corte: {res.get('slash',0):+d}%   🔨 Golpe: {res.get('blunt',0):+d}%   🏹 Perf: {res.get('pierce',0):+d}%\n"
                        f"🔥 Fuego: {res.get('fire',0):+d}%   ⚡ Elec: {res.get('electric',0):+d}%   🧪 Veneno: {res.get('poison',0):+d}%"
                    )
                card_ui["res_lbl"].config(text=res_txt)
                card_ui["btn_unlock"].config(text="⭐ Unlock +4" if is_en else "⭐ Desbloquear +4")
            
            # Status
            f_lvl = forge_levels.get(p["id"], 0)
            st_cnt = storage_map.get(p["id"], 0)
            bg_cnt = bag_map.get(p["id"], 0)
            
            if is_en:
                if f_lvl >= 20:
                    f_txt = "⭐ Shop: Unlocked (+19 Uncapped)"
                elif f_lvl >= 5:
                    f_txt = "⭐ Shop: Unlocked (+4)"
                elif f_lvl > 0:
                    f_txt = f"🔨 Shop: Level +{f_lvl-1}"
                else:
                    f_txt = "❌ Shop: Locked"
                st_txt = f"📦 Storage: {st_cnt} pcs." if st_cnt > 0 else "📦 Storage: 0 pcs."
                bg_txt = f"🎒 Bag: {bg_cnt} pcs." if bg_cnt > 0 else ""
            else:
                if f_lvl >= 20:
                    f_txt = "⭐ Tienda: Desbloqueado (+19 Destope)"
                elif f_lvl >= 5:
                    f_txt = "⭐ Tienda: Desbloqueado (+4)"
                elif f_lvl > 0:
                    f_txt = f"🔨 Tienda: Nivel +{f_lvl-1}"
                else:
                    f_txt = "❌ Tienda: Bloqueado"
                st_txt = f"📦 Almacén: {st_cnt} u." if st_cnt > 0 else "📦 Almacén: 0 u."
                bg_txt = f"🎒 Mochila: {bg_cnt} u." if bg_cnt > 0 else ""
            f_color = ACCENT_GOLD if f_lvl >= 5 else ACCENT_BLUE if f_lvl > 0 else FG_MUTED
            
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
        int_lvl, plus_lvl = self._get_selected_gear_level()
        modifiers.unlock_single_blueprint(self.save_json, pid, level=int_lvl, unlock_next_tier=True, auto_unlock_ancestors=True)
        modifiers.add_equipment_to_storage(self.save_json, pid, count=1, lvl=int_lvl, dur=50000)
        self._auto_save_and_sync()
        self.parent_app.filter_blueprints_list()
        self.display_current_set()
        
        is_en = i18n.get_language() == "en"
        title = "Blueprint & Item Unlocked" if is_en else "Plano y Objeto Desbloqueado"
        msg = (
            f"'{pid}' and its ancestor branch successfully unlocked!\n\n"
            f"1. 🛒 Chokufunsha: Available in Shop (+4) to purchase with Kill Coins.\n"
            f"2. 📦 Storage: 1 unit (+{plus_lvl}, 100% Durability) delivered to Coin Locker.\n"
            f"3. 💾 Save updated automatically."
        ) if is_en else (
            f"¡El objeto '{pid}' y toda su rama inferior han sido desbloqueados!\n\n"
            f"1. 🛒 Chokufunsha: Disponibles en tienda (+4) para comprar con Kill Coins.\n"
            f"2. 📦 Almacén: Se ha entregado 1 unidad (+{plus_lvl}, Dur 100%) en tu Almacén.\n"
            f"3. 💾 Partida guardada automáticamente."
        )
        messagebox.showinfo(title, msg)

    def add_single_piece_storage(self, pid):
        if not self.save_json or not pid:
            return
        int_lvl, plus_lvl = self._get_selected_gear_level()
        modifiers.add_equipment_to_storage(self.save_json, pid, count=1, lvl=int_lvl, dur=50000)
        self._auto_save_and_sync()
        self.parent_app.filter_blueprints_list()
        self.display_current_set()
        
        is_en = i18n.get_language() == "en"
        title = "Item Added" if is_en else "Objeto Añadido"
        msg = (
            f"1 unit of '{pid}' (+{plus_lvl}, Dur 100%) added to Coin Locker!\nSaved automatically."
        ) if is_en else (
            f"¡Se ha añadido 1 unidad de '{pid}' (+{plus_lvl}, Dur 100%) a tu Almacén!\nGuardado automáticamente."
        )
        messagebox.showinfo(title, msg)

    def unlock_current_tier_set(self):
        if not self.save_json or not self.armor_sets:
            return
        s_obj = self.armor_sets[self.set_index]
        t_obj = next((t for t in s_obj.get("tiers", []) if t["tier_num"] == self.current_tier_num), None)
        if not t_obj:
            return
            
        int_lvl, plus_lvl = self._get_selected_gear_level()
        unlocked = []

        # 1. Unlock all preceding tiers in this armor set (Tier 1, Tier 2, Tier 3, etc.)
        for tier_item in s_obj.get("tiers", []):
            if tier_item.get("tier_num", 0) < self.current_tier_num:
                for slot in ["head", "body", "legs", "weapon"]:
                    prev_p = tier_item.get(slot)
                    if prev_p and prev_p.get("id"):
                        modifiers.unlock_single_blueprint(
                            self.save_json,
                            prev_p["id"],
                            level=4,
                            unlock_next_tier=True,
                            auto_unlock_ancestors=True
                        )

        # 2. Unlock the current tier pieces + weapon and deliver to storage
        for slot in ["head", "body", "legs", "weapon"]:
            p = t_obj.get(slot)
            if p and p.get("id"):
                pid = p["id"]
                modifiers.unlock_single_blueprint(
                    self.save_json,
                    pid,
                    level=int_lvl,
                    unlock_next_tier=True,
                    auto_unlock_ancestors=True
                )
                modifiers.add_equipment_to_storage(self.save_json, pid, count=1, lvl=int_lvl, dur=50000)
                unlocked.append(f"{p['name']} ({p.get('name_es', p['name'])})")
                
        self._auto_save_and_sync()
        self.parent_app.filter_blueprints_list()
        self.display_current_set()
        
        is_en = i18n.get_language() == "en"
        title = "Complete Set + Weapon Unlocked" if is_en else "Set + Arma Completa Desbloqueados"
        s_name = s_obj['name_en'] if is_en else s_obj.get('name_es', s_obj['name_en'])
        t_name = t_obj.get('tier_name_en', t_obj['tier_name']) if is_en else t_obj['tier_name']
        msg = (
            f"{s_name} ({t_name}), preceding branch tiers, and signature weapon unlocked!\n\n"
            f"🛒 Chokufunsha: Pieces, lower tiers, and weapon ready to purchase in Shop with KC.\n"
            f"📦 Storage: 1 copy of each armor piece + weapon (+{plus_lvl}, 100% Durability) added to Coin Locker.\n"
            f"💾 Save file updated automatically.\n\n"
            + "\n".join([f"• {u}" for u in unlocked])
        ) if is_en else (
            f"¡El {s_name} ({t_name}), sus tiers inferiores y su arma han sido desbloqueados!\n\n"
            f"🛒 Tienda Chokufunsha: Las piezas, los tiers previos y el arma están listos para comprar con Kill Coins.\n"
            f"📦 Almacén: Se ha entregado 1 copia de cada armadura + el arma (Nivel +{plus_lvl}, 100% Durabilidad) en tu Almacén.\n"
            f"💾 Partida guardada automáticamente.\n\n"
            + "\n".join([f"• {u}" for u in unlocked])
        )
        messagebox.showinfo(title, msg)

    def add_current_tier_set_storage(self):
        if not self.save_json or not self.armor_sets:
            return
        s_obj = self.armor_sets[self.set_index]
        t_obj = next((t for t in s_obj.get("tiers", []) if t["tier_num"] == self.current_tier_num), None)
        if not t_obj:
            return
            
        int_lvl, plus_lvl = self._get_selected_gear_level()
        added = []
        for slot in ["head", "body", "legs", "weapon"]:
            p = t_obj.get(slot)
            if p and p.get("id"):
                modifiers.add_equipment_to_storage(self.save_json, p["id"], count=1, lvl=int_lvl, dur=50000)
                added.append(f"{p['name']} ({p.get('name_es', p['name'])})")
                
        self._auto_save_and_sync()
        self.parent_app.filter_blueprints_list()
        self.display_current_set()
        
        is_en = i18n.get_language() == "en"
        title = "Set + Weapon Added" if is_en else "Set + Arma Añadidos al Almacén"
        msg = (
            f"Added 3 armor pieces + signature weapon (+{plus_lvl}, Dur 100%) to Coin Locker!\n\n"
            + "\n".join([f"• {a}" for a in added])
            + "\n\nSaved automatically."
        ) if is_en else (
            f"¡Se han añadido al Almacén las 3 piezas del set + el arma característica (Nivel +{plus_lvl}, Dur 100%)!\n\n"
            + "\n".join([f"• {a}" for a in added])
            + "\n\nPartida guardada automáticamente."
        )
        messagebox.showinfo(title, msg)

if __name__ == "__main__":
    from editor_gui import CompleteSaveEditorGUI
    app = CompleteSaveEditorGUI()
    app.mainloop()
