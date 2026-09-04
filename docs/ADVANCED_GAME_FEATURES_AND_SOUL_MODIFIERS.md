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
* `save_json["soul"]["team_id"]` -> Assigned team (e.g., "01" Tokyo, "11" California).

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

## 6. Waiting Room Facilities (Level 100) & Player Rank Architecture

### 1. KC Bank & SPLithium Tank Expansion (`soul.safe_level` & `soul.spirit_tank_level`)
* In the game client database table `master_spirit_tank_level`, facility upgrades scale from **Level 1 to Level 100**.
* Setting `safe_level = 100` and `spirit_tank_level = 100` expands capacity to **2,560,000+** Kill Coins and SPLithium.
* The Save Editor provides an interactive input allowing any custom level (1-100) as well as a one-click maximum button.

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
* `skill`: Additional decal slots unlocked via steroids (**3** additional, for a full total of **8 slots**).
* `bag`: Extra Death Bag capacity slots (safe max: **3**).
* `rage`: Extra Rage gauge bars (**1** additional bar).

### 2. Live Combat State: `save["soul"]["chr"]["chrs"][uid]`
In `chr.chrs`, the actual in-game runtime state is stored:
* `name`: Fighter display name.
* `type`: Engine class archetype code (`"BAL"` All-Rounder, `"BRE"` Striker, `"DEF"` Defender, `"TEC"` Attacker, `"SHT"` Shooter, `"COL"` Collector, `"SKI"` Skill Master, `"LUK"` Lucky Star).
* `grade`: Base grade (**1 to 6**; internal maximum is **6**).
* `limit_break`: Uncap stage (**0 to 4**; Grade 6 with Limit Break 4 represents **Tier 8 / G8** in the community).
* `hp`: Current combat health pool (e.g., **20,000** HP).
* `state`: Fighter state (`"GUARD"`, `"REST"`, `"DEAD"`).
* `escdie`: Rescue flag (0 = alive and ready).

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
A notorious bug in save modification was an infinite loading hang occurring when entering or riding the Royal Express elevator. Reverse engineering and community testing (discovered by Stephengw3 on Reddit) revealed the exact root cause:
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
* **Shop Max Mode (+19 Completed)**:
  Level 20 has:
  `{"ptid": "PT_ARM_WP003_005", "lvl": 20, "research_type": "FINISHED", "receive_type": "CHARGE"}`
  * In-game behavior: The shop sells the item at Level 20 (+19). The R&D menu shows the item as 100% completed.

### Bulk Uncap Processing Architecture
The bulk uncap feature (`⚡ Mejorar Todo a Nivel +19`) iterates across all **377+ authentic uncapped weapons and armors**:
1. Uses pre-cached SQLite parent mapping from `master_part` (`nextptid` relationships) to resolve ancestors in constant time (`O(1)`).
2. Guarantees prerequisite ancestor tiers (e.g. Tier 1, Tier 2, Tier 3, Tier 4 Base) are safely registered at Level 5 (+4 `CHARGE`) so the game's evolution prerequisite checks succeed.
3. Places the final uncapped tier at Level 19 `CHARGE`, instantly populating the entire Chokufunsha R&D catalog without skipping game logic.

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

*Technical reference verified against the official masters.db database and the Unreal Engine save pipeline of LET IT DIE.*
