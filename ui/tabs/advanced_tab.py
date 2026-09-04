# -*- coding: utf-8 -*-
"""
Advanced & Backups Tab Mixin for LET IT DIE Save Editor.
"""

import os
import time
import tkinter as tk
from tkinter import ttk, messagebox

import save_io
import i18n
from i18n import t
from ui.theme import ACCENT_GOLD, FG_MUTED


class AdvancedTabMixin:
    """Provides methods for constructing and handling the Advanced & Backups Tab."""

    def _build_advanced_tab(self):
        self.tab_advanced.columnconfigure(0, weight=1)
        self.tab_advanced.columnconfigure(1, weight=1)
        
        # Left: Backup Manager
        box_bak = ttk.LabelFrame(self.tab_advanced, text=t("bak_title"), padding=12)
        box_bak.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        
        bak_tree_frame = ttk.Frame(box_bak)
        bak_tree_frame.pack(fill="both", expand=True, pady=4)
        bak_scroll = ttk.Scrollbar(bak_tree_frame, orient="vertical")
        self.backups_tree = ttk.Treeview(bak_tree_frame, columns=("date", "size"), show="tree headings", height=12, yscrollcommand=bak_scroll.set)
        bak_scroll.config(command=self.backups_tree.yview)
        self.backups_tree.heading("#0", text=t("bak_col_file"))
        self.backups_tree.heading("date", text=t("bak_col_date"))
        self.backups_tree.heading("size", text=t("bak_col_size"))
        
        self.backups_tree.column("#0", width=220)
        self.backups_tree.column("date", width=140, anchor="center")
        self.backups_tree.column("size", width=80, anchor="center")
        
        bak_scroll.pack(side="right", fill="y")
        self.backups_tree.pack(side="left", fill="both", expand=True)
        
        btn_f = ttk.Frame(box_bak)
        btn_f.pack(fill="x", pady=4)
        ttk.Button(btn_f, text=t("bak_create_btn"), style="Accent.TButton", command=self.create_manual_backup).pack(side="left", padx=2, fill="x", expand=True)
        ttk.Button(btn_f, text=t("bak_restore_btn"), command=self._restore_selected_backup).pack(side="left", padx=2, fill="x", expand=True)
        
        # Right: JSON Tools & Wiki Links
        box_tools = ttk.LabelFrame(self.tab_advanced, text=t("bak_tools_title"), padding=12)
        box_tools.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        
        ttk.Label(box_tools, text=t("bak_json_lbl"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        json_f = ttk.Frame(box_tools)
        json_f.pack(fill="x", pady=4)
        ttk.Button(json_f, text=t("bak_export_json"), command=self.export_json).pack(side="left", padx=2, fill="x", expand=True)
        ttk.Button(json_f, text=t("bak_import_json"), command=self.import_json).pack(side="left", padx=2, fill="x", expand=True)
        
        ttk.Separator(box_tools, orient="horizontal").pack(fill="x", pady=10)
        ttk.Label(box_tools, text=t("bak_links_lbl"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        ttk.Label(box_tools, text=t("bak_links_txt"), font=("Segoe UI", 8), foreground=FG_MUTED).pack(anchor="w", pady=2)

    def refresh_backups_list(self):
        self.backups_tree.delete(*self.backups_tree.get_children())
            
        if not self.save_path:
            return
            
        save_dir = os.path.dirname(self.save_path)
        base_name = os.path.basename(self.save_path)
        
        found_backups = {}
        for bdir in [save_dir, save_io.PROJECT_BACKUPS_DIR]:
            if os.path.isdir(bdir):
                for f in os.listdir(bdir):
                    if f.startswith(base_name) and f.endswith(".bak"):
                        fp = os.path.join(bdir, f)
                        if f not in found_backups:
                            st = os.stat(fp)
                            found_backups[f] = (fp, st.st_size, st.st_mtime)
                            
        for f, (fp, sz, mt) in sorted(found_backups.items(), key=lambda x: x[1][2], reverse=True):
            mtime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mt))
            thumb = self.get_photo("reversal_metal", (20, 20))
            node_id = self.backups_tree.insert("", "end", text=f" {f}", image=thumb or "", values=(mtime_str, f"{sz // 1024} KB"))
            self.tree_images[node_id] = thumb

    def _restore_selected_backup(self):
        sel = self.backups_tree.selection()
        if not sel:
            messagebox.showwarning(t("notice"), t("mb_select_backup_restore"))
            return
        node = sel[0]
        bak_name = self.backups_tree.item(node, "text").strip()
        
        # Check both directories
        save_dir = os.path.dirname(self.save_path)
        bak_path = os.path.join(save_dir, bak_name)
        if not os.path.exists(bak_path):
            bak_path = os.path.join(save_io.PROJECT_BACKUPS_DIR, bak_name)
            
        if not os.path.exists(bak_path):
            messagebox.showerror(t("error"), t("mb_backup_not_found", name=bak_name))
            return
        
        if messagebox.askyesno(t("mb_confirm_restore_title"), t("mb_confirm_restore_msg", name=bak_name)):
            try:
                save_io.restore_backup(bak_path, self.save_path)
                self.load_save(self.save_path)
                messagebox.showinfo(t("mb_restore_success_title"), t("mb_restore_success_msg"))
            except Exception as e:
                messagebox.showerror(t("error"), t("mb_restore_error", err=e))
