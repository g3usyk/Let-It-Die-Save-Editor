# LET IT DIE - Offline Save Editor & Encyclopedia

An open-source desktop save editing suite and comprehensive game database for the PC (Steam) release of **LET IT DIE**.

The tool operates directly on local `.sav` files, reading compressed game data, allowing granular adjustments to fighters, equipment, decals, and storage, and recompressing the save while maintaining full file integrity and automated backups.

---

## Download & Installation

### Option 1: Standalone Windows Installer (Recommended for Players)

If you just want to use the editor without dealing with code, Python, or command-line tools:

1. Go to the **[Releases](https://github.com/g3usyk/Let-It-Die-Save-Editor/releases)** page.
2. Download the latest installer:
   - `LetItDieSaveEditor_Setup.exe`
3. Double-click the installer and complete the setup wizard.
4. Launch the application from your Desktop or Start Menu shortcut.
5. No additional software or dependencies are required.

---

### Option 2: Running from Source / Modifying the Code (For Developers)

The entire codebase is 100% open-source, readable Python. You can clone the repository, inspect all logic, tweak features, modify databases, or build your own custom fork:

1. Clone or download the repository:
   ```bash
   git clone https://github.com/g3usyk/Let-It-Die-Save-Editor.git
   cd Let-It-Die-Save-Editor
   ```
2. Ensure you have Python 3.10+ installed ([python.org](https://www.python.org/downloads/)).
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the editor:
   ```bash
   python editor_gui.py
   ```
   Or double-click **`run_editor.bat`**.

---

## Technical Documentation & Reverse Engineering Notes

All reverse-engineering notes, engine save keys, and data tables extracted from `masters.db` are documented in English inside the **[`docs/`](docs/)** directory:

- **[Internal Save Architecture & Soul Modifiers Reference](docs/ADVANCED_GAME_FEATURES_AND_SOUL_MODIFIERS.md)**:
  Full technical breakdown of internal save paths (`soul.bodyuser`, `soul.chr`, `soul.psskl`, `soul.pr`), fighter stat calculations (level allocations vs combat health), Death 'Roids bonuses, TDM rank tables, inventory slot bindings, and elevator station IDs.
- **[Verified Material Catalog & R&D Database](docs/GAME_DATABASE_VERIFIED_NOTES.md)**:
  Complete reference indexing all 106 authentic crafting materials with internal item IDs, localized names, star rarities, and tower sector classifications.
- **[Master Game Encyclopedia & Data Tables](docs/LET_IT_DIE_COMPLETE_ENCYCLOPEDIA.md)**:
  Extracted reference tables covering 1,370 equipment pieces, 385 weapons, and 368 decals with exact combat effect descriptions.

---

## Security, Privacy & Transparency

- **100% Open Source**: All source code is completely visible and readable in plain Python (`editor_gui.py`, `save_io.py`, `modifiers.py`). There is zero obfuscation or compiled proprietary blobs.
- **Offline & Local**: Save processing occurs strictly on your machine in memory. The tool does not collect personal data, telemetry, or account credentials. The only network request made is an optional check against the public GitHub releases API to inform you when a new version is available.
- **Rolling Backups**: The editor creates a timestamped `.bak` file in `Backups/` before writing any changes, keeping the 10 most recent versions so you can restore your original save at any point.

---

## Features

### Currencies and Resources
- Modify Kill Coins, Death Metals, SPLithium, and Bloodnium directly.
- Safety boundaries prevent integer overflow crashes.

### Fighter Freezer Management
- View and manage all fighters stored in your freezer.
- Modify attributes:
  - Class (All-Rounder, Striker, Defender, Attacker, Shooter, Collector, Skill Master, Lucky Star).
  - Grade and uncapped stats (HP, STM, STR, DEX, VIT, LUK).
- Equip endgame preset builds directly into active loadouts:
  - Tengoku Climber (High-floor progression setup)
  - KAMAS Shooter (Ranged DPS optimization)
  - Melee Striker (Heavy burst damage configuration)
  - TDM Defender (High resistance and tank setup)

### Decal Inventory
- Full database of 626 official decals extracted from game data.
- Distinct handling for Standard and Premium (`_P`) decals.
- Filter by collaboration events (World of Tanks, No More Heroes, Killer7, Gravity Rush, Tengoku Meta) and playstyles (Addicts, Critical, Tank, Vampire, Farming, Set Synergies).

### Blueprints and R&D Forge
- Complete catalog of 1,370 equipment pieces and 385 weapons.
- Filter by gear slot (Head, Body, Legs, Weapon), manufacturer faction (D.O.D. ARMS, War Ensemble, Candle Wolf, M.I.L.K., 4 Forcemen, Jackals, RE Recycling, Special/Events), and damage types (Slash, Blunt, Pierce, Fire, Electric, Poison).
- Set unlock states (Shop unlocked +1 to +4, In R&D).
- Includes an R&D repair tool to resolve corrupted recipe states.

### Materials and Storage Locker
- Tower floor sector classification (1F-10F DOD, 11F-20F WE, 21F-30F CW, 31F-40F MILK, 41F-50F Battle, 51F+ Tengoku).
- Filter by inventory state: In Stock, Low Stock (< 10), Out of Stock.
- Instant Coin Locker expansion to 500, 1000, or the maximum cap of 2000 slots.
- Max stock preset (x100 to all materials).

### Weapon Mastery
- Adjust proficiency levels for all 35+ weapon categories from level 1 to 30.
- Quick preset to max out all masteries at once.

### Armor Sets Encyclopedia
- Interactive set viewer covering 60+ armor lines across Tiers 1-4, including uncapped stats (+19).
- Full coverage of collaboration sets (Travis Touchdown, Tank Commander, Kat, Momoko, Meijin, Reaper, and the 4 Forcemen).

---

## Save Architecture and Technical Reference

This section outlines how LET IT DIE save files operate for developers wanting to write custom extensions or tools.

### Save File Location
The editor scans all local drives for the standard Steam library directory:
```
<SteamLibrary>\steamapps\common\LET IT DIE\Savedata\
```
Default typical location:
```
C:\Program Files (x86)\Steam\steamapps\common\LET IT DIE\Savedata\
```

### Binary Format & Compression
LET IT DIE `.sav` files use a 16-byte binary wrapper followed by sequential zlib compression blocks:

| Byte Range | Type | Purpose |
| :--- | :--- | :--- |
| `0x00 - 0x03` | Char array | Magic number: `BRG\0` (`0x42 0x52 0x47 0x00`) |
| `0x04 - 0x07` | uint32 (LE) | Format version indicator 1 |
| `0x08 - 0x0B` | uint32 (LE) | Format version indicator 2 |
| `0x0C - 0x0F` | Char array | Compression tag: `ZL\0\0` (zlib) |

Following byte `0x10`, repeating chunk blocks are structured as:
- `uncompressed_chunk_size` (uint32, little-endian, 4 bytes)
- `compressed_chunk_size` (uint32, little-endian, 4 bytes)
- `compressed_bytes` (zlib payload of length `compressed_chunk_size`)

Concatenating the decompressed streams yields valid UTF-8 JSON.

### Core JSON Schema (`soul`)
- `soul.money`, `soul.dm`, `soul.spl`, `soul.deathstone`: Player currency balances.
- `soul.bodyuser`: List of stored fighters with class codes (0-7), grades, and status.
- `soul.chr`: Detailed fighter progression attributes, uncapped levels, and decal slot bindings.
- `soul.psskl`: Owned decal inventory list (`id`, `cnt`, `lock`).
- `soul.pr`: R&D forge recipe progress (`id`, `status` [0: locked, 1: shop, 2: remodel, 3: map], `level`).
- `soul.item`: Coin Locker contents (`id`, `cnt`, `slot`).
- `soul.openelvflr`: Unlocked elevator destinations.
- `soul.mastery`: Weapon proficiencies (`PTARMTP_00` to `PTARMTP_64`).

For complete schema details and property paths, refer to [docs/ADVANCED_GAME_FEATURES_AND_SOUL_MODIFIERS.md](docs/ADVANCED_GAME_FEATURES_AND_SOUL_MODIFIERS.md).

---

## Python API Quickstart

Developers can read and write save files using the following standalone pattern:

```python
import json
import zlib
import struct

def read_save(filepath: str) -> dict:
    with open(filepath, "rb") as f:
        data = f.read()

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
        chunks.append(zlib.decompress(data[offset:offset+comp_size]))
        offset += comp_size

    return json.loads(b"".join(chunks).decode("utf-8"))

def write_save(save_dict: dict, output_path: str):
    raw_json = json.dumps(save_dict, ensure_ascii=False).encode("utf-8")
    header = b"BRG\x00\x01\x00\x00\x00\x00\x00\x00\x00ZL\x00\x00"
    
    chunk_size = 65536
    body = bytearray()
    for i in range(0, len(raw_json), chunk_size):
        chunk = raw_json[i:i + chunk_size]
        comp = zlib.compress(chunk)
        body += struct.pack("<II", len(chunk), len(comp))
        body += comp

    with open(output_path, "wb") as f:
        f.write(header + body)

# Usage example:
save = read_save("save.sav")
save["soul"]["money"] = 9999999
write_save(save, "save_modified.sav")
```

---

## Repository Structure

- `editor_gui.py`: Primary Tkinter desktop application with live English/Spanish switching.
- `save_io.py`: Binary decompressor/compressor, Steam path auto-detection, and backup engine.
- `modifiers.py`: High-level modifications (currencies, stats, inventory, R&D states).
- `i18n.py`: Bilingual localization dictionary and formatter.
- `game_data.py`: Weapon categories, mastery mapping, and item constants.
- `updater.py`: Version checking against the public GitHub Releases API.
- `run_editor.bat`: Convenient launcher script for running directly from source.
- `requirements.txt`: Python package requirements (`sv-ttk`, `pillow`).
- `docs/`: In-depth reference notes, complete item tables, and technical specifications.
- `tools/`: Packaging scripts (`build_exe.py`, `installer.iss`) and extraction utilities.

---

## Compiling Your Own Build

To package your modifications into a standalone `.exe` or installer:

1. Compile the portable binary:
   ```bash
   python build_exe.py
   ```
   (or run `tools\Compilar_EXE.bat`).
2. Generate the Windows setup wizard (requires Inno Setup 6):
   ```bash
   tools\Compilar_Instalador.bat
   ```
   The resulting setup executable will be placed in `dist/`.

---

## License & Disclaimer

This project is licensed under the [MIT License](LICENSE).

This software is an unofficial, community-developed utility intended for personal, offline use and educational purposes. It is not affiliated with, maintained by, or endorsed by Grasshopper Manufacture, Supertrick Games, or GungHo Online Entertainment. Always verify your save backups prior to applying edits.
