# -*- coding: utf-8 -*-
"""
Visual Fighter Model Gallery Dialog for LET IT DIE Save Editor.
Allows browsing and choosing official character models / faces with in-game portraits.
"""

import os
import re
import tkinter as tk
from tkinter import ttk
import i18n
from i18n import t
from ui.theme import (
    BG_DARK, BG_PANEL, BG_CARD, FG_MAIN, FG_MUTED,
    ACCENT_GOLD, ACCENT_CYAN, ACCENT_BLUE,
)


def get_fighter_model_art(model_str):
    """Resolves any model string to its official icon path relative to icons/."""
    if not model_str:
        return "all_official/body_female_001.png"
    m = re.search(r"BODY_(FEMALE|MALE)_(\d+)", str(model_str), re.IGNORECASE)
    if m:
        gender = m.group(1).lower()
        num = int(m.group(2))
        return f"all_official/body_{gender}_{num:03d}.png"
    m2 = re.search(r"(Female|Male)\s*(\d+)", str(model_str), re.IGNORECASE)
    if m2:
        gender = m2.group(1).lower()
        num = int(m2.group(2))
        return f"all_official/body_{gender}_{num:03d}.png"
    return "all_official/body_female_001.png"


class FighterModelGalleryDialog(tk.Toplevel):
    """Modal dialog displaying all 16 official in-game fighter model portraits."""

    def __init__(self, parent, current_model="", on_select_cb=None):
        super().__init__(parent)
        self.title(t("f_gallery_title"))
        self.geometry("660x520")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)
        self.transient(parent)
        self.grab_set()

        self.parent_app = parent
        self.current_model = str(current_model)
        self.on_select_cb = on_select_cb
        self.img_refs = []

        self._build_ui()

    def _build_ui(self):
        # Header banner
        header = tk.Frame(self, bg=BG_PANEL, padx=16, pady=10)
        header.pack(fill="x")
        
        tk.Label(
            header,
            text=t("f_gallery_header"),
            font=("Segoe UI", 12, "bold"),
            bg=BG_PANEL,
            fg=ACCENT_GOLD
        ).pack(anchor="w")
        
        tk.Label(
            header,
            text=t("f_gallery_sub"),
            font=("Segoe UI", 9),
            bg=BG_PANEL,
            fg=FG_MUTED
        ).pack(anchor="w", pady=(2, 0))

        # Notebook for Female and Male models
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=12, pady=10)

        # Tab 1: Female (1-8)
        female_tab = tk.Frame(nb, bg=BG_DARK, padx=10, pady=10)
        nb.add(female_tab, text=t("f_gallery_female_tab"))
        self._populate_grid(female_tab, "female")

        # Tab 2: Male (1-8)
        male_tab = tk.Frame(nb, bg=BG_DARK, padx=10, pady=10)
        nb.add(male_tab, text=t("f_gallery_male_tab"))
        self._populate_grid(male_tab, "male")

        # If current model is Male, start on the Male tab
        if "MALE" in self.current_model.upper():
            nb.select(male_tab)

        # Bottom actions
        bottom = tk.Frame(self, bg=BG_PANEL, padx=16, pady=10)
        bottom.pack(fill="x", side="bottom")
        
        btn_close = ttk.Button(bottom, text=t("btn_close"), command=self.destroy)
        btn_close.pack(side="right", padx=6)

    def _populate_grid(self, parent_frame, gender):
        # 4 columns x 2 rows
        for idx in range(1, 9):
            row = (idx - 1) // 4
            col = (idx - 1) % 4
            
            code = f"BODY_{gender.upper()}_{idx:03d}"
            label_name = f"{gender.capitalize()} {idx}"
            full_opt = f"{label_name} ({code})"
            art_rel = f"all_official/body_{gender}_{idx:03d}.png"
            
            is_active = (code in self.current_model or label_name.lower() in self.current_model.lower())
            
            border_color = ACCENT_GOLD if is_active else BG_PANEL
            card = tk.Frame(parent_frame, bg=border_color, bd=2, relief="solid", padx=6, pady=6, cursor="hand2")
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            
            # Inner container
            inner = tk.Frame(card, bg=BG_CARD, padx=6, pady=4)
            inner.pack(fill="both", expand=True)
            
            img_lbl = tk.Label(inner, bg=BG_CARD, cursor="hand2")
            img_lbl.pack(pady=(2, 4))
            app = getattr(self, "parent_app", None) or getattr(self, "master", None)
            if app and hasattr(app, "set_widget_image"):
                photo = app.set_widget_image(img_lbl, art_rel, size=(64, 78), preserve_aspect=True)
                if photo:
                    self.img_refs.append(photo)
            elif app and hasattr(app, "get_photo"):
                photo = app.get_photo(art_rel, size=(64, 78), preserve_aspect=True)
                if photo:
                    img_lbl.config(image=photo)
                    img_lbl.image = photo
                    self.img_refs.append(photo)
                
            name_lbl = tk.Label(
                inner,
                text=label_name,
                font=("Segoe UI", 9, "bold"),
                bg=BG_CARD,
                fg=ACCENT_GOLD if is_active else FG_MAIN,
                cursor="hand2"
            )
            name_lbl.pack()
            
            code_lbl = tk.Label(
                inner,
                text=f"({code})",
                font=("Segoe UI", 7),
                bg=BG_CARD,
                fg=ACCENT_CYAN if is_active else FG_MUTED,
                cursor="hand2"
            )
            code_lbl.pack()

            # Click events
            def make_handler(opt_str, c_code):
                return lambda e: self._choose_model(opt_str, c_code)

            for widget in (card, inner, img_lbl, name_lbl, code_lbl):
                widget.bind("<Button-1>", make_handler(full_opt, code))

    def _choose_model(self, full_opt, code):
        if self.on_select_cb:
            self.on_select_cb(full_opt, code)
        self.destroy()
