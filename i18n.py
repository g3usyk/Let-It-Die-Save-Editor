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
        "app_title": "LET IT DIE - Deep Save Editor Pro (Master Cyberpunk Edition)",
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
        
        # Dashboard HUD
        "hud_fighter": "Luchador:",
        "hud_rank": "Rango Base:",
        "hud_tdm": "🏆 TDM: Diamante",
        "hud_bag": "Bolsa:",
        "hud_slots": "slots",
        
        # Tabs (Concise, fit without truncation)
        "tab_currencies": " Monedas & VIP ",
        "tab_fighters": " Luchadores ",
        "tab_materials": " Materiales ",
        "tab_decals": " Calcomanías ",
        "tab_blueprints": " Planos ",
        "tab_mastery": " Maestría ",
        "tab_tower": " Torre & TDM ",
        "tab_advanced": " Respaldos ",

        # Tab 1: Currencies & VIP
        "curr_box_title": "💰 Recursos y Divisas Principales",
        "dm_lbl": "Metales de Muerte (DM):",
        "kc_lbl": "Monedas Kill Coins (KC):",
        "spl_lbl": "Litio SPLithium (SPL):",
        "bl_lbl": "Sangrenio (Bloodnium):",
        "re_lbl": "Puntos de Reciclaje (RE):",
        "max_all_curr_btn": "⭐ MAXIMIZAR TODAS LAS DIVISAS AL TOPE",
        "wr_box_title": "🏦 Mejoras de Instalaciones de la Sala de Espera",
        "bank_lvl_lbl": "Nivel del Banco de KC (1-100):",
        "tank_lvl_lbl": "Nivel del Tanque de SPL (1-100):",
        "player_rank_lbl": "Rango de Jugador (1-100):",
        "apply_wr_btn": "💾 Guardar Mejoras",
        "max_wr_btn": "⭐ Maximizar al Nivel 100",
        "wr_hint": "ℹ️ El Rango y sus puntos oficiales se calculan y sincronizan automáticamente.",
        "vip_box_title": "👑 Pase Expreso Royal VIP",
        "vip_active": "Estado: ACTIVO • Expira en: {days} días ({date})",
        "vip_inactive": "Estado: Inactivo",
        "vip_days_lbl": "Días de Pase VIP:",
        "activate_vip_btn": "👑 Activar VIP",
        "vip_30d": "30 Días",
        "vip_90d": "90 Días",
        "vip_1y": "1 Año",
        "vip_10y": "10 Años",
        "account_perks_title": "🎒 Ventajas de Cuenta y Bolsa de Muerte",
        "account_summary_title": "📋 Resumen de Cuenta y Estado de Partida",
        "max_streak_btn": "🔥 Racha a 365 Días",
        "tw_playlog_title": "📊 Registro de Exploración de la Torre y Estadísticas",
        "tw_max_floor_lbl": "Piso Récord:",
        "tw_set_floor_btn": "🏆 Guardar Piso",
        "tw_interrupt_lbl": "Interrupciones de Torre:",
        "tw_reset_interrupt_btn": "🛡️ Limpiar Penalizaciones de Desconexión / Muerte",
        "tw_stats_title": "Estadísticas de Exploración:",

        # Tab 2: Fighters (Freezer)
        "f_freezer_title": "Luchadores en el Congelador (Fighter Freezer)",
        "f_col_name": "Luchador / Clase",
        "f_col_num": "#",
        "f_col_lvl": "Nivel",
        "f_col_state": "Estado",
        "f_state_alive": "Vivo",
        "f_state_dead": "Muerto",
        "f_tech_sheet": "Ficha Técnica del Luchador",
        "f_select_prompt": "Selecciona un luchador",
        "f_class_meta": "Clase: {cls} | Grado: Tier {grd} ★ | Nivel: {lvl}",
        "f_id_config": "Identidad y Configuración del Luchador",
        "f_lbl_name": "Nombre:",
        "f_lbl_class": "Clase:",
        "f_lbl_grade": "Grado (Tier ★):",
        "f_lbl_level": "Nivel (1-247):",
        "f_lbl_hp_cur": "Salud HP Actual:",
        "f_lbl_bag": "Bolsa (Slots):",
        "f_base_stats_box": "Nivel de Atributos Base (Puntos de Estadística 1 a 35)",
        "f_hp_vit": "HP (Vitalidad):",
        "f_stm_res": "STM (Resistencia):",
        "f_str_pow": "STR (Fuerza):",
        "f_dex_agi": "DEX (Destreza):",
        "f_vit_def": "VIT (Defensa):",
        "f_luk_luck": "LUK (Suerte):",
        "f_apply_btn": "💾 APLICAR CAMBIOS AL LUCHADOR",
        "f_revive_btn": "❤️ Revivir al 100%",
        "f_max_stats_btn": "⭐ Maximizar Stats (Lv 247)",
        "f_equipped_decals_box": "Calcomanías Equipadas en este Luchador",
        "f_slot_prefix": "Espacio",
        "f_slot_empty": "[Vacío]",
        "f_presets_box": "Presets de Calcomanías Meta (8 Slots)",
        "f_preset_btn": "🥋 EQUIPAR PRESET DIRECTO EN ESTE LUCHADOR",
        "f_inject_preset_btn": "📦 Inyectar Set al Inventario (x5 cada una)",

        # Tab 3: Materials & Storage
        "mat_search": "🔍 Buscar:",
        "mat_cat_lbl": "Categoría:",
        "mat_stock_lbl": "Stock:",
        "mat_rarity_lbl": "Rareza:",
        "mat_all": "Todos",
        "mat_in_stock": "📦 En Stock (> 0)",
        "mat_low_stock": "⚠️ Stock Bajo (< 10)",
        "mat_out_stock": "❌ Agotado (0)",
        "mat_floors_lbl": "Torre:",
        "mat_card_title": "Ficha Oficial de Material R&D",
        "mat_select_prompt": "Selecciona un material",
        "mat_cat_info": "Categoría: {cat} | Rareza: {rare} ({id})",
        "mat_in_storage": "📦 En tu Almacén: {qty} u.",
        "mat_none_in_storage": "📦 En tu Almacén: 0 u. (No tienes)",
        "mat_desc_default": "Material oficial de R&D para fabricar y mejorar armas y armaduras en Chokufunsha.",
        "mat_set_qty_lbl": "Añadir / Establecer:",
        "mat_set_btn": "Establecer",
        "mat_locker_cap_title": "Capacidad del Coin Locker",
        "mat_locker_status": "Almacén: {used:,} / {cap:,} casillas ocupadas ({free:,} libres)",
        "mat_expand_500": "+500 Casillas",
        "mat_expand_1000": "+1,000 Casillas",
        "mat_expand_max": "⭐ 6,000 (Tope)",
        "mat_expand_custom": "🚀 Personalizado...",
        "mat_locker_custom_prompt": "Capacidad actual: {cur:,} casillas ({occ:,} objetos guardados).\n\nIntroduce la capacidad deseada para el Coin Locker:\n\n💡 Recomendado para fluidez sin lag: 6,000 a 7,000 casillas.\n⚠️ Atención: Valores de 20,000 a 50,000 saturan el motor del juego y causan lag.",
        "mat_locker_limit_title": "Límite de Seguridad",
        "mat_locker_limit_msg": "Tienes {occ:,} objetos guardados en el almacén.\nNo se puede reducir por debajo de {occ:,} casillas para proteger tu equipo.",
        "mat_locker_updated_title": "Capacidad Actualizada",
        "mat_locker_updated_msg": "¡Almacén ajustado con éxito!\n\n• Capacidad anterior: {old:,} casillas\n• Nueva capacidad: {new:,} casillas ({occ:,} objetos guardados)\n\nSe ha sincronizado masters.db (COINLOCKER_EXPAND_LIMIT_COUNT = {new:,}) y soul.cl.\nGuardado automáticamente.",
        "mat_locker_status_bar": "Almacén ajustado de {old:,} a {new:,} casillas.",

        # Death Bag Masters Mod Dialogs
        "db_mod_box_title": "🎒 Mod de Bolsa en el Juego (masters.db)",
        "db_mod_status_active": "✅ Mod Activo: Base {base} slots (+VIP = {total} slots)",
        "db_mod_status_vanilla": "ℹ️ masters.db Original: 18 a 54 slots según clase (+10 VIP)",
        "db_mod_status_missing": "⚠️ masters.db no encontrado",
        "db_expand_btn": "🎒 Expandir a 60+ Slots",
        "db_restore_btn": "🔄 Restaurar Original",
        "db_expand_title": "🎒 Expandir Bolsa en masters.db",
        "db_expand_prompt": "Introduce la capacidad base de slots para todos los luchadores:\n\nValores sugeridos: 50, 60, 70, 80\n(Nota: Con el Pase VIP obtendrás +10 slots adicionales sobre este valor)",
        "db_expand_success_title": "Bolsa Modificada",
        "db_expand_success_msg": "¡Bolsa de luchadores ampliada con éxito en el juego!\n\n• Capacidad base para todas las clases: {target} slots\n• Con Pase VIP activo: {vip} slots\n\nArchivo modificado:\n{path}",
        "db_restore_title": "Restaurar Bolsa",
        "db_restore_prompt": "¿Deseas restaurar la capacidad oficial de la bolsa del juego (18-54 slots según clase)?",
        "db_restore_success_title": "Bolsa Restaurada",
        "db_restore_success_msg": "¡Capacidad de bolsa restaurada a los valores oficiales del juego!\n\nArchivo:\n{path}",

        # Tab 4: Decals & Skills
        "decal_search": "🔍 Buscar:",
        "decal_rare_lbl": "Rareza:",
        "decal_type_lbl": "Tipo:",
        "decal_poss_lbl": "Posesión:",
        "decal_all": "Todas",
        "decal_premium": "Premium (_P)",
        "decal_standard": "Estándar",
        "decal_owned": "📦 Poseídas (> 0)",
        "decal_missing": "❌ Faltantes (0)",
        "decal_pack_meta": "🏆 Pack Meta",
        "decal_unlock_all": "✨ Desbloquear Todas",
        "decal_copies_lbl": "Copias:",
        "decal_events_lbl": "🎯 Eventos:",
        "decal_event_all": "🌐 Todas",
        "decal_styles_lbl": "⚡ Estilos:",
        "decal_style_all": "Todos",
        "decal_style_crit": "💥 Crítico",
        "decal_style_tank": "🛡️ Tanque",
        "decal_style_vamp": "🩸 Vampiro",
        "decal_style_farm": "📦 Farmeo",
        "decal_style_sets": "🎭 Sets",
        "decal_col_icon": "Icono / Nombre Oficial",
        "decal_col_rare": "Rareza",
        "decal_col_id": "ID Calcomanía",
        "decal_col_type": "Tipo",
        "decal_col_qty": "Cantidad",
        "decal_card_title": "Ficha Técnica de la Calcomanía",
        "decal_select_prompt": "Selecciona una calcomanía",
        "decal_type_and_owned": "Tipo: {type} | Poseídas: x{cnt}",
        "decal_copies_edit_lbl": "Copias en Bolsa/Almacén:",
        "decal_set_btn": "Establecer",
        "decal_plus1": "+1 Copia",
        "decal_plus5": "+5 Copias",
        "decal_zero": "Agotar (0)",

        # Tab 5: Blueprints & Chokufunsha
        "bp_search": "🔍 Buscar:",
        "bp_slot_lbl": "Ranura:",
        "bp_slot_all": "Todos",
        "bp_slot_helmets": "🪖 Cascos",
        "bp_slot_bodies": "👕 Pechos",
        "bp_slot_legs": "👖 Piernas",
        "bp_slot_weapons": "⚔️ Armas",
        "bp_faction_lbl": "Facción:",
        "bp_fac_all": "Todas",
        "bp_fac_dod": "🔨 D.O.D. ARMS",
        "bp_fac_we": "🎖️ WAR ENSEMBLE",
        "bp_fac_cw": "🕯️ CANDLE WOLF",
        "bp_fac_milk": "🥛 M.I.L.K.",
        "bp_fac_44ce": "⚡ 4 FORCEMEN & TENGOKU",
        "bp_fac_jackals": "🕶️ JACKALS",
        "bp_fac_re": "♻️ RE (Reciclador)",
        "bp_fac_spe": "🎭 Especial / Evento",
        "bp_fac_gen": "⚔️ General / Otras",
        "bp_view_sets_btn": "👘 Visor de Sets por Nivel",
        "bp_poss_lbl": "Posesión:",
        "bp_poss_all": "Todos",
        "bp_poss_storage": "📦 En Almacén (> 0)",
        "bp_poss_shop": "⭐ Desbloqueados en Tienda (+4)",
        "bp_poss_rnd": "🔨 En I+D (REMODEL / MAP)",
        "bp_poss_locked": "❌ Bloqueados (Faltantes)",
        "bp_dmg_lbl": "Daño:",
        "bp_dmg_all": "Todos",
        "bp_dmg_slash": "🗡️ Corte (Slash)",
        "bp_dmg_blunt": "🔨 Golpe (Blunt)",
        "bp_dmg_pierce": "🏹 Perforación (Pierce)",
        "bp_dmg_fire": "🔥 Fuego (Burn)",
        "bp_dmg_elec": "⚡ Electricidad (Electric)",
        "bp_dmg_poison": "🧪 Veneno (Poison)",
        "bp_unlock_all_lbl": "Nivel a desbloquear:",
        "bp_repair_btn": "🔧 Reparar I+D",
        "bp_collabs_lbl": "🎯 Eventos:",
        "bp_collab_all": "🌐 Todos",
        "bp_collab_re": "♻️ Ediciones RE",
        "bp_col_item": "Plano / Nombre Oficial",
        "bp_col_slot": "Ranura",
        "bp_col_faction": "Facción",
        "bp_col_status": "Estado Forja",
        "bp_col_storage": "Almacén",
        "bp_col_bag": "Bolsa",
        "bp_col_id": "ID Plano",
        "bp_card_title": "Ficha Técnica de Plano Chokufunsha",
        "bp_select_prompt": "Selecciona un equipo",
        "bp_status_info": "Forja: {status} | Almacén: {storage} | Bolsa: {bag}",
        "bp_base_def": "Defensa Base: {def_b} (A +4: {def_4}) | Durabilidad: {dur}",
        "bp_base_atk": "Ataque Base: {atk_b} (A +4: {atk_4}) | Durabilidad: {dur}",
        "bp_view_set_btn": "👘 Ver Conjunto en Visor de Sets",
        "bp_no_set": "👘 No pertenece a un conjunto",
        "bp_indiv_actions_title": "Acciones Individuales para esta Pieza",
        "bp_lvl_lbl": "Nivel:",
        "bp_unlock_shop_btn": "⭐ Desbloquear en Tienda",
        "bp_send_storage_btn": "📦 Enviar 1 u. al Almacén",
        "bp_deposit_kit_btn": "🛠️ Depositar Kit de Forja (+10 u.)",
        "bp_mass_actions_title": "Modificadores y Mejoras Masivas",
        "bp_inf_dur_btn": "✨ Durabilidad Infinita (999,999) en Todo",
        "bp_inf_ammo_btn": "🎯 Munición Máxima (9,999) en Armas",
        "bp_upg_all19_btn": "⚡ Mejorar Todo a Nivel +19 (Uncapped)",
        "bp_upg_all24_btn": "🔥 Mejorar Todo a Nivel +24 (Máximo Uncapped)",
        "bp_unlock_all_btn": "🌟 DESBLOQUEAR TODO",

        # Tab 6: Weapon Masteries
        "wm_target_lvl_lbl": "Nivel Deseado:",
        "wm_set_all_btn": "⭐ Establecer TODAS las Maestrías",
        "wm_col_type": "Tipo de Arma",
        "wm_col_code": "Código Interno",
        "wm_col_lvl": "Nivel de Maestría",
        "wm_col_exp": "Puntos de Experiencia (EXP)",
        "wm_lvl_val": "Nivel {lvl} / 20",

        # Tab 7: Tower & TDM Unlocks
        "tw_left_title": "Torre de Barbs, Ascensores y Stamp Rally",
        "tw_elev_title": "🛗 Ascensores y Pisos de la Torre (1 al 51+ Tengoku)",
        "tw_elev_sub": "Desbloquea el acceso directo a todos los pisos del 1 al 40, Battle Royale 41-50 y Tengoku.",
        "tw_elev_btn": "🛗 Desbloquear TODOS los Ascensores y Pisos",
        "tw_stamp_title": "🎯 Stamp Rally 100% Perfecto (Sellos del Tío Death)",
        "tw_stamp_sub": "Marca todos los sellos de la Torre en PERFECT. Desbloquea la Guadaña del Tío Death.",
        "tw_stamp_btn": "⭐ Completar Sellos en PERFECT (Desbloquea Guadaña)",
        "tw_bag_title": "🎒 Expansión de la Bolsa de la Muerte",
        "tw_bag_cap_lbl": "Capacidad de Slots:",
        "tw_bag_btn": "🎒 Expandir Bolsa",
        "tw_cont_title": "♾️ Revives / Continues Gratuitos Ilimitados",
        "tw_cont_lbl": "Continues Gratis:",
        "tw_cont_btn": "♾️ Establecer Continues",
        "tw_shop_title": "🛒 Tienda Secreta y Cajas de Muerte",
        "tw_shop_btn": "🛒 Resetear Cooldown Tienda Gyaku-Funsha",
        "tw_boxes_btn": "📦 Abrir Inmediatamente Cajas de Muerte (Lost Bags)",
        "tw_right_title": "Tokyo Death Metro, Buzón y Compendios",
        "tw_tdm_title": "🏆 Rango y Puntuación TDM (Tokyo Death Metro)",
        "tw_rank_lbl": "Rango:",
        "tw_apply_btn": "🏆 Aplicar",
        "tw_inbox_title": "🎁 Inyector a la Caja de Recompensas (Rewards Box)",
        "tw_inbox_sub": "Envía recursos directamente a tu buzón para acumularlos sin límite de capacidad.",
        "tw_res_lbl": "Recurso:",
        "tw_qty_lbl": "Cantidad:",
        "tw_inbox_btn": "📬 Enviar Regalo al Buzón",
        "tw_comp_title": "📚 Compendios y Personalización de Sala",
        "tw_comp_mats_btn": "🍄 Completar Compendios del Tío Death (63 Setas + 24 Bestias)",
        "tw_comp_room_btn": "🎨 Desbloquear Todas las Personalizaciones de Sala de Espera (113)",
        "tw_comp_quests_btn": "📜 Completar Todas las Misiones Oficiales (232 Quests)",
        "tw_comp_mags_btn": "📖 Desbloquear Colección de Revistas (36) y Radio Jukebox",

        # Tab 8: Backups & Advanced
        "bak_title": "🛡️ Gestor de Respaldos de Seguridad (.bak)",
        "bak_col_file": "Archivo de Respaldo",
        "bak_col_date": "Fecha de Creación",
        "bak_col_size": "Tamaño",
        "bak_create_btn": "🛡️ Crear Nuevo Respaldo",
        "bak_restore_btn": "🔄 Restaurar Respaldo",
        "bak_tools_title": "🛠️ Herramientas Avanzadas y Enlaces Oficiales",
        "bak_json_lbl": "Exportar / Importar Partida en JSON legible:",
        "bak_export_json": "📤 Exportar a JSON",
        "bak_import_json": "📥 Importar desde JSON",
        "bak_links_lbl": "Enlaces y Recursos de la Comunidad:",
        "bak_links_txt": "• Wiki Oficial: letitdie.wiki.gg\n• Forja y R&D: Chokufunsha Complete DB\n• Calculadora de Daño y Stats",

        # Armor Sets Dialog
        "dialog_armor_viewer_title": "👘 Visor Oficial de Sets y Tiers de Armadura (Wiki.gg)",
        "dialog_armor_set_label": "👘 CONJUNTO DE ARMADURA:",
        "dialog_evolution_label": "Evolución / Nivel:",
        "dialog_preview_title": "🧍 Previsualización del Conjunto (Modelo 3D Oficial)",
        "dialog_slot_head": "🪖 CASCO (Head)",
        "dialog_slot_body": "👕 PECHERA (Body Armor)",
        "dialog_slot_legs": "👖 PANTALONES (Legs / Pants)",
        "dialog_slot_weapon": "⚔️ ARMA CARACTERÍSTICA (Signature Weapon)",
        "dialog_atk_base": "⚔️ Ataque Base: {atk} (A +4: ~{atk4})  |  Durabilidad: {dur}",
        "dialog_weapon_paired": "🔥 Arma característica oficial emparejada con este conjunto de armadura.",
        "dialog_def_base": "🛡️ Defensa Base: {def_b} (A +4: {def4})  |  Durabilidad: {dur}",
        "dialog_res_slash": "Corte",
        "dialog_res_blunt": "Golpe",
        "dialog_res_pierce": "Perf",
        "dialog_res_fire": "Fuego",
        "dialog_res_elec": "Elec",
        "dialog_res_poison": "Veneno",
        "dialog_shop_unlocked": "⭐ Tienda: Desbloqueado (+{lvl})",
        "dialog_shop_lvl": "🔨 Tienda: Nivel +{lvl}",
        "dialog_shop_locked": "❌ Tienda: Bloqueado",
        "dialog_storage_cnt": "📦 Almacén: {cnt} u.",
        "dialog_bag_cnt": "🎒 Mochila: {cnt} u.",
        "dialog_unlock_piece_btn": "⭐ Desbloquear +4",
        "dialog_add_piece_btn": "🎁 +1 al Almacén",
        "dialog_unlock_full_tier_btn": "⭐ Desbloquear Set + Arma Completa (Tier a +4 en Tienda y Almacén)",
        "dialog_add_full_tier_btn": "🎁 Añadir Set Completo al Almacén (Casco + Pechera + Piernas)",
        "dialog_close_btn": "Cerrar",

        # Inventory Viewer & Smart Analyzer
        "dialog_inventory_title": "📋 Visor de Inventario Completo en Partida (Almacén y Mochila)",
        "dialog_smart_analyzer_title": "🧠 Analizador Inteligente de Inventario y Forja (R&D)",
        "dialog_smart_analyzer_sub": "Calcula las necesidades exactas de tus recetas activas en I+D para abastecer tu almacén sin saturarlo ni meter cosas de más.",

        # General
        "notice": "Aviso",
        "error": "Error",
        "confirm": "Confirmar",
        "saved_ok": "¡Partida guardada exitosamente!",
        "auto_saved_ok": "Guardado automáticamente."
    },

    "en": {
        # App & Header
        "app_title": "LET IT DIE - Deep Save Editor Pro (Master Cyberpunk Edition)",
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
        
        # Dashboard HUD
        "hud_fighter": "Fighter:",
        "hud_rank": "Base Rank:",
        "hud_tdm": "🏆 TDM: Diamond",
        "hud_bag": "Bag:",
        "hud_slots": "slots",
        
        # Tabs (Concise, fit without truncation)
        "tab_currencies": " Currencies ",
        "tab_fighters": " Fighters ",
        "tab_materials": " Materials ",
        "tab_decals": " Decals ",
        "tab_blueprints": " Blueprints ",
        "tab_mastery": " Mastery ",
        "tab_tower": " Tower & TDM ",
        "tab_advanced": " Backups ",

        # Tab 1: Currencies & VIP
        "curr_box_title": "💰 Main Resources & Currencies",
        "dm_lbl": "Death Metals (DM):",
        "kc_lbl": "Kill Coins (KC):",
        "spl_lbl": "SPLithium (SPL):",
        "bl_lbl": "Bloodnium (BL):",
        "re_lbl": "Recycle Points (RE):",
        "max_all_curr_btn": "⭐ MAX ALL CURRENCIES & RESOURCES",
        "wr_box_title": "🏦 Waiting Room Facilities & Capacities",
        "bank_lvl_lbl": "KC Bank Level (1-100):",
        "tank_lvl_lbl": "SPL Tank Level (1-100):",
        "player_rank_lbl": "Player Rank (1-100):",
        "apply_wr_btn": "💾 Save Upgrades",
        "max_wr_btn": "⭐ Max All to Level 100",
        "wr_hint": "ℹ️ Player Rank and official points are calculated and synced automatically.",
        "vip_box_title": "👑 Royal Express VIP Pass",
        "vip_active": "Status: ACTIVE • Expires in: {days} days ({date})",
        "vip_inactive": "Status: Inactive",
        "vip_days_lbl": "VIP Pass Days:",
        "activate_vip_btn": "👑 Activate VIP",
        "vip_30d": "30 Days",
        "vip_90d": "90 Days",
        "vip_1y": "1 Year",
        "vip_10y": "10 Years",
        "account_perks_title": "🎒 Account Perks & Death Bag Expansion",
        "account_summary_title": "📋 Account Profile & Save Metadata",
        "max_streak_btn": "🔥 Streak to 365 Days",
        "tw_playlog_title": "📊 Tower Exploration Records & Playlog",
        "tw_max_floor_lbl": "Max Recorded Floor:",
        "tw_set_floor_btn": "🏆 Save Max Floor",
        "tw_interrupt_lbl": "Tower Disconnections:",
        "tw_reset_interrupt_btn": "🛡️ Reset Death / Disconnection Penalties",
        "tw_stats_title": "Exploration Statistics:",

        # Tab 2: Fighters (Freezer)
        "f_freezer_title": "Fighters in Freezer Roster",
        "f_col_name": "Fighter / Class",
        "f_col_num": "#",
        "f_col_lvl": "Level",
        "f_col_state": "Status",
        "f_state_alive": "Alive",
        "f_state_dead": "Dead",
        "f_tech_sheet": "Fighter Technical Profile",
        "f_select_prompt": "Select a fighter",
        "f_class_meta": "Class: {cls} | Grade: Tier {grd} ★ | Level: {lvl}",
        "f_id_config": "Fighter Identity & Configuration",
        "f_lbl_name": "Name:",
        "f_lbl_class": "Class:",
        "f_lbl_grade": "Grade (Tier ★):",
        "f_lbl_level": "Level (1-247):",
        "f_lbl_hp_cur": "Current HP:",
        "f_lbl_bag": "Bag (Slots):",
        "f_base_stats_box": "Base Attribute Points (Stat Points 1 to 35)",
        "f_hp_vit": "HP (Vitality):",
        "f_stm_res": "STM (Stamina):",
        "f_str_pow": "STR (Strength):",
        "f_dex_agi": "DEX (Dexterity):",
        "f_vit_def": "VIT (Defense):",
        "f_luk_luck": "LUK (Luck):",
        "f_apply_btn": "💾 APPLY CHANGES TO FIGHTER",
        "f_revive_btn": "❤️ Revive to 100% HP",
        "f_max_stats_btn": "⭐ Max Stats (Lv 247)",
        "f_equipped_decals_box": "Equipped Decals on this Fighter",
        "f_slot_prefix": "Slot",
        "f_slot_empty": "[Empty]",
        "f_presets_box": "Meta Decal Presets (8 Slots)",
        "f_preset_btn": "🥋 EQUIP PRESET DIRECTLY ON THIS FIGHTER",
        "f_inject_preset_btn": "📦 Inject Set into Inventory (x5 each)",

        # Tab 3: Materials & Storage
        "mat_search": "🔍 Search:",
        "mat_cat_lbl": "Category:",
        "mat_stock_lbl": "Stock:",
        "mat_rarity_lbl": "Rarity:",
        "mat_all": "All",
        "mat_in_stock": "📦 In Stock (> 0)",
        "mat_low_stock": "⚠️ Low Stock (< 10)",
        "mat_out_stock": "❌ Out of Stock (0)",
        "mat_floors_lbl": "Tower:",
        "mat_card_title": "Official R&D Material Details",
        "mat_select_prompt": "Select a material",
        "mat_cat_info": "Category: {cat} | Rarity: {rare} ({id})",
        "mat_in_storage": "📦 In your Storage: {qty} pcs.",
        "mat_none_in_storage": "📦 In your Storage: 0 pcs. (Out of Stock)",
        "mat_desc_default": "Official R&D crafting and upgrade material for Chokufunsha gear.",
        "mat_set_qty_lbl": "Add / Set Qty:",
        "mat_set_btn": "Set Qty",
        "mat_locker_cap_title": "Coin Locker Capacity",
        "mat_locker_status": "Storage: {used:,} / {cap:,} slots used ({free:,} free)",
        "mat_expand_500": "+500 Slots",
        "mat_expand_1000": "+1,000 Slots",
        "mat_expand_max": "⭐ 6,000 (Max)",
        "mat_expand_custom": "🚀 Custom...",
        "mat_locker_custom_prompt": "Current capacity: {cur:,} slots ({occ:,} items stored).\n\nEnter desired capacity for the Coin Locker:\n\n💡 Recommended for smooth, lag-free gameplay: 6,000 to 7,000 slots.\n⚠️ Notice: Values above 20,000 overload the game engine and cause severe UI lag.",
        "mat_locker_limit_title": "Safety Limit",
        "mat_locker_limit_msg": "You currently have {occ:,} items stored in your Coin Locker.\nCapacity cannot be reduced below {occ:,} slots to protect your equipment.",
        "mat_locker_updated_title": "Capacity Updated",
        "mat_locker_updated_msg": "Coin Locker successfully updated!\n\n• Previous capacity: {old:,} slots\n• New capacity: {new:,} slots ({occ:,} items stored)\n\nSynchronized masters.db (COINLOCKER_EXPAND_LIMIT_COUNT = {new:,}) and soul.cl.\nSaved automatically.",
        "mat_locker_status_bar": "Storage adjusted from {old:,} to {new:,} slots.",

        # Death Bag Masters Mod Dialogs
        "db_mod_box_title": "🎒 In-Game Death Bag Mod (masters.db)",
        "db_mod_status_active": "✅ Mod Active: Base {base} slots (+VIP = {total} slots)",
        "db_mod_status_vanilla": "ℹ️ Official masters.db: 18 to 54 slots by class (+10 VIP)",
        "db_mod_status_missing": "⚠️ masters.db not found",
        "db_expand_btn": "🎒 Expand to 60+ Slots",
        "db_restore_btn": "🔄 Restore Official",
        "db_expand_title": "🎒 Expand Death Bag in masters.db",
        "db_expand_prompt": "Enter base bag capacity for all fighters:\n\nSuggested values: 50, 60, 70, 80\n(Note: Active VIP pass provides +10 bonus slots on top of this value)",
        "db_expand_success_title": "Death Bag Expanded",
        "db_expand_success_msg": "Fighter Death Bag successfully expanded in the game!\n\n• Base capacity for all classes: {target} slots\n• With active VIP pass: {vip} slots\n\nModified file:\n{path}",
        "db_restore_title": "Restore Death Bag",
        "db_restore_prompt": "Do you want to restore official in-game bag capacity (18-54 slots depending on class)?",
        "db_restore_success_title": "Death Bag Restored",
        "db_restore_success_msg": "Bag capacity restored to official game defaults!\n\nFile:\n{path}",

        # Tab 4: Decals & Skills
        "decal_search": "🔍 Search:",
        "decal_rare_lbl": "Rarity:",
        "decal_type_lbl": "Type:",
        "decal_poss_lbl": "Possession:",
        "decal_all": "All",
        "decal_premium": "Premium (_P)",
        "decal_standard": "Standard",
        "decal_owned": "📦 Possessed (> 0)",
        "decal_missing": "❌ Missing (0)",
        "decal_pack_meta": "🏆 Meta Pack",
        "decal_unlock_all": "✨ Unlock All",
        "decal_copies_lbl": "Copies:",
        "decal_events_lbl": "🎯 Events:",
        "decal_event_all": "🌐 All",
        "decal_styles_lbl": "⚡ Styles:",
        "decal_style_all": "All",
        "decal_style_crit": "💥 Critical",
        "decal_style_tank": "🛡️ Tank",
        "decal_style_vamp": "🩸 Vampire",
        "decal_style_farm": "📦 Farming",
        "decal_style_sets": "🎭 Sets",
        "decal_col_icon": "Icon / Official Name",
        "decal_col_rare": "Rarity",
        "decal_col_id": "Decal ID",
        "decal_col_type": "Type",
        "decal_col_qty": "Count",
        "decal_card_title": "Official Decal Technical Sheet",
        "decal_select_prompt": "Select a decal",
        "decal_type_and_owned": "Type: {type} | Owned: x{cnt}",
        "decal_copies_edit_lbl": "Copies in Bag/Storage:",
        "decal_set_btn": "Set Copies",
        "decal_plus1": "+1 Copy",
        "decal_plus5": "+5 Copies",
        "decal_zero": "Clear (0)",

        # Tab 5: Blueprints & Chokufunsha
        "bp_search": "🔍 Search:",
        "bp_slot_lbl": "Slot:",
        "bp_slot_all": "All",
        "bp_slot_helmets": "🪖 Helmets",
        "bp_slot_bodies": "👕 Bodies",
        "bp_slot_legs": "👖 Pants",
        "bp_slot_weapons": "⚔️ Weapons",
        "bp_faction_lbl": "Faction:",
        "bp_fac_all": "All",
        "bp_fac_dod": "🔨 D.O.D. ARMS",
        "bp_fac_we": "🎖️ WAR ENSEMBLE",
        "bp_fac_cw": "🕯️ CANDLE WOLF",
        "bp_fac_milk": "🥛 M.I.L.K.",
        "bp_fac_44ce": "⚡ 4 FORCEMEN & TENGOKU",
        "bp_fac_jackals": "🕶️ JACKALS",
        "bp_fac_re": "♻️ RE (Recycler)",
        "bp_fac_spe": "🎭 Special / Event",
        "bp_fac_gen": "⚔️ General / Other",
        "bp_view_sets_btn": "👘 Tier Armor Sets Viewer",
        "bp_poss_lbl": "Status:",
        "bp_poss_all": "All",
        "bp_poss_storage": "📦 In Storage (> 0)",
        "bp_poss_shop": "⭐ Unlocked in Shop (+4)",
        "bp_poss_rnd": "🔨 In R&D (REMODEL / MAP)",
        "bp_poss_locked": "❌ Locked (Missing)",
        "bp_dmg_lbl": "Damage:",
        "bp_dmg_all": "All",
        "bp_dmg_slash": "🗡️ Slash",
        "bp_dmg_blunt": "🔨 Blunt",
        "bp_dmg_pierce": "🏹 Pierce",
        "bp_dmg_fire": "🔥 Fire",
        "bp_dmg_elec": "⚡ Electric",
        "bp_dmg_poison": "🧪 Poison",
        "bp_unlock_all_lbl": "Unlock Level:",
        "bp_repair_btn": "🔧 Repair R&D",
        "bp_collabs_lbl": "🎯 Events:",
        "bp_collab_all": "🌐 All",
        "bp_collab_re": "♻️ RE Editions",
        "bp_col_item": "Blueprint / Official Name",
        "bp_col_slot": "Slot",
        "bp_col_faction": "Faction",
        "bp_col_status": "Forge Status",
        "bp_col_storage": "Storage",
        "bp_col_bag": "Bag",
        "bp_col_id": "Blueprint ID",
        "bp_card_title": "Chokufunsha Blueprint Details",
        "bp_select_prompt": "Select an equipment piece",
        "bp_status_info": "Forge: {status} | Storage: {storage} | Bag: {bag}",
        "bp_base_def": "Base Defense: {def_b} (At +4: {def_4}) | Durability: {dur}",
        "bp_base_atk": "Base Attack: {atk_b} (At +4: {atk_4}) | Durability: {dur}",
        "bp_view_set_btn": "👘 View Set in Armor Sets Viewer",
        "bp_no_set": "👘 Does not belong to a set",
        "bp_indiv_actions_title": "Individual Piece Actions",
        "bp_lvl_lbl": "Level:",
        "bp_unlock_shop_btn": "⭐ Unlock in Shop",
        "bp_send_storage_btn": "📦 Send 1 to Storage",
        "bp_deposit_kit_btn": "🛠️ Deposit Forge Kit (+10 pcs)",
        "bp_mass_actions_title": "Bulk Gear Modifiers",
        "bp_inf_dur_btn": "✨ Infinite Durability (999,999) on All",
        "bp_inf_ammo_btn": "🎯 Max Ammo (9,999) on Firearms",
        "bp_upg_all19_btn": "⚡ Upgrade All to Level +19 (Uncapped)",
        "bp_upg_all24_btn": "🔥 Upgrade All to Level +24 (Max Uncapped)",
        "bp_unlock_all_btn": "🌟 UNLOCK ALL",

        # Tab 6: Weapon Masteries
        "wm_target_lvl_lbl": "Desired Level:",
        "wm_set_all_btn": "⭐ Set ALL Weapon Masteries",
        "wm_col_type": "Weapon Type",
        "wm_col_code": "Internal Code",
        "wm_col_lvl": "Mastery Level",
        "wm_col_exp": "Experience Points (EXP)",
        "wm_lvl_val": "Level {lvl} / 20",

        # Tab 7: Tower & TDM Unlocks
        "tw_left_title": "Tower of Barbs, Elevators & Stamp Rally",
        "tw_elev_title": "🛗 Elevators & Tower Floors (1 to 51+ Tengoku)",
        "tw_elev_sub": "Unlocks direct access to all floors 1-40, Battle Royale 41-50, and Tengoku.",
        "tw_elev_btn": "🛗 Unlock ALL Elevators & Floors",
        "tw_stamp_title": "🎯 Stamp Rally 100% Perfect (Uncle Death)",
        "tw_stamp_sub": "Marks all stamps as PERFECT. Unlocks Uncle Death's Scythe.",
        "tw_stamp_btn": "⭐ Complete All Stamps in PERFECT (Unlocks Scythe)",
        "tw_bag_title": "🎒 Death Bag Expansion",
        "tw_bag_cap_lbl": "Slot Capacity:",
        "tw_bag_btn": "🎒 Expand Bag",
        "tw_cont_title": "♾️ Unlimited Free Revives / Continues",
        "tw_cont_lbl": "Free Continues:",
        "tw_cont_btn": "♾️ Set Continues",
        "tw_shop_title": "🛒 Secret Shop & Death Boxes",
        "tw_shop_btn": "🛒 Reset Gyaku-Funsha Shop Cooldown",
        "tw_boxes_btn": "📦 Open Pending Death Boxes Immediately (Lost Bags)",
        "tw_right_title": "Tokyo Death Metro, Mailbox & Compendiums",
        "tw_tdm_title": "🏆 TDM Rank & Score (Tokyo Death Metro)",
        "tw_rank_lbl": "Rank:",
        "tw_apply_btn": "🏆 Apply",
        "tw_inbox_title": "🎁 Rewards Box Injector",
        "tw_inbox_sub": "Sends resources directly to your mailbox with no storage limit.",
        "tw_res_lbl": "Resource:",
        "tw_qty_lbl": "Quantity:",
        "tw_inbox_btn": "📬 Send Present to Mailbox",
        "tw_comp_title": "📚 Compendiums & Room Customizations",
        "tw_comp_mats_btn": "🍄 Complete Uncle Death Compendiums (63 Shrooms + 24 Beasts)",
        "tw_comp_room_btn": "🎨 Unlock All Waiting Room Customizations (113)",
        "tw_comp_quests_btn": "📜 Complete All Official Quests (232 Quests)",
        "tw_comp_mags_btn": "📖 Unlock Magazine Collection (36) & Radio Jukebox",

        # Tab 8: Backups & Advanced
        "bak_title": "🛡️ Security Backups Manager (.bak)",
        "bak_col_file": "Backup File",
        "bak_col_date": "Creation Date",
        "bak_col_size": "Size",
        "bak_create_btn": "🛡️ Create New Backup",
        "bak_restore_btn": "🔄 Restore Backup",
        "bak_tools_title": "🛠️ Advanced Tools & Official Links",
        "bak_json_lbl": "Export / Import Save in readable JSON:",
        "bak_export_json": "📤 Export to JSON",
        "bak_import_json": "📥 Import from JSON",
        "bak_links_lbl": "Community Links & Official Resources:",
        "bak_links_txt": "• Official Wiki: letitdie.wiki.gg\n• Crafting & R&D: Chokufunsha Complete DB\n• Damage & Stat Calculator",

        # Armor Sets Dialog
        "dialog_armor_viewer_title": "👘 Official Armor Sets & Tiers Viewer (Wiki.gg)",
        "dialog_armor_set_label": "👘 ARMOR SET:",
        "dialog_evolution_label": "Evolution / Tier:",
        "dialog_preview_title": "🧍 Set Preview (Official 3D Model)",
        "dialog_slot_head": "🪖 HEAD (Helmet)",
        "dialog_slot_body": "👕 BODY (Chest Armor)",
        "dialog_slot_legs": "👖 LEGS (Pants)",
        "dialog_slot_weapon": "⚔️ SIGNATURE WEAPON",
        "dialog_atk_base": "⚔️ Base Attack: {atk} (At +4: ~{atk4})  |  Durability: {dur}",
        "dialog_weapon_paired": "🔥 Official signature weapon paired with this armor set.",
        "dialog_def_base": "🛡️ Base Defense: {def_b} (At +4: {def4})  |  Durability: {dur}",
        "dialog_res_slash": "Slash",
        "dialog_res_blunt": "Blunt",
        "dialog_res_pierce": "Pierce",
        "dialog_res_fire": "Fire",
        "dialog_res_elec": "Electric",
        "dialog_res_poison": "Poison",
        "dialog_shop_unlocked": "⭐ Shop: Unlocked (+{lvl})",
        "dialog_shop_lvl": "🔨 Shop: Level +{lvl}",
        "dialog_shop_locked": "❌ Shop: Locked",
        "dialog_storage_cnt": "📦 Storage: {cnt} pcs.",
        "dialog_bag_cnt": "🎒 Bag: {cnt} pcs.",
        "dialog_unlock_piece_btn": "⭐ Unlock +4",
        "dialog_add_piece_btn": "🎁 +1 to Storage",
        "dialog_unlock_full_tier_btn": "⭐ Unlock Complete Set + Weapon (Tier +4 in Shop & Storage)",
        "dialog_add_full_tier_btn": "🎁 Add Complete Set to Storage (Head + Body + Legs)",
        "dialog_close_btn": "Close",

        # Inventory Viewer & Smart Analyzer
        "dialog_inventory_title": "📋 Full In-Game Inventory Viewer (Coin Locker & Death Bag)",
        "dialog_smart_analyzer_title": "🧠 Smart Inventory & Forge Analyzer (R&D)",
        "dialog_smart_analyzer_sub": "Calculates exact material requirements for your active R&D recipes to stock your coin locker without clutter.",

        # General
        "notice": "Notice",
        "error": "Error",
        "confirm": "Confirm",
        "saved_ok": "Save game modified and backed up successfully!",
        "auto_saved_ok": "Saved automatically."
    }
}

def t(key, **kwargs):
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
    if not item:
        return ""
    lang = get_language()
    if lang == "en":
        return item.get("name_en") or item.get("name_es") or item.get("name") or str(item.get("id", ""))
    else:
        return item.get("name_es") or item.get("name_en") or item.get("name") or str(item.get("id", ""))

def get_item_desc(item):
    if not item:
        return ""
    lang = get_language()
    if lang == "en":
        return item.get("desc_en") or item.get("desc_es") or ""
    else:
        return item.get("desc_es") or item.get("desc_en") or ""

def get_set_name(set_obj):
    if not set_obj:
        return ""
    lang = get_language()
    if lang == "en":
        return set_obj.get("name_en") or set_obj.get("name_es") or set_obj.get("id", "")
    else:
        return set_obj.get("name_es") or set_obj.get("name_en") or set_obj.get("id", "")
