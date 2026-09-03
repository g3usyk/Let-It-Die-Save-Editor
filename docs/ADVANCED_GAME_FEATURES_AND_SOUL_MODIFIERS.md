# LET IT DIE - Enciclopedia de Estructuras Internas y Funciones Avanzadas del Guardado
> **Documento de Referencia Tecnica y Modificadores del Nucleo (soul / save_json)**
> *Version 1.0 - Totalmente documentado con IDs, rutas JSON y funcionamiento de motor.*

---

## Indice de Contenidos
1. [1. Sistema de Ascensores y Pisos de la Torre](#1-sistema-de-ascensores-y-pisos-de-la-torre)
2. [2. Stamp Rally y Recompensas del Tio Death (Sellos Perfectos)](#2-stamp-rally-y-recompensas-del-tio-death-sellos-perfectos)
3. [3. Expansion y Estructura de la Bolsa de la Muerte (Death Bag)](#3-expansion-y-estructura-de-la-bolsa-de-la-muerte-death-bag)
4. [4. Sistema de Rango y Puntos TDM (Tokyo Death Metro)](#4-sistema-de-rango-y-puntos-tdm-tokyo-death-metro)
5. [5. Bolsas Misteriosas TDM (Mystery Bags)](#5-bolsas-misteriosas-tdm-mystery-bags)
6. [6. Buzon de Regalos y Recompensas de la Sala de Espera (soul.present)](#6-buzon-de-regalos-y-recompensas-de-la-sala-de-espera-soulpresent)
7. [7. Continues Gratuitos y Sistema de Resurreccion](#7-continues-gratuitos-y-sistema-de-resurreccion)
8. [8. Compendios del Tio Death (msrbook y bstbook)](#8-compendios-del-tio-death-msrbook-y-bstbook)
9. [9. Personalizacion de Sala de Espera y Skins (hubcustom y armorskin)](#9-personalizacion-de-sala-de-espera-y-skins-hubcustom-y-armorskin)
10. [10. Luchadores, Atributos y Ranuras de Calcomanias (bodyuser y chr)](#10-luchadores-atributos-y-ranuras-de-calcomanias-bodyuser-y-chr)

---

## 1. Sistema de Ascensores y Pisos de la Torre

### Rutas en el Guardado
* `save_json["soul"]["openelvflr"]` -> Lista de identificadores oficiales de ascensores desbloqueados en la Torre.

### Estructura de openelvflr (100% Verificada)
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

### Funcionamiento
* Al registrar los IDs oficiales `ELV_MAIN_...` y `ELV_SUB...`, el ascensor de la Sala de Espera y los ascensores intermedios de los 4 distritos (AMS, ARC, MET, RFT) quedan permanentemente operativos.

---

## 2. Stamp Rally y Recompensas del Tio Death (Multiplicadores de Investigacion)

### Ruta en el Guardado
* `save_json["soul"]["researchstamp"]` -> Multiplicadores globales de combate del Tio Death.
* `save_json["soul"]["partresearch"]["user"]` -> Planos desbloqueados en Chokufunsha.

### Estructura de researchstamp (100% Verificada)
```json
[
  {"type": "SLASH", "rate": 2.8},
  {"type": "HIT", "rate": 1.6},
  {"type": "LEGS", "rate": 1.2},
  {"type": "HEAD", "rate": 0.6},
  {"type": "BODY", "rate": 1.4}
]
```

### Recompensas de Sellos
* **Guadaña Legendaria del Tío Death (`PT_ARM_WP050_001` / Uncle Death's Scythe):** Se inyecta en `partresearch.user` con niveles 1 al 4 completados (`FINISHED`) y nivel 5 listo para forjar y comprar directamente en Chokufunsha con Kill Coins.

---

## 3. Expansion y Estructura de la Bolsa de la Muerte (Death Bag)

### Rutas en el Guardado
* `save_json["soul"]["bag_slot"]` -> Capacidad global base (por defecto 20).
* `save_json["soul"]["deathbag"]` -> Diccionario por uid con la lista de slots de inventario activos.
* `save_json["bodyuser"][uid][i]["bag"]` -> Capacidad especifica por luchador (ampliable a 30, 40 o 50).

### Estructura de Slots en deathbag
```json
{
  "uid": 443455,
  "cid": "c39c2170-24fd-493d-ae16-b5453328add2",
  "slot": 1,
  "type": 0,
  "eid": "uuid-del-item",
  "site": "EQSITE_WEAPON_R1",
  "arm_slot": 0
}
```

### Sitios de Equipamiento (site)
* `"EQSITE_HEAD"` -> Casco / Mascara
* `"EQSITE_BODY"` -> Pecho / Armadura superior
* `"EQSITE_LEGS"` -> Pantalones / Armadura inferior
* `"EQSITE_WEAPON_R1"` / `"EQSITE_WEAPON_R2"` -> Armas en mano derecha
* `"EQSITE_WEAPON_L1"` / `"EQSITE_WEAPON_L2"` -> Armas en mano izquierda
* `""` (vacio) -> Objeto guardado en la mochila / bolsillo

---

## 4. Sistema de Rango y Puntos TDM (Tokyo Death Metro)

### Rutas en el Guardado
* `save_json["soul"]["tdm_rank"]` -> ID del rango competitivo TDM.
* `save_json["soul"]["tdm_point"]` -> Puntuacion de asaltos TDM.
* `save_json["soul"]["team_id"]` -> Equipo asignado (ej. "01" Tokio, "11" California, etc.).

### Tabla de IDs de Rango TDM
| Rango | ID en Partida | Puntos Requeridos |
|---|---|---|
| **Bronce III - I** | `TDM_RANK_01_01` a `TDM_RANK_01_03` | 0 - 999 |
| **Plata III - I** | `TDM_RANK_02_01` a `TDM_RANK_02_03` | 1,000 - 1,499 |
| **Oro III - I** | `TDM_RANK_03_01` a `TDM_RANK_03_03` | 1,500 - 1,999 |
| **Platino III - I** | `TDM_RANK_04_01` a `TDM_RANK_04_03` | 2,000 - 2,999 |
| **Diamante III** | `TDM_RANK_05_01` | 3,000 - 3,199 |
| **Diamante II** | `TDM_RANK_05_02` | 3,200 - 3,499 |
| **Diamante I (Top Tier)** | `TDM_RANK_05_03` | 3,500+ |

---

## 5. Bolsas Misteriosas TDM (Mystery Bags)

### Ruta en el Guardado
* `save_json["soul"]["mysterybag"]` -> Diccionario indexado por rareza.

### Estructura de Bolsas
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

### Recompensas por Rareza
* **RAINBOW (Arcoiris):** Death Metals (x1 a x5), Calcomanias 4? y 5?, Planos Forcemen 44CE, Muerteroides Purpura/Naranja.
* **PLATINUM (Platino):** Calcomanias 4?, Materiales Grado 6 a 8, Metales de Jefes.
* **GOLD (Oro):** 50,000+ KC / SPL, Materiales Grado 5 a 6, Calcomanias 3?.
* **SILVER (Plata):** 20,000 KC / SPL, Materiales Grado 3 a 5.
* **COPPER (Cobre):** 5,000 KC / SPL, Setas y Materiales Basicos.

---

## 6. Buzon de Regalos y Recompensas de la Sala de Espera (soul.present)

### Ruta en el Guardado
* `save_json["soul"]["present"]` -> Lista de envios pendientes en la Caja de Recompensas.

### Estructura de Regalo
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

### Tipos Validos (type)
* `"MONEY"` -> Kill Coins directas
* `"SPIRIT"` -> SPLithium directo
* `"MEDAL"` -> Metales de Muerte (Death Metals)
* `"ITEM"` -> Material de Forja (`val0` = `itemid`)
* `"DECAL"` -> Calcomania (`val0` = `sklid`)
* `"EQUIPMENT"` -> Arma o Armadura (`val0` = `ptid`)

---

## 7. Continues Gratuitos y Sistema de Resurreccion

---

## 7. Desbloqueo de Pisos y Ascensores (openelvflr)

Para habilitar el viaje rápido gratuito entre todas las zonas de la Torre (D.O.D., War Ensemble, Candle Wolf, M.I.L.K. y Tengoku) sin pagar Kill Coins:
* `save_json["soul"]["openelvflr"]` -> Lista de identificadores de ascensores (`ELV_MAIN_...` y `ELV_SUB...`).

---

## 8. Compendios del Tío Death (msrbook y bstbook)

* `save_json["soul"]["msrbook"]` -> Libro de 63 Setas descubiertas, comidas, lanzadas y cocinadas.
* `save_json["soul"]["bstbook"]` -> Libro de 24 Bestias (ranas, lagartos, escorpiones, caracoles, pájaros).

### Estructura de Entrada
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

## 9. Personalización de Sala de Espera y Skins (hubcustom y armorskin)

### Rutas en el Guardado
* `save_json["soul"]["hubcustom"]` -> 113 personalizaciones visuales de la Sala de Espera (`cstmid` y `flg`: 0=bloqueado, 1=poseído/desbloqueado, 2/6=equipado).
* `save_json["soul"]["armorskin"]` -> Skins estéticas aplicadas sobre el equipo.
* `save_json["soul"]["last_visiting_shop_time"]` -> Timestamp de visita a la tienda ambulante Gyaku-Funsha (fijar en 0 elimina el cooldown de 1 hora).

---

## 10. Arquitectura Real de Luchadores en el Motor (bodyuser y chr)

El motor de LET IT DIE divide la información de cada luchador en dos secciones complementarias:

### 1. Puntos de Atributo y Mejoras de Muerteroides: `save["bodyuser"][uid]`
En `bodyuser`, los campos de estadísticas **no representan los puntos de vida o daño directos**, sino los **puntos de asignación de nivel** (rango 1 a 45 por estadística):
* `lvl`: Nivel total (en Tier 8 / Grado 6 max: **247**, calculado como la suma de asignaciones base - 5).
* `hp`, `str`, `dex`, `vit`, `stm`, `luk`: Puntos de estadística base (máximo **45** cada uno).
* `hp_bonus`, `str_bonus`, `dex_bonus`, `vit_bonus`, `stm_bonus`, `luk_bonus`: Bonificaciones de desvelo por **Muerteroides (Death 'Roids)** (máximo **20** cada uno).
* `skill`: Ranuras adicionales de calcomanías desbloqueadas con esteroides (**3** adicionales, para un total de **8 ranuras completas**).
* `bag`: Capacidad adicional de bolsa por M.I.N.G.O. (máximo seguro = **3**).
* `rage`: Barras de furia adicionales desbloqueadas (**1** adicional).

### 2. Estado de Combate en Vivo: `save["soul"]["chr"]["chrs"][uid]`
En `chr.chrs`, se almacena el estado real del personaje en combate:
* `name`: Nombre visible del luchador.
* `type`: Clase oficial del motor (`"BAL"`, `"BRE"`, `"DEF"`, `"TEC"`, `"SHT"`, `"COL"`, `"SKI"`, `"LUK"`).
* `grade`: Grado del luchador (**1 a 6**; en las tablas maestras `master_bodylvl_status_value` el grado máximo es **6**).
* `limit_break`: Nivel de Desvelo / Limit Break (**0 a 4**; un Grado 6 con Limit Break 4 equivale a lo que la comunidad llama **Tier 8**).
* `hp`: Salud de combate real (ej. **20,000** HP).
* `state`: Estado actual (`"GUARD"`, `"REST"`, `"DEAD"`).
* `escdie`: Bandera de rescate (0 = vivo y listo para jugar).

---

## 11. Modificadores de Equipamiento: Durabilidad Infinita y Munición Masiva

### Rutas en el Guardado
* `save["part"]["pts"][uid]` -> Inventario de equipamiento en Coin Locker.
* `save["soul"]["deathbag"][fighter_uid]` -> Objetos dentro de las bolsas de los luchadores.

### Esquema de Equipamiento
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
* `dur`: Durabilidad del arma o armadura. Con `999,999` el objeto es virtualmente irrompible.
* `rest`: Balas en el cargador actual. Con `9,999` no se requiere recargar durante combates prolongados.
* `spare`: Munición en la reserva del arma.
* `lvl`: Nivel de mejora del objeto (+19 corresponde al límite Uncapped de Tengoku).

---

## 12. Presets de Calcomanías Meta (8 Slots)

Configuraciones competitivas verificadas disponibles con 1 clic:
1. **Tengoku God Climber (Pisos 51F–350F+)**:
   * `SKL_FIGHTER_STUP_01_P` (Ultimate Fighter)
   * `SKL_ATKUP_NODMG_P` (Serial Killer)
   * `SKL_ATKUP_03_P` (Golden Gym)
   * `SKL_DRAIN_01_P` (Vampire)
   * `SKL_HPUP_03_P` (Super Heavy Tank)
   * `SKL_ARRNG_STATUP_ALL_P` (Professional Cosplayer)
   * `SKL_STRENGTHEN_BODY_01_P` (Joker)
   * `SKL_HEADSHOTUP_P` (One Shot One Kill)
2. **Tirador KAMAS Definitivo**:
   * `SKL_HEADSHOTUP_P`, `SKL_ATKUP_NODMG_P`, `SKL_FIGHTER_STUP_01_P`, `SKL_ATKUP_03_P`, `SKL_WEP_SPDUP_P`, `SKL_CRIUP_02_P`, `SKL_DRAIN_01_P`, `SKL_SEARCHUP_ITEM_P`.
3. **Destructor Melee (Mayal / Machete / Katana)**:
   * `SKL_FIGHTER_STUP_01_P`, `SKL_ATKUP_03_P`, `SKL_ATKUP_NODMG_P`, `SKL_DRAIN_01_P`, `SKL_HPUP_02_P`, `SKL_DEFUP_02_P`, `SKL_STRENGTHEN_BODY_01_P`, `SKL_RGSPDUP_02_P`.
4. **Pesadilla de Defensa TDM**:
   * `SKL_HPUP_03_P`, `SKL_HPUP_02_P`, `SKL_DEFUP_02_P`, `SKL_SNOWWHITE_P`, `SKL_STRENGTHEN_BODY_01_P`, `SKL_ATKDEFUP_HPLOW_01_P`, `SKL_FIGHTER_STUP_01_P`, `SKL_ATKUP_CRIUP_DEFDWN_P`.

---

## 13. Inyector de Sets Endgame (44CE Forcemen, Jackals & Tengoku)

Permite forjar y entregar en el Almacén sets completos con durabilidad 999k y registrar sus planos en Chokufunsha:
* **White Steel (44CE D.O.D.)**: `PT_ARM_WP055_001` (Static Massager), `PT_ARM_WP002_001` (Spike Bat), `PT_DIY_HEAD_4F_01`, `PT_DIY_TOPS_4F_01`, `PT_DIY_BTM_4F_01`.
* **Red Napalm (44CE WAR ENSEMBLE)**: `PT_ARM_WP056_001` (M2G-87 Spike Launcher), `PT_MIL_HEAD_4F_01`, `PT_MIL_TOPS_4F_01`, `PT_MIL_BTM_4F_01`.
* **Black Thunder (44CE CANDLE WOLF)**: `PT_ARM_WP057_001` (Energy Sword), `PT_FAN_HEAD_4F_01`, `PT_FAN_TOPS_4F_01`, `PT_FAN_BTM_4F_01`.
* **Pale Wind (44CE M.I.L.K.)**: `PT_ARM_WP058_001` (Force Wand), `PT_SPO_HEAD_4F_01`, `PT_SPO_TOPS_4F_01`, `PT_SPO_BTM_4F_01`.
* **Sets Jackals v1 / v2 / v3**: Espada Jackal X (`PT_ARM_WP001_JAC_11`), Blaster Jackal Y (`PT_ARM_WP016_JAC_11`), Yo-Yo Jackal Z (`PT_ARM_WP027_JAC_11`) y armaduras completas Jackal X, Y, Z.
* **Armas Legendarias de Tengoku**: Muspelheim (`PT_ARM_WP060_001`), Judgement Day (`PT_ARM_WP061_001`), Predator (`PT_ARM_WP062_001`), Emperor (`PT_ARM_WP063_001`), Lethal Weapon (`PT_ARM_WP064_001`).

---

## 14. Autocompletador de Misiones Oficiales (Quests)

### Rutas en el Guardado
* `save["soul"]["quest"]["user"]` -> Lista de entradas `{"qid": quest_id, "ordcnt": 1, "clrcnt": 1}`.
Al marcar `clrcnt = 1`, el motor considera completadas las misiones oficiales de la tabla `master_quest` (derrotar enemigos, escalar sin ropa, etc.) y entrega automáticamente los Death Metals y recompensas en el Buzón.

---

## 15. Revistas Yotsuyama y Gramola de Radio

### Rutas en el Guardado
* `save["soul"]["magazine"]["status_list"]` -> Cadena separada por comas con 36 valores. Valor `2` indica revista o cómic leído y coleccionado en la Sala de Espera.
* `save["soul"]["radio"]` -> Estado y canales de la gramola de música con las canciones oficiales de las bandas japonesas de LET IT DIE.

---

## 16. Sistema de Respaldos Rotativos Automáticos

* Archivos con formato: `<nombre_partida>.sav.YYYYMMDD_HHMMSS.bak`.
* Política de retención rotativa automática: mantiene los últimos 10 respaldos y descarta los obsoletos.
* Restauración con 1 clic en la pestaña Avanzado de la GUI.

---

*Documento técnico 100% verificado contra la base de datos oficial masters.db y el motor Unreal de LET IT DIE.*