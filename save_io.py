import os
import shutil
import struct
import zlib
import json
import datetime

DEFAULT_SAVEDATA_DIR = r"E:\SteamLibrary\steamapps\common\LET IT DIE\Savedata"

PROJECT_BACKUPS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Backups")

def get_default_save_path():
    if os.path.isdir(DEFAULT_SAVEDATA_DIR):
        sav_files = [os.path.join(DEFAULT_SAVEDATA_DIR, f) for f in os.listdir(DEFAULT_SAVEDATA_DIR) if f.endswith(".sav")]
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

def compress_save(save_json, version=2, chunk_size=900152):
    json_bytes = json.dumps(save_json, separators=(',', ':')).encode('utf-8')
    total_uncomp_size = len(json_bytes)
    
    header = b"BRG\x00" + struct.pack("<II", version, total_uncomp_size) + b"ZLIB"
    
    chunks = []
    for i in range(0, total_uncomp_size, chunk_size):
        chunk_raw = json_bytes[i:i+chunk_size]
        comp = zlib.compress(chunk_raw)
        chunk_header = struct.pack("<II", len(chunk_raw), len(comp))
        chunks.append(chunk_header + comp)
    
    eof_marker = struct.pack("<I", 0)
    return header + b"".join(chunks) + eof_marker

def save_to_file(arg1, arg2, version=2, make_backup=True):
    if isinstance(arg1, (dict, list)):
        save_json, output_path = arg1, arg2
    else:
        output_path, save_json = arg1, arg2
        
    if make_backup and os.path.exists(output_path):
        create_backup(output_path)
    
    binary_data = compress_save(save_json, version=version)
    with open(output_path, "wb") as f:
        f.write(binary_data)
