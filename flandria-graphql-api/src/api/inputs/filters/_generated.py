from typing import Optional

import strawberry

from src.api import enums

from .scalar_filters import BooleanFilter, EnumFilter, NumberFilter, StringFilter


@strawberry.input
class BaseMixinFilter:
    code: Optional[StringFilter] = strawberry.UNSET
    name: Optional[StringFilter] = strawberry.UNSET
    icon: Optional[StringFilter] = strawberry.UNSET
    is_tradable: Optional[BooleanFilter] = strawberry.UNSET
    is_destroyable: Optional[BooleanFilter] = strawberry.UNSET
    npc_sell_price: Optional[NumberFilter] = strawberry.UNSET
    is_sellable: Optional[BooleanFilter] = strawberry.UNSET
    is_storageable: Optional[BooleanFilter] = strawberry.UNSET
    grade: Optional[EnumFilter[enums.ItemGrade]] = strawberry.UNSET
    duration: Optional[NumberFilter] = strawberry.UNSET
    stack_size: Optional[NumberFilter] = strawberry.UNSET
    npc_buy_price: Optional[NumberFilter] = strawberry.UNSET


@strawberry.input
class RowIDMixinFilter:
    row_id: Optional[NumberFilter] = strawberry.UNSET


@strawberry.input
class ActorMixinFilter:
    code: Optional[StringFilter] = strawberry.UNSET
    name: Optional[StringFilter] = strawberry.UNSET
    icon: Optional[StringFilter] = strawberry.UNSET
    level: Optional[NumberFilter] = strawberry.UNSET
    grade: Optional[EnumFilter[enums.ActorGrade]] = strawberry.UNSET
    is_inanimate: Optional[BooleanFilter] = strawberry.UNSET
    is_sea: Optional[BooleanFilter] = strawberry.UNSET
    is_ship: Optional[BooleanFilter] = strawberry.UNSET
    is_air: Optional[BooleanFilter] = strawberry.UNSET
    is_tameable: Optional[BooleanFilter] = strawberry.UNSET
    experience: Optional[NumberFilter] = strawberry.UNSET
    health_points: Optional[NumberFilter] = strawberry.UNSET
    recovery_rate: Optional[NumberFilter] = strawberry.UNSET
    minimum_physical_damage: Optional[NumberFilter] = strawberry.UNSET
    maximum_physical_damage: Optional[NumberFilter] = strawberry.UNSET
    minimum_magical_damage: Optional[NumberFilter] = strawberry.UNSET
    maximum_magical_damage: Optional[NumberFilter] = strawberry.UNSET
    physical_defense: Optional[NumberFilter] = strawberry.UNSET
    magical_defense: Optional[NumberFilter] = strawberry.UNSET
    physical_evasion_rate: Optional[NumberFilter] = strawberry.UNSET
    physical_hit_rate: Optional[NumberFilter] = strawberry.UNSET
    magical_hit_rate: Optional[NumberFilter] = strawberry.UNSET
    critical_rate: Optional[NumberFilter] = strawberry.UNSET
    critical_resistance_rate: Optional[NumberFilter] = strawberry.UNSET
    sea_attack_aoe_range: Optional[NumberFilter] = strawberry.UNSET
    ship_guns_count: Optional[NumberFilter] = strawberry.UNSET
    ship_guns_speed: Optional[NumberFilter] = strawberry.UNSET
    ship_attack_range: Optional[NumberFilter] = strawberry.UNSET
    attack_cast_time: Optional[NumberFilter] = strawberry.UNSET
    attack_cooldown: Optional[NumberFilter] = strawberry.UNSET
    despawn_delay_time: Optional[NumberFilter] = strawberry.UNSET
    attack_vision_range: Optional[NumberFilter] = strawberry.UNSET
    nearby_attack_vision_range: Optional[NumberFilter] = strawberry.UNSET
    is_ranged: Optional[BooleanFilter] = strawberry.UNSET
    attack_range: Optional[NumberFilter] = strawberry.UNSET
    walking_speed: Optional[NumberFilter] = strawberry.UNSET
    running_speed: Optional[NumberFilter] = strawberry.UNSET
    turning_speed: Optional[NumberFilter] = strawberry.UNSET
    messages_code: Optional[StringFilter] = strawberry.UNSET
    posion_resistance: Optional[NumberFilter] = strawberry.UNSET
    fire_resistance: Optional[NumberFilter] = strawberry.UNSET
    cold_resistance: Optional[NumberFilter] = strawberry.UNSET
    lightning_resistance: Optional[NumberFilter] = strawberry.UNSET
    holy_resistance: Optional[NumberFilter] = strawberry.UNSET
    dark_resistance: Optional[NumberFilter] = strawberry.UNSET
    messages: Optional["ActorMessageFilter"] = strawberry.UNSET


@strawberry.input
class ActorModelMixinFilter:
    model_scale: Optional[NumberFilter] = strawberry.UNSET


@strawberry.input
class FlorensiaModelMixinFilter:
    model_name: Optional[StringFilter] = strawberry.UNSET
    models: Optional["Available3DModelFilter"] = strawberry.UNSET


@strawberry.input
class SkillMixinFilter:
    code: Optional[StringFilter] = strawberry.UNSET
    reference_code: Optional[StringFilter] = strawberry.UNSET
    name: Optional[StringFilter] = strawberry.UNSET
    icon: Optional[StringFilter] = strawberry.UNSET
    required_level_land: Optional[NumberFilter] = strawberry.UNSET
    required_level_sea: Optional[NumberFilter] = strawberry.UNSET
    skill_level: Optional[NumberFilter] = strawberry.UNSET
    skill_max_level: Optional[NumberFilter] = strawberry.UNSET
    mana_cost: Optional[NumberFilter] = strawberry.UNSET
    accuracy: Optional[NumberFilter] = strawberry.UNSET
    hit_correction: Optional[NumberFilter] = strawberry.UNSET
    cooldown: Optional[NumberFilter] = strawberry.UNSET
    cast_time: Optional[NumberFilter] = strawberry.UNSET
    cast_distance: Optional[NumberFilter] = strawberry.UNSET
    dash_distance: Optional[NumberFilter] = strawberry.UNSET
    push_distance: Optional[NumberFilter] = strawberry.UNSET
    effect_range: Optional[NumberFilter] = strawberry.UNSET
    effect_angle: Optional[NumberFilter] = strawberry.UNSET
    is_persistent: Optional[BooleanFilter] = strawberry.UNSET
    duration: Optional[NumberFilter] = strawberry.UNSET
    toggle_tick_time: Optional[NumberFilter] = strawberry.UNSET
    toggle_operator: Optional[StringFilter] = strawberry.UNSET
    toggle_hp_value: Optional[NumberFilter] = strawberry.UNSET
    toggle_mp_value: Optional[NumberFilter] = strawberry.UNSET
    required_weapons: Optional[StringFilter] = strawberry.UNSET
    description: Optional[StringFilter] = strawberry.UNSET


@strawberry.input
class EffectMixinFilter:
    effects: Optional["EffectFilter"] = strawberry.UNSET


@strawberry.input
class ClassSeaMixinFilter:
    is_armored: Optional[BooleanFilter] = strawberry.UNSET
    is_big_gun: Optional[BooleanFilter] = strawberry.UNSET
    is_torpedo: Optional[BooleanFilter] = strawberry.UNSET
    is_maintenance: Optional[BooleanFilter] = strawberry.UNSET
    is_assault: Optional[BooleanFilter] = strawberry.UNSET


@strawberry.input
class ClassLandMixinFilter:
    is_noble: Optional[BooleanFilter] = strawberry.UNSET
    is_court_magician: Optional[BooleanFilter] = strawberry.UNSET
    is_magic_knight: Optional[BooleanFilter] = strawberry.UNSET
    is_saint: Optional[BooleanFilter] = strawberry.UNSET
    is_priest: Optional[BooleanFilter] = strawberry.UNSET
    is_shaman: Optional[BooleanFilter] = strawberry.UNSET
    is_mercenary: Optional[BooleanFilter] = strawberry.UNSET
    is_gladiator: Optional[BooleanFilter] = strawberry.UNSET
    is_guardian_swordsman: Optional[BooleanFilter] = strawberry.UNSET
    is_explorer: Optional[BooleanFilter] = strawberry.UNSET
    is_excavator: Optional[BooleanFilter] = strawberry.UNSET
    is_sniper: Optional[BooleanFilter] = strawberry.UNSET


@strawberry.input
class ArmorMixinFilter:
    level_land: Optional[NumberFilter] = strawberry.UNSET
    level_sea: Optional[NumberFilter] = strawberry.UNSET
    physical_defense: Optional[NumberFilter] = strawberry.UNSET
    magical_defense: Optional[NumberFilter] = strawberry.UNSET


@strawberry.input
class ItemSetMixinFilter:
    item_set_code: Optional[StringFilter] = strawberry.UNSET
    item_set: Optional["ItemSetFilter"] = strawberry.UNSET


@strawberry.input
class UpgradeRuleMixinFilter:
    upgrade_rule_base_code: Optional[StringFilter] = strawberry.UNSET
    upgrade_rule: Optional["UpgradeRuleFilter"] = strawberry.UNSET


@strawberry.input
class WeaponMixinFilter:
    level_land: Optional[NumberFilter] = strawberry.UNSET
    level_sea: Optional[NumberFilter] = strawberry.UNSET
    minimum_physical_damage: Optional[NumberFilter] = strawberry.UNSET
    maximum_physical_damage: Optional[NumberFilter] = strawberry.UNSET
    minimum_magical_damage: Optional[NumberFilter] = strawberry.UNSET
    maximum_magical_damage: Optional[NumberFilter] = strawberry.UNSET
    attack_speed: Optional[NumberFilter] = strawberry.UNSET
    attack_range: Optional[NumberFilter] = strawberry.UNSET
    item_flag: Optional[EnumFilter[enums.ItemFlag]] = strawberry.UNSET


@strawberry.input
class EquipmentMixinFilter:
    gender: Optional[EnumFilter[enums.Gender]] = strawberry.UNSET
    level_land: Optional[NumberFilter] = strawberry.UNSET
    level_sea: Optional[NumberFilter] = strawberry.UNSET
    item_flag: Optional[EnumFilter[enums.ItemFlag]] = strawberry.UNSET


@strawberry.input
class ExtraEquipmentModelMixinFilter: ...


@strawberry.input
class ShipBaseMixinFilter:
    npc_tune_price: Optional[NumberFilter] = strawberry.UNSET
    level_sea: Optional[NumberFilter] = strawberry.UNSET
    guns_front: Optional[NumberFilter] = strawberry.UNSET
    guns_side: Optional[NumberFilter] = strawberry.UNSET
    crew_size: Optional[NumberFilter] = strawberry.UNSET
    physical_defense: Optional[NumberFilter] = strawberry.UNSET
    protection: Optional[NumberFilter] = strawberry.UNSET
    balance: Optional[NumberFilter] = strawberry.UNSET
    dp: Optional[NumberFilter] = strawberry.UNSET
    en: Optional[NumberFilter] = strawberry.UNSET
    en_usage: Optional[NumberFilter] = strawberry.UNSET
    en_recovery: Optional[NumberFilter] = strawberry.UNSET
    acceleration: Optional[NumberFilter] = strawberry.UNSET
    deceleration: Optional[NumberFilter] = strawberry.UNSET
    turning_power: Optional[NumberFilter] = strawberry.UNSET
    favorable_wind: Optional[NumberFilter] = strawberry.UNSET
    adverse_wind: Optional[NumberFilter] = strawberry.UNSET
    physical_damage: Optional[NumberFilter] = strawberry.UNSET
    weapon_range: Optional[NumberFilter] = strawberry.UNSET
    critical_chance: Optional[NumberFilter] = strawberry.UNSET
    reload_speed: Optional[NumberFilter] = strawberry.UNSET
    hit_range: Optional[NumberFilter] = strawberry.UNSET


@strawberry.input
class RandomBoxFilter(BaseMixinFilter, RowIDMixinFilter):
    level_land: Optional[NumberFilter] = strawberry.UNSET
    level_sea: Optional[NumberFilter] = strawberry.UNSET
    rewards: Optional["RandomBoxRewardFilter"] = strawberry.UNSET


@strawberry.input
class RandomBoxRewardFilter:
    index: Optional[NumberFilter] = strawberry.UNSET
    random_box_code: Optional[StringFilter] = strawberry.UNSET
    reward_code: Optional[StringFilter] = strawberry.UNSET
    quantity: Optional[NumberFilter] = strawberry.UNSET
    probability: Optional[NumberFilter] = strawberry.UNSET
    item: Optional["ItemListFilter"] = strawberry.UNSET


@strawberry.input
class QuestFilter:
    code: Optional[StringFilter] = strawberry.UNSET
    is_sea: Optional[BooleanFilter] = strawberry.UNSET
    level: Optional[NumberFilter] = strawberry.UNSET
    is_mercenary: Optional[BooleanFilter] = strawberry.UNSET
    is_saint: Optional[BooleanFilter] = strawberry.UNSET
    is_noble: Optional[BooleanFilter] = strawberry.UNSET
    is_explorer: Optional[BooleanFilter] = strawberry.UNSET
    experience: Optional[NumberFilter] = strawberry.UNSET
    money: Optional[NumberFilter] = strawberry.UNSET
    selectable_items_count: Optional[NumberFilter] = strawberry.UNSET
    title: Optional[StringFilter] = strawberry.UNSET
    description: Optional[StringFilter] = strawberry.UNSET
    pre_dialog: Optional[StringFilter] = strawberry.UNSET
    start_dialog: Optional[StringFilter] = strawberry.UNSET
    run_dialog: Optional[StringFilter] = strawberry.UNSET
    finish_dialog: Optional[StringFilter] = strawberry.UNSET
    previous_quest_code: Optional[StringFilter] = strawberry.UNSET
    start_npc_code: Optional[StringFilter] = strawberry.UNSET
    start_area_code: Optional[StringFilter] = strawberry.UNSET
    end_npc_code: Optional[StringFilter] = strawberry.UNSET
    previous_quest: Optional["QuestFilter"] = strawberry.UNSET
    start_npc: Optional["NpcFilter"] = strawberry.UNSET
    start_area: Optional["MapAreaFilter"] = strawberry.UNSET
    end_npc: Optional["NpcFilter"] = strawberry.UNSET
    give_items: Optional["QuestGiveItemFilter"] = strawberry.UNSET
    reward_items: Optional["QuestRewardItemFilter"] = strawberry.UNSET
    missions: Optional["QuestMissionFilter"] = strawberry.UNSET


@strawberry.input
class QuestGiveItemFilter:
    quest_code: Optional[StringFilter] = strawberry.UNSET
    item_code: Optional[StringFilter] = strawberry.UNSET
    amount: Optional[NumberFilter] = strawberry.UNSET
    item: Optional["ItemListFilter"] = strawberry.UNSET


@strawberry.input
class QuestMissionFilter:
    index: Optional[NumberFilter] = strawberry.UNSET
    quest_code: Optional[StringFilter] = strawberry.UNSET
    work_type: Optional[EnumFilter[enums.QuestMissionType]] = strawberry.UNSET
    count: Optional[NumberFilter] = strawberry.UNSET
    description: Optional[StringFilter] = strawberry.UNSET
    map_code: Optional[StringFilter] = strawberry.UNSET
    x: Optional[NumberFilter] = strawberry.UNSET
    y: Optional[NumberFilter] = strawberry.UNSET
    monster_code: Optional[StringFilter] = strawberry.UNSET
    item_code: Optional[StringFilter] = strawberry.UNSET
    quest_item_code: Optional[StringFilter] = strawberry.UNSET
    npc_code: Optional[StringFilter] = strawberry.UNSET
    map: Optional["MapFilter"] = strawberry.UNSET
    monster: Optional["MonsterFilter"] = strawberry.UNSET
    item: Optional["ItemListFilter"] = strawberry.UNSET
    quest_item: Optional["QuestItemFilter"] = strawberry.UNSET
    npc: Optional["NpcFilter"] = strawberry.UNSET


@strawberry.input
class QuestRewardItemFilter:
    index: Optional[NumberFilter] = strawberry.UNSET
    quest_code: Optional[StringFilter] = strawberry.UNSET
    item_code: Optional[StringFilter] = strawberry.UNSET
    amount: Optional[NumberFilter] = strawberry.UNSET
    item: Optional["ItemListFilter"] = strawberry.UNSET


@strawberry.input
class QuestItemFilter(BaseMixinFilter, RowIDMixinFilter):
    quests_by_mission: Optional["QuestFilter"] = strawberry.UNSET
    quests_by_give_item: Optional["QuestFilter"] = strawberry.UNSET


@strawberry.input
class QuestScrollFilter(BaseMixinFilter, RowIDMixinFilter):
    quest_code: Optional[StringFilter] = strawberry.UNSET
    quest: Optional["QuestFilter"] = strawberry.UNSET


@strawberry.input
class MonsterFilter(
    ActorMixinFilter, RowIDMixinFilter, ActorModelMixinFilter, FlorensiaModelMixinFilter
):
    skill_1_code: Optional[StringFilter] = strawberry.UNSET
    skill_1_chance: Optional[NumberFilter] = strawberry.UNSET
    skill_2_code: Optional[StringFilter] = strawberry.UNSET
    skill_2_chance: Optional[NumberFilter] = strawberry.UNSET
    skill_1: Optional["MonsterSkillFilter"] = strawberry.UNSET
    skill_2: Optional["MonsterSkillFilter"] = strawberry.UNSET
    drops: Optional["DropFilter"] = strawberry.UNSET
    money: Optional["MoneyFilter"] = strawberry.UNSET
    positions: Optional["MonsterPositionFilter"] = strawberry.UNSET


@strawberry.input
class NpcFilter(
    ActorMixinFilter, RowIDMixinFilter, ActorModelMixinFilter, FlorensiaModelMixinFilter
):
    positions: Optional["NpcPositionFilter"] = strawberry.UNSET
    quests: Optional["QuestFilter"] = strawberry.UNSET
    store_items: Optional["NpcStoreItemFilter"] = strawberry.UNSET


@strawberry.input
class NpcStoreItemFilter:
    index: Optional[NumberFilter] = strawberry.UNSET
    section_name: Optional[StringFilter] = strawberry.UNSET
    page_name: Optional[StringFilter] = strawberry.UNSET
    npc_code: Optional[StringFilter] = strawberry.UNSET
    item_code: Optional[StringFilter] = strawberry.UNSET
    item: Optional["ItemListFilter"] = strawberry.UNSET


@strawberry.input
class ActorMessageFilter:
    index: Optional[NumberFilter] = strawberry.UNSET
    code: Optional[StringFilter] = strawberry.UNSET
    trigger: Optional[EnumFilter[enums.MonsterMessageTrigger]] = strawberry.UNSET
    message: Optional[StringFilter] = strawberry.UNSET


@strawberry.input
class MonsterSkillFilter(
    SkillMixinFilter, EffectMixinFilter, ClassSeaMixinFilter, ClassLandMixinFilter
): ...


@strawberry.input
class DropFilter:
    index: Optional[NumberFilter] = strawberry.UNSET
    quantity: Optional[NumberFilter] = strawberry.UNSET
    probability: Optional[NumberFilter] = strawberry.UNSET
    monster_code: Optional[StringFilter] = strawberry.UNSET
    item_code: Optional[StringFilter] = strawberry.UNSET
    monster: Optional["MonsterFilter"] = strawberry.UNSET
    item: Optional["ItemListFilter"] = strawberry.UNSET


@strawberry.input
class MoneyFilter:
    monster_code: Optional[StringFilter] = strawberry.UNSET
    probability: Optional[NumberFilter] = strawberry.UNSET
    min: Optional[NumberFilter] = strawberry.UNSET
    max: Optional[NumberFilter] = strawberry.UNSET
    monster: Optional["MonsterFilter"] = strawberry.UNSET


@strawberry.input
class MonsterPositionFilter:
    index: Optional[NumberFilter] = strawberry.UNSET
    monster_code: Optional[StringFilter] = strawberry.UNSET
    map_code: Optional[StringFilter] = strawberry.UNSET
    amount: Optional[NumberFilter] = strawberry.UNSET
    respawn_time: Optional[NumberFilter] = strawberry.UNSET
    x: Optional[NumberFilter] = strawberry.UNSET
    y: Optional[NumberFilter] = strawberry.UNSET
    z: Optional[NumberFilter] = strawberry.UNSET
    monster: Optional["MonsterFilter"] = strawberry.UNSET
    map: Optional["MapFilter"] = strawberry.UNSET


@strawberry.input
class NpcPositionFilter:
    index: Optional[NumberFilter] = strawberry.UNSET
    npc_code: Optional[StringFilter] = strawberry.UNSET
    map_code: Optional[StringFilter] = strawberry.UNSET
    x: Optional[NumberFilter] = strawberry.UNSET
    y: Optional[NumberFilter] = strawberry.UNSET
    z: Optional[NumberFilter] = strawberry.UNSET
    npc: Optional["NpcFilter"] = strawberry.UNSET
    map: Optional["MapFilter"] = strawberry.UNSET


@strawberry.input
class FishingBaitFilter(BaseMixinFilter, RowIDMixinFilter): ...


@strawberry.input
class FishingMaterialFilter(BaseMixinFilter, RowIDMixinFilter): ...


@strawberry.input
class EssenceFilter(BaseMixinFilter, RowIDMixinFilter, EffectMixinFilter):
    equip_type: Optional[EnumFilter[enums.EssenceEquipType]] = strawberry.UNSET
    required_level: Optional[NumberFilter] = strawberry.UNSET
    is_core: Optional[BooleanFilter] = strawberry.UNSET


@strawberry.input
class EssenceHelpFilter(BaseMixinFilter, RowIDMixinFilter):
    description: Optional[StringFilter] = strawberry.UNSET


@strawberry.input
class CoatFilter(
    ArmorMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    FlorensiaModelMixinFilter,
    UpgradeRuleMixinFilter,
): ...


@strawberry.input
class PantsFilter(
    ArmorMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    FlorensiaModelMixinFilter,
    UpgradeRuleMixinFilter,
): ...


@strawberry.input
class GauntletFilter(
    ArmorMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    FlorensiaModelMixinFilter,
    UpgradeRuleMixinFilter,
): ...


@strawberry.input
class ShoesFilter(
    ArmorMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    FlorensiaModelMixinFilter,
    UpgradeRuleMixinFilter,
): ...


@strawberry.input
class ShieldFilter(
    ArmorMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    FlorensiaModelMixinFilter,
): ...


@strawberry.input
class CariadFilter(
    WeaponMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    UpgradeRuleMixinFilter,
    FlorensiaModelMixinFilter,
): ...


@strawberry.input
class DaggerFilter(
    WeaponMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    UpgradeRuleMixinFilter,
    FlorensiaModelMixinFilter,
): ...


@strawberry.input
class DualsFilter(
    WeaponMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    UpgradeRuleMixinFilter,
    FlorensiaModelMixinFilter,
): ...


@strawberry.input
class FishingRodFilter(
    WeaponMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    UpgradeRuleMixinFilter,
    FlorensiaModelMixinFilter,
): ...


@strawberry.input
class OneHandedSwordFilter(
    WeaponMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    UpgradeRuleMixinFilter,
    FlorensiaModelMixinFilter,
): ...


@strawberry.input
class RapierFilter(
    WeaponMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    UpgradeRuleMixinFilter,
    FlorensiaModelMixinFilter,
): ...


@strawberry.input
class RifleFilter(
    WeaponMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    UpgradeRuleMixinFilter,
    FlorensiaModelMixinFilter,
): ...


@strawberry.input
class TwoHandedSwordFilter(
    WeaponMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    UpgradeRuleMixinFilter,
    FlorensiaModelMixinFilter,
): ...


@strawberry.input
class AccessoryFilter(
    EquipmentMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
):
    accessory_type: Optional[EnumFilter[enums.AccessoryType]] = strawberry.UNSET


@strawberry.input
class DressFilter(
    EquipmentMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    ExtraEquipmentModelMixinFilter,
    FlorensiaModelMixinFilter,
): ...


@strawberry.input
class HatFilter(
    EquipmentMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassLandMixinFilter,
    EffectMixinFilter,
    ItemSetMixinFilter,
    ExtraEquipmentModelMixinFilter,
    FlorensiaModelMixinFilter,
): ...


@strawberry.input
class ShipAnchorFilter(
    ShipBaseMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassSeaMixinFilter,
    EffectMixinFilter,
): ...


@strawberry.input
class ShipBodyFilter(
    ShipBaseMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassSeaMixinFilter,
    EffectMixinFilter,
): ...


@strawberry.input
class ShipFigureFilter(
    ShipBaseMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassSeaMixinFilter,
    EffectMixinFilter,
): ...


@strawberry.input
class ShipFlagFilter(
    ShipBaseMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassSeaMixinFilter,
    EffectMixinFilter,
): ...


@strawberry.input
class ShipFrontFilter(
    ShipBaseMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassSeaMixinFilter,
    EffectMixinFilter,
): ...


@strawberry.input
class ShipHeadMastFilter(
    ShipBaseMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassSeaMixinFilter,
    EffectMixinFilter,
): ...


@strawberry.input
class ShipMagicStoneFilter(
    ShipBaseMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassSeaMixinFilter,
    EffectMixinFilter,
): ...


@strawberry.input
class ShipMainMastFilter(
    ShipBaseMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassSeaMixinFilter,
    EffectMixinFilter,
): ...


@strawberry.input
class ShipNormalWeaponFilter(
    ShipBaseMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassSeaMixinFilter,
    EffectMixinFilter,
): ...


@strawberry.input
class ShipShellFilter(BaseMixinFilter, RowIDMixinFilter):
    level_sea: Optional[NumberFilter] = strawberry.UNSET
    physical_damage: Optional[NumberFilter] = strawberry.UNSET
    explosion_range: Optional[NumberFilter] = strawberry.UNSET


@strawberry.input
class ShipSpecialWeaponFilter(
    ShipBaseMixinFilter,
    BaseMixinFilter,
    RowIDMixinFilter,
    ClassSeaMixinFilter,
    EffectMixinFilter,
): ...


@strawberry.input
class PetFilter(BaseMixinFilter, RowIDMixinFilter):
    initial_courage: Optional[NumberFilter] = strawberry.UNSET
    initial_patience: Optional[NumberFilter] = strawberry.UNSET
    initial_wisdom: Optional[NumberFilter] = strawberry.UNSET
    is_unlimited: Optional[BooleanFilter] = strawberry.UNSET


@strawberry.input
class PetCombineHelpFilter(BaseMixinFilter, RowIDMixinFilter):
    value: Optional[NumberFilter] = strawberry.UNSET


@strawberry.input
class PetCombineStoneFilter(BaseMixinFilter, RowIDMixinFilter):
    min_value: Optional[NumberFilter] = strawberry.UNSET
    max_value: Optional[NumberFilter] = strawberry.UNSET


@strawberry.input
class PetSkillFilter(
    SkillMixinFilter, EffectMixinFilter, ClassSeaMixinFilter, ClassLandMixinFilter
): ...


@strawberry.input
class PetSkillStoneFilter(BaseMixinFilter, RowIDMixinFilter):
    skill_code: Optional[StringFilter] = strawberry.UNSET
    skill: Optional["PetSkillFilter"] = strawberry.UNSET


@strawberry.input
class RidingPetFilter(BaseMixinFilter, RowIDMixinFilter):
    description: Optional[StringFilter] = strawberry.UNSET


@strawberry.input
class PlayerSkillFilter(
    SkillMixinFilter, EffectMixinFilter, ClassSeaMixinFilter, ClassLandMixinFilter
):
    required_skills: Optional["PlayerRequiredSkillFilter"] = strawberry.UNSET


@strawberry.input
class SkillBookFilter(BaseMixinFilter, RowIDMixinFilter):
    skill_code: Optional[StringFilter] = strawberry.UNSET
    skill: Optional["PlayerSkillFilter"] = strawberry.UNSET


@strawberry.input
class PlayerLevelStatFilter:
    base_class: Optional[EnumFilter[enums.BaseClassType]] = strawberry.UNSET
    level: Optional[NumberFilter] = strawberry.UNSET
    max_hp: Optional[NumberFilter] = strawberry.UNSET
    max_mp: Optional[NumberFilter] = strawberry.UNSET
    avoidance: Optional[NumberFilter] = strawberry.UNSET
    melee_min_attack: Optional[NumberFilter] = strawberry.UNSET
    melee_max_attack: Optional[NumberFilter] = strawberry.UNSET
    melee_hitrate: Optional[NumberFilter] = strawberry.UNSET
    melee_critical_rate: Optional[NumberFilter] = strawberry.UNSET
    range_min_attack: Optional[NumberFilter] = strawberry.UNSET
    range_max_attack: Optional[NumberFilter] = strawberry.UNSET
    range_hitrate: Optional[NumberFilter] = strawberry.UNSET
    range_critical_rate: Optional[NumberFilter] = strawberry.UNSET
    magic_min_attack: Optional[NumberFilter] = strawberry.UNSET
    magic_max_attack: Optional[NumberFilter] = strawberry.UNSET
    magic_hitrate: Optional[NumberFilter] = strawberry.UNSET
    magic_critical_rate: Optional[NumberFilter] = strawberry.UNSET


@strawberry.input
class PlayerStatusStatFilter:
    base_class: Optional[EnumFilter[enums.BaseClassType]] = strawberry.UNSET
    point_level: Optional[NumberFilter] = strawberry.UNSET
    stat_type: Optional[EnumFilter[enums.StatType]] = strawberry.UNSET
    max_hp_increment: Optional[NumberFilter] = strawberry.UNSET
    max_mp_increment: Optional[NumberFilter] = strawberry.UNSET
    avoidance_increment: Optional[NumberFilter] = strawberry.UNSET
    melee_min_attack_increment: Optional[NumberFilter] = strawberry.UNSET
    melee_max_attack_increment: Optional[NumberFilter] = strawberry.UNSET
    melee_hitrate_increment: Optional[NumberFilter] = strawberry.UNSET
    melee_critical_rate_increment: Optional[NumberFilter] = strawberry.UNSET
    range_min_attack_increment: Optional[NumberFilter] = strawberry.UNSET
    range_max_attack_increment: Optional[NumberFilter] = strawberry.UNSET
    range_hitrate_increment: Optional[NumberFilter] = strawberry.UNSET
    range_critical_rate_increment: Optional[NumberFilter] = strawberry.UNSET
    magic_min_attack_increment: Optional[NumberFilter] = strawberry.UNSET
    magic_max_attack_increment: Optional[NumberFilter] = strawberry.UNSET
    magic_hitrate_increment: Optional[NumberFilter] = strawberry.UNSET
    magic_critical_rate_increment: Optional[NumberFilter] = strawberry.UNSET


@strawberry.input
class RecipeFilter(BaseMixinFilter, RowIDMixinFilter):
    result_code: Optional[StringFilter] = strawberry.UNSET
    result_quantity: Optional[NumberFilter] = strawberry.UNSET
    result_item: Optional["ItemListFilter"] = strawberry.UNSET
    required_materials: Optional["RecipeRequiredMaterialFilter"] = strawberry.UNSET


@strawberry.input
class RecipeRequiredMaterialFilter:
    recipe_code: Optional[StringFilter] = strawberry.UNSET
    material_code: Optional[StringFilter] = strawberry.UNSET
    quantity: Optional[NumberFilter] = strawberry.UNSET
    item: Optional["ItemListFilter"] = strawberry.UNSET


@strawberry.input
class ProductionFilter(RowIDMixinFilter):
    code: Optional[StringFilter] = strawberry.UNSET
    type: Optional[EnumFilter[enums.SecondJobType]] = strawberry.UNSET
    points_required: Optional[NumberFilter] = strawberry.UNSET
    result_code: Optional[StringFilter] = strawberry.UNSET
    result_quantity: Optional[NumberFilter] = strawberry.UNSET
    result_item: Optional["ItemListFilter"] = strawberry.UNSET
    required_materials: Optional["ProductionRequiredMaterialFilter"] = strawberry.UNSET


@strawberry.input
class ProductionRequiredMaterialFilter:
    production_code: Optional[StringFilter] = strawberry.UNSET
    material_code: Optional[StringFilter] = strawberry.UNSET
    quantity: Optional[NumberFilter] = strawberry.UNSET
    item: Optional["ItemListFilter"] = strawberry.UNSET


@strawberry.input
class ProductionBookFilter(BaseMixinFilter, RowIDMixinFilter):
    production_code: Optional[StringFilter] = strawberry.UNSET
    production: Optional["ProductionFilter"] = strawberry.UNSET


@strawberry.input
class UpgradeHelpFilter(BaseMixinFilter, RowIDMixinFilter):
    description: Optional[StringFilter] = strawberry.UNSET


@strawberry.input
class UpgradeStoneFilter(BaseMixinFilter, RowIDMixinFilter):
    description: Optional[StringFilter] = strawberry.UNSET


@strawberry.input
class UpgradeCrystalFilter(BaseMixinFilter, RowIDMixinFilter):
    description: Optional[StringFilter] = strawberry.UNSET


@strawberry.input
class UpgradeRuleFilter(EffectMixinFilter):
    code: Optional[StringFilter] = strawberry.UNSET
    base_code: Optional[StringFilter] = strawberry.UNSET
    level: Optional[NumberFilter] = strawberry.UNSET
    cost: Optional[NumberFilter] = strawberry.UNSET


@strawberry.input
class SealBreakHelpFilter(BaseMixinFilter, RowIDMixinFilter):
    description: Optional[StringFilter] = strawberry.UNSET


@strawberry.input
class ItemListFilter(ClassLandMixinFilter, ClassSeaMixinFilter, EffectMixinFilter):
    code: Optional[StringFilter] = strawberry.UNSET
    tablename: Optional[StringFilter] = strawberry.UNSET
    name: Optional[StringFilter] = strawberry.UNSET
    icon: Optional[StringFilter] = strawberry.UNSET
    grade: Optional[EnumFilter[enums.ItemGrade]] = strawberry.UNSET
    gender: Optional[EnumFilter[enums.Gender]] = strawberry.UNSET
    duration: Optional[NumberFilter] = strawberry.UNSET
    level_land: Optional[NumberFilter] = strawberry.UNSET
    level_sea: Optional[NumberFilter] = strawberry.UNSET
    model_name: Optional[StringFilter] = strawberry.UNSET


@strawberry.input
class PlayerRequiredSkillFilter:
    skill_code: Optional[StringFilter] = strawberry.UNSET
    required_skill_code: Optional[StringFilter] = strawberry.UNSET
    skill: Optional["PlayerSkillFilter"] = strawberry.UNSET


@strawberry.input
class EffectFilter:
    index: Optional[NumberFilter] = strawberry.UNSET
    ref_code: Optional[StringFilter] = strawberry.UNSET
    effect_code: Optional[EnumFilter[enums.EffectCode]] = strawberry.UNSET
    operator: Optional[StringFilter] = strawberry.UNSET
    value: Optional[NumberFilter] = strawberry.UNSET


@strawberry.input
class ItemSetFilter(EffectMixinFilter):
    code: Optional[StringFilter] = strawberry.UNSET
    name: Optional[StringFilter] = strawberry.UNSET
    items: Optional["ItemSetItemFilter"] = strawberry.UNSET


@strawberry.input
class ItemSetItemFilter:
    set_code: Optional[StringFilter] = strawberry.UNSET
    slot: Optional[EnumFilter[enums.ItemSetSlot]] = strawberry.UNSET
    item_code: Optional[StringFilter] = strawberry.UNSET
    item: Optional["ItemListFilter"] = strawberry.UNSET


@strawberry.input
class MapFilter:
    code: Optional[StringFilter] = strawberry.UNSET
    name: Optional[StringFilter] = strawberry.UNSET
    left: Optional[NumberFilter] = strawberry.UNSET
    top: Optional[NumberFilter] = strawberry.UNSET
    width: Optional[NumberFilter] = strawberry.UNSET
    height: Optional[NumberFilter] = strawberry.UNSET
    areas: Optional["MapAreaFilter"] = strawberry.UNSET
    monsters: Optional["MonsterPositionFilter"] = strawberry.UNSET
    npcs: Optional["NpcPositionFilter"] = strawberry.UNSET


@strawberry.input
class MapAreaFilter:
    map_code: Optional[StringFilter] = strawberry.UNSET
    area_code: Optional[StringFilter] = strawberry.UNSET
    name: Optional[StringFilter] = strawberry.UNSET


@strawberry.input
class BulletFilter(BaseMixinFilter, RowIDMixinFilter): ...


@strawberry.input
class ConsumableFilter(BaseMixinFilter, RowIDMixinFilter):
    description: Optional[StringFilter] = strawberry.UNSET
    level_land: Optional[NumberFilter] = strawberry.UNSET
    level_sea: Optional[NumberFilter] = strawberry.UNSET
    cooldown_id: Optional[NumberFilter] = strawberry.UNSET
    cooldown: Optional[NumberFilter] = strawberry.UNSET
    cast_time: Optional[NumberFilter] = strawberry.UNSET
    value: Optional[NumberFilter] = strawberry.UNSET
    skill_code: Optional[StringFilter] = strawberry.UNSET


@strawberry.input
class MaterialFilter(BaseMixinFilter, RowIDMixinFilter): ...


@strawberry.input
class TowerFloorFilter:
    code: Optional[StringFilter] = strawberry.UNSET
    floor_number: Optional[NumberFilter] = strawberry.UNSET
    time: Optional[NumberFilter] = strawberry.UNSET
    monsters: Optional["TowerFloorMonsterFilter"] = strawberry.UNSET


@strawberry.input
class TowerFloorMonsterFilter:
    floor_code: Optional[StringFilter] = strawberry.UNSET
    monster_code: Optional[StringFilter] = strawberry.UNSET
    amount: Optional[NumberFilter] = strawberry.UNSET
    monster: Optional["MonsterFilter"] = strawberry.UNSET


@strawberry.input
class Available3DModelFilter:
    asset_path: Optional[StringFilter] = strawberry.UNSET
    filename: Optional[StringFilter] = strawberry.UNSET
    model_name: Optional[StringFilter] = strawberry.UNSET
    animation_name: Optional[StringFilter] = strawberry.UNSET
    character_class: Optional[EnumFilter[enums.Model3DClass]] = strawberry.UNSET
    gender: Optional[EnumFilter[enums.Model3DGender]] = strawberry.UNSET


@strawberry.input
class FusionHelpFilter(BaseMixinFilter, RowIDMixinFilter):
    description: Optional[StringFilter] = strawberry.UNSET
