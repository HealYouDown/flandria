from typing import Optional

import strawberry

from .sort_direction import SortDirection


@strawberry.input
class BaseMixinSort:
    code: Optional[SortDirection] = strawberry.UNSET
    name: Optional[SortDirection] = strawberry.UNSET
    icon: Optional[SortDirection] = strawberry.UNSET
    is_tradable: Optional[SortDirection] = strawberry.UNSET
    is_destroyable: Optional[SortDirection] = strawberry.UNSET
    npc_sell_price: Optional[SortDirection] = strawberry.UNSET
    is_sellable: Optional[SortDirection] = strawberry.UNSET
    is_storageable: Optional[SortDirection] = strawberry.UNSET
    duration: Optional[SortDirection] = strawberry.UNSET
    stack_size: Optional[SortDirection] = strawberry.UNSET
    npc_buy_price: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class RowIDMixinSort:
    row_id: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class ActorMixinSort:
    code: Optional[SortDirection] = strawberry.UNSET
    name: Optional[SortDirection] = strawberry.UNSET
    icon: Optional[SortDirection] = strawberry.UNSET
    level: Optional[SortDirection] = strawberry.UNSET
    is_inanimate: Optional[SortDirection] = strawberry.UNSET
    is_sea: Optional[SortDirection] = strawberry.UNSET
    is_ship: Optional[SortDirection] = strawberry.UNSET
    is_air: Optional[SortDirection] = strawberry.UNSET
    is_tameable: Optional[SortDirection] = strawberry.UNSET
    experience: Optional[SortDirection] = strawberry.UNSET
    health_points: Optional[SortDirection] = strawberry.UNSET
    recovery_rate: Optional[SortDirection] = strawberry.UNSET
    minimum_physical_damage: Optional[SortDirection] = strawberry.UNSET
    maximum_physical_damage: Optional[SortDirection] = strawberry.UNSET
    minimum_magical_damage: Optional[SortDirection] = strawberry.UNSET
    maximum_magical_damage: Optional[SortDirection] = strawberry.UNSET
    physical_defense: Optional[SortDirection] = strawberry.UNSET
    magical_defense: Optional[SortDirection] = strawberry.UNSET
    physical_evasion_rate: Optional[SortDirection] = strawberry.UNSET
    physical_hit_rate: Optional[SortDirection] = strawberry.UNSET
    magical_hit_rate: Optional[SortDirection] = strawberry.UNSET
    critical_rate: Optional[SortDirection] = strawberry.UNSET
    critical_resistance_rate: Optional[SortDirection] = strawberry.UNSET
    sea_attack_aoe_range: Optional[SortDirection] = strawberry.UNSET
    ship_guns_count: Optional[SortDirection] = strawberry.UNSET
    ship_guns_speed: Optional[SortDirection] = strawberry.UNSET
    ship_attack_range: Optional[SortDirection] = strawberry.UNSET
    attack_cast_time: Optional[SortDirection] = strawberry.UNSET
    attack_cooldown: Optional[SortDirection] = strawberry.UNSET
    despawn_delay_time: Optional[SortDirection] = strawberry.UNSET
    attack_vision_range: Optional[SortDirection] = strawberry.UNSET
    nearby_attack_vision_range: Optional[SortDirection] = strawberry.UNSET
    is_ranged: Optional[SortDirection] = strawberry.UNSET
    attack_range: Optional[SortDirection] = strawberry.UNSET
    walking_speed: Optional[SortDirection] = strawberry.UNSET
    running_speed: Optional[SortDirection] = strawberry.UNSET
    turning_speed: Optional[SortDirection] = strawberry.UNSET
    messages_code: Optional[SortDirection] = strawberry.UNSET
    posion_resistance: Optional[SortDirection] = strawberry.UNSET
    fire_resistance: Optional[SortDirection] = strawberry.UNSET
    cold_resistance: Optional[SortDirection] = strawberry.UNSET
    lightning_resistance: Optional[SortDirection] = strawberry.UNSET
    holy_resistance: Optional[SortDirection] = strawberry.UNSET
    dark_resistance: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class ActorModelMixinSort:
    model_scale: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class FlorensiaModelMixinSort:
    model_name: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class SkillMixinSort:
    code: Optional[SortDirection] = strawberry.UNSET
    reference_code: Optional[SortDirection] = strawberry.UNSET
    name: Optional[SortDirection] = strawberry.UNSET
    icon: Optional[SortDirection] = strawberry.UNSET
    required_level_land: Optional[SortDirection] = strawberry.UNSET
    required_level_sea: Optional[SortDirection] = strawberry.UNSET
    skill_level: Optional[SortDirection] = strawberry.UNSET
    skill_max_level: Optional[SortDirection] = strawberry.UNSET
    mana_cost: Optional[SortDirection] = strawberry.UNSET
    accuracy: Optional[SortDirection] = strawberry.UNSET
    hit_correction: Optional[SortDirection] = strawberry.UNSET
    cooldown: Optional[SortDirection] = strawberry.UNSET
    cast_time: Optional[SortDirection] = strawberry.UNSET
    cast_distance: Optional[SortDirection] = strawberry.UNSET
    dash_distance: Optional[SortDirection] = strawberry.UNSET
    push_distance: Optional[SortDirection] = strawberry.UNSET
    effect_range: Optional[SortDirection] = strawberry.UNSET
    effect_angle: Optional[SortDirection] = strawberry.UNSET
    is_persistent: Optional[SortDirection] = strawberry.UNSET
    duration: Optional[SortDirection] = strawberry.UNSET
    toggle_tick_time: Optional[SortDirection] = strawberry.UNSET
    toggle_operator: Optional[SortDirection] = strawberry.UNSET
    toggle_hp_value: Optional[SortDirection] = strawberry.UNSET
    toggle_mp_value: Optional[SortDirection] = strawberry.UNSET
    required_weapons: Optional[SortDirection] = strawberry.UNSET
    description: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class EffectMixinSort: ...


@strawberry.input
class ClassSeaMixinSort:
    is_armored: Optional[SortDirection] = strawberry.UNSET
    is_big_gun: Optional[SortDirection] = strawberry.UNSET
    is_torpedo: Optional[SortDirection] = strawberry.UNSET
    is_maintenance: Optional[SortDirection] = strawberry.UNSET
    is_assault: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class ClassLandMixinSort:
    is_noble: Optional[SortDirection] = strawberry.UNSET
    is_court_magician: Optional[SortDirection] = strawberry.UNSET
    is_magic_knight: Optional[SortDirection] = strawberry.UNSET
    is_saint: Optional[SortDirection] = strawberry.UNSET
    is_priest: Optional[SortDirection] = strawberry.UNSET
    is_shaman: Optional[SortDirection] = strawberry.UNSET
    is_mercenary: Optional[SortDirection] = strawberry.UNSET
    is_gladiator: Optional[SortDirection] = strawberry.UNSET
    is_guardian_swordsman: Optional[SortDirection] = strawberry.UNSET
    is_explorer: Optional[SortDirection] = strawberry.UNSET
    is_excavator: Optional[SortDirection] = strawberry.UNSET
    is_sniper: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class ArmorMixinSort:
    level_land: Optional[SortDirection] = strawberry.UNSET
    level_sea: Optional[SortDirection] = strawberry.UNSET
    physical_defense: Optional[SortDirection] = strawberry.UNSET
    magical_defense: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class ItemSetMixinSort:
    item_set_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class UpgradeRuleMixinSort:
    upgrade_rule_base_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class WeaponMixinSort:
    level_land: Optional[SortDirection] = strawberry.UNSET
    level_sea: Optional[SortDirection] = strawberry.UNSET
    minimum_physical_damage: Optional[SortDirection] = strawberry.UNSET
    maximum_physical_damage: Optional[SortDirection] = strawberry.UNSET
    minimum_magical_damage: Optional[SortDirection] = strawberry.UNSET
    maximum_magical_damage: Optional[SortDirection] = strawberry.UNSET
    attack_speed: Optional[SortDirection] = strawberry.UNSET
    attack_range: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class EquipmentMixinSort:
    level_land: Optional[SortDirection] = strawberry.UNSET
    level_sea: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class ExtraEquipmentModelMixinSort:
    model_variant: Optional[SortDirection] = strawberry.UNSET


@strawberry.input
class ShipBaseMixinSort:
    npc_tune_price: Optional[SortDirection] = strawberry.UNSET
    level_sea: Optional[SortDirection] = strawberry.UNSET
    guns_front: Optional[SortDirection] = strawberry.UNSET
    guns_side: Optional[SortDirection] = strawberry.UNSET
    crew_size: Optional[SortDirection] = strawberry.UNSET
    physical_defense: Optional[SortDirection] = strawberry.UNSET
    protection: Optional[SortDirection] = strawberry.UNSET
    balance: Optional[SortDirection] = strawberry.UNSET
    dp: Optional[SortDirection] = strawberry.UNSET
    en: Optional[SortDirection] = strawberry.UNSET
    en_usage: Optional[SortDirection] = strawberry.UNSET
    en_recovery: Optional[SortDirection] = strawberry.UNSET
    acceleration: Optional[SortDirection] = strawberry.UNSET
    deceleration: Optional[SortDirection] = strawberry.UNSET
    turning_power: Optional[SortDirection] = strawberry.UNSET
    favorable_wind: Optional[SortDirection] = strawberry.UNSET
    adverse_wind: Optional[SortDirection] = strawberry.UNSET
    physical_damage: Optional[SortDirection] = strawberry.UNSET
    weapon_range: Optional[SortDirection] = strawberry.UNSET
    critical_chance: Optional[SortDirection] = strawberry.UNSET
    reload_speed: Optional[SortDirection] = strawberry.UNSET
    hit_range: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class RandomBoxSort(BaseMixinSort, RowIDMixinSort):
    level_land: Optional[SortDirection] = strawberry.UNSET
    level_sea: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class RandomBoxRewardSort:
    index: Optional[SortDirection] = strawberry.UNSET
    random_box_code: Optional[SortDirection] = strawberry.UNSET
    reward_code: Optional[SortDirection] = strawberry.UNSET
    quantity: Optional[SortDirection] = strawberry.UNSET
    probability: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class QuestSort:
    code: Optional[SortDirection] = strawberry.UNSET
    is_sea: Optional[SortDirection] = strawberry.UNSET
    level: Optional[SortDirection] = strawberry.UNSET
    is_mercenary: Optional[SortDirection] = strawberry.UNSET
    is_saint: Optional[SortDirection] = strawberry.UNSET
    is_noble: Optional[SortDirection] = strawberry.UNSET
    is_explorer: Optional[SortDirection] = strawberry.UNSET
    experience: Optional[SortDirection] = strawberry.UNSET
    money: Optional[SortDirection] = strawberry.UNSET
    selectable_items_count: Optional[SortDirection] = strawberry.UNSET
    title: Optional[SortDirection] = strawberry.UNSET
    description: Optional[SortDirection] = strawberry.UNSET
    pre_dialog: Optional[SortDirection] = strawberry.UNSET
    start_dialog: Optional[SortDirection] = strawberry.UNSET
    run_dialog: Optional[SortDirection] = strawberry.UNSET
    finish_dialog: Optional[SortDirection] = strawberry.UNSET
    previous_quest_code: Optional[SortDirection] = strawberry.UNSET
    start_npc_code: Optional[SortDirection] = strawberry.UNSET
    start_area_code: Optional[SortDirection] = strawberry.UNSET
    end_npc_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class QuestGiveItemSort:
    quest_code: Optional[SortDirection] = strawberry.UNSET
    item_code: Optional[SortDirection] = strawberry.UNSET
    amount: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class QuestMissionSort:
    index: Optional[SortDirection] = strawberry.UNSET
    quest_code: Optional[SortDirection] = strawberry.UNSET
    count: Optional[SortDirection] = strawberry.UNSET
    description: Optional[SortDirection] = strawberry.UNSET
    map_code: Optional[SortDirection] = strawberry.UNSET
    x: Optional[SortDirection] = strawberry.UNSET
    y: Optional[SortDirection] = strawberry.UNSET
    monster_code: Optional[SortDirection] = strawberry.UNSET
    item_code: Optional[SortDirection] = strawberry.UNSET
    quest_item_code: Optional[SortDirection] = strawberry.UNSET
    npc_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class QuestRewardItemSort:
    index: Optional[SortDirection] = strawberry.UNSET
    quest_code: Optional[SortDirection] = strawberry.UNSET
    item_code: Optional[SortDirection] = strawberry.UNSET
    amount: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class QuestItemSort(BaseMixinSort, RowIDMixinSort): ...


@strawberry.input(one_of=True)
class QuestScrollSort(BaseMixinSort, RowIDMixinSort):
    quest_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class MonsterSort(
    ActorMixinSort, RowIDMixinSort, ActorModelMixinSort, FlorensiaModelMixinSort
):
    skill_1_code: Optional[SortDirection] = strawberry.UNSET
    skill_1_chance: Optional[SortDirection] = strawberry.UNSET
    skill_2_code: Optional[SortDirection] = strawberry.UNSET
    skill_2_chance: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class NpcSort(
    ActorMixinSort, RowIDMixinSort, ActorModelMixinSort, FlorensiaModelMixinSort
): ...


@strawberry.input(one_of=True)
class NpcStoreItemSort:
    index: Optional[SortDirection] = strawberry.UNSET
    section_name: Optional[SortDirection] = strawberry.UNSET
    page_name: Optional[SortDirection] = strawberry.UNSET
    npc_code: Optional[SortDirection] = strawberry.UNSET
    item_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class ActorMessageSort:
    index: Optional[SortDirection] = strawberry.UNSET
    code: Optional[SortDirection] = strawberry.UNSET
    message: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class MonsterSkillSort(
    SkillMixinSort, EffectMixinSort, ClassSeaMixinSort, ClassLandMixinSort
): ...


@strawberry.input(one_of=True)
class DropSort:
    index: Optional[SortDirection] = strawberry.UNSET
    quantity: Optional[SortDirection] = strawberry.UNSET
    probability: Optional[SortDirection] = strawberry.UNSET
    monster_code: Optional[SortDirection] = strawberry.UNSET
    item_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class MoneySort:
    monster_code: Optional[SortDirection] = strawberry.UNSET
    probability: Optional[SortDirection] = strawberry.UNSET
    min: Optional[SortDirection] = strawberry.UNSET
    max: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class MonsterPositionSort:
    index: Optional[SortDirection] = strawberry.UNSET
    monster_code: Optional[SortDirection] = strawberry.UNSET
    map_code: Optional[SortDirection] = strawberry.UNSET
    amount: Optional[SortDirection] = strawberry.UNSET
    respawn_time: Optional[SortDirection] = strawberry.UNSET
    x: Optional[SortDirection] = strawberry.UNSET
    y: Optional[SortDirection] = strawberry.UNSET
    z: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class NpcPositionSort:
    index: Optional[SortDirection] = strawberry.UNSET
    npc_code: Optional[SortDirection] = strawberry.UNSET
    map_code: Optional[SortDirection] = strawberry.UNSET
    x: Optional[SortDirection] = strawberry.UNSET
    y: Optional[SortDirection] = strawberry.UNSET
    z: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class FishingBaitSort(BaseMixinSort, RowIDMixinSort): ...


@strawberry.input(one_of=True)
class FishingMaterialSort(BaseMixinSort, RowIDMixinSort): ...


@strawberry.input(one_of=True)
class EssenceSort(BaseMixinSort, RowIDMixinSort, EffectMixinSort):
    required_level: Optional[SortDirection] = strawberry.UNSET
    is_core: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class EssenceHelpSort(BaseMixinSort, RowIDMixinSort):
    description: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class CoatSort(
    ArmorMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    FlorensiaModelMixinSort,
    UpgradeRuleMixinSort,
): ...


@strawberry.input(one_of=True)
class PantsSort(
    ArmorMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    FlorensiaModelMixinSort,
    UpgradeRuleMixinSort,
): ...


@strawberry.input(one_of=True)
class GauntletSort(
    ArmorMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    FlorensiaModelMixinSort,
    UpgradeRuleMixinSort,
): ...


@strawberry.input(one_of=True)
class ShoesSort(
    ArmorMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    FlorensiaModelMixinSort,
    UpgradeRuleMixinSort,
): ...


@strawberry.input(one_of=True)
class ShieldSort(
    ArmorMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    FlorensiaModelMixinSort,
): ...


@strawberry.input(one_of=True)
class CariadSort(
    WeaponMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    UpgradeRuleMixinSort,
    FlorensiaModelMixinSort,
): ...


@strawberry.input(one_of=True)
class DaggerSort(
    WeaponMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    UpgradeRuleMixinSort,
    FlorensiaModelMixinSort,
): ...


@strawberry.input(one_of=True)
class DualsSort(
    WeaponMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    UpgradeRuleMixinSort,
    FlorensiaModelMixinSort,
): ...


@strawberry.input(one_of=True)
class FishingRodSort(
    WeaponMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    UpgradeRuleMixinSort,
    FlorensiaModelMixinSort,
): ...


@strawberry.input(one_of=True)
class OneHandedSwordSort(
    WeaponMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    UpgradeRuleMixinSort,
    FlorensiaModelMixinSort,
): ...


@strawberry.input(one_of=True)
class RapierSort(
    WeaponMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    UpgradeRuleMixinSort,
    FlorensiaModelMixinSort,
): ...


@strawberry.input(one_of=True)
class RifleSort(
    WeaponMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    UpgradeRuleMixinSort,
    FlorensiaModelMixinSort,
): ...


@strawberry.input(one_of=True)
class TwoHandedSwordSort(
    WeaponMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    UpgradeRuleMixinSort,
    FlorensiaModelMixinSort,
): ...


@strawberry.input(one_of=True)
class AccessorySort(
    EquipmentMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
): ...


@strawberry.input(one_of=True)
class DressSort(
    EquipmentMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    ExtraEquipmentModelMixinSort,
    FlorensiaModelMixinSort,
): ...


@strawberry.input(one_of=True)
class HatSort(
    EquipmentMixinSort,
    BaseMixinSort,
    RowIDMixinSort,
    ClassLandMixinSort,
    EffectMixinSort,
    ItemSetMixinSort,
    ExtraEquipmentModelMixinSort,
    FlorensiaModelMixinSort,
): ...


@strawberry.input(one_of=True)
class ShipAnchorSort(
    ShipBaseMixinSort, BaseMixinSort, RowIDMixinSort, ClassSeaMixinSort, EffectMixinSort
): ...


@strawberry.input(one_of=True)
class ShipBodySort(
    ShipBaseMixinSort, BaseMixinSort, RowIDMixinSort, ClassSeaMixinSort, EffectMixinSort
): ...


@strawberry.input(one_of=True)
class ShipFigureSort(
    ShipBaseMixinSort, BaseMixinSort, RowIDMixinSort, ClassSeaMixinSort, EffectMixinSort
): ...


@strawberry.input(one_of=True)
class ShipFlagSort(
    ShipBaseMixinSort, BaseMixinSort, RowIDMixinSort, ClassSeaMixinSort, EffectMixinSort
): ...


@strawberry.input(one_of=True)
class ShipFrontSort(
    ShipBaseMixinSort, BaseMixinSort, RowIDMixinSort, ClassSeaMixinSort, EffectMixinSort
): ...


@strawberry.input(one_of=True)
class ShipHeadMastSort(
    ShipBaseMixinSort, BaseMixinSort, RowIDMixinSort, ClassSeaMixinSort, EffectMixinSort
): ...


@strawberry.input(one_of=True)
class ShipMagicStoneSort(
    ShipBaseMixinSort, BaseMixinSort, RowIDMixinSort, ClassSeaMixinSort, EffectMixinSort
): ...


@strawberry.input(one_of=True)
class ShipMainMastSort(
    ShipBaseMixinSort, BaseMixinSort, RowIDMixinSort, ClassSeaMixinSort, EffectMixinSort
): ...


@strawberry.input(one_of=True)
class ShipNormalWeaponSort(
    ShipBaseMixinSort, BaseMixinSort, RowIDMixinSort, ClassSeaMixinSort, EffectMixinSort
): ...


@strawberry.input(one_of=True)
class ShipShellSort(BaseMixinSort, RowIDMixinSort):
    level_sea: Optional[SortDirection] = strawberry.UNSET
    physical_damage: Optional[SortDirection] = strawberry.UNSET
    explosion_range: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class ShipSpecialWeaponSort(
    ShipBaseMixinSort, BaseMixinSort, RowIDMixinSort, ClassSeaMixinSort, EffectMixinSort
): ...


@strawberry.input(one_of=True)
class PetSort(BaseMixinSort, RowIDMixinSort):
    initial_courage: Optional[SortDirection] = strawberry.UNSET
    initial_patience: Optional[SortDirection] = strawberry.UNSET
    initial_wisdom: Optional[SortDirection] = strawberry.UNSET
    is_unlimited: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class PetCombineHelpSort(BaseMixinSort, RowIDMixinSort):
    value: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class PetCombineStoneSort(BaseMixinSort, RowIDMixinSort):
    min_value: Optional[SortDirection] = strawberry.UNSET
    max_value: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class PetSkillSort(
    SkillMixinSort, EffectMixinSort, ClassSeaMixinSort, ClassLandMixinSort
): ...


@strawberry.input(one_of=True)
class PetSkillStoneSort(BaseMixinSort, RowIDMixinSort):
    skill_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class RidingPetSort(BaseMixinSort, RowIDMixinSort):
    description: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class PlayerSkillSort(
    SkillMixinSort, EffectMixinSort, ClassSeaMixinSort, ClassLandMixinSort
): ...


@strawberry.input(one_of=True)
class SkillBookSort(BaseMixinSort, RowIDMixinSort):
    skill_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class PlayerLevelStatSort:
    level: Optional[SortDirection] = strawberry.UNSET
    max_hp: Optional[SortDirection] = strawberry.UNSET
    max_mp: Optional[SortDirection] = strawberry.UNSET
    avoidance: Optional[SortDirection] = strawberry.UNSET
    melee_min_attack: Optional[SortDirection] = strawberry.UNSET
    melee_max_attack: Optional[SortDirection] = strawberry.UNSET
    melee_hitrate: Optional[SortDirection] = strawberry.UNSET
    melee_critical_rate: Optional[SortDirection] = strawberry.UNSET
    range_min_attack: Optional[SortDirection] = strawberry.UNSET
    range_max_attack: Optional[SortDirection] = strawberry.UNSET
    range_hitrate: Optional[SortDirection] = strawberry.UNSET
    range_critical_rate: Optional[SortDirection] = strawberry.UNSET
    magic_min_attack: Optional[SortDirection] = strawberry.UNSET
    magic_max_attack: Optional[SortDirection] = strawberry.UNSET
    magic_hitrate: Optional[SortDirection] = strawberry.UNSET
    magic_critical_rate: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class PlayerStatusStatSort:
    point_level: Optional[SortDirection] = strawberry.UNSET
    max_hp_increment: Optional[SortDirection] = strawberry.UNSET
    max_mp_increment: Optional[SortDirection] = strawberry.UNSET
    avoidance_increment: Optional[SortDirection] = strawberry.UNSET
    melee_min_attack_increment: Optional[SortDirection] = strawberry.UNSET
    melee_max_attack_increment: Optional[SortDirection] = strawberry.UNSET
    melee_hitrate_increment: Optional[SortDirection] = strawberry.UNSET
    melee_critical_rate_increment: Optional[SortDirection] = strawberry.UNSET
    range_min_attack_increment: Optional[SortDirection] = strawberry.UNSET
    range_max_attack_increment: Optional[SortDirection] = strawberry.UNSET
    range_hitrate_increment: Optional[SortDirection] = strawberry.UNSET
    range_critical_rate_increment: Optional[SortDirection] = strawberry.UNSET
    magic_min_attack_increment: Optional[SortDirection] = strawberry.UNSET
    magic_max_attack_increment: Optional[SortDirection] = strawberry.UNSET
    magic_hitrate_increment: Optional[SortDirection] = strawberry.UNSET
    magic_critical_rate_increment: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class RecipeSort(BaseMixinSort, RowIDMixinSort):
    result_code: Optional[SortDirection] = strawberry.UNSET
    result_quantity: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class RecipeRequiredMaterialSort:
    recipe_code: Optional[SortDirection] = strawberry.UNSET
    material_code: Optional[SortDirection] = strawberry.UNSET
    quantity: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class ProductionSort(RowIDMixinSort):
    code: Optional[SortDirection] = strawberry.UNSET
    points_required: Optional[SortDirection] = strawberry.UNSET
    result_code: Optional[SortDirection] = strawberry.UNSET
    result_quantity: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class ProductionRequiredMaterialSort:
    production_code: Optional[SortDirection] = strawberry.UNSET
    material_code: Optional[SortDirection] = strawberry.UNSET
    quantity: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class ProductionBookSort(BaseMixinSort, RowIDMixinSort):
    production_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class UpgradeHelpSort(BaseMixinSort, RowIDMixinSort):
    description: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class UpgradeStoneSort(BaseMixinSort, RowIDMixinSort):
    description: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class UpgradeCrystalSort(BaseMixinSort, RowIDMixinSort):
    description: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class UpgradeRuleSort(EffectMixinSort):
    code: Optional[SortDirection] = strawberry.UNSET
    base_code: Optional[SortDirection] = strawberry.UNSET
    level: Optional[SortDirection] = strawberry.UNSET
    cost: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class SealBreakHelpSort(BaseMixinSort, RowIDMixinSort):
    description: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class ItemListSort(ClassLandMixinSort, ClassSeaMixinSort, EffectMixinSort):
    code: Optional[SortDirection] = strawberry.UNSET
    tablename: Optional[SortDirection] = strawberry.UNSET
    name: Optional[SortDirection] = strawberry.UNSET
    icon: Optional[SortDirection] = strawberry.UNSET
    duration: Optional[SortDirection] = strawberry.UNSET
    level_land: Optional[SortDirection] = strawberry.UNSET
    level_sea: Optional[SortDirection] = strawberry.UNSET
    model_name: Optional[SortDirection] = strawberry.UNSET
    model_variant: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class PlayerRequiredSkillSort:
    skill_code: Optional[SortDirection] = strawberry.UNSET
    required_skill_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class EffectSort:
    index: Optional[SortDirection] = strawberry.UNSET
    ref_code: Optional[SortDirection] = strawberry.UNSET
    operator: Optional[SortDirection] = strawberry.UNSET
    value: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class ItemSetSort(EffectMixinSort):
    code: Optional[SortDirection] = strawberry.UNSET
    name: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class ItemSetItemSort:
    set_code: Optional[SortDirection] = strawberry.UNSET
    item_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class MapSort:
    code: Optional[SortDirection] = strawberry.UNSET
    name: Optional[SortDirection] = strawberry.UNSET
    left: Optional[SortDirection] = strawberry.UNSET
    top: Optional[SortDirection] = strawberry.UNSET
    width: Optional[SortDirection] = strawberry.UNSET
    height: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class MapAreaSort:
    map_code: Optional[SortDirection] = strawberry.UNSET
    area_code: Optional[SortDirection] = strawberry.UNSET
    name: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class BulletSort(BaseMixinSort, RowIDMixinSort): ...


@strawberry.input(one_of=True)
class ConsumableSort(BaseMixinSort, RowIDMixinSort):
    description: Optional[SortDirection] = strawberry.UNSET
    level_land: Optional[SortDirection] = strawberry.UNSET
    level_sea: Optional[SortDirection] = strawberry.UNSET
    cooldown_id: Optional[SortDirection] = strawberry.UNSET
    cooldown: Optional[SortDirection] = strawberry.UNSET
    cast_time: Optional[SortDirection] = strawberry.UNSET
    value: Optional[SortDirection] = strawberry.UNSET
    skill_code: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class MaterialSort(BaseMixinSort, RowIDMixinSort): ...


@strawberry.input(one_of=True)
class TowerFloorSort:
    code: Optional[SortDirection] = strawberry.UNSET
    floor_number: Optional[SortDirection] = strawberry.UNSET
    time: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class TowerFloorMonsterSort:
    floor_code: Optional[SortDirection] = strawberry.UNSET
    monster_code: Optional[SortDirection] = strawberry.UNSET
    amount: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class Available3DModelSort:
    asset_path: Optional[SortDirection] = strawberry.UNSET
    filename: Optional[SortDirection] = strawberry.UNSET
    model_name: Optional[SortDirection] = strawberry.UNSET
    model_variant: Optional[SortDirection] = strawberry.UNSET
    animation_name: Optional[SortDirection] = strawberry.UNSET


@strawberry.input(one_of=True)
class FusionHelpSort(BaseMixinSort, RowIDMixinSort):
    description: Optional[SortDirection] = strawberry.UNSET
