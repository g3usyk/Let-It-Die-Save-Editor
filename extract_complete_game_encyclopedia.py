import sqlite3
import json
import os

db_path = r"E:\SteamLibrary\steamapps\common\LET IT DIE\BrgGame\Content\masters.db"
out_dir = r"c:\Users\sipi_\Downloads\Let it die mod"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("1. Building master localization dictionaries...")
sections = ['PT_ARM', 'PT_HEAD', 'PT_BODY', 'PT_LEG', 'SKILL_NAME', 'SKILL_DESCRIPTION', 'MATERIAL', 'MATERIAL_DSC', 'MUSHROOM', 'MUSHROOM_BEAST', 'MUSHROOM_DSC']
cur.execute(f"SELECT sct, id, lang, txt FROM master_text WHERE sct IN ({','.join('?' for _ in sections)}) AND lang IN ('int', 'esn');", sections)

text_db = {}
for sct, tid, lang, txt in cur.fetchall():
    clean_txt = txt.replace("\r\n", " ").replace("\n", " ").replace("|", "-").strip()
    text_db.setdefault(f"{sct}.{tid}", {})[lang] = clean_txt

def get_loc(sct, tid, default=""):
    key = f"{sct}.TXT_{tid}" if not tid.startswith("TXT_") else f"{sct}.{tid}"
    t_entry = text_db.get(key, {})
    name_es = t_entry.get("esn") or t_entry.get("int") or default
    name_en = t_entry.get("int") or default
    return name_es, name_en

print("2. Extracting All 1,370 Equipment & Weapons (master_part)...")
cur.execute("SELECT id, name, type, drcat, rarity, dur, atk, def, price_b, price_s, lvllmt FROM master_part;")
equipment_list = []
weapons_list = []
armors_heads = []
armors_tops = []
armors_btms = []

for pid, name_key, ptype, drcat, rarity, dur, atk, pdef, price_b, price_s, lvllmt in cur.fetchall():
    clean_key = name_key.split(".")[-1]
    
    sct = "PT_ARM"
    item_type_label = "Arma (Weapon)"
    if ptype == "PTTP_HEAD" or ptype == "PTTP_MASK":
        sct = "PT_HEAD"
        item_type_label = "Casco (Head Armor)"
    elif ptype == "PTTP_BODY":
        sct = "PT_BODY"
        item_type_label = "Pecho (Body Armor)"
    elif ptype == "PTTP_LEGS" or ptype == "PTTP_PANTS":
        sct = "PT_LEG"
        item_type_label = "Pantalones (Leg Armor)"
        
    name_es, name_en = get_loc(sct, clean_key, default=pid)
    
    # Clean faction name
    fac = "General / Sin Facción"
    if drcat == "DRCAT_DIY": fac = "D.O.D. ARMS"
    elif drcat == "DRCAT_MILITARY": fac = "WAR ENSEMBLE"
    elif drcat == "DRCAT_FANTASY": fac = "CANDLE WOLF"
    elif drcat == "DRCAT_SPORTS": fac = "M.I.L.K."
    elif drcat == "DRCAT_FOUR_FORCE_MEN": fac = "4 FORCEMEN"
    elif drcat == "DRCAT_JACKALS": fac = "JACKALS"
    
    entry = {
        "id": pid,
        "name_es": name_es,
        "name_en": name_en,
        "type": item_type_label,
        "raw_type": ptype,
        "faction": fac,
        "rarity": rarity,
        "durability": dur,
        "attack": atk,
        "defense": pdef,
        "price_kc": price_b,
        "sell_kc": price_s,
        "max_lvl": lvllmt
    }
    equipment_list.append(entry)
    
    if ptype == "PTTP_ARM":
        weapons_list.append(entry)
    elif ptype == "PTTP_HEAD" or ptype == "PTTP_MASK":
        armors_heads.append(entry)
    elif ptype == "PTTP_BODY":
        armors_tops.append(entry)
    elif ptype == "PTTP_LEGS" or ptype == "PTTP_PANTS":
        armors_btms.append(entry)

print(f"-> Weapons: {len(weapons_list)} | Heads: {len(armors_heads)} | Tops: {len(armors_tops)} | Legs: {len(armors_btms)}")

print("3. Extracting All 1,346 R&D Blueprints (master_part_research)...")
cur.execute("SELECT ptid, is_initial, is_open, mate1_id, mate2_id, mate3_id, mate4_id, mate5_id, craft_money, craft_spirit, init_waiting_minute FROM master_part_research;")
blueprint_recipes = []
for ptid, is_init, is_open, m1, m2, m3, m4, m5, kc, spl, wait_min in cur.fetchall():
    eq_match = next((e for e in equipment_list if e["id"] == ptid), None)
    name_es = eq_match["name_es"] if eq_match else ptid
    name_en = eq_match["name_en"] if eq_match else ptid
    cat = eq_match["type"] if eq_match else "Desconocido"
    fac = eq_match["faction"] if eq_match else "General"
    rarity = eq_match["rarity"] if eq_match else 1
    
    mats = [m for m in [m1, m2, m3, m4, m5] if m and m != "NONE" and m != ""]
    
    blueprint_recipes.append({
        "ptid": ptid,
        "name_es": name_es,
        "name_en": name_en,
        "category": cat,
        "faction": fac,
        "rarity": rarity,
        "cost_kc": kc,
        "cost_spl": spl,
        "craft_time_min": wait_min,
        "materials": mats
    })

print(f"-> Blueprints / Recipes: {len(blueprint_recipes)}")

print("4. Extracting All 368 Skill Decals (master_skill)...")
cur.execute("SELECT id, no, display_label, name, desc, rarity, premium, category, buy_money, buy_spirit, buy_recycle_point FROM master_skill;")
decals_list = []
for sid, sno, dlabel, name_key, desc_key, rarity, prem, cat, buy_kc, buy_spl, buy_re in cur.fetchall():
    clean_name_key = name_key.split(".")[-1]
    clean_desc_key = desc_key.split(".")[-1]
    
    name_es, name_en = get_loc("SKILL_NAME", clean_name_key, default=sid)
    desc_es, desc_en = get_loc("SKILL_DESCRIPTION", clean_desc_key, default="")
    
    decals_list.append({
        "id": sid,
        "no": sno,
        "name_es": name_es,
        "name_en": name_en,
        "rarity": rarity,
        "premium": bool(prem),
        "category": cat,
        "desc_es": desc_es,
        "desc_en": desc_en,
        "buy_kc": buy_kc,
        "buy_spl": buy_spl,
        "buy_re": buy_re
    })

print(f"-> Decals: {len(decals_list)}")

# Save JSON Datasets
with open(os.path.join(out_dir, "all_equipment_encyclopedia.json"), "w", encoding="utf-8") as f:
    json.dump(equipment_list, f, indent=2, ensure_ascii=False)

with open(os.path.join(out_dir, "all_blueprints_recipes.json"), "w", encoding="utf-8") as f:
    json.dump(blueprint_recipes, f, indent=2, ensure_ascii=False)

with open(os.path.join(out_dir, "all_decals_encyclopedia.json"), "w", encoding="utf-8") as f:
    json.dump(decals_list, f, indent=2, ensure_ascii=False)

# Generate Grand Markdown Encyclopedia Document
enc_path = os.path.join(out_dir, "LET_IT_DIE_COMPLETE_ENCYCLOPEDIA.md")
with open(enc_path, "w", encoding="utf-8") as f:
    f.write("# 💀 LET IT DIE (Offline) - Gran Enciclopedia Completa de Datos Oficiales\n\n")
    f.write("Extraído y verificado directamente de los archivos del juego (`masters.db`):\n")
    f.write(f"- **1,370 Piezas de Equipo** ({len(weapons_list)} Armas, {len(armors_heads)} Cascos, {len(armors_tops)} Pechos, {len(armors_btms)} Pantalones)\n")
    f.write(f"- **{len(blueprint_recipes)} Planos y Recetas de Investigación Chokufunsha**\n")
    f.write(f"- **{len(decals_list)} Calcomanías Oficiales con Efectos en Español e Inglés**\n\n")
    f.write("---\n\n")
    
    # 1. Decals Section
    f.write(f"## 🏷️ 1. Calcomanías Oficiales (`master_skill` - {len(decals_list)} Calcomanías)\n\n")
    f.write("| ID Calcomanía | Nombre en Español | Nombre en Inglés | Rareza | Premium | Efecto de Combate |\n")
    f.write("| :--- | :--- | :--- | :---: | :---: | :--- |\n")
    for d in decals_list:
        f.write(f"| `{d['id']}` | **{d['name_es']}** | {d['name_en']} | {d['rarity']}★ | {'⭐ PREMIUM' if d['premium'] else 'Estándar'} | {d['desc_es']} |\n")
        
    f.write("\n---\n\n")
    
    # 2. Weapons Section
    f.write(f"## ⚔️ 2. Armas Oficiales (`master_part` - {len(weapons_list)} Armas)\n\n")
    f.write("| ID de Arma | Nombre en Español | Nombre en Inglés | Facción | Rareza | Ataque Base | Durabilidad |\n")
    f.write("| :--- | :--- | :--- | :--- | :---: | :---: | :---: |\n")
    for w in weapons_list:
        f.write(f"| `{w['id']}` | **{w['name_es']}** | {w['name_en']} | {w['faction']} | {w['rarity']}★ | {w['attack']} | {w['durability']} |\n")
        
    f.write("\n---\n\n")
    
    # 3. Armors Section
    f.write(f"## 🪖 3. Armaduras Oficiales (`master_part` - {len(armors_heads)} Cascos, {len(armors_tops)} Pechos, {len(armors_btms)} Piernas)\n\n")
    f.write("| ID de Armadura | Tipo | Nombre en Español | Nombre en Inglés | Facción | Rareza | Defensa Base | Durabilidad |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |\n")
    for a in (armors_heads + armors_tops + armors_btms):
        f.write(f"| `{a['id']}` | {a['type']} | **{a['name_es']}** | {a['name_en']} | {a['faction']} | {a['rarity']}★ | {a['defense']} | {a['durability']} |\n")

print(f"Saved complete official encyclopedia to {enc_path}!")
