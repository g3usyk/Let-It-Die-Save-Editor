# -*- coding: utf-8 -*-
"""
ImageCombobox Component for LET IT DIE Save Editor.
Custom combobox widget displaying official icons inside the dropdown list items as well as on the display header.
"""

import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ui.theme import (
    BG_DARK, BG_PANEL, BG_CARD, BG_CARD_HOVER,
    FG_MAIN, FG_MUTED, ACCENT_GOLD, ACCENT_CYAN
)


class ImageCombobox(tk.Frame):
    """Combobox widget displaying an icon next to every item in the dropdown list and selection bar."""

    def __init__(
        self,
        parent,
        values_with_icons,
        textvariable=None,
        command=None,
        width=260,
        height=34,
        icon_size=(24, 30),
        get_photo_cb=None,
        *args,
        **kwargs
    ):
        super().__init__(parent, bg=BG_DARK, bd=1, relief="solid", *args, **kwargs)
        self.values = values_with_icons  # List of tuples: [(display_text, icon_rel_path), ...]
        self.var = textvariable or tk.StringVar()
        self.command = command
        self.icon_size = icon_size
        self.get_photo_cb = get_photo_cb
        self.popup = None
        self._photo_cache = {}
        self._select_callbacks = []

        # Display Bar
        self.bar = tk.Frame(self, bg=BG_CARD, cursor="hand2")
        self.bar.pack(fill="both", expand=True)

        self.icon_lbl = tk.Label(self.bar, bg=BG_CARD, cursor="hand2")
        self.icon_lbl.pack(side="left", padx=(6, 6), pady=2)

        self.text_lbl = tk.Label(
            self.bar,
            text="",
            bg=BG_CARD,
            fg=FG_MAIN,
            font=("Segoe UI", 9),
            anchor="w",
            cursor="hand2"
        )
        self.text_lbl.pack(side="left", fill="x", expand=True, pady=2)

        self.arrow_lbl = tk.Label(
            self.bar,
            text=" ▾ ",
            bg=BG_CARD,
            fg=ACCENT_CYAN,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        )
        self.arrow_lbl.pack(side="right", padx=(2, 8), pady=2)

        for w in (self, self.bar, self.icon_lbl, self.text_lbl, self.arrow_lbl):
            w.bind("<Button-1>", lambda e: self.toggle_popup())

        self.var.trace_add("write", lambda *args: self._on_var_changed())
        if self.values:
            init_val = self.var.get() or self.values[0][0]
            self.set(init_val)

    def _get_icon(self, rel_path, size=None):
        if not rel_path:
            return None
        size = size or self.icon_size
        cache_key = (rel_path, size)
        if cache_key in self._photo_cache:
            return self._photo_cache[cache_key]

        if self.get_photo_cb:
            img = self.get_photo_cb(rel_path, size=size, preserve_aspect=True)
            if img:
                self._photo_cache[cache_key] = img
                return img

        # Fallback direct disk read
        full = os.path.join("icons", rel_path)
        if not os.path.exists(full):
            return None
        try:
            with Image.open(full) as im:
                im = im.convert("RGBA")
                im.thumbnail(size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(im)
                self._photo_cache[cache_key] = photo
                return photo
        except Exception:
            return None

    def _on_var_changed(self):
        val = self.var.get()
        matched_icon = None
        display_text = val
        for text, icon in self.values:
            if text == val or val in text:
                matched_icon = icon
                display_text = text
                break
        self.text_lbl.config(text=display_text)
        ico = self._get_icon(matched_icon, size=self.icon_size) if matched_icon else None
        if ico:
            self.icon_lbl.config(image=ico)
            self.icon_lbl.image = ico
        else:
            self.icon_lbl.config(image="")

    def set(self, value):
        self.var.set(value)
        self._on_var_changed()

    def get(self):
        return self.var.get()

    def bind(self, seq, func, add=None):
        if seq == "<<ComboboxSelected>>":
            self._select_callbacks.append(func)
        else:
            super().bind(seq, func, add)

    def toggle_popup(self):
        if self.popup and self.popup.winfo_exists():
            self.close_popup()
        else:
            self.open_popup()

    def open_popup(self):
        self.close_popup()
        self.update_idletasks()

        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 2
        w = max(self.winfo_width(), 310)
        h = min(len(self.values) * 38 + 12, 260)

        self.popup = tk.Toplevel(self)
        self.popup.wm_overrideredirect(True)
        self.popup.geometry(f"{w}x{h}+{x}+{y}")
        self.popup.configure(bg=BG_PANEL, bd=1, relief="solid")
        self.popup.attributes("-topmost", True)

        canvas = tk.Canvas(self.popup, bg=BG_PANEL, highlightthickness=0, yscrollincrement=20)
        scroll = ttk.Scrollbar(self.popup, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=BG_PANEL)

        canvas.create_window((0, 0), window=frame, anchor="nw", width=w - 18)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scroll.set)

        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        cur_val = self.var.get()

        def _on_wheel(e):
            delta = getattr(e, "delta", 0)
            if delta != 0:
                step = -1 if delta > 0 else 1
                units = step * max(1, abs(int(delta / 40)))
            elif getattr(e, "num", None) == 4:
                units = -3
            elif getattr(e, "num", None) == 5:
                units = 3
            else:
                return "break"
            try:
                canvas.yview_scroll(units, "units")
            except Exception:
                pass
            return "break"

        self.popup.bind("<MouseWheel>", _on_wheel)
        self.popup.bind("<Button-4>", _on_wheel)
        self.popup.bind("<Button-5>", _on_wheel)
        canvas.bind("<MouseWheel>", _on_wheel)
        canvas.bind("<Button-4>", _on_wheel)
        canvas.bind("<Button-5>", _on_wheel)
        frame.bind("<MouseWheel>", _on_wheel)
        frame.bind("<Button-4>", _on_wheel)
        frame.bind("<Button-5>", _on_wheel)

        for text, icon in self.values:
            is_active = (text == cur_val or cur_val in text)
            row_bg = BG_CARD_HOVER if is_active else BG_PANEL
            row = tk.Frame(frame, bg=row_bg, cursor="hand2")
            row.pack(fill="x", padx=3, pady=1)

            ico = self._get_icon(icon, size=(24, 30))
            if ico:
                i_lbl = tk.Label(row, image=ico, bg=row_bg, cursor="hand2")
                i_lbl.image = ico
                i_lbl.pack(side="left", padx=4, pady=2)
            else:
                i_lbl = None

            t_lbl = tk.Label(
                row,
                text=text,
                bg=row_bg,
                fg=ACCENT_GOLD if is_active else FG_MAIN,
                font=("Segoe UI", 9, "bold" if is_active else "normal"),
                anchor="w",
                cursor="hand2"
            )
            t_lbl.pack(side="left", fill="x", expand=True, padx=4, pady=2)

            def make_select(t=text):
                return lambda e: self._select_item(t)

            def make_hover(r=row, t=t_lbl, i=i_lbl, active=is_active):
                def on_enter(e):
                    r.config(bg=BG_CARD_HOVER)
                    t.config(bg=BG_CARD_HOVER, fg=ACCENT_CYAN)
                    if i:
                        i.config(bg=BG_CARD_HOVER)

                def on_leave(e):
                    base_bg = BG_CARD_HOVER if active else BG_PANEL
                    base_fg = ACCENT_GOLD if active else FG_MAIN
                    r.config(bg=base_bg)
                    t.config(bg=base_bg, fg=base_fg)
                    if i:
                        i.config(bg=base_bg)

                return on_enter, on_leave

            on_ent, on_lve = make_hover()
            for widget in (row, t_lbl) + ((i_lbl,) if i_lbl else ()):
                widget.bind("<Button-1>", make_select())
                widget.bind("<Enter>", on_ent)
                widget.bind("<Leave>", on_lve)
                widget.bind("<MouseWheel>", _on_wheel)
                widget.bind("<Button-4>", _on_wheel)
                widget.bind("<Button-5>", _on_wheel)

        self.popup.bind("<Escape>", lambda e: self.close_popup())
        self.popup.focus_set()

        root = self.winfo_toplevel()
        self._root_click_id = root.bind("<ButtonPress-1>", self._check_click_outside, add="+")

    def _check_click_outside(self, event):
        if not self.popup or not self.popup.winfo_exists():
            return
        x, y = event.x_root, event.y_root
        px, py = self.popup.winfo_rootx(), self.popup.winfo_rooty()
        pw, ph = self.popup.winfo_width(), self.popup.winfo_height()
        # Also include self (the combobox itself) so clicking toggle doesn't instantly close & reopen
        sx, sy = self.winfo_rootx(), self.winfo_rooty()
        sw, sh = self.winfo_width(), self.winfo_height()
        if (sx <= x <= sx + sw and sy <= y <= sy + sh):
            return
        if not (px <= x <= px + pw and py <= y <= py + ph):
            self.close_popup()

    def _select_item(self, text):
        self.set(text)
        self.close_popup()
        if self.command:
            self.command(text)
        for cb in self._select_callbacks:
            cb(None)

    def close_popup(self):
        if self.popup and self.popup.winfo_exists():
            self.popup.destroy()
            self.popup = None
