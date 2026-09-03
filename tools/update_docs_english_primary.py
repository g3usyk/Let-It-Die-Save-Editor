# -*- coding: utf-8 -*-
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")

def build_materials_doc():
    mats_file = os.path.join(BASE_DIR, "all_materials_db.json")
    with open(mats_file, "r", encoding="utf-8") as f:
        mats = json.load(f)

    category_titles = [
        ("Aluminio (Aluminum)", "Aluminum (8 items)"),
        ("Cobre (Copper)", "Copper (8 items)"),
        ("Textiles y Fibras (Cloth)", "Textiles & Fibers (8 items)"),
        ("Hierro y Acero (Iron & Steel)", "Iron & Steel (8 items)"),
        ("Petróleo y Aceites (Oil)", "Petroleum & Oils (8 items)"),
        ("Maderas (Wood)", "Wood & Planks (8 items)"),
        ("D.O.D. ARMS (Metals)", "D.O.D. ARMS Faction Metals (9 items)"),
        ("WAR ENSEMBLE (Metals)", "WAR ENSEMBLE Faction Metals (9 items)"),
        ("CANDLE WOLF (Metals)", "CANDLE WOLF Faction Metals (9 items)"),
        ("M.I.L.K. (Metals)", "M.I.L.K. Faction Metals (9 items)"),
        ("Metales de Jefes (Boss Metals)", "Boss Metals (5 items)"),
        ("Materiales Jackals y Tengoku", "Tengoku, Jackals & Rare Materials (11 items)"),
        ("Esteroides / Rostest (Luchadores)", "Death 'Roids / Fighter Enhancers (14 items)")
    ]

    grouped = {}
    for m in mats:
        c = m.get("category", "")
        grouped.setdefault(c, []).append(m)

    out = [
        "# LET IT DIE - Verified Game Database & Material Catalog (masters.db)",
        "",
        "Comprehensive technical reference indexing all 106 authentic crafting and enhancement materials extracted directly from the game client master database (`masters.db`).",
        "",
        "Primary language is **English** with **Spanish** provided as secondary reference for international players and modders.",
        "",
        "---",
        ""
    ]

    for cat_raw, title in category_titles:
        items = grouped.get(cat_raw, [])
        if not items:
            for k, v in grouped.items():
                if cat_raw.split()[0] in k:
                    items = v
                    break
        if not items:
            continue

        out.append(f"### {title}")
        out.append("")
        out.append("| Internal Save ID | English Name (Primary) | Spanish Name (Secondary) | Rarity | Purpose / Notes (EN / ES) |")
        out.append("| :--- | :--- | :--- | :---: | :--- |")
        for it in items:
            itemid = it.get("itemid", "")
            name_en = it.get("name_en", "")
            name_es = it.get("name_es", "")
            rarity = f"{it.get('rarity', 1)}★"
            desc_en = it.get("desc_en", "R&D Material")
            desc_es = it.get("desc_es", "Material para I+D")
            purpose = f"{desc_en} / {desc_es}" if desc_en != desc_es else desc_en
            out.append(f"| `{itemid}` | **{name_en}** | {name_es} | {rarity} | {purpose} |")
        out.append("")
        out.append("---")
        out.append("")

    target = os.path.join(DOCS_DIR, "GAME_DATABASE_VERIFIED_NOTES.md")
    with open(target, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"Updated: {target}")

def build_encyclopedia_doc():
    decals_file = os.path.join(BASE_DIR, "all_decals_encyclopedia.json")
    equip_file = os.path.join(BASE_DIR, "all_equipment_encyclopedia.json")

    with open(decals_file, "r", encoding="utf-8") as f:
        decals = json.load(f)
    with open(equip_file, "r", encoding="utf-8") as f:
        equip = json.load(f)

    out = [
        "# LET IT DIE - Master Game Encyclopedia & Data Tables",
        "",
        "Complete technical encyclopedia extracted and verified directly from the game client master database (`masters.db`).",
        "",
        "Primary language is **English** with **Spanish** provided as secondary reference.",
        "",
        "- **1,370 Equipment Pieces** (Weapons, Helmets, Chest Armors, Pants)",
        "- **626 Skill Decals** (Standard and Premium variants with combat perks)",
        "- **Chokufunsha Blueprints & R&D Recipes**",
        "",
        "---",
        "",
        "## 1. Official Decals (master_skill - 626 Decals)",
        "",
        "| Decal ID | English Name (Primary) | Spanish Name (Secondary) | Rarity | Type | Combat Effect (English / Spanish) |",
        "| :--- | :--- | :--- | :---: | :---: | :--- |"
    ]

    for d in decals:
        did = d.get("id", "")
        name_en = d.get("name_en", "")
        name_es = d.get("name_es", "")
        rarity = f"{d.get('rarity', 1)}★"
        t_type = "Premium" if d.get("premium") else "Standard"
        desc_en = d.get("desc_en", "").replace("\n", " ").replace("//", " ").strip()
        desc_es = d.get("desc_es", "").replace("\n", " ").replace("//", " ").strip()
        
        effect_str = f"{desc_en}<br>*(ES: {desc_es})*" if desc_es and desc_es != desc_en else desc_en
        out.append(f"| `{did}` | **{name_en}** | {name_es} | {rarity} | {t_type} | {effect_str} |")

    out.append("")
    out.append("---")
    out.append("")
    out.append("## 2. Official Weapons (master_part - 385 Weapons)")
    out.append("")
    out.append("| Weapon ID | English Name (Primary) | Spanish Name (Secondary) | Faction | Rarity | Base Attack | Durability |")
    out.append("| :--- | :--- | :--- | :--- | :---: | :---: | :---: |")

    weapons = [e for e in equip if e.get("raw_type") == "PTTP_ARM" or "_WP" in e.get("id", "")]
    for w in weapons:
        wid = w.get("id", "")
        name_en = w.get("name_en", "")
        name_es = w.get("name_es", "")
        faction = w.get("faction", "General")
        rarity = f"{w.get('rarity', 0)}★"
        atk = w.get("attack", 0)
        dur = w.get("durability", 1400)
        out.append(f"| `{wid}` | **{name_en}** | {name_es} | {faction} | {rarity} | {atk} | {dur} |")

    out.append("")
    out.append("---")
    out.append("")
    out.append("## 3. Official Armor Pieces (master_part - Helmets, Body, Pants)")
    out.append("")
    out.append("| Armor ID | Slot | English Name (Primary) | Spanish Name (Secondary) | Faction | Rarity | Base Defense | Durability |")
    out.append("| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: |")

    armors = [e for e in equip if e.get("raw_type") in ("PTTP_HEAD", "PTTP_BODY", "PTTP_PANTS", "PTTP_LEGS") or any(k in e.get("id", "") for k in ("_HEAD_", "_TOPS_", "_BTM_"))]
    for a in armors:
        aid = a.get("id", "")
        raw_t = a.get("raw_type", "")
        if raw_t == "PTTP_HEAD" or "_HEAD_" in aid:
            slot = "Head"
        elif raw_t == "PTTP_BODY" or "_TOPS_" in aid:
            slot = "Body"
        else:
            slot = "Legs"
        name_en = a.get("name_en", "")
        name_es = a.get("name_es", "")
        faction = a.get("faction", "General")
        rarity = f"{a.get('rarity', 0)}★"
        defs = a.get("defense", 0)
        dur = a.get("durability", 1400)
        out.append(f"| `{aid}` | {slot} | **{name_en}** | {name_es} | {faction} | {rarity} | {defs} | {dur} |")

    target = os.path.join(DOCS_DIR, "LET_IT_DIE_COMPLETE_ENCYCLOPEDIA.md")
    with open(target, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"Updated: {target}")

if __name__ == "__main__":
    build_materials_doc()
    build_encyclopedia_doc()
