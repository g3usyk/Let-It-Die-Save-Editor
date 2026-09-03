# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import modifiers
import i18n
from i18n import t
from ui.theme import *

class SmartInventoryAnalyzerDialog(tk.Toplevel):
    def __init__(self, parent, save_json, on_modified_cb=None):
        super().__init__(parent)
        self.title(t("dialog_smart_analyzer_title"))
        self.geometry("880x640")
        self.minsize(740, 520)
        self.configure(bg=BG_DARK)
        self.transient(parent)
        self.grab_set()
        
        self.parent = parent
        self.save_json = save_json
        self.on_modified_cb = on_modified_cb
        
        self._build_ui()
        self.refresh_analysis()
        
    def _build_ui(self):
        # Header banner
        header_frame = tk.Frame(self, bg=BG_PANEL, padx=14, pady=10)
        header_frame.pack(fill="x")
        
        title_lbl = tk.Label(
            header_frame,
            text=t("dialog_smart_analyzer_title"),
            font=("Segoe UI", 13, "bold"),
            bg=BG_PANEL,
            fg=ACCENT_GOLD
        )
        title_lbl.pack(anchor="w")
        
        sub_lbl = tk.Label(
            header_frame,
            text=t("dialog_smart_analyzer_sub"),
            font=("Segoe UI", 9),
            bg=BG_PANEL,
            fg=FG_MUTED
        )
        sub_lbl.pack(anchor="w", pady=(2, 6))
        
        # Storage Capacity indicator
        self.cap_lbl = tk.Label(
            header_frame,
            text="Almacén (Coin Locker): Calculando...",
            font=("Segoe UI", 9, "bold"),
            bg=BG_PANEL,
            fg=FG_MAIN
        )
        self.cap_lbl.pack(anchor="w")
        
        self.cap_bar = ttk.Progressbar(header_frame, orient="horizontal", mode="determinate", length=400)
        self.cap_bar.pack(fill="x", pady=(3, 0))
        
        # Metrics summary row
        metrics_frame = tk.Frame(self, bg=BG_DARK, padx=14, pady=8)
        metrics_frame.pack(fill="x")
        
        self.m_recipes_lbl = self._create_metric_card(metrics_frame, "🔨 Recetas Activas", "---", ACCENT_BLUE)
        self.m_needed_lbl = self._create_metric_card(metrics_frame, "📋 Materiales Requeridos", "---", FG_MAIN)
        self.m_deficit_lbl = self._create_metric_card(metrics_frame, "⚠️ Materiales con Déficit", "---", ACCENT_RED)
        self.m_units_lbl = self._create_metric_card(metrics_frame, "📦 Unidades Faltantes", "---", ACCENT_GOLD)
        
        # Table of Materials
        table_frame = tk.Frame(self, bg=BG_DARK, padx=14, pady=4)
        table_frame.pack(fill="both", expand=True)
        
        cols = ("id", "needed", "stock", "deficit", "status")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="tree headings", height=12)
        
        self.tree.heading("#0", text="Material de Forja (Nombre Oficial)")
        self.tree.heading("id", text="ID Ítem")
        self.tree.heading("needed", text="Requerido por Recetas")
        self.tree.heading("stock", text="En Almacén")
        self.tree.heading("deficit", text="Faltante Neto")
        self.tree.heading("status", text="Estado")
        
        self.tree.column("#0", width=280)
        self.tree.column("id", width=140)
        self.tree.column("needed", width=120, anchor="center")
        self.tree.column("stock", width=90, anchor="center")
        self.tree.column("deficit", width=90, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        
        # Scrollbars
        ysb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        ysb.pack(side="right", fill="y")
        
        # Row tags styling
        self.tree.tag_configure("tag_deficit", foreground=ACCENT_RED)
        self.tree.tag_configure("tag_ok", foreground=ACCENT_GREEN)
        
        # Bottom Actions Bar
        action_bar = tk.Frame(self, bg=BG_PANEL, padx=14, pady=10)
        action_bar.pack(fill="x")
        
        btn_supply_needed = ttk.Button(
            action_bar,
            text="⚡ Suministrar Solo Faltantes para I+D (Sin Excesos)",
            style="Accent.TButton",
            command=self._on_supply_missing
        )
        btn_supply_needed.pack(side="left", padx=4)
        
        btn_top_up = ttk.Button(
            action_bar,
            text="⚖️ Top-Up Inteligente (Rellenar hasta X)",
            command=self._on_smart_top_up
        )
        btn_top_up.pack(side="left", padx=4)
        
        btn_refresh = ttk.Button(
            action_bar,
            text="🔄 Actualizar",
            command=self.refresh_analysis
        )
        btn_refresh.pack(side="left", padx=4)
        
        btn_expand_storage = ttk.Button(
            action_bar,
            text="🚀 Ampliar Almacén",
            command=self._on_expand_storage
        )
        btn_expand_storage.pack(side="left", padx=4)
        
        btn_close = ttk.Button(
            action_bar,
            text="Cerrar",
            command=self.destroy
        )
        btn_close.pack(side="right", padx=4)
        
    def _create_metric_card(self, parent, title, initial_val, color):
        card = tk.Frame(parent, bg=BG_CARD, padx=10, pady=6, highlightbackground=BG_PANEL, highlightthickness=1)
        card.pack(side="left", fill="x", expand=True, padx=4)
        
        t_lbl = tk.Label(card, text=title, font=("Segoe UI", 8), bg=BG_CARD, fg=FG_MUTED)
        t_lbl.pack(anchor="w")
        
        v_lbl = tk.Label(card, text=initial_val, font=("Segoe UI", 13, "bold"), bg=BG_CARD, fg=color)
        v_lbl.pack(anchor="w")
        return v_lbl
        
    def refresh_analysis(self):
        self.tree.delete(*self.tree.get_children())
            
        res = modifiers.analyze_active_recipes_materials(self.save_json)
        
        # Storage bar
        used = res["storage_used"]
        tot = res["storage_total"]
        free = res["storage_free"]
        pct = (used / tot * 100) if tot > 0 else 0
        self.cap_lbl.config(text=f"Almacén (Coin Locker): {used:,} / {tot:,} casillas ocupadas ({free:,} libres - {pct:.1f}% lleno)")
        self.cap_bar["maximum"] = tot
        self.cap_bar["value"] = used
        
        # Metrics
        deficit_items = [m for m in res["materials"] if m["deficit"] > 0]
        total_deficit_units = sum(m["deficit"] for m in deficit_items)
        
        self.m_recipes_lbl.config(text=str(res["total_active_recipes"]))
        self.m_needed_lbl.config(text=f"{res['total_materials_needed']} tipos")
        self.m_deficit_lbl.config(text=f"{len(deficit_items)} tipos")
        self.m_units_lbl.config(text=f"{total_deficit_units} u.")
        
        # Populate table
        for m in res["materials"]:
            tag = "tag_deficit" if m["deficit"] > 0 else "tag_ok"
            status_text = f"⚠️ FALTA (-{m['deficit']})" if m["deficit"] > 0 else "✅ OK"
            self.tree.insert(
                "",
                "end",
                text=m["name"],
                values=(m["itemid"], m["needed"], m["stock"], m["deficit"], status_text),
                tags=(tag,)
            )
            
    def _on_supply_missing(self):
        analysis = modifiers.analyze_active_recipes_materials(self.save_json)
        deficit_items = [m for m in analysis["materials"] if m["deficit"] > 0]
        if not deficit_items:
            messagebox.showinfo(t("analyzer_full_stock_title"), t("analyzer_full_stock_msg"))
            return
            
        tot_units = sum(m["deficit"] for m in deficit_items)
        if analysis["storage_free"] < tot_units:
            if not messagebox.askyesno(t("analyzer_limited_space_title"), t("analyzer_limited_space_msg", free=analysis['storage_free'], req=tot_units)):
                return
                
        added_types, added_units = modifiers.smart_supply_missing_materials(self.save_json)
        self.refresh_analysis()
        if self.on_modified_cb:
            self.on_modified_cb(f"Smart Supply: {added_units} missing materials ({added_types} types)." if i18n.get_language() == "en" else f"Suministrados {added_units} materiales faltantes ({added_types} tipos) para recetas de I+D.")
        messagebox.showinfo(
            t("analyzer_supplied_title"),
            t("analyzer_supplied_msg", units=added_units, types=added_types)
        )
        
    def _on_smart_top_up(self):
        target = simpledialog.askinteger(
            t("analyzer_topup_title"),
            t("analyzer_topup_prompt"),
            initialvalue=15,
            minvalue=1,
            maxvalue=99,
            parent=self
        )
        if not target:
            return
            
        added_types, added_units = modifiers.smart_top_up_materials(self.save_json, target_qty=target)
        self.refresh_analysis()
        if self.on_modified_cb:
            self.on_modified_cb(f"Smart Top-Up: {added_types} materials leveled to {target} (+{added_units})." if i18n.get_language() == "en" else f"Top-Up Inteligente: Nivelados {added_types} materiales a {target} unidades (+{added_units} unidades).")
        messagebox.showinfo(
            t("analyzer_topup_done_title"),
            t("analyzer_topup_done_msg", target=target, types=added_types, units=added_units)
        )

    def _on_expand_storage(self):
        current_cap = len(self.save_json.get("soul", {}).get("cl", []))
        target = simpledialog.askinteger(
            t("analyzer_expand_title"),
            t("analyzer_expand_prompt", cap=current_cap),
            initialvalue=max(current_cap, 6000),
            minvalue=current_cap,
            maxvalue=20000,
            parent=self
        )
        if not target or target <= current_cap:
            return
            
        old_c, new_c = modifiers.expand_storage_capacity(self.save_json, target_capacity=target)
        self.refresh_analysis()
        if self.on_modified_cb:
            self.on_modified_cb(f"Coin locker expanded: {old_c:,} -> {new_c:,} slots." if i18n.get_language() == "en" else f"Almacén ampliado de {old_c:,} a {new_c:,} casillas.")
        messagebox.showinfo(
            t("analyzer_expand_done_title"),
            t("analyzer_expand_done_msg", old_cap=old_c, new_cap=new_c)
        )

