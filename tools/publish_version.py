"""
Script helper to automate bumping version, committing, and pushing to GitHub.
"""

import json
import os
import subprocess
import sys
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(BASE_DIR, "version.json")

def main():
    print("==================================================")
    print("  LET IT DIE SAVE EDITOR - PUBLICADOR DE VERSIONES")
    print("==================================================")
    
    # Read current version
    current_ver = "2.2.0"
    if os.path.exists(VERSION_FILE):
        try:
            with open(VERSION_FILE, "r", encoding="utf-8") as f:
                v_data = json.load(f)
                current_ver = v_data.get("version", current_ver)
        except Exception:
            v_data = {}
    else:
        v_data = {}

    print(f"\nVersión actual: {current_ver}")
    new_ver = input(f"Introduce nueva versión [Presiona Enter para mantener {current_ver}]: ").strip()
    if not new_ver:
        new_ver = current_ver

    msg = input("Describe los cambios de esta versión: ").strip()
    if not msg:
        msg = f"Actualización v{new_ver}"

    # Update version.json
    v_data["version"] = new_ver
    v_data["release_date"] = str(date.today())
    if "changelog" not in v_data or not isinstance(v_data["changelog"], list):
        v_data["changelog"] = []
    v_data["changelog"].insert(0, msg)
    v_data["changelog"] = v_data["changelog"][:10]  # Keep last 10 entries

    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump(v_data, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] version.json actualizado a v{new_ver}")

    # Update CURRENT_VERSION in updater.py
    updater_file = os.path.join(BASE_DIR, "updater.py")
    if os.path.exists(updater_file):
        with open(updater_file, "r", encoding="utf-8") as f:
            u_content = f.read()
        import re
        u_content = re.sub(r'CURRENT_VERSION = "[^"]+"', f'CURRENT_VERSION = "{new_ver}"', u_content)
        with open(updater_file, "w", encoding="utf-8") as f:
            f.write(u_content)

    # Git operations
    print("\nEjecutando git add...")
    subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)

    print(f"Ejecutando git commit -m '{msg}'...")
    subprocess.run(["git", "commit", "-m", f"v{new_ver}: {msg}"], cwd=BASE_DIR)

    print("Subiendo cambios a GitHub (git push origin main)...")
    res = subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR)
    
    if res.returncode == 0:
        print("\n==================================================")
        print(f"  ¡VERSIÓN v{new_ver} PUBLICADA CON ÉXITO EN GITHUB!")
        print("  Todos los usuarios recibirán la actualización.")
        print("==================================================")
    else:
        print("\n[AVISO] git push no se completó. Si es la primera vez, asegúrate de haber creado el repositorio remoto.")

if __name__ == "__main__":
    main()
