# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from ui.theme import BG_CARD

def setup_mousewheel_dispatcher(root_or_top):
    """
    Installs a centralized, intelligent mousewheel dispatcher on the top-level window.
    This guarantees:
      1. Only the container currently hovered under the mouse pointer scrolls.
      2. Hidden/unmapped tabs never receive scroll events (zero cross-tab leakage).
      3. Child widgets (buttons, entries, comboboxes, cards) do not break scrolling on hover.
      4. ttk.Treeview, Text, and popup dialogs preserve their native scrolling.
    """
    try:
        top = root_or_top.winfo_toplevel()
    except Exception:
        top = root_or_top

    if getattr(top, "_global_mousewheel_installed", False):
        return

    top._global_mousewheel_installed = True
    top.bind_all("<MouseWheel>", _on_global_mousewheel, add="+")
    top.bind_all("<Button-4>", _on_global_mousewheel, add="+")
    top.bind_all("<Button-5>", _on_global_mousewheel, add="+")


def _on_global_mousewheel(event):
    widget = getattr(event, "widget", None)
    try:
        x_root = getattr(event, "x_root", None)
        y_root = getattr(event, "y_root", None)
        if x_root is not None and y_root is not None and hasattr(widget, "winfo_containing"):
            hovered = widget.winfo_containing(x_root, y_root)
            if hovered is not None:
                widget = hovered
    except Exception:
        pass

    if not widget:
        return

    # Calculate scroll units (negative = up, positive = down)
    delta = getattr(event, "delta", 0)
    num = getattr(event, "num", None)
    if delta != 0:
        step = -1 if delta > 0 else 1
        units = step * max(1, abs(int(delta / 40)))
    elif num == 4:
        units = -3
    elif num == 5:
        units = 3
    else:
        return

    curr = widget
    while curr is not None:
        try:
            # Never scroll unmapped / hidden tabs or containers
            if hasattr(curr, "winfo_ismapped") and not curr.winfo_ismapped():
                return "break"
        except Exception:
            return "break"

        # ttk.Treeview handles mousewheel via its own class binding
        if isinstance(curr, ttk.Treeview):
            return

        # Text and Listbox widgets handle their own scrolling
        if isinstance(curr, (tk.Text, tk.Listbox)):
            return

        # ScrollableFrame container
        if hasattr(curr, "canvas") and hasattr(curr, "content"):
            try:
                curr.canvas.yview_scroll(units, "units")
            except Exception:
                pass
            return "break"

        # Raw Canvas (such as ImageCombobox dropdown popup or custom canvases)
        if isinstance(curr, tk.Canvas):
            try:
                curr.yview_scroll(units, "units")
            except Exception:
                pass
            return "break"

        # Stop at window boundaries to avoid escaping modal dialogs or popups
        if isinstance(curr, (tk.Toplevel, tk.Tk)):
            break

        curr = getattr(curr, "master", None)


class ScrollableFrame(ttk.Frame):
    """
    A smooth, flick-free scrollable container frame supporting unified MouseWheel routing.
    Eliminates Enter/Leave jitter and unbinding bugs.
    """
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=BG_CARD, yscrollincrement=20)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content = ttk.Frame(self.canvas)
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        
        self.content.bind("<Configure>", self._on_content_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Install global dispatcher on top-level window once
        self.after_idle(lambda: setup_mousewheel_dispatcher(self))

    def _on_content_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def scroll(self, units):
        """Programmatically scroll the canvas by units."""
        self.canvas.yview_scroll(units, "units")
