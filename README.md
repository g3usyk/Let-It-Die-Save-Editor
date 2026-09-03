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

## Installation and Downloads

### Method 1: Windows Installer (Recommended)
1. Download `Instalador_LetItDieSaveEditor_v3.5.exe` from the [Releases](https://github.com/g3usyk/Let-It-Die-Save-Editor/releases) page.
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

## Language Support
The interface supports real-time bilingual switching between **English** and **Spanish**:
- Toggle the language selector in the top-right header at any time.
- All tabs, category filters, item names, stats, dialogs, and tables update immediately.
- The chosen language persists in `config.json` across sessions.

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

## Disclaimer

This software is an unofficial, community-developed tool intended for personal, offline use and educational purposes. It is not affiliated with, maintained by, or endorsed by Grasshopper Manufacture, Supertrick Games, or GungHo Online Entertainment. Always keep backups of your save files prior to making modifications.
