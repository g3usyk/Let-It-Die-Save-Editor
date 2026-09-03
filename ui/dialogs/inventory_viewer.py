# -*- coding: utf-8 -*-
import os
import json
import tkinter as tk
from tkinter import ttk
from collections import Counter
import modifiers
import i18n
from i18n import t
from ui.theme import *

class InventoryViewerDialog(tk.Toplevel):
    """Dialog that displays the complete physical inventory of the player's Coin Locker and Fighter Deathbag."""
    def __init__(self, parent, save_json, equipment_db, materials_db, shrooms_beasts_db=None):
        super().__init__(parent)
        self.title(t("dialog_inventory_title"))
        self.geometry("960x650")
        self.configure(bg=BG_DARK)
        self.transient(parent)
        self.grab_set()
        
        self.save_json = save_json
        self.equipment_db = {e["id"]: e for e in equipment_db} if isinstance(equipment_db, list) else dict(equipment_db)
        self.materials_db = {m["itemid"]: m for m in materials_db} if isinstance(materials_db, list) else dict(materials_db)
        
        if shrooms_beasts_db:
            self.shrooms_beasts_db = shrooms_beasts_db
        else:
            sb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_shrooms_beasts_db.json")
            if os.path.exists(sb_path):
                try:
                    with open(sb_path, "r", encoding="utf-8") as f:
                        self.shrooms_beasts_db = json.load(f)
                except Exception:
                    self.shrooms_beasts_db = {}
            else:
                self.shrooms_beasts_db = {}
                
        self.parent_app = parent
        self.tree_images = {}
        
        self._build_ui()
        self.refresh_inventory()
        
    def _build_ui(self):
        # Header frame
        header = tk.Frame(self, bg=BG_PANEL, padx=14, pady=10)
        header.pack(fill="x")
        
        ttk.Label(header, text=t("inv_title"), font=("Segoe UI", 13, "bold"), foreground=ACCENT_GOLD).pack(anchor="w")
        self.cap_lbl = ttk.Label(header, text="...", font=("Segoe UI", 10))
        self.cap_lbl.pack(anchor="w", pady=(3, 4))
        
        self.cap_bar = ttk.Progressbar(header, orient="horizontal", mode="determinate", length=400)
        self.cap_bar.pack(fill="x")
        
        # Filter and Search row
        filter_frame = tk.Frame(self, bg=BG_DARK, padx=14, pady=8)
        filter_frame.pack(fill="x")
        
        ttk.Label(filter_frame, text=t("inv_search")).pack(side="left", padx=2)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_inventory())
        ttk.Entry(filter_frame, textvariable=self.search_var, width=16).pack(side="left", padx=2)
        
        ttk.Label(filter_frame, text=t("inv_cat")).pack(side="left", padx=(10, 2))
        self.cat_filter_var = tk.StringVar(value=t("inv_cat_all"))
        self.cat_values = [
            t("inv_cat_all"),
            t("inv_cat_mats"),
            t("inv_cat_gear"),
            t("inv_cat_shrooms"),
            t("inv_cat_bag")
        ]
        cb_cat = ttk.Combobox(
            filter_frame,
            textvariable=self.cat_filter_var,
            values=self.cat_values,
            state="readonly",
            width=22
        )
        cb_cat.pack(side="left", padx=2)
        cb_cat.bind("<<ComboboxSelected>>", lambda e: self.refresh_inventory())
        
        ttk.Button(filter_frame, text=t("inv_refresh"), command=self.refresh_inventory).pack(side="right", padx=3)
        
        # Treeview
        table_frame = tk.Frame(self, bg=BG_DARK, padx=14, pady=4)
        table_frame.pack(fill="both", expand=True)
        
        cols = ("qty", "loc", "cat", "id")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="tree headings", height=16)
        self.tree.heading("#0", text=t("inv_col_name"))
        self.tree.heading("qty", text=t("inv_col_qty"))
        self.tree.heading("loc", text=t("inv_col_loc"))
        self.tree.heading("cat", text=t("inv_col_cat"))
        self.tree.heading("id", text=t("inv_col_id"))
        
        self.tree.column("#0", width=380)
        self.tree.column("qty", width=90, anchor="center")
        self.tree.column("loc", width=120, anchor="center")
        self.tree.column("cat", width=150)
        self.tree.column("id", width=140)
        
        self.tree.tag_configure("tag_material", foreground=ACCENT_GOLD)
        self.tree.tag_configure("tag_gear", foreground=ACCENT_BLUE)
        self.tree.tag_configure("tag_bag", foreground=ACCENT_GREEN)
        self.tree.tag_configure("tag_shroom", foreground="#FFB347")
        self.tree.tag_configure("tag_beast", foreground="#77DD77")
        
        ysb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        ysb.pack(side="right", fill="y")
        
        # Bottom Bar
        bottom_bar = tk.Frame(self, bg=BG_PANEL, padx=14, pady=8)
        bottom_bar.pack(fill="x")
        
        self.status_lbl = ttk.Label(bottom_bar, text="---", font=("Segoe UI", 9))
        self.status_lbl.pack(side="left")
        
        ttk.Button(bottom_bar, text=t("dialog_close_btn"), command=self.destroy).pack(side="right", padx=2)

    def refresh_inventory(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        if not self.save_json:
            return
            
        is_en = i18n.get_language() == "en"
        cl = self.save_json.get("soul", {}).get("cl", [])
        total_slots = len(cl)
        used_slots = len([c for c in cl if c.get("type") != -1 and c.get("eid")])
        free_slots = max(0, total_slots - used_slots)
        pct = (used_slots / total_slots * 100) if total_slots > 0 else 0
        
        self.cap_lbl.config(
            text=t("inv_cap_lbl", used=used_slots, total=total_slots, free=free_slots, pct=pct)
        )
        self.cap_bar["value"] = pct
        
        query = self.search_var.get().lower().strip()
        cat_filter = self.cat_filter_var.get()
        
        is_cat_all = (cat_filter == t("inv_cat_all")) or ("Todos" in cat_filter) or ("All" in cat_filter)
        is_cat_mats = ("Material" in cat_filter)
        is_cat_gear = ("Arma" in cat_filter) or ("Gear" in cat_filter) or ("Weapon" in cat_filter)
        is_cat_shrooms = ("Seta" in cat_filter) or ("Shroom" in cat_filter) or ("Mushroom" in cat_filter) or ("Beast" in cat_filter) or ("Criatura" in cat_filter)
        is_cat_bag = ("Mochila" in cat_filter) or ("Bag" in cat_filter) or ("Equip" in cat_filter)
        
        # 1. Materials from save["item"]["items"]
        items = self.save_json.get("item", {}).get("items", [])
        mat_counts = Counter()
        for it in items:
            mat_counts[it.get("itemid", "")] += 1
            
        # 2. Equipment counts from save["part"]["pts"]
        storage_gear, bag_gear = modifiers.get_equipment_inventory_counts(self.save_json)
        
        # 3. Mushrooms from save["mushroom"]["msrs"]
        shroom_items = self.save_json.get("mushroom", {}).get("msrs", [])
        shroom_counts = Counter()
        for sh in shroom_items:
            mid = sh.get("msrid", "")
            if mid:
                state = sh.get("state", 0)
                owner = sh.get("owner", "COIN_LOCKER")
                shroom_counts[(mid, state, owner)] += 1
                
        # 4. Beasts from save["beast"]["bsts"]
        beast_items = self.save_json.get("beast", {}).get("bsts", [])
        beast_counts = Counter()
        for bst in beast_items:
            bid = bst.get("bstid", "")
            if bid:
                owner = bst.get("owner", "COIN_LOCKER")
                beast_counts[(bid, owner)] += 1
                
        total_entries = 0
        total_units = 0
        
        # Insert Materials
        if is_cat_all or is_cat_mats:
            for itemid, qty in mat_counts.items():
                if not itemid or qty <= 0:
                    continue
                info = self.materials_db.get(itemid, {})
                name_es = info.get("name_es", info.get("name", itemid))
                name_en = info.get("name_en", "")
                cat = info.get("category", "Material" if is_en else "Materiales")
                
                if query and (query not in name_es.lower() and query not in name_en.lower() and query not in itemid.lower() and query not in cat.lower()):
                    continue
                    
                if is_en:
                    display_name = f"{name_en} ({name_es})" if name_es and name_en != name_es else (name_en or name_es)
                else:
                    display_name = f"{name_es} ({name_en})" if name_en and name_en != name_es else (name_es or name_en)
                icon_k = self.parent_app._get_mat_photo_key(itemid, name_en or name_es)
                thumb = self.parent_app.get_photo(icon_k, size=(24, 24))
                
                node = self.tree.insert(
                    "",
                    "end",
                    text=f" {display_name}",
                    image=thumb or "",
                    values=(t("inv_unit_str", qty=qty), t("inv_loc_storage"), cat, itemid),
                    tags=("tag_material",)
                )
                self.tree_images[node] = thumb
                total_entries += 1
                total_units += qty
                
        # Insert Mushrooms
        if is_cat_all or is_cat_shrooms:
            for (mid, state, owner), qty in shroom_counts.items():
                meta = self.shrooms_beasts_db.get(mid, {})
                is_cooked = (state == 1)
                if is_cooked:
                    name_en = meta.get("cooked_name_en") or (meta.get("name_en", mid) + " (Grilled)")
                    name_es = meta.get("cooked_name_es") or (meta.get("name_es", mid) + " (Asada)")
                else:
                    name_en = meta.get("name_en", mid)
                    name_es = meta.get("name_es", mid)
                    
                cat = "Mushroom" if is_en else "Seta"
                if query and (query not in name_es.lower() and query not in name_en.lower() and query not in mid.lower() and query not in cat.lower()):
                    continue
                    
                if is_en:
                    display_name = f"{name_en} ({name_es})" if name_es and name_en != name_es else name_en
                else:
                    display_name = f"{name_es} ({name_en})" if name_en and name_en != name_es else name_es
                    
                loc_txt = t("inv_loc_storage") if owner == "COIN_LOCKER" else t("inv_loc_bag")
                clean_slug = (meta.get("name_en") or mid).lower().replace(" ", "_").replace("-", "_")
                thumb = self.parent_app.get_photo(clean_slug, size=(24, 24)) or self.parent_app.get_photo("01_heartshroom_1", size=(24, 24))
                
                node = self.tree.insert(
                    "",
                    "end",
                    text=f" {display_name}",
                    image=thumb or "",
                    values=(t("inv_unit_str", qty=qty), loc_txt, cat, mid),
                    tags=("tag_shroom",)
                )
                self.tree_images[node] = thumb
                total_entries += 1
                total_units += qty
                
            # Insert Beasts
            for (bid, owner), qty in beast_counts.items():
                meta = self.shrooms_beasts_db.get(bid, {})
                name_en = meta.get("name_en", bid)
                name_es = meta.get("name_es", bid)
                cat = "Beast" if is_en else "Criatura"
                
                if query and (query not in name_es.lower() and query not in name_en.lower() and query not in bid.lower() and query not in cat.lower()):
                    continue
                    
                if is_en:
                    display_name = f"{name_en} ({name_es})" if name_es and name_en != name_es else name_en
                else:
                    display_name = f"{name_es} ({name_en})" if name_en and name_en != name_es else name_es
                    
                loc_txt = t("inv_loc_storage") if owner == "COIN_LOCKER" else t("inv_loc_bag")
                clean_slug = (meta.get("name_en") or bid).lower().replace(" ", "_").replace("-", "_")
                thumb = self.parent_app.get_photo(clean_slug, size=(24, 24)) or self.parent_app.get_photo("golden_frog", size=(24, 24)) or self.parent_app.get_photo("snails", size=(24, 24))
                
                node = self.tree.insert(
                    "",
                    "end",
                    text=f" {display_name}",
                    image=thumb or "",
                    values=(t("inv_unit_str", qty=qty), loc_txt, cat, bid),
                    tags=("tag_beast",)
                )
                self.tree_images[node] = thumb
                total_entries += 1
                total_units += qty

        # Insert Storage Equipment
        if is_cat_all or is_cat_gear:
            for ptid, qty in storage_gear.items():
                if not ptid or qty <= 0:
                    continue
                info = self.equipment_db.get(ptid, {})
                name_es = info.get("name_es", ptid)
                name_en = info.get("name_en", "")
                cat = info.get("type", "Gear" if is_en else "Equipo")
                
                if query and (query not in name_es.lower() and query not in name_en.lower() and query not in ptid.lower() and query not in cat.lower()):
                    continue
                    
                display_name = f"{name_en} ({name_es})" if is_en and name_en else (f"{name_es} ({name_en})" if name_en and name_en != name_es else name_es)
                art_rel = self.parent_app._find_equipment_art(ptid)
                thumb = self.parent_app.get_photo(art_rel, size=(24, 24))
                
                node = self.tree.insert(
                    "",
                    "end",
                    text=f" {display_name}",
                    image=thumb or "",
                    values=(t("inv_unit_str", qty=qty), t("inv_loc_storage"), cat, ptid),
                    tags=("tag_gear",)
                )
                self.tree_images[node] = thumb
                total_entries += 1
                total_units += qty
                
        # Insert Bag Equipment
        if is_cat_all or is_cat_bag:
            for ptid, qty in bag_gear.items():
                if not ptid or qty <= 0:
                    continue
                info = self.equipment_db.get(ptid, {})
                name_es = info.get("name_es", ptid)
                name_en = info.get("name_en", "")
                cat = info.get("type", "Gear" if is_en else "Equipo")
                
                if query and (query not in name_es.lower() and query not in name_en.lower() and query not in ptid.lower() and query not in cat.lower()):
                    continue
                    
                display_name = f"{name_en} ({name_es})" if is_en and name_en else (f"{name_es} ({name_en})" if name_en and name_en != name_es else name_es)
                art_rel = self.parent_app._find_equipment_art(ptid)
                thumb = self.parent_app.get_photo(art_rel, size=(24, 24))
                
                node = self.tree.insert(
                    "",
                    "end",
                    text=f" {display_name}",
                    image=thumb or "",
                    values=(t("inv_unit_str", qty=qty), t("inv_loc_bag"), cat, ptid),
                    tags=("tag_bag",)
                )
                self.tree_images[node] = thumb
                total_entries += 1
                total_units += qty
                
        if is_en:
            self.status_lbl.config(text=f"Showing {total_entries} unique item types ({total_units:,} physical units total).")
        else:
            self.status_lbl.config(text=f"Mostrando {total_entries} tipos de objetos distintos ({total_units:,} unidades físicas en total).")

