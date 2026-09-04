# -*- coding: utf-8 -*-
"""
LET IT DIE Save Modifiers Facade.

This module exposes the complete backward-compatible API for all save modifications.
Internal implementations are organized into domain services in the `core` package:
- core.helpers: Save metadata, player UID, database paths, cache.
- core.currencies: Kill Coins, SPLithium, Death Metals, Bloodnium, Recycle Points, VIP pass.
- core.fighters: Fighter stats, healing, revival, deathbag management.
- core.mastery: Weapon mastery levels.
- core.decals: Decal inventory, unlock all decals, meta presets.
- core.storage: Coin locker slots, materials, mushrooms, beasts, mystery bags.
- core.blueprints: Blueprints unlock, sanitization, equipment research, durability.
- core.tower: Floor progression, elevators, stamps, quests, magazines, music.
"""

from core.helpers import (
    ALL_DECALS_FILE,
    ALL_EQUIPMENT_FILE,
    TOWER_MAP_DATA_FILE,
    get_equipment_meta,
    get_tower_map_data,
    get_player_uid,
    get_masters_db_path,
    load_all_known_decals,
    load_all_equipment,
    get_save_summary,
    get_account_overview,
)

from core.currencies import (
    set_currencies,
    set_death_metals,
    set_kill_coins,
    set_splithium,
    set_bloodnium,
    set_recycle_points,
    get_rank_points_for_rank,
    set_player_rank,
    upgrade_waiting_room,
    set_vip_pass,
    deactivate_vip_pass,
    set_tdm_rank,
    get_player_currencies,
    get_waiting_room_info,
    get_vip_status,
    max_all_currencies,
    activate_vip_express_pass,
    max_login_streak,
)

from core.fighters import (
    max_fighter_level_and_stats,
    revive_all_fighters,
    update_fighter,
    expand_death_bag,
    upgrade_fighter_tier8,
    get_deathbag_masters_status,
    expand_deathbag_capacity,
    restore_deathbag_capacity,
    get_all_fighters_info,
    swap_fighter_positions,
    move_fighter_up,
    move_fighter_down,
    sync_fighter_slots,
    clone_fighter,
    create_new_fighter,
    delete_fighter,
    is_tutorial_cleared,
)



from core.mastery import (
    max_all_weapon_mastery,
    set_weapon_mastery,
    max_weapon_masteries,
    set_single_weapon_mastery,
)

from core.decals import (
    add_or_update_decals,
    unlock_all_decals,
    add_top_meta_decals,
    apply_decal_preset_to_inventory,
    equip_decal_preset_on_fighter,
)

from core.storage import (
    _assign_to_coin_locker,
    sync_storage_slots,
    add_materials_to_storage,
    add_mushrooms_to_storage,
    add_beasts_to_storage,
    add_rainbow_bags,
    add_all_mystery_bags,
    add_mystery_bags,
    send_present_to_reward_box,
    sync_mystery_bags_to_deathbox,
    analyze_storage_stock,
    smart_supply_missing_materials,
    smart_top_up_materials,
    expand_storage_capacity,
    get_mystery_bags_summary,
    add_material_to_storage,
    add_all_materials_to_storage,
    expand_coin_locker_capacity,
    instant_open_deathboxes,
)

from core.blueprints import (
    repair_and_sanitize_blueprints,
    unlock_blueprints,
    repair_all_storage_equipment,
    add_equipment_to_storage,
    analyze_active_recipes_materials,
    get_equipment_inventory_counts,
    get_blueprints_unlock_map,
    unlock_single_blueprint,
    send_blueprint_to_rnd,
    get_equipment_ancestors,
    unlock_all_blueprints,
    repair_unlocked_blueprints_states,
    get_part_research_status,
    get_storage_equipment_counts,
    get_bag_equipment_counts,
    set_infinite_durability_all_equipment,
    set_massive_ammo_all_weapons,
    upgrade_all_equipment_max_level,
    inject_endgame_set,
)

from core.tower import (
    unlock_all_tower_elevators,
    set_all_stamps_perfect,
    set_free_continues,
    complete_encyclopedia_books,
    unlock_all_elevators,
    unlock_all_hub_customizations,
    reset_wandering_shop_timer,
    complete_all_quests,
    reset_floor_to_waiting_room,
    unlock_all_magazines,
    unlock_all_radio_music,
    get_tower_playlog,
    set_tower_max_floor,
    reset_tower_interruptions,
    unlock_tutorial_and_waiting_room,
)

from core import __all__
