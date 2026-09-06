# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import modifiers
from i18n import t
from ui.theme import *

class CreateFighterDialog(tk.Toplevel):
    def __init__(self, parent, save_json, on_created_cb=None):
        super().__init__(parent)
        self.title(t("f_create_title"))
        self.geometry("520x460")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)
        self.transient(parent)
        self.grab_set()
        
        self.parent = parent
        self.save_json = save_json
        self.on_created_cb = on_created_cb
        
        self._build_ui()
        
    def _build_ui(self):
        # Header banner
        header = tk.Frame(self, bg=BG_PANEL, padx=16, pady=12)
        header.pack(fill="x")
        
        tk.Label(
            header,
            text=f"🥋 {t('f_create_title')}",
            font=("Segoe UI", 13, "bold"),
            bg=BG_PANEL,
            fg=ACCENT_GOLD
        ).pack(anchor="w")
        
        tk.Label(
            header,
            text=t("f_create_desc"),
            font=("Segoe UI", 9),
            bg=BG_PANEL,
            fg=FG_MUTED
        ).pack(anchor="w", pady=(2, 0))
        
        # Form Container
        form_frame = tk.Frame(self, bg=BG_DARK, padx=20, pady=16)
        form_frame.pack(fill="both", expand=True)
        
        # 1. Name
        tk.Label(form_frame, text=t("f_create_name_lbl"), font=("Segoe UI", 9, "bold"), bg=BG_DARK, fg=FG_MAIN).grid(row=0, column=0, sticky="w", pady=8)
        self.name_var = tk.StringVar(value=t("f_create_default_name"))
        name_entry = ttk.Entry(form_frame, textvariable=self.name_var, width=28)
        name_entry.grid(row=0, column=1, sticky="w", pady=8)
        name_entry.focus()
        
        # 2. Class
        tk.Label(form_frame, text=t("f_lbl_class"), font=("Segoe UI", 9, "bold"), bg=BG_DARK, fg=FG_MAIN).grid(row=1, column=0, sticky="w", pady=8)
        self.class_options = [
            (t("cls_opt_bal"), "BAL"),
            (t("cls_opt_bre"), "BRE"),
            (t("cls_opt_def"), "DEF"),
            (t("cls_opt_tec"), "TEC"),
            (t("cls_opt_sht"), "SHT"),
            (t("cls_opt_col"), "COL"),
            (t("cls_opt_ski"), "SKI"),
            (t("cls_opt_luk"), "LUK"),
        ]
        self.class_var = tk.StringVar(value=self.class_options[0][0])
        cb_class = ttk.Combobox(form_frame, textvariable=self.class_var, values=[opt[0] for opt in self.class_options], state="readonly", width=32)
        cb_class.grid(row=1, column=1, sticky="w", pady=8)
        
        # 3. Grade / Tier
        tk.Label(form_frame, text=t("f_lbl_grade"), font=("Segoe UI", 9, "bold"), bg=BG_DARK, fg=FG_MAIN).grid(row=2, column=0, sticky="w", pady=8)
        self.grade_options = [
            (t("grd_opt_t6"), 6),
            (t("grd_opt_t5"), 5),
            (t("grd_opt_t4"), 4),
            (t("grd_opt_t3"), 3),
            (t("grd_opt_t2"), 2),
            (t("grd_opt_t1"), 1),
        ]
        self.grade_var = tk.StringVar(value=self.grade_options[0][0])
        cb_grade = ttk.Combobox(form_frame, textvariable=self.grade_var, values=[opt[0] for opt in self.grade_options], state="readonly", width=32)
        cb_grade.grid(row=2, column=1, sticky="w", pady=8)
        
        # 4. Model / Appearance
        tk.Label(form_frame, text=t("f_lbl_model"), font=("Segoe UI", 9, "bold"), bg=BG_DARK, fg=FG_MAIN).grid(row=3, column=0, sticky="w", pady=8)

        self.models_list = [f"Female {i} (BODY_FEMALE_{i:03d})" for i in range(1, 9)] + [f"Male {i} (BODY_MALE_{i:03d})" for i in range(1, 9)]
        self.model_var = tk.StringVar(value=self.models_list[0])
        
        from ui.dialogs.fighter_model_gallery import get_fighter_model_art
        from ui.components import ImageCombobox
        
        model_items = [
            (opt, get_fighter_model_art(opt)) for opt in self.models_list
        ]
        m_row = tk.Frame(form_frame, bg=BG_DARK)
        m_row.grid(row=3, column=1, sticky="w", pady=8)
        
        get_photo = getattr(self.parent, "get_photo", None)
        self.cb_model = ImageCombobox(
            m_row,
            values_with_icons=model_items,
            textvariable=self.model_var,
            get_photo_cb=get_photo,
            width=240
        )
        self.cb_model.pack(side="left", padx=(0, 6))
        
        btn_gal = ttk.Button(m_row, text=t("f_create_gallery_btn"), command=self._open_gallery)
        btn_gal.pack(side="left")
        
        # 5. Max stats checkbox
        self.max_stats_var = tk.BooleanVar(value=True)
        cb_max = ttk.Checkbutton(form_frame, text=t("f_create_max_stats"), variable=self.max_stats_var)
        cb_max.grid(row=4, column=0, columnspan=2, sticky="w", pady=(14, 8))
        
        # Action Buttons
        btn_frame = tk.Frame(self, bg=BG_PANEL, padx=16, pady=12)
        btn_frame.pack(fill="x", side="bottom")
        
        btn_cancel = ttk.Button(btn_frame, text=t("dialog_cancel_btn"), command=self.destroy)
        btn_cancel.pack(side="right", padx=6)
        
        btn_create = ttk.Button(btn_frame, text="✅ " + t("f_create_confirm"), style="Success.TButton", command=self._do_create)
        btn_create.pack(side="right", padx=6)

    def _do_create(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning(t("f_create_invalid_name_title"), t("f_create_invalid_name_msg"), parent=self)
            return
            
        # Extract class code
        cls_txt = self.class_var.get()
        cls_code = next((opt[1] for opt in self.class_options if opt[0] == cls_txt), "BAL")
        
        # Extract grade
        grd_txt = self.grade_var.get()
        grade = next((opt[1] for opt in self.grade_options if opt[0] == grd_txt), 6)
        
        model = self.model_var.get()
        max_stats = self.max_stats_var.get()
        
        ok, res = modifiers.create_new_fighter(
            self.save_json,
            name=name,
            clazz=cls_code,
            grade=grade,
            body_model=model,
            max_stats=max_stats
        )
        
        if not ok:
            messagebox.showerror(t("f_create_err_title"), t("f_create_err_msg", err=res), parent=self)
            return
            
        messagebox.showinfo(t("f_create_success_title"), t("f_create_success_msg", name=name), parent=self)
        if self.on_created_cb:
            self.on_created_cb()
        self.destroy()

    def _open_gallery(self):
        from ui.dialogs.fighter_model_gallery import FighterModelGalleryDialog
        def on_pick(full_opt, code):
            self.model_var.set(full_opt)
            if hasattr(self, "cb_model"):
                self.cb_model.set(full_opt)
        FighterModelGalleryDialog(self, current_model=self.model_var.get(), on_select_cb=on_pick)
