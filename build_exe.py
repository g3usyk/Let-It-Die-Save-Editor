# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")
BUILD_DIR = os.path.join(BASE_DIR, "build")
ICON_ICO = os.path.join(BASE_DIR, "icons", "app_icon.ico")
if not os.path.exists(ICON_ICO):
    ICON_ICO = os.path.join(BASE_DIR, "app_icon.ico")

def build():
    print("=" * 60)
    print("Building LET IT DIE Save Editor - Standalone Executable (.exe)")
    print("=" * 60)

    data_files = [
        ("all_materials_db.json", "."),
        ("all_equipment_encyclopedia.json", "."),
        ("all_decals_encyclopedia.json", "."),
        ("armor_sets_encyclopedia.json", "."),
        ("icon_map.json", "."),
        ("version.json", "."),
    ]

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=LetItDieSaveEditor",
        "--noconsole",
        "--onedir",
        "--clean",
        "--noconfirm",
    ]

    if os.path.exists(ICON_ICO):
        cmd.extend(["--icon", ICON_ICO])

    for src, dst in data_files:
        src_path = os.path.join(BASE_DIR, src)
        if os.path.exists(src_path):
            cmd.extend(["--add-data", f"{src_path};{dst}"])

    hidden_imports = [
        "sv_ttk",
        "PIL",
        "PIL.Image",
        "PIL.ImageTk",
        "urllib.request",
        "json",
        "zlib",
        "struct",
        "shutil",
        "datetime",
        "re"
    ]
    for hi in hidden_imports:
        cmd.extend(["--hidden-import", hi])

    cmd.append(os.path.join(BASE_DIR, "editor_gui.py"))

    print("Running command:\n", " ".join(cmd))
    result = subprocess.run(cmd, cwd=BASE_DIR)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("BUILD SUCCESSFUL!")
        app_dist = os.path.join(DIST_DIR, "LetItDieSaveEditor")
        
        src_icons = os.path.join(BASE_DIR, "icons")
        dst_icons = os.path.join(app_dist, "icons")
        if os.path.isdir(src_icons) and not os.path.isdir(dst_icons):
            print(f"Copying icons to distribution folder: {dst_icons} ...")
            shutil.copytree(src_icons, dst_icons)

        os.makedirs(os.path.join(app_dist, "Backups"), exist_ok=True)

        print(f"Output folder: {app_dist}")
        print(f"Executable: {os.path.join(app_dist, 'LetItDieSaveEditor.exe')}")
        print("=" * 60)
        return True
    else:
        print("\nBUILD FAILED with return code:", result.returncode)
        return False

if __name__ == "__main__":
    success = build()
    sys.exit(0 if success else 1)
