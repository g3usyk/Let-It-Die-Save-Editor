# LET IT DIE - Offline Save Editor & Encyclopedia

A desktop save editing suite and comprehensive game database for the PC (Steam) release of **LET IT DIE**.

The tool operates directly on local `.sav` files, reading compressed game data, allowing granular adjustments to fighters, equipment, decals, and storage, and recompressing the save while maintaining file integrity and automated backups.

---

## Features

### Currencies and Resources
- Modify Kill Coins, Death Metals, SPLithium, and Bloodnium directly.
- Supports values up to standard game caps with built-in safety boundaries to prevent save overflow.

### Fighter Freezer Management
- Inspect all fighters currently stored in the freezer (alive or frozen).
- Edit individual fighter attributes:
  - Level, Class (All-Rounder, Striker, Defender, Attacker, Shooter, Collector, Skill Master, Lucky Star).
  - Grade and uncapped stats (HP, STM, STR, DEX, VIT, LUK).
- Equip endgame preset builds directly into active loadouts:
  - Tengoku Climber (High-floor progression setup)
  - KAMAS Shooter (Ranged DPS optimization)
  - Melee Striker (Heavy burst damage configuration)
  - TDM Defender (High resistance and tank setup)

### Decal Injection and Management
- Complete database of 626 official decals extracted from game data.
- Separate handling for Standard and Premium (`_P`) variants.
- Categorized by event collaborations and combat playstyles:
  - Collaborations: World of Tanks, No More Heroes, Killer7, Gravity Rush, and Tengoku Meta.
  - Tactical Roles: Weapon Addicts, Critical Damage, Tank / Defense, Vampire / Life Leech, Farming / Quality of Life, and Armor Set Synergy decals.
- Add or adjust decal quantities in storage.

### Blueprints and R&D Forge
- Full catalog of 1,370 equipment pieces and 385 weapons.
- Filter by gear slot (Head, Body, Legs, Weapon), manufacturer faction (D.O.D. ARMS, War Ensemble, Candle Wolf, M.I.L.K., 4 Forcemen, Jackals, RE Recycling, Special/Events), and weapon damage type:
  - Slash
  - Blunt
  - Pierce
  - Fire
  - Electric
  - Poison
- Forge unlock states:
  - Set items to Shop unlocked (+1 to +4)
  - Set items to In R&D (Remodel / Map status)
  - Unlock all blueprints preset for rapid testing.
  - Built-in R&D repair utility to fix corrupted recipe states.

### Materials and Coin Locker Expansion
- Tower floor tier classification:
  - 1F-10F (D.O.D. ARMS sector)
  - 11F-20F (War Ensemble sector)
  - 21F-30F (Candle Wolf sector)
  - 31F-40F (M.I.L.K. sector)
  - 41F-50F (Battle sector)
  - 51F+ (Tengoku and Jackal materials)
- Filter by stock status: In Stock, Low Stock (< 10), and Out of Stock.
- Instant Coin Locker expansion to 500, 1000, or the maximum cap of 2000 slots.
- Max stock preset (sets all materials to x100).
- Special mushrooms and creature support.

### Weapon Mastery
- Adjust proficiency levels for all 35+ weapon categories from level 1 to 30 (Fists, Machete, Hammer, Iron, KAMAS Rifle, Cleaver Saber, Pitching Machine, etc.).
- Preset to max out all masteries in a single action.

### Armor Sets Encyclopedia
- Interactive set viewer indexing over 60 armor lines across Tiers 1 through 4, including uncapped stats (+19).
- Full coverage of collaboration sets:
  - Travis Touchdown (No More Heroes)
  - Tank Commander (World of Tanks)
  - Kat (Gravity Rush)
  - Momoko Yamada, Meijin, Uncle Death (Reaper)
  - 4 Forcemen (White Steel, Red Napalm, Black Thunder, Pale Wind)

---

## Installation and Downloads

### Method 1: Windows Installer (Recommended)
1. Download `LetItDieSaveEditor_Setup.exe` (or `Instalador_LetItDieSaveEditor_v3.5.exe`) from the [Releases](https://github.com/g3usyk/Let-It-Die-Save-Editor/releases) page.
2. Double-click the installer and complete the setup wizard.
3. Launch the application from the newly created Desktop or Start Menu shortcut.
4. No external runtimes or Python installations are required.

### Method 2: Running from Source
If you prefer running directly from Python:
1. Clone the repository:
   ```bash
   git clone https://github.com/g3usyk/Let-It-Die-Save-Editor.git
   cd Let-It-Die-Save-Editor
   ```
2. Ensure you have Python 3.10+ installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the editor:
   ```bash
   python editor_gui.py
   ```
   Or double-click `Iniciar_Editor_Visual.bat`.

---

## Save Architecture and Backup Safety

### Save File Location
The editor automatically scans all local drives for the standard Steam library path:
```
<SteamLibrary>\steamapps\common\LET IT DIE\Savedata\
```
Default typical location:
```
C:\Program Files (x86)\Steam\steamapps\common\LET IT DIE\Savedata\
```
You can also manually load any `.sav` file through the file browser.

### Compression Format
LET IT DIE saves utilize a proprietary binary wrapper:
- Magic header: `BRG\0` (bytes `0x42 0x52 0x47 0x00`).
- Header version identifiers and compression algorithm tag (`ZL\0\0` for zlib).
- Data payload divided into sequenced chunks, where each chunk specifies its uncompressed size followed by compressed zlib data.
The editor unpacks these chunks into memory, processes the JSON data tree, and cleanly repacks them on save to ensure the game engine accepts the file without CRC or decompression errors.

### Rolling Backup System
Before any write operation is committed to disk, the editor creates a timestamped backup in the `Backups/` directory:
```
Backups/<save_filename>.<YYYYMMDD_HHMMSS>.bak
```
- The retention policy preserves the last 10 backups automatically.
- Backups can be inspected, compared, or restored directly from the application interface or by manually copying the `.bak` file over your active `.sav`.

---

## Developer Reference & Save Architecture

This section documents the internal binary layout and data schemas for developers building custom tools, bots, or mods for LET IT DIE.

### Binary Header Structure

The game save file (`.sav`) is structured into a 16-byte fixed header followed by sequential zlib compression blocks:

| Byte Offset | Size | Type | Value / Purpose |
| :--- | :--- | :--- | :--- |
| `0x00 - 0x03` | 4 bytes | Char array | Magic number: `BRG\0` (`0x42 0x52 0x47 0x00`) |
| `0x04 - 0x07` | 4 bytes | uint32 (LE) | Format version indicator 1 |
| `0x08 - 0x0B` | 4 bytes | uint32 (LE) | Format version indicator 2 |
| `0x0C - 0x0F` | 4 bytes | Char array | Compression identifier: `ZL\0\0` (Standard zlib) |

Following byte `0x10`, the payload contains repeating chunk blocks:
- `uncompressed_chunk_size` (uint32, little-endian, 4 bytes)
- `compressed_chunk_size` (uint32, little-endian, 4 bytes)
- `compressed_bytes` (zlib compressed stream of length `compressed_chunk_size`)

When reading, read each chunk and concatenate the decompressed byte streams. The end of chunks is reached when `uncompressed_chunk_size == 0` or end-of-file.
The combined decompressed payload is valid UTF-8 text containing the game's root JSON document.

### Save JSON Schema (`soul`)

The decoded JSON exposes a root dictionary whose primary game state container is `soul`. Key properties include:

#### Currencies (`soul`)
```json
{
  "soul": {
    "money": 9999999,        // Kill Coins
    "dm": 999,               // Death Metals
    "spl": 9999999,          // SPLithium
    "deathstone": 500000     // Bloodnium
  }
}
```

#### Fighter Storage (`soul.bodyuser` and `soul.chr`)
Fighter entries are separated between metadata (`bodyuser`) and combat stats (`chr`):
- `soul.bodyuser`: Contains the list of fighters in your freezer. Each record stores:
  - `id`: Unique fighter instance identifier.
  - `name`: Assigned fighter name.
  - `class`: Class archetype integer (0: All-Rounder, 1: Striker, 2: Defender, 3: Attacker, 4: Shooter, 5: Collector, 6: Skill Master, 7: Lucky Star).
  - `grade`: Fighter grade (1 to 6 / G6 Uncapped).
  - `status`: Death / freezer status.
- `soul.chr`: Maps fighter IDs to detailed attribute progression:
  - Uncapped level caps: HP, STM, STR, DEX, VIT, LUK.
  - Skill slots and active decal attachments.
  - Equipment slots for right hand, left hand, head, body, and legs.

#### Decal Inventory (`soul.psskl`)
Stores owned decals currently in the player's decal inventory/storage:
```json
[
  {
    "id": "SKL_ATK_Slash_P",  // Decal code (_P indicates Premium)
    "cnt": 5,                 // Quantity owned
    "lock": 0                 // Favorite / locked flag (0 or 1)
  }
]
```

#### R&D Forge / Blueprints (`soul.pr`)
Controls research and development states across all equipment blueprints:
```json
[
  {
    "id": "PT_DIY_ARMS_HEAD_01", // Item blueprint ID
    "status": 1,                 // 0: Locked, 1: Available in Shop, 2: Remodel, 3: MAP
    "level": 4                   // Forge tier reinforcement (+0 to +4)
  }
]
```

#### Coin Locker / Materials Storage (`soul.item`)
Materials and equipment stored in the storage locker:
```json
[
  {
    "id": "ITMT_ALUMI_5",       // Item ID
    "cnt": 100,                 // Stack count
    "slot": 12                  // Inventory slot index
  }
]
```

#### Tower Progression & Elevators (`soul.openelvflr`)
List of unlocked elevator destinations:
```json
[
  {"id": "ELV_MAIN_HUB"},
  {"id": "ELV_MAIN_AMS_FLR_01"},
  {"id": "ELV_MAIN_AMS_FLR_10"},
  {"id": "ELV_MAIN_ARC_FLR_10"}
]
```

#### Weapon Mastery (`soul.mastery` / `soul.bodyuser[].wep`)
Weapon proficiencies mapped by weapon archetype code (`PTARMTP_00` to `PTARMTP_64`):
- Points range from level 1 up to level 30 (cap).

---

## Python API Quickstart

You can use the included `save_io` module or write a standalone Python script to read and write save files programmatically:

```python
import json
import zlib
import struct

def read_save(filepath: str) -> dict:
    with open(filepath, "rb") as f:
        data = f.read()

    # Verify header magic
    if data[:4] != b"BRG\x00":
        raise ValueError("Invalid Let It Die save header.")

    offset = 16
    chunks = []
    while offset < len(data):
        if offset + 4 > len(data):
            break
        uncomp_size = struct.unpack("<I", data[offset:offset+4])[0]
        if uncomp_size == 0:
            break
        comp_size = struct.unpack("<I", data[offset+4:offset+8])[0]
        offset += 8
        chunk_data = data[offset:offset+comp_size]
        chunks.append(zlib.decompress(chunk_data))
        offset += comp_size

    raw_json = b"".join(chunks).decode("utf-8")
    return json.loads(raw_json)

def write_save(save_dict: dict, output_path: str):
    raw_json = json.dumps(save_dict, ensure_ascii=False).encode("utf-8")
    
    # 16-byte BRG header
    header = b"BRG\x00\x01\x00\x00\x00\x00\x00\x00\x00ZL\x00\x00"
    
    # Pack into 64KB uncompressed chunks
    chunk_size = 65536
    body = bytearray()
    for i in range(0, len(raw_json), chunk_size):
        chunk = raw_json[i:i + chunk_size]
        comp = zlib.compress(chunk)
        body += struct.pack("<II", len(chunk), len(comp))
        body += comp

    with open(output_path, "wb") as f:
        f.write(header + body)

# Example usage
save_data = read_save("save.sav")
save_data["soul"]["money"] = 9999999
save_data["soul"]["dm"] = 500
write_save(save_data, "save_modified.sav")
print("Save updated successfully.")
```

---

## Extracting Game Databases (`masters.db`)

The encyclopedia data used by this project is extracted directly from the game client's SQLite master database:
```
<SteamLibrary>\steamapps\common\LET IT DIE\BrgGame\Content\masters.db
```

If the game receives a future patch with new weapons, armors, or decals, you can re-extract the tables using `extract_complete_game_encyclopedia.py`:

```bash
python extract_complete_game_encyclopedia.py
```

This script:
1. Opens `masters.db` in read-only mode.
2. Extracts item definitions, faction affiliations, base stats, and descriptions.
3. Generates the corresponding JSON database files (`all_equipment_encyclopedia.json`, `all_decals_encyclopedia.json`, `all_materials_db.json`, `armor_sets_encyclopedia.json`).
4. Re-indexes sprite sheet UV coordinates in `icon_map.json`.

---

## Repository File Structure

- `editor_gui.py`: Main desktop user interface (Tkinter + sv-ttk modern dark theme) with live bilingual reload.
- `save_io.py`: Binary reading, writing, Steam path multi-drive scanning, and rolling backup management.
- `modifiers.py`: Modding logic for currencies, fighter uncapping, decal injection, and R&D recipe repairs.
- `i18n.py`: English and Spanish string translation maps and dynamic formatter.
- `game_data.py`: Weapon archetype definitions, mastery icons, and tower exploration constants.
- `updater.py`: GitHub version checker and release update notification system.
- `build_exe.py`: Automated PyInstaller compilation script.
- `installer.iss`: Inno Setup compiler script for building `Setup.exe`.
- `Compilar_EXE.bat`: Batch shortcut to compile the standalone binary.
- `Compilar_Instalador.bat`: Batch shortcut to compile the Windows installer.
- `LET_IT_DIE_COMPLETE_ENCYCLOPEDIA.md`: Full markdown reference tables of weapons, armor sets, and masteries.
- `GAME_DATABASE_VERIFIED_NOTES.md`: Verified item catalog extracted from `masters.db`.
- `ADVANCED_GAME_FEATURES_AND_SOUL_MODIFIERS.md`: Complete technical manual of internal save JSON keys and structures.

---

## Building from Source

To compile the standalone binary and installer yourself:

1. Compile the PyInstaller package:
   ```bash
   python build_exe.py
   ```
   Or run `Compilar_EXE.bat`.
2. Generate the Windows installer (requires Inno Setup 6):
   ```bash
   Compilar_Instalador.bat
   ```
   The compiled setup file will be generated in the `dist/` directory.

---

## Language Support
The interface supports real-time bilingual switching between **English** and **Spanish**:
- Toggle the language selector in the top-right header at any time.
- All tabs, category filters, item names, stats, dialogs, and tables update immediately.
- The chosen language persists in `config.json` across sessions.

---

## Disclaimer

This software is an unofficial, community-developed tool intended for personal, offline use and educational purposes. It is not affiliated with, maintained by, or endorsed by Grasshopper Manufacture, Supertrick Games, or GungHo Online Entertainment. Always keep backups of your save files prior to making modifications.
