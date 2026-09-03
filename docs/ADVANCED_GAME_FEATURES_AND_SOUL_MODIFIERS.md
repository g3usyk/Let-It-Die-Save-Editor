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

## 5. TDM Mystery Bags Architecture (mysterybag)

### Save File Path
* `save_json["soul"]["mysterybag"]` -> Dictionary indexed by tier rarity.

### Schema
```json
{
  "RAINBOW": [
    {"rarity": "RAINBOW", "cntgen": "MYSTERYBAG_GEN_RAINBOW_144"}
  ],
  "PLATINUM": [
    {"rarity": "PLATINUM", "cntgen": "MYSTERYBAG_GEN_PLATINUM_58"}
  ],
  "GOLD": [
    {"rarity": "GOLD", "cntgen": "MYSTERYBAG_GEN_GOLD_04"}
  ],
  "SILVER": [
    {"rarity": "SILVER", "cntgen": "MYSTERYBAG_GEN_SILVER_74"}
  ],
  "COPPER": [
    {"rarity": "COPPER", "cntgen": "MYSTERYBAG_GEN_COPPER_46"}
  ]
}
```

### Rewards by Rarity
* **RAINBOW:** Death Metals (x1 to x5), 4-Star & 5-Star Decals, 44CE Forcemen Blueprints, Purple/Orange Death 'Roids.
* **PLATINUM:** 4-Star Decals, Grade 6 to 8 Materials, Boss Metals.
* **GOLD:** 50,000+ KC / SPL, Grade 5 to 6 Materials, 3-Star Decals.
* **SILVER:** 20,000 KC / SPL, Grade 3 to 5 Materials.
* **COPPER:** 5,000 KC / SPL, Mushrooms and Basic Materials.

---

## 6. Reward Box / Mailbox Presents (soul.present)

### Save File Path
* `save_json["soul"]["present"]` -> List of pending rewards in the Waiting Room mailbox.

### Present Item Schema
```json
{
  "pid": "5c3f4a4d-64ad-4fae-a4d5-0820729a5637",
  "from": "ADMIN",
  "type": "MONEY",
  "num": 1000000,
  "created": 1670398513,
  "fromval": "",
  "kind": "MYSTERYBAG_RAINBOW",
  "val0": "",
  "val1": "0",
  "val2": "0",
  "val3": "0",
  "val4": "0"
}
```

### Valid Item Types
* `"MONEY"` -> Direct Kill Coins (`num` = amount)
* `"SPIRIT"` -> Direct SPLithium (`num` = amount)
* `"MEDAL"` -> Death Metals (`num` = amount)
* `"ITEM"` -> Crafting Material (`val0` = `itemid`)
* `"DECAL"` -> Skill Decal (`val0` = `sklid`)
* `"EQUIPMENT"` -> Weapon or Armor piece (`val0` = `ptid`)

---

## 7. Elevator Floor ID Reference

To unlock fast-travel across all four tower districts (D.O.D., War Ensemble, Candle Wolf, M.I.L.K., and Tengoku) without coin fees:
* `save_json["soul"]["openelvflr"]` -> Complete list of elevator station IDs (`ELV_MAIN_...` and `ELV_SUB...`).

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

## 16. Automated Rolling Backup System

* File pattern: `<save_name>.sav.YYYYMMDD_HHMMSS.bak`.
* Rolling retention policy: preserves the 10 most recent backups and discards older ones.
* Direct restore available through the Advanced tab in the GUI or via manual file replacement.

---

*Technical reference verified against the official masters.db database and the Unreal Engine save pipeline of LET IT DIE.*
