# LET IT DIE - Technical Documentation & Developer Notes

This directory contains in-depth documentation, reverse-engineered save structure specifications, and complete game data tables extracted from the official client database (`masters.db`).

---

## Documents Index

### 1. [Internal Save Architecture & Soul Modifiers Reference](ADVANCED_GAME_FEATURES_AND_SOUL_MODIFIERS.md)
A comprehensive technical manual documenting the internal `.sav` layout and JSON schema paths:
- **Tower Map, Elevators & Escalator Gate Network**: Full 980-room discovery (`soul.areaflag`), 1,119 escalator pathways (`soul.areaescflag`), elimination of the red padlock bitmask (`0x40`), 193 progression flags (`KGF_RFT_...`), and Waiting Room gate bypass to Floors 41-50 (Hazama) and Tengoku 51+.
- **Waiting Room Facilities to Level 100 & Player Rank**: KC Bank and SPL Tank capacity scaling up to Level 100, plus mathematical rank point synchronization (Ranks 1 to 130 in `master_rank_point`).
- **Equipment Evolution & Uncapping Hierarchy**: Safe +4 limit for base/intermediate tiers triggering next blueprint unlocks, and +19/+24 limits for final uncapped equipment.
- **UAC Administrative Auto-Elevation**: Windows manifest auto-elevation preventing save writing permission errors.
- **Elevator Fast Travel Network**: Complete list of 61 elevator station IDs (`ELV_MAIN_...`, `ELV_SUB...`) in `soul.openelvflr`.
- **Uncle Death Stamp Rally**: Multiplier scaling mechanics (`soul.researchstamp`) and Scythe blueprint injection (`PT_ARM_WP050_001`).
- **Death Bag Inventory**: Capacity expansion limits and active equipment site slots (`EQSITE_HEAD`, `EQSITE_BODY`, `EQSITE_WEAPON_R1/R2/L1/L2`).
- **Tokyo Death Metro (TDM)**: Competitive rank IDs (Bronze through Diamond 1) and Mystery Bag tier loot tables.
- **Mailbox / Reward Box**: Schema for injecting Kill Coins, Death Metals, SPLithium, and crafting items (`soul.present`).
- **Fighter Engine Internals**: Distinction between `bodyuser` level allocation points (1-45 stat caps, Death 'Roids) and `soul.chr` live combat states.
- **Weapon & Armor Modifiers**: Overriding durability (`999,999` unbreakable), chamber ammo (`9,999`), and Tengoku uncap levels (+19/+24).
- **Endgame Equipment IDs**: Reference list for 44CE Forcemen, Jackals, and Tengoku legendary weapons.
- **Royal Express VIP Pass Validation & Friendship Bug Fix**: Technical explanation of `soul.vip.friendship` (must be `1` to avoid elevator cutscene voice/animation stall), safe expiration rules (~100 days), and auto-healing logic.
- **Balanced 4-Chunk ZLIB Compressor**: Engine streaming decompressor compliance using 4 balanced ZLIB chunks with compact UTF-8 formatting and zero-byte trailer.
- **Chokufunsha R&D Mode vs Shop Max**: Implementation of `soul.partresearch.user` Level 19 `CHARGE` (+18 in Shop, active +19 in R&D) versus Level 20 `CHARGE` (Shop Max).
- **Emergency Waiting Room Fighter Rescue**: Immediate extraction of stuck or frozen fighters back to the Waiting Room without death penalties.

---

### 2. [Verified Material Catalog & R&D Database](GAME_DATABASE_VERIFIED_NOTES.md)
Index of all 106 crafting materials verified from `masters.db`:
- Categorized by material families: Aluminum, Copper, Cloth/Fibers, Iron/Steel, Petroleum/Oils, Wood/Planks, Faction Metals, Boss Metals, Tengoku/Jackal rare drops, and Death 'Roids.
- Contains internal game IDs, star rarities, English names, and Spanish names.

---

### 3. [Master Game Encyclopedia & Data Tables](LET_IT_DIE_COMPLETE_ENCYCLOPEDIA.md)
Reference tables covering:
- **368 Official Decals**: Internal skill IDs, English names, Spanish names, star rarities, standard/premium indicators, and exact combat perk descriptions.
- **1,370 Equipment Pieces**: Weapons, helmets, body armors, and pants.
- **1,346 Chokufunsha Blueprints**: R&D recipe progression states.
