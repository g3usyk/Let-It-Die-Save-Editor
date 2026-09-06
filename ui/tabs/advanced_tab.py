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
        
        ttk.Separator(box_tools, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(box_tools, text=t("adv_repairs_title"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        rep_f = ttk.Frame(box_tools)
        rep_f.pack(fill="x", pady=4)
        ttk.Button(rep_f, text=t("adv_repair_tdm_btn"), command=self._repair_tdm_action).pack(side="left", padx=2, fill="x", expand=True)
        ttk.Button(rep_f, text=t("adv_repair_fighters_btn"), command=self._repair_fighters_action).pack(side="left", padx=2, fill="x", expand=True)

        ttk.Separator(box_tools, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(box_tools, text=t("bak_links_lbl"), font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD).pack(anchor="w", pady=2)
        ttk.Label(box_tools, text=t("bak_links_txt"), font=("Segoe UI", 8), foreground=FG_MUTED).pack(anchor="w", pady=2)

        # Row 1: CDN Assets & Cache Manager
        box_assets = ttk.LabelFrame(self.tab_advanced, text=t("asset_box_title"), padding=12)
        box_assets.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)

        ttk.Label(box_assets, text=t("asset_box_desc"), font=("Segoe UI", 8), foreground=FG_MUTED).pack(anchor="w", pady=2)
        
        self.asset_stats_lbl = ttk.Label(box_assets, text="...", font=("Segoe UI", 9, "bold"), foreground=ACCENT_GOLD)
        self.asset_stats_lbl.pack(anchor="w", pady=4)

        self.asset_pbar = ttk.Progressbar(box_assets, orient="horizontal", mode="determinate")
        self.asset_pbar.pack(fill="x", pady=4)
        self.asset_pbar_lbl = ttk.Label(box_assets, text="", font=("Segoe UI", 8), foreground=FG_MUTED)
        self.asset_pbar_lbl.pack(anchor="w", pady=1)

        btn_assets_f = ttk.Frame(box_assets)
        btn_assets_f.pack(fill="x", pady=4)
        self.asset_dl_btn = ttk.Button(btn_assets_f, text=t("asset_download_all_btn"), style="Accent.TButton", command=self._download_all_cdn_assets)
        self.asset_dl_btn.pack(side="left", padx=2)
        ttk.Button(btn_assets_f, text=t("asset_clear_cache_btn"), command=self._clear_cdn_cache).pack(side="left", padx=2)
        ttk.Button(btn_assets_f, text="🔄 " + t("reload"), command=self.update_cache_stats).pack(side="left", padx=2)

        self.update_cache_stats()

    def update_cache_stats(self):
        if hasattr(self, "asset_manager"):
            stats = self.asset_manager.get_cache_stats()
            self.asset_stats_lbl.config(text=t("asset_cache_stats", count=stats["count"], size=stats["size_mb"]))

    def _download_all_cdn_assets(self):
        if not hasattr(self, "asset_manager"):
            return
        
        # Collect all mapped asset paths
        asset_paths = set()
        if hasattr(self, "icon_map") and isinstance(self.icon_map, dict):
            for cat in self.icon_map.values():
                if isinstance(cat, dict):
                    for p in cat.values():
                        if p:
                            asset_paths.add(p)
        if hasattr(self.asset_manager, "manifest") and self.asset_manager.manifest:
            for p in self.asset_manager.manifest.values():
                if p and "/" in p:
                    asset_paths.add(p)
        
        if not asset_paths:
            messagebox.showinfo(t("notice"), "No assets to download.")
            return

        total = len(asset_paths)
        self.asset_dl_btn.config(state="disabled")
        self.asset_pbar.config(maximum=total, value=0)
        self.asset_pbar_lbl.config(text=t("asset_downloading", current=0, total=total))

        def on_progress(cur, tot, f):
            def _ui():
                self.asset_pbar.config(value=cur)
                self.asset_pbar_lbl.config(text=t("asset_downloading", current=cur, total=tot))
            self.after(0, _ui)

        def on_complete(downloaded, errors):
            def _ui():
                self.asset_dl_btn.config(state="normal")
                self.update_cache_stats()
                self.asset_pbar_lbl.config(text="")
                messagebox.showinfo(t("notice"), t("asset_download_done", downloaded=downloaded))
            self.after(0, _ui)

        self.asset_manager.download_all_assets_async(list(asset_paths), progress_callback=on_progress, completion_callback=on_complete)

    def _clear_cdn_cache(self):
        if not hasattr(self, "asset_manager"):
            return
        if messagebox.askyesno(t("notice"), t("asset_confirm_clear")):
            self.asset_manager.clear_cache()
            self.update_cache_stats()
            messagebox.showinfo(t("notice"), t("asset_cache_cleared"))

    def refresh_backups_list(self):
        self.update_cache_stats()
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
                            
        # Pin .ORIGINAL.bak at the top, then sort others by date descending
        def _sort_key(item):
            fn, (_, _, mt) = item
            is_orig = 0 if "ORIGINAL" in fn else 1
            return (is_orig, -mt)

        for f, (fp, sz, mt) in sorted(found_backups.items(), key=_sort_key):
            mtime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mt))
            thumb = self.get_photo("reversal_metal", (20, 20))
            display_text = f"⭐ {f} [ORIGINAL]" if "ORIGINAL" in f else f" {f}"
            node_id = self.backups_tree.insert("", "end", text=display_text, values=(mtime_str, f"{sz // 1024} KB"))
            self.tree_images[node_id] = thumb

    def _restore_selected_backup(self):
        sel = self.backups_tree.selection()
        if not sel:
            messagebox.showwarning(t("notice"), t("mb_select_backup_restore"))
            return
        node = sel[0]
        raw_text = self.backups_tree.item(node, "text").strip()
        bak_name = raw_text.replace("⭐", "").replace("[ORIGINAL]", "").strip()
        
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

    def _repair_tdm_action(self):
        if not self.save_json:
            return
        if messagebox.askyesno(t("notice"), t("adv_confirm_tdm_repair")):
            import modifiers
            modifiers.repair_and_sanitize_tdm(self.save_json)
            self._auto_save()
            self.refresh_all_views()
            messagebox.showinfo(t("notice"), t("adv_tdm_repaired"))

    def _repair_fighters_action(self):
        if not self.save_json:
            return
        if messagebox.askyesno(t("notice"), t("adv_confirm_fighter_repair")):
            import modifiers
            modifiers.sanitize_fighters(self.save_json)
            self._auto_save()
            self.refresh_all_views()
            messagebox.showinfo(t("notice"), t("adv_fighters_repaired"))
