import os

# Faction & Weapon Damage Types with Official Weapon Mastery Codes (PTARMTP_00 .. PTARMTP_64)
WEAPON_CATEGORIES = [
    ("PTARMTP_00", "Manos Desnudas / Fists (Arma Básica)", "mastery_icon_fists.png"),
    ("PTARMTP_01", "Machete / Jungle Machete (D.O.D. ARMS)", "mastery_icon_machete.png"),
    ("PTARMTP_02", "Martillo de Guerra / War Hammer (D.O.D. ARMS)", "mastery_icon_hammer.png"),
    ("PTARMTP_03", "Plancha de Vapor / Hot Iron (D.O.D. ARMS)", "mastery_icon_iron.png"),
    ("PTARMTP_04", "Pistola de Clavos / Nail Gun (D.O.D. ARMS)", "mastery_icon_nail_gun.png"),
    ("PTARMTP_05", "Sierra Circular / Buzzsaw (D.O.D. ARMS)", "mastery_icon_buzzsaw.png"),
    ("PTARMTP_06", "Picahielo / Pickaxe (D.O.D. ARMS)", "mastery_icon_pickaxe.png"),
    ("PTARMTP_07", "Palo de Golf / Golf Club (WAR ENSEMBLE)", "blunt.png"),
    ("PTARMTP_08", "Cuchillo de Caza / Hunting Knife (WAR ENSEMBLE)", "mastery_icon_knife.png"),
    ("PTARMTP_09", "Hacha de Batalla / Battle Axe (CANDLE WOLF)", "mastery_icon_axe.png"),
    ("PTARMTP_10", "Espada Larga / Longsword (CANDLE WOLF)", "mastery_icon_sword.png"),
    ("PTARMTP_11", "Mayal / Flail (CANDLE WOLF)", "mastery_icon_flail.png"),
    ("PTARMTP_12", "Cuchillo Arrojadizo / Shuriken", "mastery_icon_shuriken.png"),
    ("PTARMTP_13", "Lanza de Caballero / Spear (CANDLE WOLF)", "mastery_icon_spear.png"),
    ("PTARMTP_14", "Vara de Trueno / Thunder Rod (CANDLE WOLF)", "mastery_icon_thunder_rod.png"),
    ("PTARMTP_15", "Garras de Metal / Metal Claw (WAR ENSEMBLE)", "claw_addict.png"),
    ("PTARMTP_16", "Pistola Magnum / Magnum (WAR ENSEMBLE)", "mastery_icon_magnum.png"),
    ("PTARMTP_17", "Fusil KAMAS-A1 / Assault Rifle (WAR ENSEMBLE)", "mastery_icon_assault_rifle.png"),
    ("PTARMTP_18", "Escopeta / Shotgun (WAR ENSEMBLE)", "mastery_icon_shotgun.png"),
    ("PTARMTP_19", "Fusil Francotirador / Sniper Rifle (WAR ENSEMBLE)", "mastery_icon_sniper_rifle.png"),
    ("PTARMTP_20", "Lanzacohetes / Rocket Launcher (WAR ENSEMBLE)", "mastery_icon_rocket_launcher.png"),
    ("PTARMTP_21", "Fuegos Artificiales / Fireworks (D.O.D. ARMS)", "mastery_icon_fireworks.png"),
    ("PTARMTP_22", "Motosierra / Chainsaw (D.O.D. ARMS)", "mastery_icon_chainsaw.png"),
    ("PTARMTP_23", "Motor Psycho / Motor Psycho (WAR ENSEMBLE)", "mastery_icon_motorcycle.png"),
    ("PTARMTP_24", "Taladro Gigante / Motor Drill (D.O.D. ARMS)", "mastery_icon_drill.png"),
    ("PTARMTP_25", "Katana / Muramasa Blade (CANDLE WOLF)", "mastery_icon_katana.png"),
    ("PTARMTP_26", "Bate de Béisbol / Red Hot Bat (M.I.L.K.)", "mastery_icon_bat.png"),
    ("PTARMTP_27", "Palo de Hockey / Hockey Stick (M.I.L.K.)", "mastery_icon_hockey_stick.png"),
    ("PTARMTP_28", "Bolas de Bolos / Bowling Ball (M.I.L.K.)", "mastery_icon_bowling_ball.png"),
    ("PTARMTP_30", "Espada Sierra / Cleaver Saber (WAR ENSEMBLE)", "mastery_icon_saber.png"),
    ("PTARMTP_31", "Lanzallamas / Flamethrower (D.O.D. ARMS)", "mastery_icon_flamethrower.png"),
    ("PTARMTP_34", "Ballesta Táctica / Crossbow (CANDLE WOLF)", "mastery_icon_crossbow.png"),
    ("PTARMTP_35", "Lanza de Dragón / Dragon Buster (CANDLE WOLF)", "mastery_icon_flame_rod.png"),
    ("PTARMTP_36", "Vara Eléctrica / Stun Rod (M.I.L.K.)", "mastery_icon_stun_rod.png"),
    ("PTARMTP_38", "Lanzador de Pelotas / Pitching Machine (M.I.L.K.)", "mastery_icon_pitching_machine.png"),
    ("PTARMTP_39", "Guantes de Boxeo / Boxing Glove (M.I.L.K.)", "mastery_icon_lion_dance_knuckles.png"),
    ("PTARMTP_55", "Masajeador 44CE White Steel / Massager", "mastery_icon_static_massager.png"),
    ("PTARMTP_56", "Lanzador de Púas 44CE Red Napalm / Spike Launcher", "mastery_icon_m2g-87.png"),
    ("PTARMTP_57", "Espada de Energía 44CE Black Thunder / Energy Sword", "mastery_icon_head_of_medusa.png"),
    ("PTARMTP_58", "Pistola de Veneno 44CE Pale Wind / Poison Gun", "mastery_icon_yo-yo.png"),
]

# Fighter Classes with Official Engine Codes (master_bodylvl_status_value)
FIGHTER_CLASSES = {
    "BAL": ("Todo Terreno (All-Rounder)", "all-rounder.png"),
    "BRE": ("Delantero (Striker - Foco STR)", "striker.png"),
    "DEF": ("Defensor (Defender - Foco HP/VIT)", "defender.png"),
    "TEC": ("Atacante (Attacker - Foco STR/DEX)", "attacker.png"),
    "SHT": ("Tirador (Shooter - Foco DEX)", "shooter.png"),
    "COL": ("Recolector (Collector - Bolsa Grande)", "collector.png"),
    "SKI": ("Maestro de Habilidades (Skill Master)", "skill_master.png"),
    "LUK": ("Estrella de la Suerte (Lucky Star - KC/Crit)", "lucky_star.png")
}

CLASS_CODE_ALIASES = {
    "ALL": "BAL",
    "STR": "BRE",
    "ATK": "TEC",
    "SHO": "SHT",
    "SKL": "SKI"
}

# Special Mushrooms with 100% Authentic Game IDs (master_mushroom)
SPECIAL_MUSHROOMS = [
    ("MSR_022", "Fun Fungus (Repara 100% equipo)", "18_fun_fungus_1.png"),
    ("MSR_025", "Guardshroom (Invencibilidad total)", "12_guardshroom_1.png"),
    ("MSR_020", "Slowmungus (Ralentiza el tiempo)", "13_slowmungus_1.png"),
    ("MSR_015", "Transparungus (Invisibilidad total)", "11_transparungus_1.png"),
    ("MSR_050", "Oakshroom Dorado (+300% Ataque)", "38_golden_oakshroom_1.png"),
    ("MSR_044", "Golden Lifeshroom (Revive con 100% HP)", "35_golden_lifeshroom_1.png"),
    ("MSR_043", "Lifeshroom (Revive con 50% HP)", "25_lifeshroom_1.png"),
    ("MSR_009", "Lavashroom (Cura 100% Salud)", "15_lavashroom_1.png"),
    ("MSR_031", "Frongus (Aturde enemigos en área)", "19_frongus_1.png"),
]

# Golden Beasts with 100% Authentic Game IDs (master_beast)
SPECIAL_BEASTS = [
    ("BST_GFROG", "Rana Dorada / Golden Frog (20k EXP)", "golden_frog.png"),
    ("BST_GLIZARD", "Lagarto Dorado / Golden Lizard (33k EXP)", "golden_lizard.png"),
    ("BST_GSNAIL", "Caracol Dorado / Golden Snail (40k EXP)", "golden_snail.png"),
    ("BST_GCASSOWARY", "Pájaro Dorado / Golden Bird (50k EXP)", "golden_bird.png"),
    ("BST_GCRAB", "Cangrejo Dorado / Golden Crab (30k EXP)", "golden_crab.png"),
    ("BST_GBASS", "Pez Dorado / Golden Fish (25k EXP)", "golden_fish.png"),
    ("BST_GHONEYCOMB", "Panal Dorado / Golden Honeycomb", "golden_honeycomb.png"),
    ("BST_GSCORPION", "Escorpión Dorado / Golden Scorpion (66k EXP)", "golden_scorpion.png"),
    ("BST_GPILLBUG", "Cochinilla Dorada / Golden Pillbug (22k EXP)", "golden_pillbug.png"),
    ("BST_GTURTLE", "Tortuga Dorada / Golden Turtle (45k EXP)", "golden_turtle.png"),
    ("BST_GRAT", "Rata Dorada / Golden Rat (10k EXP)", "golden_rat.png"),
]

# Rare Crafting Materials with 100% Authentic Game IDs (master_item)
RARE_MATERIALS = [
    ("ITMT_IRON_5", "Hierro Ultra Puro (Ultra-pure Iron 5★)", "ultra-pure_iron.png"),
    ("ITMT_IRON_6", "Acero Especial (Special Steel 6★)", "special_steel.png"),
    ("ITMT_OIL_6", "Biocombustible (Biofuel 6★)", "biofuel.png"),
    ("ITMT_FIBER_6", "Fibra de Carbono (Carbon Fiber 6★)", "carbon_fiber.png"),
    ("ITMT_WOOD_5", "Madera Caoba (Mahogany 5★)", "mahogany.png"),
    ("ITMT_STONE_DIY_4", "Metal D.O.D. Arms Rojo (Red Metal 4★)", "dod_arms_red_metal.png"),
    ("ITMT_STONE_DIY_6", "Metal D.O.D. Arms Púrpura (Purple Metal 5★)", "dod_arms_purple_metal.png"),
    ("ITMT_STONE_DIY_8", "Metal D.O.D. Arms Platino (Platinum Metal 7★)", "dod_arms_purple_metal.png"),
    ("ITMT_STONE_MIL_4", "Metal WAR Ensemble Rojo (Red Metal 4★)", "war_ensemble_red_metal.png"),
    ("ITMT_STONE_MIL_6", "Metal WAR Ensemble Púrpura (Purple Metal 5★)", "war_ensemble_purple_metal.png"),
    ("ITMT_STONE_MIL_8", "Metal WAR Ensemble Platino (Platinum Metal 7★)", "war_ensemble_purple_metal.png"),
    ("ITMT_STONE_FAN_4", "Metal Candle Wolf Rojo (Red Metal 4★)", "candle_wolf_red_metal.png"),
    ("ITMT_STONE_FAN_6", "Metal Candle Wolf Púrpura (Purple Metal 5★)", "candle_wolf_purple_metal.png"),
    ("ITMT_STONE_FAN_8", "Metal Candle Wolf Platino (Platinum Metal 7★)", "candle_wolf_purple_metal.png"),
    ("ITMT_STONE_SPO_4", "Metal M.I.L.K. Rojo (Red Metal 4★)", "m.i.l.k._red_metal.png"),
    ("ITMT_STONE_SPO_6", "Metal M.I.L.K. Púrpura (Purple Metal 5★)", "m.i.l.k._purple_metal.png"),
    ("ITMT_STONE_SPO_8", "Metal M.I.L.K. Platino (Platinum Metal 7★)", "m.i.l.k._purple_metal.png"),
    ("ITMT_STEROID_5", "Muerteroides Morados (Death 'Roids Purple 5★)", "reversal_metal.png"),
    ("ITMT_STEROID_6", "Muerteroides Naranjas (Death 'Roids Orange 6★)", "reversal_metal.png"),
    ("ITMT_STONE_TBR_5", "Metal de Retorno (Reversal Metal 5★)", "reversal_metal.png"),
]

# Top Tier Meta Decals with 100% Authentic Game IDs (master_skill)
TOP_META_DECALS = [
    ("SKL_FIGHTER_STUP_01_P", "Ultimate Fighter (+10% a todos los stats base)", "ultimate_fighter.png", 5),
    ("SKL_ATKUP_NODMG_P", "Serial Killer (+10% ataque hasta +100% sin recibir daño)", "serial_killer.png", 5),
    ("SKL_ATKUP_03_P", "Golden Gym (+30% ataque con todas las armas)", "golden_gym.png", 5),
    ("SKL_DRAIN_01_P", "Vampire (Restaura 7% del daño como salud)", "vampire.png", 4),
    ("SKL_SEARCHUP_ITEM_P", "Treasure Hunter (Muestra todos los cofres y enemigos)", "treasure_hunter.png", 4),
    ("SKL_HPUP_02_P", "Heavy Tank (+40% de Salud máxima)", "heavy_tank.png", 4),
    ("SKL_HPUP_03_P", "Super Heavy Tank (+50% de Salud máxima)", "heavy_tank.png", 5),
    ("SKL_DEFUP_02_P", "Diamond (+20% de Defensa total)", "diamond.png", 4),
    ("SKL_WEP_SPDUP_P", "Barbarian (+20% de Daño con armas a dos manos)", "barbarian.png", 3),
    ("SKL_HEADSHOTUP_P", "One Shot One Kill (+70% daño a la cabeza)", "one_shot_one_kill.png", 4),
    ("SKL_ATKDEFUP_HPLOW_01_P", "Bull (+60% de Ataque y Defensa con salud < 15%)", "bull.png", 3),
    ("SKL_SPDUP_02_P", "Marathon Runner (Reduce 50% consumo de stamina)", "marathon_runner.png", 3),
    ("SKL_CRIUP_02_P", "Five-Leaf Clover (+20% de Golpe Crítico)", "five-leaf_clover.png", 4),
    ("SKL_SNOWWHITE_P", "Poison Eater (El veneno te cura en vez de dañarte)", "poison_eater.png", 3),
    ("SKL_ATKUP_CRIUP_DEFDWN_P", "Special Unit Captain (+30% Ataque con set completo)", "special_unit_captain.png", 5),
    ("SKL_ARRNG_STATUP_ALL_P", "Professional Cosplayer (Gran aumento de stats)", "professional_cosplayer.png", 5),
    ("SKL_STRENGTHEN_BODY_01_P", "Joker (+15% Ataque, Defensa y Crítico)", "joker.png", 5),
    ("SKL_RGSPDUP_02_P", "King of the Wolves (Aumento masivo de Rage)", "king_of_the_wolves.png", 4),
]
