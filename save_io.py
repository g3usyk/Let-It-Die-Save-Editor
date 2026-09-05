import os
import sys
import shutil
import struct
import zlib
import json
import datetime
import uuid
import re

COMMON_STEAM_DIRS = [
    r"E:\SteamLibrary\steamapps\common\LET IT DIE\Savedata",
    r"C:\Program Files (x86)\Steam\steamapps\common\LET IT DIE\Savedata",
    r"C:\Program Files\Steam\steamapps\common\LET IT DIE\Savedata",
    r"C:\SteamLibrary\steamapps\common\LET IT DIE\Savedata",
    r"D:\SteamLibrary\steamapps\common\LET IT DIE\Savedata",
    r"F:\SteamLibrary\steamapps\common\LET IT DIE\Savedata",
    r"G:\SteamLibrary\steamapps\common\LET IT DIE\Savedata",
]

DEFAULT_SAVEDATA_DIR = r"E:\SteamLibrary\steamapps\common\LET IT DIE\Savedata"

if getattr(sys, "frozen", False):
    APP_DATA_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    APP_DATA_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_BACKUPS_DIR = os.path.join(APP_DATA_DIR, "Backups")

def get_all_detected_steam_dirs():
    """Detects all Steam library directories via Windows Registry and libraryfolders.vdf."""
    detected = list(COMMON_STEAM_DIRS)
    try:
        if sys.platform == "win32":
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as key:
                steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
                if steam_path and os.path.isdir(steam_path):
                    main_save = os.path.join(steam_path, "steamapps", "common", "LET IT DIE", "Savedata")
                    if main_save not in detected:
                        detected.insert(0, main_save)
                    vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
                    if os.path.exists(vdf_path):
                        with open(vdf_path, "r", encoding="utf-8", errors="ignore") as f:
                            for line in f:
                                m = re.search(r'"path"\s+"([^"]+)"', line)
                                if m:
                                    lib_root = m.group(1).replace("\\\\", "\\")
                                    lib_save = os.path.join(lib_root, "steamapps", "common", "LET IT DIE", "Savedata")
                                    if lib_save not in detected:
                                        detected.insert(0, lib_save)
    except Exception:
        pass
    return detected

def get_default_save_path():
    all_dirs = get_all_detected_steam_dirs()
    for d in all_dirs:
        if os.path.isdir(d):
            sav_files = [os.path.join(d, f) for f in os.listdir(d) if f.endswith(".sav")]
            if sav_files:
                return sav_files[0]
    # Fallback to local CurrentSave directory if running in repo/standalone
    local_save_dir = os.path.join(APP_DATA_DIR, "CurrentSave")
    if os.path.isdir(local_save_dir):
        sav_files = [os.path.join(local_save_dir, f) for f in os.listdir(local_save_dir) if f.endswith(".sav")]
        if sav_files:
            return sav_files[0]
    return None

def create_backup(save_path, backup_dir=None, max_backups=10):
    if not os.path.exists(save_path):
        raise FileNotFoundError(f"Save file not found: {save_path}")
    
    if backup_dir is None:
        backup_dir = PROJECT_BACKUPS_DIR
    os.makedirs(backup_dir, exist_ok=True)
    
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(save_path)
    backup_path = os.path.join(backup_dir, f"{base_name}.{timestamp}.bak")
    if os.path.exists(backup_path):
        backup_path = os.path.join(backup_dir, f"{base_name}.{now.strftime('%Y%m%d_%H%M%S_%f')}.bak")
    shutil.copy2(save_path, backup_path)
    
    # Rolling retention: keep only the latest max_backups
    try:
        backups = [os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.startswith(base_name) and f.endswith(".bak")]
        backups.sort(key=os.path.getmtime)
        while len(backups) > max_backups:
            oldest = backups.pop(0)
            try:
                os.remove(oldest)
            except OSError:
                pass
    except Exception:
        pass
        
    return backup_path

def restore_backup(backup_path, target_path):
    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Backup file not found: {backup_path}")
    os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
    shutil.copy2(backup_path, target_path)
    return True

def list_backups(backup_dir=None, save_filename=None):
    if backup_dir is None:
        backup_dir = PROJECT_BACKUPS_DIR
    if not os.path.isdir(backup_dir):
        return []
    res = []
    for f in os.listdir(backup_dir):
        if f.endswith(".bak"):
            if save_filename and not f.startswith(save_filename):
                continue
            fp = os.path.join(backup_dir, f)
            st = os.stat(fp)
            dt_str = datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            res.append({
                "filename": f,
                "path": fp,
                "size": st.st_size,
                "mtime": st.st_mtime,
                "date_str": dt_str
            })
    res.sort(key=lambda x: x["mtime"], reverse=True)
    return res

def decompress_save(path):
    with open(path, "rb") as f:
        data = f.read()

    if len(data) < 16 or data[:4] != b"BRG\x00":
        raise ValueError("Invalid Let It Die save header. Magic BRG\\0 not found.")

    v1, v2 = struct.unpack("<II", data[4:12])
    algo = data[12:16]
    
    offset = 16
    chunks = []
    while offset < len(data):
        if offset + 4 >= len(data):
            break
        uncomp_size = struct.unpack("<I", data[offset:offset+4])[0]
        if uncomp_size == 0:
            break
        comp_size = struct.unpack("<I", data[offset+4:offset+8])[0]
        offset += 8
        chunks.append(zlib.decompress(data[offset:offset+comp_size]))
        offset += comp_size

    full_decomp = b"".join(chunks)
    return json.loads(full_decomp.decode("utf-8")), v1

def _balanced_sizes(total, count):
    count = max(1, count)
    base, remainder = divmod(total, count)
    return [base + (1 if i < remainder else 0) for i in range(count)]

def compress_save(save_json, version=2, chunk_count=4, **kwargs):
    """
    Compresses save JSON using balanced chunks compatible with the game's streaming decompressor.
    Uses ensure_ascii=False, compact separators, and 4 balanced ZLIB chunks matching LID - Save Editor.
    """
    json_bytes = json.dumps(save_json, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')
    total_uncomp_size = len(json_bytes)
    
    header = b"BRG\x00" + struct.pack("<II", version, total_uncomp_size) + b"ZLIB"
    sizes = _balanced_sizes(total_uncomp_size, chunk_count)
    
    chunks = []
    pos = 0
    for sz in sizes:
        chunk_raw = json_bytes[pos:pos+sz]
        comp = zlib.compress(chunk_raw)
        chunk_header = struct.pack("<II", len(chunk_raw), len(comp))
        chunks.append(chunk_header + comp)
        pos += sz
    
    eof_marker = struct.pack("<I", 0)
    return header + b"".join(chunks) + eof_marker

def save_to_file(arg1, arg2, version=2, make_backup=True):
    if isinstance(arg1, (dict, list)):
        save_json, output_path = arg1, arg2
    else:
        output_path, save_json = arg1, arg2
        
    if make_backup and os.path.exists(output_path):
        create_backup(output_path)
    
    try:
        from core.helpers import repair_save_list_structures
        repair_save_list_structures(save_json)
    except Exception:
        pass

    try:
        from core.fighters import sanitize_fighters
        sanitize_fighters(save_json)
    except Exception:
        pass

    try:
        from core.tdm import repair_and_sanitize_tdm
        repair_and_sanitize_tdm(save_json)
    except Exception:
        pass

    binary_data = compress_save(save_json, version=version)
    
    # Atomic write to prevent file corruption
    dir_name = os.path.dirname(os.path.abspath(output_path))
    temp_path = os.path.join(dir_name, f".tmp_{uuid.uuid4().hex}.sav")
    try:
        with open(temp_path, "wb") as f:
            f.write(binary_data)
        os.replace(temp_path, output_path)
    except Exception:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
        raise

# Alias for backward and external compatibility
backup_save = create_backup

