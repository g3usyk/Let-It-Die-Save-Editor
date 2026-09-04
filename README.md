# LET IT DIE - Save Editor and Developer Reference

An open-source desktop application and technical reference suite for inspecting, editing, and repairing PC (Steam) save files for LET IT DIE.

The project operates directly on local `.sav` files, decoding the proprietary multi-chunk compressed stream, exposing validated game systems through a modular graphical interface, and repacking modifications with strict binary parity, atomic file operations, and automated rolling backups.

---

## Architecture Overview

The codebase is organized into distinct functional layers to ensure modularity, maintainability, and testability.

### 1. UI Layer and Domain Mixins (`ui/`)
The graphical user interface is built on Python's native Tkinter and TTK frameworks with a custom dark cyberpunk theme (`ui/theme.py`). Rather than maintaining a monolithic GUI class, the interface uses the Domain Mixin pattern:
- **`ui/tabs/`**: Each notebook tab is implemented as an independent mixin class (`CurrenciesTabMixin`, `FightersTabMixin`, `MaterialsTabMixin`, `DecalsTabMixin`, `BlueprintsTabMixin`, `MasteryTabMixin`, `TowerTabMixin`, `AdvancedTabMixin`).
- **`editor_gui.py`**: The primary orchestrator class `CompleteSaveEditorGUI` inherits from `tk.Tk` and all tab mixins. It handles top-level lifecycle events (file loading, auto-saving, HUD status rendering, modal dialog spawning) while delegating tab construction and event binding to the respective mixin modules.
- **`ui/dialogs/`**: Dedicated modal windows for complex workflows (custom fighter creation, blueprint R&D analyzer, armor set visualization, and full inventory inspection).
- **`ui/components/`**: Reusable widgets such as dynamic scrollable frames with native mousewheel handling.

### 2. Core Logic Layer (`core/`)
The business logic of save editing is completely decoupled from the graphical interface. Functions in `core/` receive the loaded Python dictionary (`save_json`) and perform targeted mutations without UI side effects:
- `currencies.py`: Safe arithmetic adjustments for Kill Coins, Death Metals, SPLithium, Bloodnium, Recycle Points, and bank/tank facility caps up to level 100.
- `fighters.py`: Full character manipulation, stat point allocation, grade 6 limit break/Tier 8 calculations, decal slot expansions, fighter cloning, freezer reordering, and slot synchronization.
- `storage.py`: Storage locker expansion, dynamic material insertion across all 106 authentic crafting items, stack top-ups, and bag/box distribution.
- `decals.py`: Skill decal collection management, standard/premium decal differentiation, and preset loadout injection into active fighter rosters.
- `blueprints.py`: R&D blueprint state tracking, equipment uncap levels (+4 through +19/+24), infinite durability flags, and ammo capacity overrides.
- `mastery.py`: Weapon mastery calculations across all 57 weapon categories up to level 20/30 with exact experience point mapping.
- `tower.py`: Tower of Barbs elevator network (61 stations), full map discovery (980 rooms, 1,119 escalators), physical gate unlocks (122 gates), Stamp Rally completion, and tutorial/waiting room facility unlocks.
- `helpers.py`: Common utilities including player UID resolution, save structure repair, database discovery, and account summary generation.

### 3. Save File I/O Engine (`save_io.py`)
LET IT DIE save files use a proprietary binary layout:
- **Magic Header**: 16 bytes containing the ASCII signature `BRG\0`, uint32 version, total uncompressed JSON byte length, and the algorithm identifier `ZLIB`.
- **Balanced Multi-Chunk Compression**: The uncompressed UTF-8 JSON payload is split into balanced chunks (default: 4 chunks), each compressed separately with zlib and prefixed by an 8-byte chunk descriptor (`uncompressed_size`, `compressed_size`).
- **EOF Trailer**: A 4-byte zero integer (`0x00000000`) signaling the end of the streaming decompressor.
- **Atomic File Writing**: Modified data is written to a unique temporary file (`.tmp_<uuid>.sav`) before an atomic rename (`os.replace`) replaces the active save. This eliminates corruption risks caused by process interruption or system crashes.
- **Rolling Backups**: Prior to writing, a timestamped `.bak` copy is deposited into the `Backups/` directory, retaining the 10 most recent states with automatic pruning.

### 4. Database Integration (`masters.db`)
The project dynamically queries the game's official SQLite master database (`masters.db`) located in the game client's content directory. This database supplies authentic weapon names, base damage tables, required crafting materials, and weapon evolution chains (`nextptid`). If running standalone without the full game installed, the application seamlessly falls back to pre-compiled JSON snapshots (`all_blueprints_db.json`, `all_decals_db.json`, `all_materials_db.json`, `all_shrooms_beasts_db.json`, `tower_map_data.json`).

### 5. Internationalization (`i18n.py`)
Complete bilingual support (English and Spanish) is managed via a centralized dictionary. Key parity between languages is enforced via automated unit tests.

---

## Directory Structure

```
.
├── core/                           # Core business logic for save mutations
│   ├── __init__.py                 # Public API exports
│   ├── blueprints.py               # Equipment R&D, forge recipes, and uncapping
│   ├── currencies.py               # KC, DM, SPL, Bloodnium, and facility caps
│   ├── decals.py                   # Decal collection, inventory, and presets
│   ├── fighters.py                 # Fighter attributes, cloning, and freezer logic
│   ├── helpers.py                  # Player UID detection and structure repair
│   ├── mastery.py                  # Weapon mastery levels and EXP formulas
│   ├── storage.py                  # Materials, beasts, mushrooms, and coin locker
│   └── tower.py                    # Elevators, 980-room map, gates, and tutorial flags
├── ui/                             # User interface presentation layer
│   ├── components/                 # Reusable Tkinter custom widgets
│   │   ├── __init__.py
│   │   └── scrollable_frame.py     # Canvas-based smooth scrollable frame
│   ├── dialogs/                    # Specialized modal windows
│   │   ├── __init__.py
│   │   ├── armor_set_viewer.py     # Armor set inspection and full gear viewer
│   │   ├── create_fighter.py       # Custom fighter creation wizard
│   │   ├── inventory_viewer.py     # Full inventory browser and item inspector
│   │   └── smart_analyzer.py       # Blueprint R&D material requirement calculator
│   ├── tabs/                       # Modular notebook tab mixins
│   │   ├── __init__.py             # Exports all domain mixins
│   │   ├── advanced_tab.py         # Backups manager and JSON import/export
│   │   ├── blueprints_tab.py       # 1,370 equipment items, uncap, and forge actions
│   │   ├── currencies_tab.py       # Resources, bank/tank upgrades, and VIP pass
│   │   ├── decals_tab.py           # 626 decals, filters, and preset equipment
│   │   ├── fighters_tab.py         # Fighter freezer, slots, stats, and reordering
│   │   ├── mastery_tab.py          # Weapon mastery table and bulk setters
│   │   ├── materials_tab.py        # 106 materials catalog, storage stock, and locker
│   │   └── tower_tab.py            # Elevators, stamps, quests, and TDM configuration
│   └── theme.py                    # Color palette constants and TTK styling definitions
├── tests/                          # Automated unit test suite
│   ├── __init__.py
│   ├── test_blueprints.py          # Blueprint evolution and uncap validation
│   ├── test_currencies.py          # Resource boundaries and VIP logic
│   ├── test_decals.py              # Decal loading and preset equipping
│   ├── test_fighters.py            # Fighter stats, freezer ordering, and fresh save
│   ├── test_helpers.py             # UID extraction and schema repair
│   ├── test_i18n.py                # Translation key parity and formatting
│   ├── test_mastery.py             # Weapon mastery calculations
│   ├── test_save_io.py             # Binary compression roundtrip and backups
│   ├── test_storage.py             # Storage additions and capacity expansion
│   └── test_tower.py               # Elevators, gates, and tutorial unlock flags
├── tools/                          # Developer utilities and build scripts
│   ├── editor_cli.py               # Interactive command-line save editor
│   ├── extract_complete_game_encyclopedia.py # SQLite database dump utility
│   ├── publish_version.py          # Release tagging and manifest updater
│   └── update_docs_english_primary.py # Documentation synchronization script
├── docs/                           # In-depth technical documentation
│   ├── README.md                   # Documentation index
│   ├── ADVANCED_GAME_FEATURES_AND_SOUL_MODIFIERS.md # Save schema reference
│   ├── GAME_DATABASE_VERIFIED_NOTES.md # Material catalog and flag IDs
│   └── LET_IT_DIE_COMPLETE_ENCYCLOPEDIA.md # Equipment, weapon, and decal tables
├── editor_gui.py                   # Main GUI entrypoint and window orchestrator
├── save_io.py                      # Binary save decompressor, compressor, and backup manager
├── modifiers.py                    # Compatibility facade re-exporting core functions
├── game_data.py                    # Static game enumerations and class definitions
├── i18n.py                         # Internationalization engine and dictionaries
├── build_exe.py                    # PyInstaller standalone build configuration
├── run_tests.py                    # Test runner executing all unit tests
├── requirements.txt                # Python package dependencies
└── tower_map_data.json             # Pre-compiled indices for 980 rooms and 1,119 escalators
```

---

## Save File Schema and Key Engine Paths

Understanding how LET IT DIE represents state in memory and storage is essential for contributing.

### 1. Fighter Engine Hierarchy
Character information is split across three structures keyed by the player's User ID (`uid`):
- **`save_json["bodyuser"][uid]`**: Array of fighter base structures containing permanent attribute allocations (1-45 points across HP, STR, DEX, VIT, STM, LUK), Death 'Roids bonuses (+20 each for Tier 8), MINGO bag expansions (0-3), and decal slot expansions (0-3).
- **`save_json["soul"]["chr"]["chrs"][uid]`**: Array of live combat entities containing visual model meshes (`BODY_FEMALE_001` through `BODY_MALE_008`), head gasmasks, class codes (`BAL`, `STR`, `DEF`, `ATK`, `SHO`, `COL`, `SKI`, `LUK`), tier grade (1-6), uncapping limit break (0-4), and live states (`GUARD`, `USE`, `WAITING_ROOM`, `DEAD`).
- **`save_json["soul"]["chr"]["slots"][uid]`**: Exactly 10 freezer slot entries mapping indices 0 through 9 to fighter UUIDs (`cid`). Empty slots must maintain `"cid": ""`.

### 2. Tower Map Exploration and Padlock Cleansing
- **`save_json["soul"]["areaflag"]`**: Contains 980 room entries `{"idx": N, "val": 33}`. If bit 64 is active (`val & 64`), the game renders a red padlock icon indicating an unreachable one-way gate. The editor strips bit 64 (`val & ~64`) across all rooms, removing all padlocks from the map.
- **`save_json["soul"]["areaescflag"]`**: Contains 1,119 escalator pathways `{"idx": N, "val": 7}`.
- **`save_json["gameflg"]["cl"]`**: Contains 122 one-way gate flags (`RELEASE_GATE_...`). Setting their value to `1` opens all physical shortcut gates and valves.

### 3. Fresh Save Initialization and Tutorial Lockout
When a new game starts from scratch, the save is locked in a prologue state:
- `gameflg["sv"]`: Contains `KGF_TUTORIAL_PROGRESS`. Until this value reaches `100`, the engine restricts facility usage.
- `gameflg["cl"]`: Requires specific interaction flags before NPCs activate:
  - `KGF_FIRST_KIWAKOROOM`: Unlocks Kiwako Seto and the Fighter Freezer interface.
  - `KGF_FIRST_BASE`: Registers the first Waiting Room arrival cutscene.
  - `KGF_FIRST_SHOP_BASE`: Activates Chokufunsha equipment forging and purchases.
  - `KGF_FIRST_KINOKOYA`: Activates the Mushroom Club (Momoko Yamada).
  - `KGF_FIRST_NAOMI`: Activates the Hater mission counter.
  - `KGF_FIRST_VIP_ELEVATORGIRL`: Activates the Direct Hell VIP elevator attendant.
  - `KGF_MET_TUTORIAL_CLEAR` and `KGF_TUTORIAL_COMP`: Concludes the subway prologue.

The editor's `unlock_tutorial_and_waiting_room(save)` function sets all these keys simultaneously and resets dungeon floor coordinates (`soul.stgid`, `soul.flrid`, `soul.areaid`) to empty strings, guaranteeing a clean spawn in the center of the Waiting Room. This function runs automatically whenever a new fighter is created or cloned on a fresh save.

---

## Development Setup

### Prerequisites
- Python 3.10 or higher.
- A functional Windows environment (tested on Windows 10/11) with Steam and LET IT DIE installed, or sample `.sav` files in `CurrentSave/`.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/g3usyk/Let-It-Die-Save-Editor.git
   cd Let-It-Die-Save-Editor
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application from source:
   ```bash
   python editor_gui.py
   ```

### Running Automated Tests
The project includes a comprehensive test suite in `tests/` covering save compression, blueprint evolution, currency bounds, storage expansions, fighter slots, and tower unlocking:
```bash
python run_tests.py
```
All pull requests must pass the full test suite with zero failures before being merged.

### Building Standalone Executable
The project uses PyInstaller with a custom build script that bundles required assets, databases, and hidden imports:
```bash
python build_exe.py
```
The compiled standalone executable and support files will be generated in `dist/LetItDieSaveEditor/`.

---

## Contribution Guidelines

### Adding a New Modifier Function
1. Implement the modification in the appropriate module under `core/` (e.g. `core/fighters.py`, `core/storage.py`).
2. Keep functions pure: accept the `save_json` dictionary as the first argument, mutate the structure safely, and return a result value or boolean.
3. Handle missing keys gracefully using `.setdefault()` or `get_or_create_list()`.
4. Export the function in `core/__init__.py` and add it to `__all__`.
5. Re-export in `modifiers.py` to maintain backward compatibility.
6. Write a corresponding unit test in `tests/` validating expected mutations on both populated and empty save schemas.

### Modifying or Adding UI Tabs
1. Open or create the appropriate mixin file in `ui/tabs/`.
2. Follow the existing naming convention: `_build_<feature>_tab(self)` for layout construction and `_<feature>_action(self)` for user event handlers.
3. Access save state exclusively through `self.save_json`.
4. After mutating state, invoke `self._auto_save()` and `self.refresh_all_views()`.
5. Display non-blocking status notifications via `self._notify(title_en, title_es, msg_en, msg_es)`.

### Localization
1. All user-facing strings must use `i18n.t("key_name")`.
2. Define both English (`en`) and Spanish (`es`) values in the `TRANSLATIONS` dictionary inside `i18n.py`.
3. Verify that `tests/test_i18n.py` passes to ensure key parity between languages.

---

## Technical Documentation Reference

For deeper technical breakdowns of specific engine mechanics, consult the documents in the `docs/` folder:
- **[Internal Save Architecture & Soul Modifiers Reference](docs/ADVANCED_GAME_FEATURES_AND_SOUL_MODIFIERS.md)**: Exhaustive JSON paths, binary chunk offsets, Death 'Roids formulas, and VIP friendship validation.
- **[Verified Material Catalog & R&D Database](docs/GAME_DATABASE_VERIFIED_NOTES.md)**: All 106 authentic crafting materials with internal IDs, localized names, and floor ranges.
- **[Master Game Encyclopedia & Data Tables](docs/LET_IT_DIE_COMPLETE_ENCYCLOPEDIA.md)**: Tables covering 1,370 equipment pieces, 385 weapons, and 368 decals.

---

## License and Disclaimer

This project is an independent open-source tool developed for educational and single-player modding purposes. It is not affiliated with, endorsed by, or connected to Grasshopper Manufacture, Supertrick Games, or GungHo Online Entertainment.
