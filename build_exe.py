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
        ("tower_map_data.json", "."),
        ("all_shrooms_beasts_db.json", "."),
        ("teamhate_template.json", "."),
        ("tdm_dummy_template.json", "."),
        ("tdm_dummy_defenders_template.json", "."),
        ("icons", "icons"),
    ]

    is_onefile = "--onefile" in sys.argv
    build_mode = "--onefile" if is_onefile else "--onedir"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=LetItDieSaveEditor",
        "--noconsole",
        build_mode,
        "--clean",
        "--noconfirm",
        "--uac-admin",
    ]


    if os.path.exists(ICON_ICO):
        cmd.extend(["--icon", ICON_ICO])

    for src, dst in data_files:
        src_path = os.path.join(BASE_DIR, src)
        if os.path.exists(src_path):
            cmd.extend(["--add-data", f"{src_path};{dst}"])

    cmd.extend(["--collect-all", "core"])
    cmd.extend(["--collect-all", "ui"])

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
        "re",
        "uuid",
        "copy",
        "core",
        "core.blueprints",
        "core.currencies",
        "core.decals",
        "core.fighters",
        "core.storage",
        "core.tower",
        "core.mastery",
        "core.helpers",
        "core.tdm",
        "ui",
        "ui.theme",
        "ui.components",
        "ui.components.image_combobox",
        "ui.components.scrollable_frame",
        "ui.tabs",
        "ui.tabs.currencies_tab",
        "ui.tabs.fighters_tab",
        "ui.tabs.materials_tab",
        "ui.tabs.decals_tab",
        "ui.tabs.blueprints_tab",
        "ui.tabs.mastery_tab",
        "ui.tabs.tower_tab",
        "ui.tabs.advanced_tab",
        "ui.dialogs",
        "ui.dialogs.create_fighter",
        "ui.dialogs.fighter_model_gallery",
        "ui.dialogs.smart_analyzer",
        "ui.dialogs.inventory_viewer",
        "ui.dialogs.armor_set_viewer",
        "i18n",
        "game_data",
        "save_io",
        "modifiers",
        "updater"
    ]
    for hi in hidden_imports:
        cmd.extend(["--hidden-import", hi])


    cmd.append(os.path.join(BASE_DIR, "editor_gui.py"))

    print("Running command:\n", " ".join(cmd))
    result = subprocess.run(cmd, cwd=BASE_DIR)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("BUILD SUCCESSFUL!")
        if is_onefile:
            target_out = os.path.join(DIST_DIR, "LetItDieSaveEditor.exe")
        else:
            target_out = os.path.join(DIST_DIR, "LetItDieSaveEditor", "LetItDieSaveEditor.exe")
        print(f"Compiled Target: {target_out}")
        print("=" * 60)
        return True

    else:
        print("\nBUILD FAILED with return code:", result.returncode)
        return False

if __name__ == "__main__":
    success = build()
    sys.exit(0 if success else 1)
