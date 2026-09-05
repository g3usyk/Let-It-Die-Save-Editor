# LET IT DIE - Internal Save Architecture & Soul Modifiers Reference
> Technical Reference Manual for Save Modders and Tool Developers
> Fully documented with game engine paths, JSON keys, and data structures.

---

## Table of Contents
1. [Tower Elevator Network and Floor Unlocks (openelvflr)](#1-tower-elevator-network-and-floor-unlocks-openelvflr)
2. [Uncle Death Stamp Rally & Research Multipliers (researchstamp)](#2-uncle-death-stamp-rally--research-multipliers-researchstamp)
3. [Death Bag Inventory Structure and Expansion (deathbag)](#3-death-bag-inventory-structure-and-expansion-deathbag)
4. [Tokyo Death Metro (TDM) Rank and Point System](#4-tokyo-death-metro-tdm-rank-and-point-system)
5. [TDM Mystery Bags Architecture (mysterybag)](#5-tdm-mystery-bags-architecture-mysterybag)
6. [Reward Box / Mailbox Presents (soul.present)](#6-reward-box--mailbox-presents-soulpresent)
7. [Elevator Floor ID Reference](#7-elevator-floor-id-reference)
8. [Uncle Death Compendiums (msrbook and bstbook)](#8-uncle-death-compendiums-msrbook-and-bstbook)
9. [Waiting Room Customization and Skins (hubcustom and armorskin)](#9-waiting-room-customization-and-skins-hubcustom-and-armorskin)
10. [Fighter Engine Architecture (bodyuser and chr)](#10-fighter-engine-architecture-bodyuser-and-chr)
11. [Equipment Modifiers: Durability and Ammunition](#11-equipment-modifiers-durability-and-ammunition)
12. [Endgame Meta Decal Loadouts (8 Slots)](#12-endgame-meta-decal-loadouts-8-slots)
13. [Endgame Equipment Sets (44CE Forcemen, Jackals, Tengoku)](#13-endgame-equipment-sets-44ce-forcemen-jackals-tengoku)
14. [Official Quest Auto-Completion (soul.quest)](#14-official-quest-auto-completion-soulquest)
15. [Yotsuyama Magazines and Jukebox Channels](#15-yotsuyama-magazines-and-jukebox-channels)
16. [Automated Rolling Backup System](#16-automated-rolling-backup-system)
17. [Equipment Evolution & Uncapping Hierarchy (+4 vs +19/+24)](#17-equipment-evolution--uncapping-hierarchy-4-vs-1924)
18. [Windows Administrative Auto-Elevation (UAC Architecture)](#18-windows-administrative-auto-elevation-uac-architecture)
19. [Royal Express VIP Pass Validation & The Friendship Bug Fix (soul.vip)](#19-royal-express-vip-pass-validation--the-friendship-bug-fix-soulvip)
20. [Balanced ZLIB Multi-Chunk Compressor (save_io.py)](#20-balanced-zlib-multi-chunk-compressor-save_iopy)
21. [Chokufunsha R&D Mode vs Shop Max for +19 Uncapped Equipment (soul.partresearch.user)](#21-chokufunsha-rd-mode-vs-shop-max-for-19-uncapped-equipment-soulpartresearchuser)
22. [Emergency Waiting Room Fighter Rescue (soul.chr.chrs)](#22-emergency-waiting-room-fighter-rescue-soulchrchrs)
23. [Full Tower Map Discovery, Escalator Pathways & Gates (soul.areaflag, soul.areaescflag, gameflg.cl)](#23-full-tower-map-discovery-escalator-pathways--gates-soulareaflag-soulareaescflag-gameflgcl)
24. [Tutorial Progression, Fresh Save Recovery & Waiting Room Facility Flags (gameflg.sv, gameflg.cl)](#24-tutorial-progression-fresh-save-recovery--waiting-room-facility-flags-gameflgsv-gameflgcl)
25. [Fighter Freezer Architecture & 10-Slot Synchronization (soul.chr.slots, bodyuser, soul.chr.chrs)](#25-fighter-freezer-architecture--10-slot-synchronization-soulchrslots-bodyuser-soulchrchrs)
26. [Chokufunsha 2D Icon Streaming & Parent-Child Inheritance Architecture (master_part.nextptid, CookedPCConsole)](#26-chokufunsha-2d-icon-streaming--parent-child-inheritance-architecture-master_partnextptid-cookedpcconsole)
27. [Skill Decal Combat Formula Placeholders & Offline Resolution (master_text, master_skill)](#27-skill-decal-combat-formula-placeholders--offline-resolution-master_text-master_skill)
28. [Weapon Mastery HUD vs Equipment Research Level Demystification (master_expert_lvl_reward, soul.expert)](#28-weapon-mastery-hud-vs-equipment-research-level-demystification-master_expert_lvl_reward-soulexpert)
29. [Defense Simulation & Raid Engine Crash Prevention (bodyuser.rage, select_arm_slots, TDM sanitization)](#29-defense-simulation--raid-engine-crash-prevention-bodyuserrage-select_arm_slots-tdm-sanitization)
30. [Legitimacy Normalization: Removal of Out-of-Bounds Stats & Fictitious Modifiers](#30-legitimacy-normalization-removal-of-out-of-bounds-stats--fictitious-modifiers)
31. [Level-Up Engine Crash Demystification (DistributeBodyLvlParam & chr.rest_exp)](#31-level-up-engine-crash-demystification-distributebodylvlparam-rva-0x118e9c0--chrrest_exp)

---

## 1. Tower Elevator Network and Floor Unlocks (openelvflr)

### Save File Path
* `save_json["soul"]["openelvflr"]` -> List of unlocked elevator station IDs across the Tower of Barbs.

### Structure of openelvflr
```json
[
  {"id": "ELV_MAIN_HUB"},
  {"id": "ELV_MAIN_AMS_FLR_01"},
  {"id": "ELV_MAIN_AMS_FLR_03"},
  {"id": "ELV_MAIN_AMS_FLR_05"},
  {"id": "ELV_MAIN_AMS_FLR_10"},
  {"id": "ELV_MAIN_ARC_FLR_01"},
  {"id": "ELV_MAIN_ARC_FLR_02"},
  {"id": "ELV_MAIN_ARC_FLR_03"},
  {"id": "ELV_MAIN_ARC_FLR_06"},
  {"id": "ELV_MAIN_ARC_FLR_09"},
  {"id": "ELV_MAIN_ARC_FLR_10"},
  {"id": "ELV_MAIN_MET_FLR_01"},
  {"id": "ELV_MAIN_MET_FLR_03"},
  {"id": "ELV_MAIN_MET_FLR_04"},
  {"id": "ELV_MAIN_MET_FLR_05"},
  {"id": "ELV_MAIN_MET_FLR_06"},
  {"id": "ELV_MAIN_MET_FLR_08"},
  {"id": "ELV_MAIN_MET_FLR_09"},
  {"id": "ELV_MAIN_MET_FLR_10"},
  {"id": "ELV_MAIN_RFT_FLR_01"},
  {"id": "ELV_MAIN_RFT_FLR_03"},
  {"id": "ELV_SUB01_AMS_FLR_02_A"},
  {"id": "ELV_SUB01_AMS_FLR_07_A"},
  {"id": "ELV_SUB01_ARC_FLR_05"},
  {"id": "ELV_SUB01_ARC_FLR_10"},
  {"id": "ELV_SUB02_AMS_FLR_02_B"},
  {"id": "ELV_SUB03_AMS_FLR_02_C"},
  {"id": "ELV_SUB1_MET_FLR_02"},
  {"id": "ELV_SUB1_MET_FLR_10"}
]
```

### Mechanics
Registering the official `ELV_MAIN_...` and `ELV_SUB...` IDs permanently enables the central Waiting Room elevator and all district elevators (AMS, ARC, MET, RFT) without paying Kill Coin fees.

---

## 2. Uncle Death Stamp Rally & Research Multipliers (researchstamp)

### Save File Paths
* `save_json["soul"]["researchstamp"]` -> Global combat damage multipliers from Uncle Death stamps.
* `save_json["soul"]["partresearch"]["user"]` -> Unlocked blueprints in Chokufunsha.

### Structure of researchstamp
```json
[
  {"type": "SLASH", "rate": 2.8},
  {"type": "HIT", "rate": 1.6},
  {"type": "LEGS", "rate": 1.2},
  {"type": "HEAD", "rate": 0.6},
  {"type": "BODY", "rate": 1.4}
]
```

### Stamp Rewards
* **Uncle Death's Legendary Scythe (`PT_ARM_WP050_001`):** Injected into `partresearch.user` with Tiers 1 through 4 marked as `FINISHED` and Tier 5 ready to forge and purchase directly at Chokufunsha using Kill Coins.

---

## 3. Death Bag Inventory Structure and Expansion (deathbag)

### Save File Paths
* `save_json["soul"]["bag_slot"]` -> Global base inventory capacity (default: 20).
* `save_json["soul"]["deathbag"]` -> Dictionary indexed by fighter UID storing active bag slots.
* `save_json["bodyuser"][uid][i]["bag"]` -> Fighter-specific bag capacity (expandable to 30, 40, or 50).

### Slot Schema in deathbag
```json
{
  "uid": 443455,
  "cid": "c39c2170-24fd-493d-ae16-b5453328add2",
  "slot": 1,
  "type": 0,
  "eid": "item-uuid-reference",
  "site": "EQSITE_WEAPON_R1",
  "arm_slot": 0
}
```

### Equipment Slots (site)
* `"EQSITE_HEAD"` -> Helmet / Mask
* `"EQSITE_BODY"` -> Chest armor
* `"EQSITE_LEGS"` -> Pants / Leg armor
* `"EQSITE_WEAPON_R1"` / `"EQSITE_WEAPON_R2"` -> Right hand weapon slots
* `"EQSITE_WEAPON_L1"` / `"EQSITE_WEAPON_L2"` -> Left hand weapon slots
* `""` (empty string) -> Loose item stored in backpack

---

## 4. Tokyo Death Metro (TDM) Rank and Point System

### Save File Paths
* `save_json["soul"]["tdm_rank"]` -> TDM competitive rank tier ID.
* `save_json["soul"]["tdm_point"]` -> TDM raid rating points.
* `save_json["soul"]["team_id"]` -> Assigned team as a **STRING** (e.g., `"52"` Mexico, `"11"` California, `"01"` Tokyo).
* `save_json["soul"]["favorite_team"]` -> Assigned favorite team as a **STRING** (must match `soul["team_id"]`).
* `save_json["teammember"]["tid"]` -> Root table team affiliation as an **INTEGER** (e.g., `52`).
* `save_json["soul"]["rank"]` -> Player rank (**1 to 115**), calculated by the authentic formula.
* `save_json["soul"]["rank_point"]` -> Rank points corresponding to the current rank.

### The Team ID String Deserialization Trap (`BrgGame-Steam.exe+0x12dbbf5` Crash)
A critical reverse engineering discovery in `BrgGame-Steam.exe`:
* At `0xf023ab` and `0xf02471`, the Unreal Engine JSON deserializer parses the team fields:
  ```cpp
  JsonObject->GetStringField(TEXT("team_id"), OutTeamIdStr);
  JsonObject->GetStringField(TEXT("favorite_team"), OutFavTeamStr);
  ```
* Because `GetStringField` checks `JsonValue->Type == EJson::String`, if `team_id` or `favorite_team` is saved as a numerical integer (e.g. `52` instead of `"52"`), the type check fails. The engine falls back to the default unassigned string `"NONE"`.
* Later, during Defense Simulation or Subway Raid loading, `0x12dba10` parses the string:
  ```cpp
  int tid = _wtoi(OutTeamIdStr.c_str()); // _wtoi(L"NONE") returns 0
  ITeamData* pTeam = GetTeam(tid);       // 0x14133d8a0: GetTeam(0) returns NULL (teams are 1-164)
  ```
* At `0x12dbbf5`:
  ```assembly
  mov rdi, [rsi + 0x48]  ; rsi is NULL (pTeam == 0) -> rdi = 0x48
  mov eax, [rdi + 8]     ; Dereferences [0x48 + 8] = [0x50] -> ACCESS VIOLATION 0xc0000005!
  ```
* **Strict Rule**: `soul["team_id"]` and `soul["favorite_team"]` must **always be string format** (e.g. `"52"`). Root `save["teammember"]["tid"]` must simultaneously be the matching **integer** (`52`).

### Authentic Player Rank Calculation Formula
The player rank displayed on your TDM license card and evaluated during matchmaking follows this exact formula:
$$\text{Rank} = \min\left(115, \max\left(1, (\text{Highest Fighter Grade} - 1) \times 15 + \text{Count of Fighters of that Grade}\right)\right)$$
* Maximum legitimate rank is **115** (10 Grade 6/8 fighters: $(6 - 1) \times 15 + 10 = 85$, plus facility uncap tiers up to 115).
* If `soul["rank"]` is manually overwritten with an arbitrary number out of sync with your fighter freezer roster, the TDM matchmaking and defense simulation state machine fails validation.

### TDM Rank Tier IDs
| Rank Tier | Internal Save ID | Required Points |
| :--- | :--- | :--- |
| **Bronze III - I** | `TDM_RANK_01_01` to `TDM_RANK_01_03` | 0 - 999 |
| **Silver III - I** | `TDM_RANK_02_01` to `TDM_RANK_02_03` | 1,000 - 1,499 |
| **Gold III - I** | `TDM_RANK_03_01` to `TDM_RANK_03_03` | 1,500 - 1,999 |
| **Platinum III - I** | `TDM_RANK_04_01` to `TDM_RANK_04_03` | 2,000 - 2,999 |
| **Diamond III** | `TDM_RANK_05_01` | 3,000 - 3,199 |
| **Diamond II** | `TDM_RANK_05_02` | 3,200 - 3,499 |
| **Diamond I (Top Tier)** | `TDM_RANK_05_03` | 3,500+ |

---

## 5. TDM Mystery Bags Architecture (mysterybag vs deathbox)

### Save File Paths
* `save_json["soul"]["mysterybag"]` -> Internal dictionary indexed by tier rarity storing generator IDs (`cntgen`).
* `save_json["soul"]["deathbox"]` -> **The actual physical in-game delivery container** (List of Objects) displayed at Uncle Death's Reward Box in the Waiting Room.

### Technical Discovery & Online-Only Architecture
In the original online live-service game, both the Reward Box (`soul.present` / `soul.deathbox`) and TDM Mystery Bags (`soul.mysterybag`) were backed by live GungHo server HTTP endpoints (`BrgNetworkResponsePresents`, `Receivedeathbox`).

In offline play, because no remote game server is running to answer these network queries, the physical terminal on the Waiting Room wall always reports as empty, and seasonal mystery bag rolls cannot be executed by the game engine. Consequently, **these non-functional controls were cleanly retired from the Save Editor UI** in favor of direct, verified offline modifications (injecting materials directly into the Coin Locker, decals into skill lists, and currencies directly into player balances).

### Deathbox Item Schema
```json
{
  "bid": "",
  "rarity": "RAINBOW",
  "type": "LOSTBAG",
  "created": 1788438689,
  "opentime": 1788438679,
  "num": 1,
  "val0": "RAINBOW",
  "val1": "",
  "val2": "",
  "val3": ""
}
```

### Critical Field: Instant Opening (`opentime`)
* If `opentime` is set to a future timestamp, the game places a lock timer on the package (e.g., 2 hours, 6 hours, 24 hours).
* By setting `opentime = current_timestamp - 10` (in the past), the package is marked as **immediately unlocked**, allowing the player to open and claim it instantly without any countdown.

### Valid In-Game Reward Types (Verified via `masters.db` `master_reward`)
| Type Code | Meaning | `val0` Value | `num` Value |
| :--- | :--- | :--- | :--- |
| `"LOSTBAG"` | TDM Mystery Bag | Rarity (`"RAINBOW"`, `"PLATINUM"`, `"GOLD"`, `"SILVER"`, `"COPPER"`) | `1` per entry |
| `"MONEY"` | Kill Coins | `""` (empty) | Exact Coin amount (e.g. `1000000`) |
| `"SPIRIT"` | SPLithium | `""` (empty) | Exact SPL amount (e.g. `1000000`) |
| `"MUSHROOM"` | Mushroom | Mushroom ID (e.g. `"MSR_043"` Golden Lifeshroom) | Quantity (or `0` for single) |
| `"BEAST"` | Creature / Beast | Beast ID (e.g. `"BST_GCASSOWARY"` Golden Bird) | Quantity |
| `"ITEM"` | R&D Material | Material ID (e.g. `"ITMT_WOOD_2"`, `"ITMT_ALUMI_8"`) | Quantity |
| `"SKILL"` | Skill Decal | Decal ID (e.g. `"SKL_ATKUP_NODMG_P"`) | `1` |
| `"PTTP_ARM"` | Weapon / Blueprint | Weapon ID (e.g. `"PT_ARM_WP011_001"`) | `1` |
| `"PTTP_BODY"` | Chest Armor piece | Armor ID (e.g. `"PT_REC_TOPS_001"`) | `1` |
| `"PTTP_HEAD"` | Helmet piece | Headgear ID (e.g. `"PT_REC_HEAD_001"`) | `1` |
| `"PTTP_LEGS"` | Pants / Leggings | Legwear ID (e.g. `"PT_REC_BTM_001"`) | `1` |
| `"1VIP"` / `"VIP"` | Express Pass | `""` (empty) | Pass count (`1` to `5`) |

### Auto-Migration
The Save Editor automatically runs `sync_mystery_bags_to_deathbox(save_json)` upon loading any save file, migrating all uncollected mystery bags from `soul.mysterybag` into `soul.deathbox` so they immediately appear in the Waiting Room.

---

## 6. Waiting Room Facilities (Level 99) & Player Rank Architecture

### 1. KC Bank & SPLithium Tank Expansion (`soul.safe_level` & `soul.spirit_tank_level`)
* In the official game database tables `master_safe_level` and `master_spirit_tank_level`, facility upgrades scale strictly from **Level 1 to Level 99** (99 rows total).
* **CRITICAL BUG PREVENTION**: Setting `safe_level = 100` causes an out-of-bounds database query in the game's C++ engine, reading uninitialized memory. This corrupts the bank limit to a negative value (**-1,696,979,938**) and the SPL tank limit to **1,763,844,543**. Because the bank limit becomes negative, any in-game transaction or reward collection immediately resets current coins to **0**.
* Setting `safe_level = 99` and `spirit_tank_level = 99` expands capacity to the official maximum of **2,560,000** Kill Coins and SPLithium with 100% stability.
* The Save Editor enforces Level 1-99 boundaries and automatically heals any saves corrupted by prior versions.

### 2. Player Rank Progression & Mathematical Synchronization (`soul.rank` & `soul.rank_point`)
* In *LET IT DIE*, **Player Rank** is the primary account level displayed on the player profile and in Tokyo Death Metro (TDM).
* The game database table `master_rank_point` indexes **130 distinct ranks** and their cumulative point requirements:
  | Player Rank | Minimum Rank Points | Notes / Milestones |
  | :---: | :---: | :--- |
  | **Rank 1** | 0 | Starting account baseline |
  | **Rank 10** | 1,000 | Early tower climbing |
  | **Rank 50** | 650,000 | Mid-game (Candle Wolf / M.I.L.K.) |
  | **Rank 61** | 1,400,000 | Grade 5 Fighter unlock |
  | **Rank 80** | 75,000,000 | Grade 6 Fighter unlock |
  | **Rank 100** | **1,600,000,000** | Endgame milestone |
  | **Rank 122** | 36,000,000,000 | Grade 6 Tier 8 / Uncapped progression |
  | **Rank 130** | **180,000,000,000** | Maximum engine cap |
* **Automatic Synchronization Requirement**: Simply changing `soul["rank"]` without updating `soul["rank_point"]` creates a desynchronization in the engine. Upon earning TDM points, the client would attempt to recalculate or glitch the rank. The Save Editor includes the complete 130-entry mathematical table, ensuring that setting any Player Rank automatically synchronizes the exact official rank points required.

---

## 7. Tower of Barbs Map Architecture, Elevators & Escalator Gate Network

### 1. Complete Tower Discovery: 980 Rooms (`soul.areaflag`)
* Across Floors 1 through 50+, the Tower of Barbs contains **980 room nodes** indexed by `idx` (0 to 979), referencing `master_area_connect_node`.
* The `val` field is an integer bitmask governing room discovery, elevator access, and gate status:
  * `Bit 0 (0x01 = 1)`: Room visited / discovered on player map.
  * `Bit 4 (0x10 = 16)`: Don Boss arena flag (Floors 10, 20, 30, 40).
  * `Bit 5 (0x20 = 32)`: Elevator hub / station unlocked.
  * `Bit 1 (0x02 = 2)`: Midboss encounter flag (Jin-Die, Coen, Goto-9).
  * **Standard Clean Room State**: `val = 33` (`0x21` = 1 + 32). Fully reveals the room on the map and enables elevator warping.
  * **Don Boss Rooms**: `val = 49` (`0x31` = 33 + 16 for Max, Jackson, Crowley, and Taro).
  * **Midboss Rooms**: `val = 51` (`0x33` = 33 + 18).

### 2. The Red Padlock Bitmask (`0x40 = 64`) & Padlock Purge
* **The Problem**: Rooms visited by a player before completing specific boss fights or activating shortcut levers receive **Bit 6 (0x40 = 64)** in `soul.areaflag` (e.g. `val = 65` or `val = 97`).
* Even if all elevators are enabled, the game client reads `val & 0x40` and renders **RED PADLOCKS** over connecting escalators on the map screen (such as Haratsuka, Futagi, Ebata, and Mitsuba).
* **The Solution**: The Save Editor systematically purges Bit 6 from all rooms (`clean_val = cur_val & ~64`), resetting all locked rooms to `val = 33`. This permanently eliminates every red padlock from the map.

### 3. Escalator Connections: 1,119 Paths (`soul.areaescflag`)
* Connecting pathways between rooms are stored in `soul.areaescflag` (1,119 entries from `master_area_connect_escalator`).
* Setting `val = 7` draws complete connecting escalator lines across all floors without fog of war.

### 4. 193 Progression Keys, Gates, Valves, and Boss Flags (`save["gameflg"]["cl"]`)
* Each locked escalator in `master_area_connect_escalator` has two prerequisite columns:
  * `key`: Mini-boss defeat requirement flag (e.g., `KGF_RFT_FIXED_AREA_BOSS_0001` through `0006`).
  * `gate`: Lever / valve / button activation flag (e.g., `KGF_RFT_FIXED_AREA_BUTTON_0001` through `0010`).
* The Save Editor injects all **193 verified gate, key, button, and boss flags** as `1`, permanently unlocking every shortcut gate, valve, and escalator door in the game.

### 5. Waiting Room Gates: Floors 41-50 (Hazama) & Tengoku (51+)
* `KGF_GAME_CLEAR = 1`: Marks the main 40-floor campaign as completed.
* `KGF_HZM_FIRST_TIME_ENTRANCE_GATE = 1`: Opens the iron gate in the Waiting Room, allowing free access to Floors 41-50 (Hazama) and the elevator to Tengoku (51+).

### 6. All 61 Official Elevator Stations (`soul.openelvflr`)
* The complete network of 61 elevator stations is registered in `soul.openelvflr`, covering both Main and Sub lines:
  * `ELV_MAIN_01` through `ELV_MAIN_50`
  * `ELV_SUB_A01_...` through `ELV_SUB_D02_...`
  * Unlocks immediate warping without requiring the player to manually discover or fund individual elevator terminals.

---

## 8. Uncle Death Compendiums (msrbook and bstbook)

* `save_json["soul"]["msrbook"]` -> Catalog of 63 discovered, eaten, thrown, and cooked mushrooms.
* `save_json["soul"]["bstbook"]` -> Catalog of 24 beasts (frogs, lizards, scorpions, snails, birds).

### Compendium Entry Schema
```json
{
  "msrid": "MSR_001",
  "is_found": 1,
  "is_eaten": 1,
  "is_thrown": 1,
  "is_cooked": 1,
  "is_checked": 1
}
```

---

## 9. Waiting Room Customization and Skins (hubcustom and armorskin)

### Save File Paths
* `save_json["soul"]["hubcustom"]` -> 113 visual customizations for the Waiting Room (`cstmid` and `flg`: 0=locked, 1=unlocked, 2/6=equipped).
* `save_json["soul"]["armorskin"]` -> Cosmetic armor skins applied over equipped gear.
* `save_json["soul"]["last_visiting_shop_time"]` -> Timestamp of last Gyaku-Funsha wandering shop visit (setting to 0 resets the 1-hour shop cooldown).

---

## 10. Fighter Engine Architecture (bodyuser and chr)

The game engine separates fighter state across two complementary structures:

### 1. Attribute Allocations & Death 'Roids: `save["bodyuser"][uid]`
In `bodyuser`, values represent level allocation points (range 1 to 45 per stat), not direct raw combat hitpoints:
* `lvl`: Total level (at Tier 8 / G6 Uncapped max: **247**, calculated as sum of allocations minus 5).
* `hp`, `str`, `dex`, `vit`, `stm`, `luk`: Base level points (maximum: **45** each).
* `hp_bonus`, `str_bonus`, `dex_bonus`, `vit_bonus`, `stm_bonus`, `luk_bonus`: Death 'Roid uncap bonuses (maximum: **20** each).
* `skill`: Additional decal slots. **For Grade 6 Limit Break 4, this MUST be `0`!** Limit Break 4 dynamically grants the 4 extra decal slots (reaching the maximum 8 or 9 slots). If set $\ge 1$, Mingo Head displays a slot desync (`45/30` or `8/6`) and freezes during uncap interactions.
* `bag`: Extra Death Bag slots from freezer level-up (0-3 for Grades 1-5). **For Grade 6 Limit Break 4, this MUST be `0`!** Total bag capacity (up to 54 slots) is dynamically computed by the engine from `limit_break: 4` and `master_body_detail`.
* `rage`: Extra Rage gauge bars. **This MUST ALWAYS be `0` across all fighters!** If `rage != 0`, the engine attempts to lot rage status from `master_bodylvl_status_value`, which contains no rows for Grade 6, causing rage gauge initialization to abort and freezing the fighter in combat.

### 2. Live Combat State: `save["soul"]["chr"]["chrs"][uid]`
In `chr.chrs`, the actual in-game runtime state is stored:
* `cid`: Unique UUID string identifying this fighter instance.
* `name`: Fighter display name.
* `type`: Engine class archetype code (`"BAL"` All-Rounder, `"BRE"` Striker, `"DEF"` Defender, `"TEC"` Attacker, `"SHT"` Shooter, `"COL"` Collector, `"SKI"` Skill Master, `"LUK"` Lucky Star).
* `grade`: Base grade (**1 to 6**; internal maximum is **6**).
* `limit_break`: Uncap stage (**0 to 4**; Grade 6 with Limit Break 4 represents **Tier 8 / G8** in the community).
* `lvl`: Must match `bodyuser.lvl` (**247** for maxed G6). Missing `lvl` causes desynchronization between fighter sheet and combat loadout.
* `hp`: Authentic canonical combat health pool determined by class (e.g., **32,600** HP for Collector, **26,670** for All-Rounder/Striker, etc.). Arbitrary values like `20,000` are non-canonical and get normalized by `sanitize_fighters`.
* `select_arm_slots`: **Must strictly be `"0,0"`**. Setting this to `"1,2"` causes out-of-bounds arm slot lookups when the fighter has fewer than 2 weapons equipped, crashing the game on spawn.
* `state`: Fighter state (`"GUARD"` in freezer, `"USE"` for currently active fighter in the Waiting Room).
* `body` & `gasmask`: Authentic model asset IDs (`"BODY_FEMALE_001"` to `"008"`, `"BODY_MALE_001"` to `"008"`, paired with `"ASSET_NF_GAS_HEAD_..."` or `"ASSET_NM_GAS_HEAD_..."`).
* `escdie`: Rescue flag (0 = alive and ready).
* `hunter_win`, `hunter_lose`, `hunter_draw`: Must be `-1` for initialized fighters.

### 3. Fighter Creation From Scratch (From 0) Rules & Safeguards
When creating a brand new fighter from 0 (`create_new_fighter`) or cloning (`clone_fighter`), the following structures are automatically guaranteed:
1. **Deathbag Initialization**: `soul["deathbag"][uid][cid]` is initialized as an empty list `[]`. If missing, opening the inventory or entering a raid simulation crashes immediately.
2. **10-Slot Freezer Access**: `sync_fighter_slots(save)` synchronizes `soul["chr"]["slots"]` to allow full access to all 10 freezer slots.
3. **Tutorial Bypass**: `_ensure_freezer_accessible(save)` automatically completes the Kiwako Seto tutorial flags if the save is fresh, preventing the Waiting Room freezer lockout.
4. **Automatic TDM & Rank Re-alignment**: Every fighter modification triggers `repair_and_sanitize_tdm(save)`, which recalculates the exact player rank, aligns `soul["team_id"]` (string), `soul["favorite_team"]` (string), `teammember["tid"]` (int), and normalizes `fortorder` into contiguous wave indices.

---

## 11. Equipment Modifiers: Durability and Ammunition

### Save File Paths
* `save["part"]["pts"][uid]` -> Storage locker equipment inventory.
* `save["soul"]["deathbag"][fighter_uid]` -> Items inside fighter bags.

### Equipment Item Schema
```json
{
  "uid": 443455,
  "eid": "008827cc-5c3a-4028-83ad-269d66d35018",
  "ptid": "PT_ARM_WP064_001",
  "grade": 0,
  "lvl": 19,
  "dur": 999999,
  "rest": 9999,
  "spare": 9999
}
```
* `dur`: Weapon/armor durability. Setting to `999,999` makes the item virtually unbreakable.
* `rest`: Loaded chamber ammunition. Setting to `9,999` bypasses standard reload cycles during extended fights.
* `spare`: Total ammunition reserve.
* `lvl`: Reinforcement stage (+19 corresponds to the Tengoku Uncapped limit).

---

## 12. Endgame Meta Decal Loadouts (8 Slots)

Tested high-performance competitive loadouts:

1. **Tengoku God Climber (Floors 51F to 350F+)**:
   * `SKL_FIGHTER_STUP_01_P` (Ultimate Fighter)
   * `SKL_ATKUP_NODMG_P` (Serial Killer)
   * `SKL_ATKUP_03_P` (Golden Gym)
   * `SKL_DRAIN_01_P` (Vampire)
   * `SKL_HPUP_03_P` (Super Heavy Tank)
   * `SKL_ARRNG_STATUP_ALL_P` (Professional Cosplayer)
   * `SKL_STRENGTHEN_BODY_01_P` (Joker)
   * `SKL_HEADSHOTUP_P` (One Shot One Kill)

2. **KAMAS God Shooter**:
   * `SKL_HEADSHOTUP_P`, `SKL_ATKUP_NODMG_P`, `SKL_FIGHTER_STUP_01_P`, `SKL_ATKUP_03_P`, `SKL_WEP_SPDUP_P`, `SKL_CRIUP_02_P`, `SKL_DRAIN_01_P`, `SKL_SEARCHUP_ITEM_P`.

3. **Melee Striker (Flail / Machete / Katana)**:
   * `SKL_FIGHTER_STUP_01_P`, `SKL_ATKUP_03_P`, `SKL_ATKUP_NODMG_P`, `SKL_DRAIN_01_P`, `SKL_HPUP_02_P`, `SKL_DEFUP_02_P`, `SKL_STRENGTHEN_BODY_01_P`, `SKL_RGSPDUP_02_P`.

4. **TDM Defensive Wall**:
   * `SKL_HPUP_03_P`, `SKL_HPUP_02_P`, `SKL_DEFUP_02_P`, `SKL_SNOWWHITE_P`, `SKL_STRENGTHEN_BODY_01_P`, `SKL_ATKDEFUP_HPLOW_01_P`, `SKL_FIGHTER_STUP_01_P`, `SKL_ATKUP_CRIUP_DEFDWN_P`.

---

## 13. Endgame Equipment Sets (44CE Forcemen, Jackals, Tengoku)

Direct injection IDs for top-tier gear:

* **White Steel (44CE D.O.D.)**: `PT_ARM_WP055_001` (Static Massager), `PT_ARM_WP002_001` (Spike Bat), `PT_DIY_HEAD_4F_01`, `PT_DIY_TOPS_4F_01`, `PT_DIY_BTM_4F_01`.
* **Red Napalm (44CE WAR ENSEMBLE)**: `PT_ARM_WP056_001` (M2G-87 Spike Launcher), `PT_MIL_HEAD_4F_01`, `PT_MIL_TOPS_4F_01`, `PT_MIL_BTM_4F_01`.
* **Black Thunder (44CE CANDLE WOLF)**: `PT_ARM_WP057_001` (Energy Sword), `PT_FAN_HEAD_4F_01`, `PT_FAN_TOPS_4F_01`, `PT_FAN_BTM_4F_01`.
* **Pale Wind (44CE M.I.L.K.)**: `PT_ARM_WP058_001` (Force Wand), `PT_SPO_HEAD_4F_01`, `PT_SPO_TOPS_4F_01`, `PT_SPO_BTM_4F_01`.
* **Jackals Gear (v1 / v2 / v3)**: Jackal Sword X (`PT_ARM_WP001_JAC_11`), Jackal Blaster Y (`PT_ARM_WP016_JAC_11`), Jackal Yo-Yo Z (`PT_ARM_WP027_JAC_11`), with complete armor suites for Jackal X, Y, and Z.
* **Tengoku Legendary Weapons**: Muspelheim (`PT_ARM_WP060_001`), Judgement Day (`PT_ARM_WP061_001`), Predator (`PT_ARM_WP062_001`), Emperor (`PT_ARM_WP063_001`), Lethal Weapon (`PT_ARM_WP064_001`).

---

## 14. Official Quest Auto-Completion (soul.quest)

### Save File Path
* `save["soul"]["quest"]["user"]` -> List of entries `{"qid": quest_id, "ordcnt": 1, "clrcnt": 1}`.
Setting `clrcnt = 1` marks the corresponding quest as completed in `master_quest` (defeating specific screamers, climbing without armor, etc.) and deposits Death Metals and rewards directly into the Mailbox.

---

## 15. Yotsuyama Magazines and Jukebox Channels

### Save File Paths
* `save["soul"]["magazine"]["status_list"]` -> Comma-separated string of 36 status flags. A value of `2` indicates the magazine issue has been read and unlocked in the Waiting Room compendium.
* `save["soul"]["radio"]` -> Audio channel flags unlocking all licensed Japanese rock and metal tracks in the Waiting Room radio.

---

---

## 16. Automated Rolling Backup System

* File pattern: `<save_name>.sav.YYYYMMDD_HHMMSS.bak`.
* Rolling retention policy: preserves the 10 most recent backups and discards older ones.
* Direct restore available through the Advanced tab in the GUI or via manual file replacement.

---

## 17. Equipment Evolution & Uncapping Hierarchy (+4 vs +19/+24)

### 1. In-Game R&D Rules & Blueprints (`save["part"]["research"]`)
In *LET IT DIE*, the crafting progression at Chokufunsha obeys strict tier and uncapping rules:
* **Base & Intermediate Tiers (Tier 1 to Tier 3)**:
  * Maximum upgrade level is strictly **+4**.
  * Reaching +4 completes the blueprint (`research_type: "FINISHED"`) and unlocks the purchase of that tier at the shop, while simultaneously unlocking the development of the **next tier blueprint** (e.g. *Pork Chopper* -> *Pork Chopper+*).
* **Final Tiers (Tier 4 / Uncapped / 44CE / Tengoku)**:
  * Reaching Tier 4 +4 triggers **Uncapping** (Limit Break).
  * Standard Uncapped weapons and armors can be enhanced up to **+19**, multiplying durability and ammo reserves.
  * Extended weapons (such as Tengoku legendary weapons: *Muspelheim*, *Predator*, *Lethal Weapon*, etc.) can be enhanced up to **+24**.

### 2. Save File Blueprint Representation
In `save["part"]["research"][uid]`:
```json
{
  "ptid": "PT_ARM_WP001_001",
  "research_type": "FINISHED",
  "lvl": 5,
  "start_time": 0,
  "comp_time": 0
}
```
* `lvl`: Enhancement level counter (`1` = base +0; `5` = +4; `20` = +19; `25` = +24).
* The Save Editor features a smart evolution engine that automatically identifies whether an item is intermediate (capping safely at +4 to promote the next tier recipe) or final (permitting full +19 / +24 uncapping).

---

## 18. Windows Administrative Auto-Elevation (UAC Architecture)

Because Steam installs games to protected directories (e.g. `C:\Program Files (x86)\Steam\...`) and saves can be locked by active system handles or cloud synchronization services, running without sufficient privileges can result in `PermissionError` when writing save files or modifying `masters.db`.

To resolve this seamlessly for all end-users:
* The standalone `.exe` is compiled with the `--uac-admin` manifest flag.
* Windows automatically prompts the user with the standard User Account Control (UAC) dialog upon launch, granting full administrative privileges and preventing save writing interruptions.

---

## 19. Royal Express VIP Pass Validation & The Friendship Bug Fix (`soul.vip`)

### Save File Path
* `save["soul"]["vip"]`: Dictionary managing the player's active Royal Express subscription, express passes, and elevator attendant friendship.

### Structure of `soul.vip`
```json
{
  "flag": 1,
  "type": 0,
  "pass_num": 99,
  "oneday_pass_num": 99,
  "expired_time": 1791063593,
  "automatic_renewal": 0,
  "friendship": 1,
  "last_use_day": 1788474564,
  "sequence": 1,
  "rest_week_flag": 0
}
```

### The "Infinite Elevator Cutscene / Loading Hang" Root Cause
A notorious bug in save modification was an infinite loading hang occurring when entering or riding the Royal Express elevator. Reverse engineering and community testing (discovered by [Stephengw3](https://github.com/Stephengw3) on Reddit) revealed the exact root cause:
1. **The Elevator Attendant Voice & Animation Dispatch**: When riding the Royal Express elevator, the attendant (`Rin`) plays a greeting cutscene with localized voice lines and animations based on the player's `"friendship"` level.
2. **Missing Asset Request (`friendship: 100`)**: If `"friendship"` is set to `100` (or any arbitrary value above legitimate game bounds), the Unreal Engine animation loader attempts to load animation/voice clips corresponding to friendship level 100. Because no such asset exists in the game data, the engine stalls indefinitely waiting for the asset streaming callback, freezing the elevator loading screen.
3. **The Solution (`friendship: 1`)**: Setting `"friendship": 1` points to an existing, valid greeting animation and voice clip, allowing the elevator sequence to play instantly and transition seamlessly to the next floor.

### Expiration Timestamp Rules
* **Safe Maximum Duration**: Up to 99 days, 23 hours, and 59 minutes (~100 days).
* Exceeding ~100 days causes the timestamp validation to mark the pass as invalid without resetting it.
* **Recommended Setting**: 30 to 90 days active, accompanied by 99 reserve passes (`pass_num: 99`, `oneday_pass_num: 99`) stored in the inventory.
* **Automated Auto-Healing**: The editor automatically audits `soul.vip.friendship` on load/save and heals any value `> 1` back to `1`.

---

## 20. Balanced ZLIB Multi-Chunk Compressor (`save_io.py`)

### Problem with Standard / Single-Chunk ZLIB Writing
Standard ZLIB compression scripts often compress the entire JSON payload into a single massive chunk or arbitrary 64KB blocks. However, *LET IT DIE*'s native engine utilizes a streaming memory-chunked decompressor designed to process save data across discrete, balanced decompression buffers. Writing imbalanced or malformed chunks can cause the game to crash or stall during the initial "Checking Save Data" phase.

### Balanced 4-Chunk Engine Specification
The editor implements the exact 4-chunk balanced streaming structure utilized by native client saves:
```python
def _balanced_sizes(total: int, count: int = 4) -> list[int]:
    base, remainder = divmod(total, count)
    return [base + (1 if i < remainder else 0) for i in range(count)]
```

### Binary Layout:
1. **Header (16 bytes)**:
   * `0x00 - 0x03`: Magic signature `BRG\0` (`0x42 0x52 0x47 0x00`).
   * `0x04 - 0x07`: Save version uint32 (typically `2`).
   * `0x08 - 0x0B`: Total uncompressed JSON byte length (uint32 LE).
   * `0x0C - 0x0F`: Compression algorithm identifier `ZLIB`.
2. **4 Balanced Data Chunks**:
   * `uncompressed_size` (uint32 LE, 4 bytes).
   * `compressed_size` (uint32 LE, 4 bytes).
   * `compressed_payload` (zlib raw stream, compressed_size bytes).
3. **EOF Trailer**:
   * `0x00000000` (uint32 0, 4 bytes marking end of stream).
4. **JSON Serialization Rules**:
   * UTF-8 encoded with `ensure_ascii=False`.
   * Strict compact separators `(',', ':')` without trailing whitespace.

---

## 21. Chokufunsha R&D Mode vs Shop Max for +19 Uncapped Equipment (`soul.partresearch.user`)

### The Challenge with Uncapped Blueprints
Players frequently want their equipment at maximum uncapped potential (+19), but in two very different ways:
* **Option A ("Shop Max")**: Ready to buy fully completed at +19 from Chokufunsha Shop.
* **Option B ("R&D Active / De Fábrica")**: Available to buy at +18 ("de fábrica el máximo"), while the final upgrade to +19 is actively waiting in the Chokufunsha R&D counter so the player can experience researching it themselves with their own materials.

### Save Schema Representation in `soul.partresearch.user`
* **Intermediate Levels (1 to 18)**:
  `{"ptid": "PT_ARM_WP003_005", "lvl": L, "research_type": "FINISHED", "receive_type": "FINISHED"}`
* **R&D Active Mode (+18 in Shop, +19 in R&D)**:
  Level 19 has:
  `{"ptid": "PT_ARM_WP003_005", "lvl": 19, "research_type": "FINISHED", "receive_type": "CHARGE"}`
  Level 20 is intentionally omitted.
  * In-game behavior: The shop sells the item at Level 19 (+18). The R&D development menu presents the active recipe to forge Level 20 (+19).
* **Shop Max Mode (+19 Completed, reflvllmt = 20)**:
  Level 20 has:
  `{"ptid": "PT_ARM_WP003_005", "lvl": 20, "research_type": "FINISHED", "receive_type": "CHARGE", "is_checked": 3}`
  * In-game behavior: The shop sells the item at Level 20 (+19). The R&D menu shows the item as 100% completed with zero pending material requirements.

### The `reflvllmt = 20` Engine Cap vs The Level 15 Anti-Pattern
In `masters.db` table `master_part`, all 301 limitbreak pieces (`is_limitbreak = 5` and `_G`) specify `reflvllmt = 20`.
* **The Level 15 Anti-Pattern**: Setting raw `lvl: 15` in the save was an erroneous attempt based on the fact that `15 + 4 = 19`. However, the engine evaluates research progress as `lvl / reflvllmt` (`15 / 20`). This caused the engine to display the item as an unfinished mid-tier upgrade (e.g. displaying material requirements like `50 / 1700`) rather than a completed store product.
* **The Level 20 Authentic Solution**: Setting `lvl: 20` with `receive_type: "CHARGE"` and `is_checked: 3` satisfies `lvl == reflvllmt`, marking the uncap research as 100% completed in Komoi's Chokufunsha Shop.

### Bulk Uncap Processing Architecture
The bulk uncap feature (`⚡ Mejorar Todo a Nivel +19`) iterates across all **377+ authentic uncapped weapons and armors**:
1. Uses pre-cached SQLite parent mapping from `master_part` (`nextptid` relationships) to resolve ancestors in constant time (`O(1)`).
2. Guarantees prerequisite ancestor tiers (e.g. Tier 1, Tier 2, Tier 3, Tier 4 Base) are safely registered at Level 5 (+4 `CHARGE`) so the game's evolution prerequisite checks succeed.
3. Places the final uncapped tier at Level 20 `CHARGE` (or Level 19 `CHARGE` in R&D mode), instantly populating the entire Chokufunsha catalog without skipping game logic.

---

## 22. Emergency Waiting Room Fighter Rescue (`soul.chr.chrs`)

### Mechanics
When fighters become stuck in elevator loading states, frozen in mid-tower transitions, or trapped in invalid room coordinates:
1. The editor targets the active fighter in `soul.chr.chrs[uid]`.
2. Resets:
   * `"floor": 0` (Waiting Room ground floor).
   * `"scene": "HUB_MAIN"` (Central Waiting Room scene).
   * `"state": "WAITING_ROOM"` (Normal standing idle state).
   * Restores full HP and stamina without triggering death or loss of equipped items/deathbag.

---

## 23. Full Tower Map Discovery, Escalator Pathways & Gates (`soul.areaflag`, `soul.areaescflag`, `gameflg.cl`)

### Tower Map Exploration Schema
The Tower of Barbs map discovery is divided across three interconnected data structures in the save file:

#### 1. Room Exploration (`soul.areaflag`)
* **List Path**: `save_json["soul"]["areaflag"]`
* **Entry Schema**: `{"idx": <int>, "val": <int>}`
* **Coverage**: Exactly 980 room indices spanning Districts 1 through 4 (AMS, ARC, MET, RFT), Hazama (41-50), and Tengoku (51+).
* **Exploration State (`val`)**:
  - `val = 33` (`0x21`): Indicates that the room has been fully discovered, mapped, and visited by the player.
  - **The Red Padlock Bitmask (`0x40` / bit 64)**:
    When a player approaches a room from a locked gate direction or discovers a room with a one-way entrance, the game applies a bitwise flag `val |= 64` (resulting in values like `97`). This places a red padlock icon on the map room node.
    The editor cleanses this bitmask using:
    ```python
    clean_val = cur_val & ~64
    existing_rooms[r_idx]["val"] = max(clean_val, 33)
    ```
    This completely eliminates all padlocks and reveals the entire tower topology cleanly.

#### 2. Escalator Connections (`soul.areaescflag`)
* **List Path**: `save_json["soul"]["areaescflag"]`
* **Entry Schema**: `{"idx": <int>, "val": <int>}`
* **Coverage**: 1,119 unique escalator indices connecting adjacent tower chambers.
* **State Value**: `val = 7` marks the escalator path as traversed and visible in both upward and downward transit routes.

#### 3. Tower Physical Gates (`gameflg.cl`)
* **List Path**: `save_json["gameflg"]["cl"]`
* **Total Official Gate Flags**: 122 `RELEASE_GATE_...` flags.
* **Mechanism**:
  Physical gates, valves, and mini-boss security doors are controlled by client flags in `cl`:
  ```json
  {"var": "RELEASE_GATE_AMS_AREA_001_A01", "value": 1, "modified": 1788365507}
  ```
  Activating all 122 flags permanently unlocks all one-way gates and bypasses throughout the Tower, preventing players from being locked behind one-way access doors.

#### 4. High-Tower Progression & Tengoku Bypass Flags
In addition to physical gates, `gameflg.cl` stores 17 critical narrative progression keys:
* `KGF_GAME_CLEAR`: Floor 40 Taro Gunkanyama defeat flag.
* `KGF_HZM_FIRST_TIME`, `KGF_HZM_FIRST_TIME_ENTRANCE_GATE`, `KGF_HZM_FIRST_TIME_HAZAMA_RULE`: Unlocks the Waiting Room gate to Floors 41-50 Battle Royale (Hazama) without requiring Floor 40 re-clearing.
* `KGF_HVN_GOTO_NEO`, `KGF_HVN_ROUTE_NEO0`, `KGF_HVN_ROUTE_NEO1`: Unlocks direct elevator access to Floor 51+ Tengoku and specialized NEO areas (D.O.D., War Ensemble, Candle Wolf, M.I.L.K.).
* `save_json["playlog"]["base"]["max_floor"] = 51`: Automatically updates the player's lifetime highest reached floor, satisfying fast-travel level gates.

---

## 24. Tutorial Progression, Fresh Save Recovery & Waiting Room Facility Flags (`gameflg.sv`, `gameflg.cl`)

### The "Fresh Save" Facility Lockout Problem
When a player starts a new playthrough from zero, the save file initializes in an uncompleted tutorial state:
1. `gameflg.sv` has `KGF_TUTORIAL_PROGRESS` set to `0` or intermediate values (`< 100`).
2. `gameflg.cl` lacks the critical receptionist interaction flag: `KGF_FIRST_KIWAKOROOM`.
3. In this state, the game client's scripting engine restricts access to the **Fighter Freezer**: Kiwako Seto will not open the freezer interface, repeating introductory dialogue or displaying facility lock messages.
4. Additional facilities remain disabled: Chokufunsha (`KGF_FIRST_SHOP_BASE`), Mushroom Club (`KGF_FIRST_KINOKOYA`), Naomi Detox Quest Counter (`KGF_FIRST_NAOMI`), and the Direct Hell VIP Elevator (`KGF_FIRST_VIP_ELEVATORGIRL`).
5. Modifying or duplicating fighters on a fresh save while in this state trapped new fighters in an inaccessible freezer, while unlocking the Tower map created a game state desync where the tower was open but the base was still in prologue mode.

### Complete Tutorial & Facility Flag Specification

#### Server-Side Progression (`gameflg.sv`)
```json
[
  {"var": "KGF_TUTORIAL_PROGRESS", "value": 100, "modified": 1788365507},
  {"var": "DELETE_NO_USER_DEATH_BAG_DATA", "value": 1, "modified": 1788365507},
  {"var": "SGF_PRESENT_FORMAT", "value": 1, "modified": 1788365507},
  {"var": "SGF_DEATHBOX_COPPER_FIRST", "value": 1, "modified": 1788365507},
  {"var": "SGF_DEATHBOX_SILVER_FIRST", "value": 1, "modified": 1788365507},
  {"var": "SGF_DEATHBOX_GOLD_FIRST", "value": 1, "modified": 1788365507}
]
```
Setting `KGF_TUTORIAL_PROGRESS` to `100` signals to the game engine that all prologue quests with Uncle Death have been fulfilled.

#### Client Facility Unlocks (`gameflg.cl`)
| Flag Identifier | Value | Effect / Unlocks |
| :--- | :---: | :--- |
| `KGF_FIRST_KIWAKOROOM` | `1` | **Fighter Freezer (Kiwako Seto)** - Opens freezer UI and character management. |
| `KGF_FIRST_BASE` | `1` | **Waiting Room Ground State** - Marks initial arrival cutscene as completed. |
| `KGF_FIRST_SHOP_BASE` | `1` | **Chokufunsha** - Unlocks weapons, armors, and R&D crafting in base. |
| `KGF_FIRST_KINOKOYA` | `1` | **Mushroom Club (Momoko Yamada)** - Unlocks decal stew and skill decals. |
| `KGF_FIRST_NAOMI` | `1` | **Hater Quests (Naomi Detox)** - Unlocks the official mission counter. |
| `KGF_FIRST_VIP_ELEVATORGIRL` | `1` | **Direct Hell VIP Elevator** - Unlocks direct elevator cabin travel. |
| `KGF_FIRST_MEIJIN` | `1` | Clears Meijin introductory tutorial dialogue. |
| `KGF_FIRST_MEIJIN_FINISH` | `1` | Clears Meijin advanced tips sequence. |
| `KGF_FIRST_PLAY` | `1` | Marks first-time account initialization as cleared. |
| `KGF_MET_TUTORIAL_CLEAR` | `1` | Metro prologue tutorial dungeon cleared. |
| `KGF_TUTORIAL_COMP` | `1` | Master tutorial completion trigger. |
| `KGF_QUEST_UNLOCKED` | `1` | General quest system availability. |
| `KGF_RADIO_SELECT_ENABLE` | `1` | Waiting Room Radio Jukebox station tuning enabled. |
| `KGF_TUTORIAL_DEATHBAG_ENABLE` | `1` | Deathbag inventory enabled for exploration. |
| `KGF_TUTORIAL_DHSERVICE_ENABLE` | `1` | Direct Hell revive service enabled. |
| `KGF_TUTORIAL_DROPDEATHBAG_ENABLE` | `1` | Item dropping and salvage enabled. |
| `KGF_TUTORIAL_ENMATYOU_ENABLE` | `1` | Uncle Death Enmatyou guide entries enabled. |
| `KGF_TUTORIAL_RAGEMOVE_ENABLE` | `1` | Rage Move combat mechanics enabled. |
| `KGF_TUTORIAL_RETURN_TITLE_ENABLE` | `1` | In-game pause menu return to title screen enabled. |
| `KGF_FORT_FIRST_TUTORIAL_COMP` | `1` | Tokyo Death Metro (TDM) introduction part 1 completed. |
| `KGF_FORT_SECOND_TUTORIAL_COMP` | `1` | Tokyo Death Metro (TDM) introduction part 2 completed. |
| `KGF_TUTORIAL_BALLOON_01..40` | `1` | Dismisses all 37 pop-up tutorial hint balloons. |
| `KGF_TUTORIAL_ENMA_READ_01..40` | `1` | Marks all Uncle Death Enmatyou tips as read. |

#### Stage Coordinates and Dungeon Purge
To prevent a player from spawning into an active tutorial dungeon instance, the editor safely clears:
```python
soul["stgid"] = ""
soul["flrid"] = ""
soul["areaid"] = ""
soul["current_died_cid"] = ""
soul["die_flag"] = 0
soul["resurrection"] = 0
```
And resets `floor.rlg` and `floor.pop` through `reset_floor_to_waiting_room(save)`. This guarantees that upon launching the game, the player spawns standing safely in the center of the Waiting Room with all facilities active.

---

## 25. Fighter Freezer Architecture & 10-Slot Synchronization (`soul.chr.slots`, `bodyuser`, `soul.chr.chrs`)

### Three-Tier Character Storage Structure
LET IT DIE distributes fighter data across three distinct dictionary trees keyed by the player's unique User ID (`uid`):

```
Save Root
│
├── bodyuser[uid]            -> Level & Stat Allocation Points
│    ├── Fighter 0 (cid_a)
│    └── Fighter 1 (cid_b)
│
├── soul.chr.chrs[uid]       -> Visuals, Class & Live Combat State
│    ├── Fighter 0 (cid_a)
│    └── Fighter 1 (cid_b)
│
└── soul.chr.slots[uid]      -> The 10 Physical Freezer Slots (0 to 9)
     ├── Slot 0 -> cid_a
     ├── Slot 1 -> cid_b
     ├── Slot 2 -> "" (Empty)
     └── ...
```

#### 1. Attribute & Allocation Tier (`bodyuser[uid]`)
Contains stat allocation point distributions (1 to 45 points per stat):
* `hp`, `str`, `dex`, `vit`, `stm`, `luk`: Base level points (1-30 standard, up to 45 with limit breaks).
* `hp_bonus` .. `luk_bonus`: Death 'Roids bonuses (+20 each for Tier 8).
* `skill`: Decal slot expansion count (0 to 3, unlocking slots 6, 7, and 8).
* `bag`: MINGO pouch expansion (+1 to +3 slots).
* `rage`: Rage gauge expansion (+1).

#### 2. Visual & Live Combat State Tier (`soul.chr.chrs[uid]`)
* `body`: Model mesh ID (`BODY_FEMALE_001` through `BODY_FEMALE_008`, `BODY_MALE_001` through `BODY_MALE_008`).
* `gasmask`: Head gasmask asset (`ASSET_NF_GAS_HEAD_...` / `ASSET_NM_GAS_HEAD_...`).
* `type`: Class code (`BAL`, `ATK`, `DEF`, `STR`, `SHO`, `COL`, `SKI`, `LUK`).
* `grade`: Tier level (1 to 6).
* `limit_break`: Uncapping level (0 to 4).
* `state`: Live status:
  - `"GUARD"`: Stored safely in the Freezer / Waiting Room defense roster.
  - `"USE"`: Currently controlled by the player in the Waiting Room.
  - `"WAITING_ROOM"`: Idle in Waiting Room.
  - `"DEAD"`: Fallen in the Tower (generates roaming Hater if unrecovered).

#### 3. The 10 Freezer Slots (`soul.chr.slots[uid]`)
The Fighter Freezer consists of exactly 10 slots (indices `0` through `9`).
* Each slot entry contains:
  ```json
  {"uid": 443455, "slot": 0, "cid": "097b0757-4530-4c7b-9188-cf8a878e8765"}
  ```
* Occupied slots reference the fighter's UUID (`cid`).
* Empty slots MUST contain an empty string (`"cid": ""`).

### Slot Synchronization Algorithm (`sync_fighter_slots`)
To prevent corruption when cloning, deleting, or reordering fighters, the editor executes:
```python
def sync_fighter_slots(save):
    uid = get_player_uid(save)
    fighters = save.get("bodyuser", {}).get(uid, [])
    slots = save.setdefault("soul", {}).setdefault("chr", {}).setdefault("slots", {}).setdefault(uid, [])
    while len(slots) < 10:
        slots.append({"uid": int(uid), "slot": len(slots), "cid": ""})
    for s_idx in range(len(slots)):
        slots[s_idx]["slot"] = s_idx
        if s_idx < len(fighters):
            slots[s_idx]["cid"] = fighters[s_idx].get("cid", "")
        else:
            slots[s_idx]["cid"] = ""
```

### Proactive Freezer Accessibility Guard (`_ensure_freezer_accessible`)
Whenever a fighter is created (`create_new_fighter`), duplicated (`clone_fighter`), or has stats edited (`update_fighter`, `max_fighter_level_and_stats`), the editor checks `is_tutorial_cleared(save)`. If the save has not yet unlocked Kiwako Seto, `unlock_tutorial_and_waiting_room(save)` is run proactively. This guarantees that newly forged or duplicated fighters can always be accessed immediately upon entering the game.

---

## 26. Chokufunsha 2D Icon Streaming & Parent-Child Inheritance Architecture (`master_part.nextptid`, `CookedPCConsole`)

### Problem Diagnosis: The "Missing Icon" Fallback Anomaly
When browsing Chokufunsha Shop after unlocking all blueprints or uncapping equipment, uncapped items (`_005` or `_G`) previously rendered with a fallback placeholder (a solid green tile with radial sunburst lines) rather than the weapon/armor's authentic 2D UI icon.

### Technical Root Cause: Asset Packaging vs Dynamic Reverse Lookup
1. **Absence of Dedicated Uncapped Icon Packages**:
   In `CookedPCConsole`, Unreal Engine 3 bundles 2D equipment icon textures as individual Scaleform GFx packages:
   * Tier 1: `UI_Icon_PT_ARM_WP006_001_SF.upk`
   * Tier 2: `UI_Icon_PT_ARM_WP006_002_SF.upk`
   * Tier 3: `UI_Icon_PT_ARM_WP006_003_SF.upk`
   * Tier 4: `UI_Icon_PT_ARM_WP006_004_SF.upk`
   * **Tier 5 / Uncapped (`PT_ARM_WP006_005`)**: **Does NOT have a dedicated `.upk` file** (`UI_Icon_PT_ARM_WP006_005_SF.upk` does not exist in the game directory).

2. **Parent-Child Reverse Lookup via `nextptid`**:
   To render the card for `PT_ARM_WP006_005`, the client binary (`BrgGame-Steam.exe` inside `UBrgJsonObjectFactory::execCreateJsonObject`) performs an SQL query against `masters.db`:
   ```sql
   SELECT id FROM master_part WHERE nextptid = 'PT_ARM_WP006_005';
   ```
   This query discovers that `PT_ARM_WP006_004` (Tier 4) is the immediate precursor of `PT_ARM_WP006_005`. The engine then inherits the 2D texture package associated with `PT_ARM_WP006_004` and displays the authentic Buzzsaw icon.

3. **The Database Wiping Anti-Pattern (`UPDATE master_part SET nextptid = ''`)**:
   A prior script attempted to make all intermediate evolution tiers visible in the shop by running:
   ```sql
   UPDATE master_part SET nextptid = '' WHERE nextptid != '';
   ```
   While this exposed intermediate tiers, it catastrophically severed all 279 uncapping links. When the engine queried `WHERE nextptid = 'PT_ARM_WP006_005'`, it received 0 rows, returned `NULL` for the UI icon resource, and displayed the generic green sunburst card.

### Invariant: 100% Factory Authenticity of `masters.db`
* `masters.db` in `BrgGame\Content\` must remain **100% factory original** (byte-for-byte identical to `masters.db.original.bak`).
* Never wipe or modify `nextptid` or any columns in `masters.db`.
* Multi-tier shop visibility is natively and cleanly achieved in the save file by registering both Tier 4 at Level 5 (`receive_type: "CHARGE"`) and Tier 5 at Level 20 (`receive_type: "CHARGE"`), allowing all tiers to be purchasable simultaneously while preserving intact icon inheritance.

---

## 27. Skill Decal Combat Formula Placeholders & Offline Resolution (`master_text`, `master_skill`)

### In-Game Token Formatting Syntax
In `masters.db` table `master_text`, skill decal descriptions contain parametric format tokens:
* `#0%`, `#1%`, `#2%`, `#3%`, `#4%`, `#5%`
* Example (`SKILL_DESCRIPTION.TXT_SKL_HPUP_03`):
  - EN: `Increase max HP by #0%.\n `
  - ES: `Aumenta un #0% los PS máximos.\n `

### Dynamic Engine Substitution
During gameplay, Unreal Engine 3 reads the active record in `master_skill` and binds the attributes:
* `#0` -> `master_skill.val0`
* `#1` -> `master_skill.val1`
* `#2` -> `master_skill.val2`
* `#3` -> `master_skill.val3`
* `#4` -> `master_skill.val4`
* `#5` -> `master_skill.val5`

### The "0% / #0%" Decal Sheet Display Glitch
When offline tools, encyclopedia extractors, or save editor interfaces dump raw strings from `master_text` without parameter substitution:
* Decals show literal `#0%` or default to `0%` in the UI.
* **Super Heavy Tank (`SKL_HPUP_03_P`)**:
  - `val0 = 60` in `master_skill`.
  - Raw `master_text`: `Aumenta un #0% los PS máximos.`
  - Evaluated: `Aumenta un 60% los PS máximos.`
* **World of Tanks (`SKL_HPUP_WOT_P`)**:
  - `val0 = 45` in `master_skill`.
  - Evaluated: `Aumenta un 45% los PS máximos.`
* **Naomi Detox (`SKL_RESUP_DECDOWN_01_P`)**:
  - `val1 = 50`, `val5 = 50` in `master_skill`.
  - Raw text: `...SPLithium obtenido un #1%.`
  - Evaluated: `Aumenta las Kill Coins de enemigos y tesoros y el SPLithium obtenido un 50%.`
* **Yo-Yo Addict / Fan del Yoyó (`SKL_YOYO_ATKUP_01`)**:
  - `val0 = 30` in `master_skill`.
  - Evaluated: `Poder de ATQ +30% con yoyós.`
* **White Feather / Pluma Blanca (`SKL_WHITEFEATHER`)**:
  - `val0 = 15`, `val1 = 70` in `master_skill`.
  - Evaluated: `Aumenta ATQ de armas perforantes en 15% y un 70% el poder de ataque al realizar un disparo a la cabeza.`

### Resolution Pipeline
All datasets in `all_decals_encyclopedia.json` and the GUI's `i18n.get_item_desc()` pre-resolve these parametric tokens against `master_skill` values and sanitize newline delimiters (`//` to `\n`), ensuring all 368 decals display authentic combat statistics.

---

## 28. Weapon Mastery HUD vs Equipment Research Level Demystification (`master_expert_lvl_reward`, `soul.expert`)

### The UI Anatomy of a Chokufunsha Shop Card
When inspecting weapons in the Chokufunsha Shop or inventory, two distinct level indicators appear on the screen, frequently confusing modders:
1. **Top-Left Card Badge (`+19`, `+4`, `+0`)**:
   Represents the **Equipment Upgrade Level** stored in `soul.partresearch.user[i]["lvl"]`.
   * For standard gear: Level 1 to 5 corresponds to `+0` through `+4`.
   * For uncapped gear: Level 20 corresponds to `+19` (or `+24` overall).
2. **Bottom-Left Card Footer (`[Fist Icon] Nvl. 20 ----/----`)**:
   Represents the active fighter's **Weapon Mastery Level** (Expert / ABP category proficiency) stored in `soul.expert`.
   * The clenched fist indicates mastery proficiency for that specific weapon category (e.g. `PTARMTP_05` Circle Saw).
   * `----/----` indicates that ABP is maxed out and no further mastery EXP is required.
   * **This is NOT the weapon's level**; it is the fighter's weapon skill!

### Mastery Calibration Architecture (`master_expert_lvl_reward`)
To prevent the game engine from permanently resetting weapon mastery to Level 0:
* **Fists (`PTARMTP_00`)**: Governed by the Fists ABP curve, reaching Level 20 at **47,000 ABP**.
* **Standard Weapons (`PTARMTP_01` to `PTARMTP_21`)**: Reach Level 20 at **3,800 ABP**.
* **Unused Engine Dummy Slots (`PTARMTP_08`, `PTARMTP_22`)**: Must be preserved strictly at `abp: -1, lvl: 1, is_checked: 0`.
* **The Level 0 Underflow Trap**: If `lvl = 20` is injected into `soul.expert` but `abp` is left at `0` (or below the required threshold for that level), the engine's startup validator detects a stat desync and zeroes the mastery level. The editor's `repair_and_sanitize_mastery()` ensures `abp >= get_required_abp(wt, lvl)` for all categories.

---

## 29. Defense Simulation & Raid Engine Crash Prevention (`bodyuser.rage`, `select_arm_slots`, TDM sanitization)

### Root Cause Analysis of TDM / Simulation Crashes
When players created or edited fighters from scratch, initiating a **Defense Simulation (Simulación de Defensa)** or invading in TDM would reliably cause an immediate engine crash. Reverse engineering the game binary (`BrgGame-Steam.exe`) revealed several interconnected issues:

1. **The `bodyuser['rage']` Level 0 Gauge Freeze & Crash**:
   * For Grade 6 limit_break 4 fighters, the game engine calculates the 5-bar Rage Gauge dynamically from `master_body_detail`.
   * If `bodyuser['rage'] != 0`, the engine's deserializer queries `master_bodylvl_status_value` for a corresponding rage progression row. Because Grade 6 fighters do not possess rage progression rows in this table, the lookup fails with unhandled null dereferences, freezing the gauge at "Level 0" and crashing when rendering or simulating combat encounters.
   * **Fix**: `f['rage'] = 0` is strictly enforced for all fighters.

2. **Mingo Head Slot Desynchronization (`skill` and `bag` in `bodyuser`)**:
   * Setting `skill` and `bag` in `bodyuser` caused Mingo Head to display corrupted fractions like `45/30` stat points and `8/6` decal slots.
   * Limit Break 4 natively yields 9 decal slots and 54 inventory slots.
   * **Fix**: For Grade 6 limit_break 4 fighters, `f['skill'] = 0` and `f['bag'] = 0` must be canonical zero.

3. **`select_arm_slots` & Death Bag Equipment Sites**:
   * In `soul.chr.chrs`, `select_arm_slots` must be `"0,0"`. Setting invalid slot pairs crashes weapon swapping logic during defense AI initialization.
   * Items in `soul.deathbag` must have strictly valid `site` (`EQSITE_HEAD`, `EQSITE_BODY`, `EQSITE_LEGS`, `EQSITE_ARMR`, `EQSITE_ARML`) with matching `arm_slot` (-1 for armor, 0..2 for right arm, 3..5 for left arm).

4. **Proactive Auto-Sanitization**:
   * Rather than requiring the player to press a hidden repair button, `sanitize_fighters(save)` and `repair_and_sanitize_tdm(save)` execute **automatically** on every fighter creation, cloning, stat update, and save write.

---

## 30. Legitimacy Normalization: Removal of Out-of-Bounds Stats & Fictitious Modifiers

### Why Abnormal Numbers Break the Game
Putting extreme or out-of-bounds values into a save file causes table boundary violations in the game's C++ engine:

1. **The Fake "+24" Equipment Myth**:
   * In *Let It Die*, maximum uncapping is strictly **+19** (`reflvllmt = 20` in `master_part`).
   * A "+24" option was a fictitious modifier with no underlying game assets, icons, or stats. Any save attempting level > 20 was clamped or caused missing asset rendering.
   * **Normalization**: The fake "+24" option was removed completely from the UI and replaced with `Unlock All Gear at Level +19 in Shop (Direct)`.

2. **Firearm Ammo Sanitization (The 9,999 Ammo Corruption Bug)**:
   * Setting `rest: 9999` and `spare: 9999` previously contaminated melee weapons (swords, bats, katanas) and armor (tops, pants, helmets) with gun ammunition keys.
   * **Normalization**: The editor now queries `master_part` to extract the authentic magazine capacity and reserve capacity for all 160 genuine ranged firearms (KAMAS, Snipers, Shotguns, Nail Guns, Launchers). Melee weapons and armors have all stray ammo keys strictly purged to 0.

3. **Durability Normalization (999,999 -> 50,000)**:
   * 999,999 durability was an unnatural cheat value.
   * **Normalization**: Durability is standardized to `50,000`, the canonical 100% full durability value of maximum uncapped gear in the game. It is virtually unbreakable in normal use while appearing 100% legitimate and safe.

4. **44CE Endgame Sets Injection**:
   * The 44CE Forcemen sets (White Steel, Red Napalm, Black Thunder, Pale Wind) are 100% authentic in-game items. Injected sets now spawn at authentic +19 (Level 20) with 50,000 durability, identical to gear crafted through legitimate in-game progression.

---

## 31. Level-Up Engine Crash Demystification (`DistributeBodyLvlParam` RVA `0x118e9c0` & `chr.rest_exp`)

### The Mystery: "I had 999,999 Bloodnium, but leveling up 1 level crashed!"
When players visited Mingo Head with a newly forged or modified fighter and attempted to level up a stat by 1 level using Bloodnium, the game immediately crashed to desktop. Reverse engineering `BrgGame-Steam.exe` inside `BrgOsBodyUser.cpp` revealed the exact C++ failure mechanism:

### Disassembly & Call Trace in `BrgGame-Steam.exe`
1. **The Mingo Head Level-Up Entry (`0x136676f`)**:
   When the player confirms a level-up, the game executes:
   ```asm
   RVA 0x136675d: lea r9, [rbx + 0x80]       ; r9 = pointer to fighter's rest_exp (from chr[i])
   RVA 0x1366764: mov r8, rdi                ; r8 = requested target stat allocation
   RVA 0x1366767: mov rcx, r13               ; rcx = fighter object
   RVA 0x136676a: mov [rsp + 0x20], rax      ; [rsp + 0x20] = pointer to soul.bloodnium_point
   RVA 0x136676f: call 0x14118e9c0           ; Call DistributeBodyLvlParam()
   ```

2. **The Dual Requirement Check in `DistributeBodyLvlParam` (`0x118f186` - `0x118f19e`)**:
   For each level being incremented from `current_lvl` to `target_lvl`, the engine queries `master_bodylvl_exp` to retrieve both `nec_exp` (required EXP) and `nec_bloodnium` (required Bloodnium). It then performs two strict comparisons:
   ```asm
   RVA 0x118f186: mov rdx, [rbp - 0x38]      ; Pointer to fighter's rest_exp
   RVA 0x118f18a: mov eax, [rdx]             ; Current available EXP
   RVA 0x118f18c: cmp eax, edi               ; Compare available EXP vs nec_exp
   RVA 0x118f18e: jl  0x14118f321            ; CRASH IF current_exp < nec_exp!
   RVA 0x118f194: mov r8, [rbp - 0x30]       ; Pointer to soul.bloodnium_point
   RVA 0x118f198: mov ecx, [r8]              ; Current available Bloodnium
   RVA 0x118f19b: cmp ecx, r14d              ; Compare available Bloodnium vs nec_bloodnium
   RVA 0x118f19e: jl  0x14118f321            ; CRASH IF current_bloodnium < nec_bloodnium!
   ```
   If either condition fails, execution jumps to `0x14118f321`, invoking:
   ```cpp
   appErrorf(TEXT("body_lvl distribute failed! cid=%s, grade=%d, exp=%d, nec_exp=%d, bloodnium=%d, nec_bloodnium=%d"), ...);
   ```

3. **The Root Causes**:
   * **Missing `rest_exp`**: When fighters were created from scratch or upgraded via save editor, `chr["rest_exp"]` was left at `0`. Although the Mingo Head UI only highlights the Bloodnium cost on uncapped fighters, the C++ engine mathematically requires `rest_exp >= nec_exp`. Because `0 < nec_exp`, the EXP assertion failed and crashed the game.
   * **Missing `chr["lvl"]`**: The save schema previously omitted `"lvl"` from `soul.chr.chrs[i]`, relying only on `bodyuser["lvl"]`. In `DistributeBodyLvlParam` (`0x118eb42`), `r15 + 0x1c` reads `chr.lvl`. With the field missing, the engine evaluated current level as `0`, desynchronizing level progression and attempting to query invalid stat tables.
   * **Missing Death 'Roids (`ITMT_STEROID`) & `Array.h` Assertion Crash**: When uncapping stats, skill decal slots, death bag capacity, or rage at Mingo Head, `master_bodylvl_limit_break_item` mandates Death 'Roids (`ITMT_STEROID_1` through `6`). If the player's storage has 0 Death 'Roids, the engine logs `cid %s do not have %s => %d` and falls through to an unchecked element removal on an empty internal container. This triggers Unreal Engine's `Array.h(635): Assertion failed: i >= 0 && i < ArrayNum`, invoking `appErrorf` / `RaiseException(1, ...)` and crashing straight to desktop.

### The Automated Solution
1. **EXP Injection**:
   * All fighters now automatically receive authentic `total_exp` consistent with their level (482,191 for Grade 6 level 247; 139,875 for level 140; etc.).
   * Fighters are pre-populated with reserve `rest_exp` (`9,999,999` for Grade 6, `5,000,000` for lower tiers), guaranteeing that any manual level-up at Mingo Head or the Fighter Freezer has more than enough EXP to satisfy `nec_exp`.
2. **Level Synchronization**:
   * `bodyuser["lvl"]` and `soul.chr.chrs[i]["lvl"]` are strictly synchronized to the same value on every save, creation, and edit.
3. **Database-Aligned Base Stats**:
   * Newly forged fighters receive canonical stats matching `param_lv_max` for their grade (Grade 1=5, Grade 2=9, Grade 3=13, Grade 4=17, Grade 5=21, Grade 6=25/45).
4. **Death 'Roid Stocking & Coin Locker Expansion**:
   * Expanded Coin Locker capacity to 1,500 slots.
   * Injected 50x of each Death 'Roid tier (`ITMT_STEROID_1` through `ITMT_STEROID_6`, 300 total) into the player's Coin Locker, ensuring the Mingo Head material requirement is always satisfied.

---

*Technical reference verified against the official masters.db database and the Unreal Engine save pipeline of LET IT DIE.*

