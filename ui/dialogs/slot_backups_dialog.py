# -*- coding: utf-8 -*-
"""
Slot Backups Dialog for LET IT DIE Save Editor.
Displays and manages historical backups isolated for a specific save slot.
"""

import os
import time
import tkinter as tk
from tkinter import ttk, messagebox

import i18n
from i18n import t
from ui.theme import BG_DARK, BG_PANEL, BG_CARD, FG_TEXT, FG_MUTED, ACCENT_GOLD, ACCENT_CYAN, ACCENT_GREEN
import core.save_slots as save_slots


class SlotBackupsDialog(tk.Toplevel):
    """Interactive modal dialog displaying historical backups for a specific slot."""

    def __init__(self, parent, slot_num, active_save_path=None, on_restored_cb=None):
        super().__init__(parent)
        self.parent = parent
        self.slot_num = slot_num
        self.active_save_path = active_save_path
        self.on_restored_cb = on_restored_cb

        self.title(t("slot_bak_dialog_title", slot=slot_num))
        self.geometry("760x530")
        self.minsize(680, 450)
        self.configure(bg=BG_DARK)
        self.transient(parent)
        self.grab_set()

        self._node_to_filename = {}
        self._build_ui()
        self.refresh_backups()

        # Center on parent
        self.update_idletasks()
        try:
            px = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
            py = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
            self.geometry(f"+{max(0, px)}+{max(0, py)}")
        except Exception:
            pass

    def _build_ui(self):
        # Header Frame
        hdr = tk.Frame(self, bg=BG_PANEL, padx=14, pady=10)
        hdr.pack(fill="x")

        tk.Label(
            hdr,
            text=f"🛡️ {t('slot_bak_header_title', slot=self.slot_num)}",
            font=("Segoe UI", 12, "bold"),
            fg=ACCENT_GOLD,
            bg=BG_PANEL
        ).pack(side="left")

        self.lbl_subtitle = tk.Label(
            hdr,
            text=t("slot_bak_subtitle"),
            font=("Segoe UI", 8),
            fg=FG_MUTED,
            bg=BG_PANEL
        )
        self.lbl_subtitle.pack(side="right", padx=4)

        # Content Frame
        body = tk.Frame(self, bg=BG_DARK, padx=14, pady=10)
        body.pack(fill="both", expand=True)

        tree_frame = tk.Frame(body, bg=BG_CARD)
        tree_frame.pack(fill="both", expand=True)

        scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        cols = ("date", "size", "type")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=cols,
            show="tree headings",
            selectmode="browse",
            yscrollcommand=scroll.set
        )
        scroll.config(command=self.tree.yview)

        self.tree.heading("#0", text=t("slot_bak_col_file"), anchor="w")
        self.tree.heading("date", text=t("bak_col_date"), anchor="center")
        self.tree.heading("size", text=t("bak_col_size"), anchor="center")
        self.tree.heading("type", text=t("slot_bak_col_type"), anchor="center")

        self.tree.column("#0", width=300, anchor="w")
        self.tree.column("date", width=160, anchor="center")
        self.tree.column("size", width=85, anchor="center")
        self.tree.column("type", width=130, anchor="center")

        scroll.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # Selected Backup Preview Card
        self.preview_frame = tk.Frame(body, bg=BG_CARD, padx=10, pady=8, highlightbackground=ACCENT_CYAN, highlightthickness=1)
        self.preview_frame.pack(fill="x", pady=(8, 0))

        self.lbl_preview_title = tk.Label(
            self.preview_frame,
            text=t("slot_bak_preview_lbl"),
            font=("Segoe UI", 9, "bold"),
            fg=ACCENT_GOLD,
            bg=BG_CARD
        )
        self.lbl_preview_title.pack(anchor="w")

        self.lbl_preview_details = tk.Label(
            self.preview_frame,
            text=t("slot_bak_preview_none"),
            font=("Segoe UI", 8),
            fg=FG_TEXT,
            bg=BG_CARD,
            justify="left"
        )
        self.lbl_preview_details.pack(anchor="w", pady=(2, 0))

        # Action Buttons Frame
        btn_bar = tk.Frame(self, bg=BG_PANEL, padx=14, pady=10)
        btn_bar.pack(fill="x")

        self.btn_restore = ttk.Button(
            btn_bar,
            text=t("slot_bak_restore_slot_btn"),
            command=self._restore_to_slot_action
        )
        self.btn_restore.pack(side="left", padx=3)

        self.btn_restore_active = ttk.Button(
            btn_bar,
            text=t("slot_bak_restore_active_btn"),
            style="Accent.TButton",
            command=self._restore_to_active_action
        )
        self.btn_restore_active.pack(side="left", padx=3)

        self.btn_new_bak = ttk.Button(
            btn_bar,
            text=t("slot_bak_create_btn"),
            command=self._create_backup_action
        )
        self.btn_new_bak.pack(side="left", padx=3)

        self.btn_del_bak = ttk.Button(
            btn_bar,
            text=t("slot_bak_delete_btn"),
            command=self._delete_backup_action
        )
        self.btn_del_bak.pack(side="left", padx=3)

        ttk.Button(
            btn_bar,
            text=t("dialog_close_btn"),
            command=self.destroy
        ).pack(side="right", padx=3)

    def refresh_backups(self):
        self.tree.delete(*self.tree.get_children())
        self._node_to_filename.clear()
        slot_info = save_slots.get_slot_info(self.slot_num, force_refresh=True)
        backups = slot_info.get("backups", [])

        if not backups:
            self.tree.insert("", "end", text=f"  {t('slot_bak_empty')}", values=("-", "-", "-"))
            self.lbl_preview_details.config(text=t("slot_bak_empty"))
            self.btn_restore.config(state="disabled")
            self.btn_restore_active.config(state="disabled")
            self.btn_del_bak.config(state="disabled")
            return

        self.btn_restore.config(state="normal")
        self.btn_restore_active.config(state="normal")
        self.btn_del_bak.config(state="normal")

        for b in backups:
            fn = b["filename"]
            is_orig = b.get("is_original", False)
            is_session = b.get("is_session", False) or "_session_" in fn
            if is_orig:
                display_title = f"⭐ {fn}"
                type_lbl = t("slot_bak_type_orig")
            elif is_session:
                display_title = f"🕒 {fn}"
                type_lbl = t("slot_bak_type_session")
            else:
                display_title = f"📦 {fn}"
                type_lbl = t("slot_bak_type_auto")

            sz_str = f"{b['size'] // 1024} KB"
            node_id = self.tree.insert(
                "", "end",
                text=display_title,
                values=(b.get("date_str", "-"), sz_str, type_lbl)
            )
            self._node_to_filename[node_id] = fn

        # Auto-select first item
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[0])
            self._on_tree_select()

    def _on_tree_select(self, event=None):
        fn = self._get_selected_filename()
        if not fn:
            self.lbl_preview_details.config(text=t("slot_bak_preview_none"))
            return
        backups_dir = save_slots.get_slot_backups_dir(self.slot_num)
        bak_path = os.path.join(backups_dir, fn)
        meta = save_slots.get_backup_metadata(bak_path)
        if not meta or "error" in meta:
            self.lbl_preview_details.config(text=f"{fn} ({os.path.getsize(bak_path)//1024 if os.path.exists(bak_path) else 0} KB)")
            return

        p_name = meta.get("player_name", "Senpai")
        f_name = meta.get("fighter_name", "Fighter")
        f_class = meta.get("fighter_class", "BAL")
        f_grade = meta.get("fighter_grade", 1)
        f_lvl = meta.get("fighter_lvl", 1)
        flr = meta.get("max_floor", 0)
        haters = meta.get("haters_killed", 0)
        kc = meta.get("kill_coins", 0)
        dm = meta.get("death_metals", 0)
        spl = meta.get("splithium", 0)
        bl = meta.get("bloodnium", 0)

        self.lbl_preview_details.config(
            text=f"👤 {p_name} • 🥋 {f_name} ({f_class} ★{f_grade} Lv.{f_lvl})\n"
                 f"🗼 {t('slot_lbl_floor', floor=flr)}  |  ⚔️ {t('slot_lbl_haters', haters=haters)}  |  "
                 f"🪙 {kc:,} KC  |  💎 {dm:,} DM  |  ⚡ {spl:,} SPL  |  🩸 {bl:,} BL"
        )

    def _get_selected_filename(self):
        sel = self.tree.selection()
        if not sel:
            return None
        node_id = sel[0]
        if node_id in self._node_to_filename:
            return self._node_to_filename[node_id]
        raw_text = self.tree.item(node_id, "text").strip()
        clean = raw_text.replace("⭐", "").replace("🕒", "").replace("📦", "").strip()
        if not clean.endswith(".bak"):
            return None
        return clean

    def _restore_to_slot_action(self):
        fn = self._get_selected_filename()
        if not fn:
            messagebox.showwarning(t("notice"), t("slot_bak_select_first"), parent=self)
            return

        if messagebox.askyesno(
            t("confirm"),
            t("slot_bak_confirm_restore_slot", file=fn, slot=self.slot_num),
            parent=self
        ):
            try:
                save_slots.restore_slot_backup(self.slot_num, fn, active_target_path=None)
                if self.on_restored_cb:
                    self.on_restored_cb(self.slot_num, active_updated=False)
                messagebox.showinfo(
                    t("notice"),
                    t("slot_bak_restored_slot_ok", slot=self.slot_num),
                    parent=self
                )
                self.refresh_backups()
            except Exception as e:
                messagebox.showerror(t("error"), str(e), parent=self)

    def _restore_to_active_action(self):
        fn = self._get_selected_filename()
        if not fn:
            messagebox.showwarning(t("notice"), t("slot_bak_select_first"), parent=self)
            return

        if not self.active_save_path or not os.path.exists(self.active_save_path):
            messagebox.showwarning(t("notice"), t("mb_load_save_first"), parent=self)
            return

        if messagebox.askyesno(
            t("confirm"),
            t("slot_bak_confirm_restore_active", file=fn, slot=self.slot_num),
            parent=self
        ):
            try:
                save_slots.restore_slot_backup(self.slot_num, fn, active_target_path=self.active_save_path)
                if self.on_restored_cb:
                    self.on_restored_cb(self.slot_num, active_updated=True)
                messagebox.showinfo(
                    t("notice"),
                    t("slot_bak_restored_active_ok", slot=self.slot_num),
                    parent=self
                )
                self.destroy()
            except Exception as e:
                messagebox.showerror(t("error"), str(e), parent=self)

    def _create_backup_action(self):
        try:
            res = save_slots.create_slot_backup(self.slot_num)
            if not res:
                messagebox.showwarning(t("notice"), t("slot_bak_no_save_to_backup"), parent=self)
                return
            self.refresh_backups()
            messagebox.showinfo(
                t("notice"),
                t("mb_backup_created_msg", file=os.path.basename(res)),
                parent=self
            )
        except Exception as e:
            messagebox.showerror(t("error"), str(e), parent=self)

    def _delete_backup_action(self):
        fn = self._get_selected_filename()
        if not fn:
            messagebox.showwarning(t("notice"), t("slot_bak_select_first"), parent=self)
            return

        if "ORIGINAL" in fn:
            messagebox.showwarning(t("notice"), t("slot_bak_cannot_delete_original"), parent=self)
            return

        if messagebox.askyesno(t("confirm"), t("slot_bak_confirm_delete", file=fn), parent=self):
            b_dir = save_slots.get_slot_backups_dir(self.slot_num)
            p = os.path.join(b_dir, fn)
            try:
                if os.path.exists(p):
                    os.remove(p)
                self.refresh_backups()
            except Exception as e:
                messagebox.showerror(t("error"), str(e), parent=self)
