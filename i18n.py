# -*- coding: utf-8 -*-
"""
Internationalization (i18n) Module for LET IT DIE Save Editor.
Supports dynamic switching between Spanish (es) and English (en).
"""

import os
import json
import locale

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# Default language detection
def _detect_system_language():
    try:
        loc = locale.getdefaultlocale()[0] or ""
        return "es" if "es" in loc.lower() else "en"
    except Exception:
        return "en"

_current_language = None

def get_language():
    global _current_language
    if _current_language is None:
        _current_language = load_saved_language()
    return _current_language

def set_language(lang_code):
    global _current_language
    if lang_code in ("es", "en"):
        _current_language = lang_code
        save_language_preference(lang_code)

def load_saved_language():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                lang = cfg.get("language")
                if lang in ("es", "en"):
                    return lang
        except Exception:
            pass
    return _detect_system_language()

def save_language_preference(lang_code):
    cfg = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}
    cfg["language"] = lang_code
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

# Master Translations Dictionary
TRANSLATIONS = {
    "es": {
        # App & Header
        "app_title": "LET IT DIE - Deep Save Editor Pro v2.2.0 (Master Cyberpunk Edition)",
        "save_file": "PARTIDA (.sav):",
        "browse": "📁 Examinar...",
        "reload": "🔄 Recargar",
        "backup": "🛡️ Backup",
        "armor_sets": "👘 Sets de Armadura",
        "rnd_analyzer": "🧠 Analizador I+D",
        "updates": "⚡ Actualizaciones",
        "save_game": "💾 GUARDAR PARTIDA",
        "lang_label": "🌐 Idioma:",
        "no_save_detected": "No se detectó partida automáticamente. Haz clic en 'Examinar' para abrir tu archivo .sav",
        
        # Dashboard
        "fighter_prefix": "Luchador:",
        "base_rank_prefix": "Rango Base:",
        "tdm_prefix": "🏆 TDM:",
        "bag_prefix": "Bolsa:",
        "slots_suffix": "slots",
        
        # Tabs
        "tab_currencies": " Monedas y VIP ",
        "tab_fighters": " Luchadores (Congelador) ",
        "tab_materials": " Materiales y Forja (106) ",
        "tab_decals": " Calcomanías (626) ",
        "tab_blueprints": " Planos Chokufunsha (1,370) ",
        "tab_mastery": " Maestría de Armas ",
        "tab_tower": " Desbloqueos Maestros y Torre ",
        "tab_advanced": " Enciclopedia y Respaldos ",

        # Tab 1: Player & Currencies
        "currencies_title": "Monedas Principales (Locker & Banco)",
        "kill_coins": "Kill Coins (KC):",
        "death_metals": "Death Metals (DM):",
        "splithium": "SPLithium (SPL):",
        "bloodnium": "Bloodnium (BL):",
        "recycle_points": "Puntos de Reciclaje (RE):",
        "global_max_res": "⭐ MAXIMIZAR TODOS LOS RECURSOS (x9,999,999)",
        "quick_exchange": "Tasa de Cambio Rápida:",
        "kc_pack_1m": "🪙 +1,000,000 KC",
        "dm_pack_100": "💎 +100 DM",
        "spl_pack_1m": "⚡ +1,000,000 SPL",
        "bl_pack_50k": "🩸 +50,000 BL",
        "vip_express_pass": "Pase Expreso VIP:",
        "days": "días",
        "apply_vip": "Aplicar Días",
        "unlimited_vip": "🎫 Pase VIP Ilimitado (365 días + 99 tickets)",
        "mystery_bags": "Bolsas Misteriosas TDM:",
        "mystery_qty": "Cantidad c/u:",
        "add_bags_btn": "Añadir Bolsas",
        "all_bags_pack": "🎁 Pack de Todas las Bolsas (Bronce/Plata/Oro/Arcoíris)",
        "storage_limits": "Capacidad Máxima de Banco y Tanque SPL:",
        "bank_cap": "Banco KC:",
        "tank_cap": "Tanque SPL:",
        "apply_caps": "Aplicar Límites",
        "max_storage_btn": "📦 Capacidad Máxima de Almacenamiento (1,500 slots)",

        # Tab 2: Fighters
        "fighter_roster": "Congelador de Luchadores",
        "fighter_stats_title": "Atributos y Estadísticas del Luchador",
        "f_name": "Nombre:",
        "f_class": "Clase:",
        "f_tier": "Grado / Tier:",
        "f_level": "Nivel:",
        "f_hp": "Salud (HP):",
        "f_stm": "Resistencia (STM):",
        "f_str": "Fuerza (STR):",
        "f_dex": "Destreza (DEX):",
        "f_vit": "Vitalidad (VIT):",
        "f_luk": "Suerte (LUK):",
        "max_stats_btn": "⭐ MAXIMIZAR NIVEL Y ATRIBUTOS",
        "unlock_tier8_btn": "👑 DESBLOQUEAR TIER 8 (GOD TIER)",
        "revive_healed_btn": "❤️ Revivir y Sanar Luchador",
        "revive_all_btn": "❤️ Revivir a Todos los Luchadores",
        "equip_preset_direct": "🥋 EQUIPAR PRESET DIRECTO EN ESTE LUCHADOR",
        "equipped_decals_title": "Calcomanías Equipadas en Ranuras Activas",
        "slot_prefix": "Ranura",
        
        # Fighter Classes
        "class_All-Rounder": "Todoterreno",
        "class_Striker": "Luchador (Striker)",
        "class_Defender": "Defensor",
        "class_Attacker": "Atacante",
        "class_Shooter": "Tirador (Shooter)",
        "class_Collector": "Recolector",
        "class_Skill Master": "Maestro de Habilidades",
        "class_Lucky Star": "Estrella de la Suerte",

        # Tab 3: Materials
        "search_label": "Buscar:",
        "category_label": "Categoría:",
        "stock_label": "Stock:",
        "rarity_label": "Rareza:",
        "stock_all": "Todo el Stock",
        "stock_in": "📦 En Stock (> 0)",
        "stock_low": "⚠️ Stock Bajo (< 10)",
        "stock_out": "❌ Agotado (0)",
        "floors_label": "Pisos de la Torre:",
        "floor_all": "🌐 Todos",
        "floor_dod": "🏢 1F-10F (DOD)",
        "floor_we": "🏭 11F-20F (WE)",
        "floor_cw": "🏰 21F-30F (CW)",
        "floor_milk": "🏟️ 31F-40F (MILK)",
        "floor_battle": "🌌 41F-50F (Battle)",
        "floor_tengoku": "👑 51F+ (Tengoku)",
        "coin_locker_btn": "📦 Depositar en Almacén",
        "max_all_mats_btn": "💎 Stock Máximo (x100 de Todo)",
        "mat_name_col": "Material",
        "mat_cat_col": "Categoría",
        "mat_rare_col": "Rareza",
        "mat_stock_col": "Stock",

        # Tab 4: Decals
        "decal_events_label": "Eventos y Colabs:",
        "decal_styles_label": "Estilos Tácticos:",
        "event_all": "🌐 Todas",
        "event_wot": "💥 World of Tanks",
        "event_nmh": "⚔️ No More Heroes",
        "event_k7": "🎯 Killer7",
        "event_gr": "🌀 Gravity Rush",
        "event_tengoku": "🗼 Tengoku & Meta",
        "style_all": "Todos",
        "style_addicts": "⚔️ Addicts",
        "style_crit": "💥 Crítico",
        "style_tank": "🛡️ Tanque",
        "style_vamp": "🩸 Vampiro",
        "style_farm": "📦 Farmeo",
        "style_sets": "🎭 Sets",
        "poss_label": "Posesión:",
        "poss_all": "Todas",
        "poss_owned": "📦 Poseídas (> 0)",
        "poss_missing": "❌ Faltantes (0)",
        "type_label": "Tipo:",
        "type_all": "Todas",
        "type_p": "Premium (_P)",
        "type_std": "Estándar",
        "unlock_all_decals_btn": "✨ Desbloquear Todas",
        "meta_pack_btn": "🏆 Pack Meta",
        "decal_qty_label": "Copias:",
        "apply_copies_btn": "Establecer Copias",
        "decal_name_col": "Calcomanía",
        "decal_rare_col": "Rareza",
        "decal_id_col": "ID Oficial",
        "decal_prem_col": "Tipo",
        "decal_count_col": "Cantidad",

        # Tab 5: Blueprints & Gear
        "gear_cat_label": "Pieza:",
        "gear_cat_all": "Todas las Piezas",
        "gear_cat_weapons": "🗡️ Armas",
        "gear_cat_helmets": "🪖 Cascos",
        "gear_cat_bodies": "👕 Pechos",
        "gear_cat_pants": "👖 Pantalones",
        "faction_label": "Facción:",
        "faction_all": "Todas las Facciones",
        "dmg_label": "Daño:",
        "dmg_all": "Todos los Tipos",
        "dmg_slash": "🗡️ Corte (Slash)",
        "dmg_blunt": "🔨 Golpe (Blunt)",
        "dmg_pierce": "🏹 Perforación (Pierce)",
        "dmg_fire": "🔥 Fuego (Burn)",
        "dmg_elec": "⚡ Electricidad (Electric)",
        "dmg_poison": "🧪 Veneno (Poison)",
        "bp_poss_all": "Todo el Estado",
        "bp_poss_storage": "📦 En Almacén (> 0)",
        "bp_poss_store": "⭐ Desbloqueados en Tienda (+4)",
        "bp_poss_rnd": "🔨 En I+D (REMODEL / MAP)",
        "bp_poss_locked": "❌ Bloqueados (Faltantes)",
        "level_label": "Nivel:",
        "unlock_in_store_btn": "⭐ Desbloquear en Tienda",
        "send_1_storage_btn": "📦 Enviar 1 u. al Almacén",
        "deposit_kit_btn": "🔨 Depositar Kit de Forja (+10 u.)",
        "view_set_btn": "👘 Ver Conjunto",
        "no_set_btn": "👘 No pertenece a un conjunto",
        "infinite_durability_btn": "✨ Durabilidad Infinita (999,999) en Todo",
        "massive_ammo_btn": "🎯 Munición Máxima (9,999) en Armas",
        "upgrade_19_btn": "⚡ Subir Todo a Nivel +19",
        "unlock_all_bp_btn": "📜 Desbloquear Todos los Planos (+4)",
        "inject_set_btn": "🌓 Inyectar Set Completo al Almacén",
        "forge_status_prefix": "Forja:",
        "storage_prefix": "Almacén:",
        "bag_prefix_status": "Bolsa:",
        "def_base_label": "Defensa Base:",
        "atk_base_label": "Ataque Base:",
        "dur_label": "Durabilidad:",

        # Tab 6: Hub & TDM
        "hub_custom_title": "Personalizaciones de la Sala de Espera (Hub)",
        "unlock_all_custom_btn": "🎨 Desbloquear Todas las Personalizaciones (Pisos/Fuentes)",
        "gyaku_title": "Tienda Ambulante Gyaku-Funsha",
        "reset_gyaku_btn": "⏱️ Reiniciar Tiempo de Gyaku-Funsha (0s / Disponible)",
        "deathboxes_title": "Cajas de Muerte Pendientes",
        "instant_deathboxes_btn": "🎁 Abrir Cajas de Muerte al Instante",
        "quests_title": "Misiones Oficiales de la Torre de Barbas",
        "complete_quests_btn": "📜 Completar Todas las Misiones (6,252 Misiones)",
        "magazines_title": "Colección de Revistas de Tío Death",
        "unlock_magazines_btn": "📖 Leer Todas las Revistas (36 Revistas)",
        "jukebox_title": "Radio Jukebox de la Sala de Espera",
        "unlock_jukebox_btn": "📻 Desbloquear Toda la Música y Jukebox",

        # Tab 7: Advanced Modifiers
        "bag_expand_title": "Bolsa de Muerte (Death Bag)",
        "bag_expand_btn": "🎒 Expandir Capacidad de Bolsa a 50 Ranuras",
        "free_cont_title": "Continuaciones Gratuitas Ilimitadas",
        "free_cont_btn": "♾️ Establecer Continuaciones Gratuitas",
        "rare_mats_title": "Inyector de Metales Reversión y Materiales Raros",
        "rare_mats_btn": "💎 Inyectar Lote de Metales Raros (+10 c/u)",

        # Dialogs
        "dialog_armor_viewer_title": "👘 Visor Oficial de Sets y Tiers de Armadura (Wiki.gg)",
        "dialog_armor_set_label": "👘 CONJUNTO DE ARMADURA:",
        "dialog_evolution_label": "Evolución / Nivel:",
        "dialog_preview_title": "🧍 Previsualización del Conjunto (Modelo 3D Oficial)",
        "dialog_stats_title": "Estadísticas del Conjunto en este Tier",
        "dialog_actions_title": "Acciones del Conjunto",
        "dialog_inject_tier_btn": "📦 Depositar este Tier Completo al Almacén",
        "dialog_unlock_tier_btn": "⭐ Desbloquear Planos de este Tier (+4)",
        "dialog_resistances": "Resistencias Elementales:",
        "dialog_inventory_title": "📋 Visor de Inventario Completo en Partida (Almacén y Mochila)",
        "dialog_smart_analyzer_title": "🧠 Analizador Inteligente de Inventario y Forja (R&D)",
        "dialog_smart_analyzer_sub": "Calcula las necesidades exactas de tus recetas activas en I+D para abastecer tu almacén sin saturarlo ni meter cosas de más.",
        "res_slash": "Corte",
        "res_blunt": "Golpe",
        "res_pierce": "Perforación",
        "res_fire": "Fuego",
        "res_elec": "Electricidad",
        "res_poison": "Veneno",

        # Updater Dialog
        "updater_avail_title": "⚡ Actualización Disponible - Let It Die Save Editor",
        "updater_avail_header": "🚀 ¡NUEVA VERSIÓN DISPONIBLE!",
        "updater_current_vs_new": "Versión actual: v{current}  ➔  Nueva versión: v{remote}",
        "updater_changelog_title": "Novedades y Mejoras:",
        "updater_safe_notice": "Tus partidas guardadas se conservarán 100% seguras.",
        "updater_btn_now": "⚡ ACTUALIZAR AHORA",
        "updater_btn_later": "Más tarde",
        "updater_up_to_date": "¡Tienes la versión más reciente (v{version})!",
        "updater_check_err": "No se pudo comprobar actualizaciones:\n{error}",
        "updater_success": "¡El editor se ha actualizado correctamente!\n\nReinicia el programa para aplicar todas las mejoras.",
        "updater_error": "No se pudo completar la actualización automática:\n\n{error}",

        # General Notifications
        "save_success": "¡Partida guardada y respaldada exitosamente!",
        "backup_success": "Copia de seguridad manual creada exitosamente:\n{path}",
        "action_complete": "Acción completada con éxito.",
        "notice": "Aviso",
        "error": "Error",
        "confirm": "Confirmar",
    },

    "en": {
        # App & Header
        "app_title": "LET IT DIE - Deep Save Editor Pro v2.2.0 (Master Cyberpunk Edition)",
        "save_file": "SAVE FILE (.sav):",
        "browse": "📁 Browse...",
        "reload": "🔄 Reload",
        "backup": "🛡️ Backup",
        "armor_sets": "👘 Armor Sets",
        "rnd_analyzer": "🧠 R&D Analyzer",
        "updates": "⚡ Updates",
        "save_game": "💾 SAVE GAME",
        "lang_label": "🌐 Language:",
        "no_save_detected": "No save file automatically detected. Click 'Browse' to select your .sav file",
        
        # Dashboard
        "fighter_prefix": "Fighter:",
        "base_rank_prefix": "Base Rank:",
        "tdm_prefix": "🏆 TDM:",
        "bag_prefix": "Bag:",
        "slots_suffix": "slots",
        
        # Tabs
        "tab_currencies": " Currencies & VIP ",
        "tab_fighters": " Fighters (Freezer) ",
        "tab_materials": " Materials & Forge (106) ",
        "tab_decals": " Decals & Skills (626) ",
        "tab_blueprints": " Chokufunsha Blueprints (1,370) ",
        "tab_mastery": " Weapon Masteries ",
        "tab_tower": " Tower & Master Unlocks ",
        "tab_advanced": " Encyclopedia & Backups ",

        # Tab 1: Player & Currencies
        "currencies_title": "Main Currencies (Coin Locker & Bank)",
        "kill_coins": "Kill Coins (KC):",
        "death_metals": "Death Metals (DM):",
        "splithium": "SPLithium (SPL):",
        "bloodnium": "Bloodnium (BL):",
        "recycle_points": "Recycle Points (RE):",
        "global_max_res": "⭐ MAX ALL RESOURCES (x9,999,999)",
        "quick_exchange": "Quick Currency Packs:",
        "kc_pack_1m": "🪙 +1,000,000 KC",
        "dm_pack_100": "💎 +100 DM",
        "spl_pack_1m": "⚡ +1,000,000 SPL",
        "bl_pack_50k": "🩸 +50,000 BL",
        "vip_express_pass": "VIP Express Pass:",
        "days": "days",
        "apply_vip": "Apply Days",
        "unlimited_vip": "🎫 Unlimited VIP Pass (365 days + 99 tickets)",
        "mystery_bags": "TDM Mystery Bags:",
        "mystery_qty": "Quantity each:",
        "add_bags_btn": "Add Bags",
        "all_bags_pack": "🎁 All Mystery Bags Pack (Bronze/Silver/Gold/Rainbow)",
        "storage_limits": "Max Bank & SPL Tank Capacity:",
        "bank_cap": "KC Bank:",
        "tank_cap": "SPL Tank:",
        "apply_caps": "Apply Limits",
        "max_storage_btn": "📦 Max Storage Locker Capacity (1,500 slots)",

        # Tab 2: Fighters
        "fighter_roster": "Fighter Freezer Roster",
        "fighter_stats_title": "Fighter Attributes & Stats",
        "f_name": "Name:",
        "f_class": "Class:",
        "f_tier": "Grade / Tier:",
        "f_level": "Level:",
        "f_hp": "Health (HP):",
        "f_stm": "Stamina (STM):",
        "f_str": "Strength (STR):",
        "f_dex": "Dexterity (DEX):",
        "f_vit": "Vitality (VIT):",
        "f_luk": "Luck (LUK):",
        "max_stats_btn": "⭐ MAX LEVEL AND STATS",
        "unlock_tier8_btn": "👑 UNLOCK TIER 8 (GOD TIER)",
        "revive_healed_btn": "❤️ Revive & Heal Fighter",
        "revive_all_btn": "❤️ Revive All Fighters",
        "equip_preset_direct": "🥋 EQUIP PRESET DIRECTLY ON THIS FIGHTER",
        "equipped_decals_title": "Equipped Decals in Active Slots",
        "slot_prefix": "Slot",
        
        # Fighter Classes
        "class_All-Rounder": "All-Rounder",
        "class_Striker": "Striker",
        "class_Defender": "Defender",
        "class_Attacker": "Attacker",
        "class_Shooter": "Shooter",
        "class_Collector": "Collector",
        "class_Skill Master": "Skill Master",
        "class_Lucky Star": "Lucky Star",

        # Tab 3: Materials
        "search_label": "Search:",
        "category_label": "Category:",
        "stock_label": "Stock:",
        "rarity_label": "Rarity:",
        "stock_all": "All Stock",
        "stock_in": "📦 In Stock (> 0)",
        "stock_low": "⚠️ Low Stock (< 10)",
        "stock_out": "❌ Out of Stock (0)",
        "floors_label": "Tower Floors:",
        "floor_all": "🌐 All",
        "floor_dod": "🏢 1F-10F (DOD)",
        "floor_we": "🏭 11F-20F (WE)",
        "floor_cw": "🏰 21F-30F (CW)",
        "floor_milk": "🏟️ 31F-40F (MILK)",
        "floor_battle": "🌌 41F-50F (Battle)",
        "floor_tengoku": "👑 51F+ (Tengoku)",
        "coin_locker_btn": "📦 Deposit into Storage",
        "max_all_mats_btn": "💎 Max Storage Stock (x100 of All)",
        "mat_name_col": "Material",
        "mat_cat_col": "Category",
        "mat_rare_col": "Rarity",
        "mat_stock_col": "Stock",

        # Tab 4: Decals
        "decal_events_label": "Events & Collabs:",
        "decal_styles_label": "Tactical Styles:",
        "event_all": "🌐 All",
        "event_wot": "💥 World of Tanks",
        "event_nmh": "⚔️ No More Heroes",
        "event_k7": "🎯 Killer7",
        "event_gr": "🌀 Gravity Rush",
        "event_tengoku": "🗼 Tengoku & Meta",
        "style_all": "All",
        "style_addicts": "⚔️ Addicts",
        "style_crit": "💥 Critical",
        "style_tank": "🛡️ Tank",
        "style_vamp": "🩸 Vampire",
        "style_farm": "📦 Farming",
        "style_sets": "🎭 Sets",
        "poss_label": "Possession:",
        "poss_all": "All",
        "poss_owned": "📦 Possessed (> 0)",
        "poss_missing": "❌ Missing (0)",
        "type_label": "Type:",
        "type_all": "All",
        "type_p": "Premium (_P)",
        "type_std": "Standard",
        "unlock_all_decals_btn": "✨ Unlock All",
        "meta_pack_btn": "🏆 Meta Pack",
        "decal_qty_label": "Copies:",
        "apply_copies_btn": "Set Copies",
        "decal_name_col": "Decal Name",
        "decal_rare_col": "Rarity",
        "decal_id_col": "Official ID",
        "decal_prem_col": "Type",
        "decal_count_col": "Count",

        # Tab 5: Blueprints & Gear
        "gear_cat_label": "Piece:",
        "gear_cat_all": "All Pieces",
        "gear_cat_weapons": "🗡️ Weapons",
        "gear_cat_helmets": "🪖 Helmets",
        "gear_cat_bodies": "👕 Bodies",
        "gear_cat_pants": "👖 Pants",
        "faction_label": "Faction:",
        "faction_all": "All Factions",
        "dmg_label": "Damage:",
        "dmg_all": "All Damage Types",
        "dmg_slash": "🗡️ Slash",
        "dmg_blunt": "🔨 Blunt",
        "dmg_pierce": "🏹 Pierce",
        "dmg_fire": "🔥 Burn",
        "dmg_elec": "⚡ Electric",
        "dmg_poison": "🧪 Poison",
        "bp_poss_all": "All Forge States",
        "bp_poss_storage": "📦 In Storage (> 0)",
        "bp_poss_store": "⭐ Unlocked in Shop (+4)",
        "bp_poss_rnd": "🔨 In R&D (REMODEL / MAP)",
        "bp_poss_locked": "❌ Locked (Missing)",
        "level_label": "Level:",
        "unlock_in_store_btn": "⭐ Unlock in Shop",
        "send_1_storage_btn": "📦 Send 1 to Storage",
        "deposit_kit_btn": "🔨 Deposit Forge Kit (+10 pcs)",
        "view_set_btn": "👘 View Set",
        "no_set_btn": "👘 Does not belong to a set",
        "infinite_durability_btn": "✨ Infinite Durability (999,999) on All",
        "massive_ammo_btn": "🎯 Max Ammo (9,999) on Firearms",
        "upgrade_19_btn": "⚡ Upgrade All Gear to Level +19",
        "unlock_all_bp_btn": "📜 Unlock All Blueprints (+4)",
        "inject_set_btn": "🌓 Inject Full Set into Storage",
        "forge_status_prefix": "Forge:",
        "storage_prefix": "Storage:",
        "bag_prefix_status": "Bag:",
        "def_base_label": "Base Defense:",
        "atk_base_label": "Base Attack:",
        "dur_label": "Durability:",

        # Tab 6: Hub & TDM
        "hub_custom_title": "Waiting Room Decors & Customizations",
        "unlock_all_custom_btn": "🎨 Unlock All Customizations (Floors/Fountains)",
        "gyaku_title": "Gyaku-Funsha Wandering Shop",
        "reset_gyaku_btn": "⏱️ Reset Gyaku-Funsha Timer (0s / Available Now)",
        "deathboxes_title": "Pending Death Boxes",
        "instant_deathboxes_btn": "🎁 Open Pending Death Boxes Instantly",
        "quests_title": "Tower of Barbs Official Quests",
        "complete_quests_btn": "📜 Complete All Quests (6,252 Quests)",
        "magazines_title": "Uncle Death Magazine Collection",
        "unlock_magazines_btn": "📖 Read All Magazines (36 Magazines)",
        "jukebox_title": "Waiting Room Radio Jukebox",
        "unlock_jukebox_btn": "📻 Unlock Full Soundtrack & Jukebox",

        # Tab 7: Advanced Modifiers
        "bag_expand_title": "Death Bag Capacity",
        "bag_expand_btn": "🎒 Expand Death Bag to 50 Slots",
        "free_cont_title": "Unlimited Free Continues",
        "free_cont_btn": "♾️ Enable Free Continues",
        "rare_mats_title": "Reversal Metals & Rare Resources Injector",
        "rare_mats_btn": "💎 Inject Rare Metals Bundle (+10 each)",

        # Dialogs
        "dialog_armor_viewer_title": "👘 Official Armor Sets & Tiers Viewer (Wiki.gg)",
        "dialog_armor_set_label": "👘 ARMOR SET:",
        "dialog_evolution_label": "Evolution / Tier:",
        "dialog_preview_title": "🧍 Set Preview (Official 3D Model)",
        "dialog_stats_title": "Set Attributes in this Tier",
        "dialog_actions_title": "Set Actions",
        "dialog_inject_tier_btn": "📦 Deposit Complete Tier into Storage",
        "dialog_unlock_tier_btn": "⭐ Unlock Blueprints for this Tier (+4)",
        "dialog_resistances": "Elemental Resistances:",
        "dialog_inventory_title": "📋 Full In-Game Inventory Viewer (Coin Locker & Death Bag)",
        "dialog_smart_analyzer_title": "🧠 Smart Inventory & Forge Analyzer (R&D)",
        "dialog_smart_analyzer_sub": "Calculates exact material requirements for your active R&D recipes to stock your coin locker without clutter.",
        "res_slash": "Slash",
        "res_blunt": "Blunt",
        "res_pierce": "Pierce",
        "res_fire": "Fire",
        "res_elec": "Electric",
        "res_poison": "Poison",

        # Updater Dialog
        "updater_avail_title": "⚡ Update Available - Let It Die Save Editor",
        "updater_avail_header": "🚀 NEW VERSION AVAILABLE!",
        "updater_current_vs_new": "Current version: v{current}  ➔  New version: v{remote}",
        "updater_changelog_title": "What's New & Improvements:",
        "updater_safe_notice": "Your save games are 100% safe and untouched.",
        "updater_btn_now": "⚡ UPDATE NOW",
        "updater_btn_later": "Later",
        "updater_up_to_date": "You have the latest version (v{version})!",
        "updater_check_err": "Could not check for updates:\n{error}",
        "updater_success": "Editor updated successfully!\n\nPlease restart the application to apply all changes.",
        "updater_error": "Automatic update could not complete:\n\n{error}",

        # General Notifications
        "save_success": "Save game modified and backed up successfully!",
        "backup_success": "Manual backup created successfully:\n{path}",
        "action_complete": "Action completed successfully.",
        "notice": "Notice",
        "error": "Error",
        "confirm": "Confirm",
    }
}

def t(key, **kwargs):
    """
    Translates a key according to the active language.
    Falls back to English or key name if missing.
    """
    lang = get_language()
    val = TRANSLATIONS.get(lang, {}).get(key)
    if val is None:
        val = TRANSLATIONS.get("en", {}).get(key, key)
    if kwargs:
        try:
            return val.format(**kwargs)
        except Exception:
            return val
    return val

def get_item_name(item):
    """Returns the localized name of an equipment, decal, or material item."""
    if not item:
        return ""
    lang = get_language()
    if lang == "en":
        return item.get("name_en") or item.get("name_es") or item.get("name") or str(item.get("id", ""))
    else:
        return item.get("name_es") or item.get("name_en") or item.get("name") or str(item.get("id", ""))

def get_item_desc(item):
    """Returns the localized description of a decal or material item."""
    if not item:
        return ""
    lang = get_language()
    if lang == "en":
        return item.get("desc_en") or item.get("desc_es") or ""
    else:
        return item.get("desc_es") or item.get("desc_en") or ""

def get_set_name(set_obj):
    """Returns the localized set name."""
    if not set_obj:
        return ""
    lang = get_language()
    if lang == "en":
        return set_obj.get("name_en") or set_obj.get("name_es") or set_obj.get("id", "")
    else:
        return set_obj.get("name_es") or set_obj.get("name_en") or set_obj.get("id", "")
