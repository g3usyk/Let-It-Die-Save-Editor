"""
Let It Die Save Editor - Auto-Updater Module
Integrates GitHub version checking, background updates, and one-click publishing.
"""

import json
import os
import subprocess
import sys
import threading
import urllib.request
import tkinter as tk
from tkinter import ttk, messagebox

CURRENT_VERSION = "2.2.0"
REPO_OWNER = "g3usyk"
REPO_NAME = "Let-It-Die-Save-Editor"
RAW_VERSION_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/version.json"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"

def parse_version_tuple(v_str):
    """Converts a semantic version string like '2.2.0' to a comparable tuple (2, 2, 0)."""
    try:
        clean = v_str.strip().lstrip("vV")
        parts = [int(p) for p in clean.split(".") if p.isdigit()]
        return tuple(parts)
    except Exception:
        return (0, 0, 0)

def get_local_version_info():
    """Reads local version.json if present, fallback to CURRENT_VERSION."""
    v_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "version.json")
    if os.path.exists(v_file):
        try:
            with open(v_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "version": CURRENT_VERSION,
        "name": "Let It Die - Complete Save Editor",
        "release_date": "2026-09-02",
        "changelog": []
    }

def check_for_updates(timeout=4):
    """
    Checks GitHub for a newer version.
    Returns: (bool has_update, dict remote_info or None, str error or None)
    """
    local_info = get_local_version_info()
    local_v = parse_version_tuple(local_info.get("version", CURRENT_VERSION))
    
    # 1. Try checking via raw.githubusercontent.com
    req = urllib.request.Request(
        RAW_VERSION_URL,
        headers={"User-Agent": "LetItDie-SaveEditor-Updater"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read().decode("utf-8")
            remote_info = json.loads(data)
            remote_v = parse_version_tuple(remote_info.get("version", "0.0.0"))
            if remote_v > local_v:
                return (True, remote_info, None)
            return (False, remote_info, None)
    except Exception as e_raw:
        # 2. Try git remote check if .git directory exists
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            if os.path.exists(os.path.join(base_dir, ".git")):
                subprocess.run(["git", "fetch", "origin", "main"], cwd=base_dir, capture_output=True, timeout=timeout)
                res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=base_dir, capture_output=True, text=True)
                res_u = subprocess.run(["git", "rev-parse", "@{u}"], cwd=base_dir, capture_output=True, text=True)
                if res.returncode == 0 and res_u.returncode == 0:
                    head_hash = res.stdout.strip()
                    remote_hash = res_u.stdout.strip()
                    if head_hash != remote_hash:
                        return (True, {"version": "Nueva versión en Git", "changelog": ["Nuevos cambios disponibles en la rama principal."]}, None)
        except Exception:
            pass
        return (False, None, str(e_raw))

def perform_update_git():
    """Performs git pull and updates requirements in the local directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        # Run git pull
        pull_proc = subprocess.run(
            ["git", "pull", "origin", "main"],
            cwd=base_dir,
            capture_output=True,
            text=True,
            check=True
        )
        # Update dependencies
        req_file = os.path.join(base_dir, "requirements.txt")
        if os.path.exists(req_file):
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
                cwd=base_dir,
                capture_output=True
            )
        return True, pull_proc.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error en git pull: {e.stderr or e.stdout}"
    except Exception as ex:
        return False, str(ex)

class UpdateNotificationDialog(tk.Toplevel):
    """Visual dialog to notify the user about a new update and let them install it with 1 click."""
    def __init__(self, parent, remote_info, on_update_complete=None):
        super().__init__(parent)
        self.remote_info = remote_info
        self.on_update_complete = on_update_complete
        
        try:
            import i18n
            title_txt = i18n.t("updater_avail_title")
        except Exception:
            title_txt = "⚡ Update Available - Let It Die Save Editor"
            
        self.title(title_txt)
        self.geometry("540x420")
        self.minsize(480, 360)
        self.configure(bg="#151824")
        self.transient(parent)
        self.grab_set()
        
        self._build_ui()
        
    def _build_ui(self):
        try:
            import i18n
            t = i18n.t
        except Exception:
            t = lambda k, **kw: k
            
        local_info = get_local_version_info()
        loc_v = local_info.get("version", CURRENT_VERSION)
        rem_v = self.remote_info.get("version", "Nueva")
        rel_date = self.remote_info.get("release_date", "")

        # Header
        header = tk.Frame(self, bg="#1c2030", padx=16, pady=12)
        header.pack(fill="x")
        
        tk.Label(
            header,
            text=t("updater_avail_header"),
            font=("Segoe UI", 12, "bold"),
            fg="#f39c12",
            bg="#1c2030"
        ).pack(anchor="w")
        
        sub = t("updater_current_vs_new", current=loc_v, remote=rem_v)
        if rel_date:
            sub += f"  ({rel_date})"
        tk.Label(
            header,
            text=sub,
            font=("Segoe UI", 9),
            fg="#ffffff",
            bg="#1c2030"
        ).pack(anchor="w", pady=(3, 0))

        # Changelog area
        content_frame = tk.Frame(self, bg="#151824", padx=16, pady=12)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(
            content_frame,
            text=t("updater_changelog_title"),
            font=("Segoe UI", 10, "bold"),
            fg="#00e5ff",
            bg="#151824"
        ).pack(anchor="w", pady=(0, 6))
        
        txt_frame = tk.Frame(content_frame, bg="#1c2030", relief="flat", highlightbackground="#252b40", highlightthickness=1)
        txt_frame.pack(fill="both", expand=True)
        
        text_box = tk.Text(
            txt_frame,
            wrap="word",
            bg="#1c2030",
            fg="#f0f2f5",
            insertbackground="#ffffff",
            font=("Segoe UI", 9),
            relief="flat",
            padx=10,
            pady=8
        )
        text_box.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(txt_frame, command=text_box.yview)
        scrollbar.pack(side="right", fill="y")
        text_box.config(yscrollcommand=scrollbar.set)
        
        changelog = self.remote_info.get("changelog", [])
        if changelog:
            for item in changelog:
                text_box.insert("end", f" • {item}\n\n")
        else:
            default_changelog = " • General stability fixes and performance improvements.\n" if (hasattr(i18n, "get_language") and i18n.get_language() == "en") else " • Correcciones de estabilidad y mejoras generales del sistema.\n"
            text_box.insert("end", default_changelog)
        text_box.config(state="disabled")

        # Status label for download
        self.status_lbl = tk.Label(
            self,
            text=t("updater_safe_notice"),
            font=("Segoe UI", 8),
            fg="#9aa0b4",
            bg="#151824"
        )
        self.status_lbl.pack(pady=(2, 6))

        # Action Buttons
        btn_bar = tk.Frame(self, bg="#151824", padx=16, pady=10)
        btn_bar.pack(fill="x")
        
        self.btn_update = tk.Button(
            btn_bar,
            text=t("updater_btn_now"),
            font=("Segoe UI", 10, "bold"),
            bg="#f39c12",
            fg="#121212",
            activebackground="#e67e22",
            activeforeground="#000000",
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            command=self._start_update_action
        )
        self.btn_update.pack(side="right", padx=(8, 0))
        
        btn_later = tk.Button(
            btn_bar,
            text=t("updater_btn_later"),
            font=("Segoe UI", 9),
            bg="#252b40",
            fg="#ffffff",
            activebackground="#31374a",
            activeforeground="#ffffff",
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.destroy
        )
        btn_later.pack(side="right")

    def _start_update_action(self):
        self.btn_update.config(state="disabled", text="⏳ Actualizando...")
        self.status_lbl.config(text="Descargando los últimos cambios desde GitHub...", fg="#f39c12")
        
        def run_upd():
            ok, msg = perform_update_git()
            if ok:
                self.after(0, self._on_success)
            else:
                self.after(0, lambda: self._on_error(msg))
                
        threading.Thread(target=run_upd, daemon=True).start()

    def _on_success(self):
        try:
            import i18n
            msg = i18n.t("updater_success")
            title = i18n.t("notice")
        except Exception:
            msg = "Editor updated successfully!\nPlease restart to apply all changes."
            title = "Notice"
        messagebox.showinfo(title, msg)
        self.destroy()
        if self.on_update_complete:
            self.on_update_complete()

    def _on_error(self, err_msg):
        try:
            import i18n
            msg = i18n.t("updater_error", error=err_msg)
            title = i18n.t("error")
        except Exception:
            msg = f"Automatic update could not complete:\n\n{err_msg}"
            title = "Error"
        self.btn_update.config(state="normal", text="Reintentar")
        self.status_lbl.config(text="Error al actualizar. Revisa la consola o tu conexión.", fg="#e74c3c")
        messagebox.showerror(title, msg)

def check_updates_background(root_window, silent=True):
    """Checks for updates in a separate thread so GUI startup is instant."""
    def worker():
        try:
            import i18n
            t = i18n.t
        except Exception:
            t = lambda k, **kw: k
            
        has_update, remote_info, err = check_for_updates()
        if has_update and remote_info:
            root_window.after(0, lambda: UpdateNotificationDialog(root_window, remote_info))
        elif not silent:
            if err:
                root_window.after(0, lambda: messagebox.showwarning(t("updates"), t("updater_check_err", error=err)))
            else:
                loc = get_local_version_info().get("version", CURRENT_VERSION)
                root_window.after(0, lambda: messagebox.showinfo(t("updates"), t("updater_up_to_date", version=loc)))

    threading.Thread(target=worker, daemon=True).start()
