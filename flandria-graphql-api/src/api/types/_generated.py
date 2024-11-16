from typing import Optional

import strawberry

from src.api import enums


@strawberry.interface
class RowIDMixin:
    row_id: int


@strawberry.interface
class FlorensiaModelMixin:
    model_name: Optional[str]
    models: list["Available3DModel"]


@strawberry.interface
class EffectMixin:
    effects: list["Effect"]


@strawberry.interface
class ClassLandMixin:
    is_noble: bool
    is_court_magician: bool
    is_magic_knight: bool
    is_saint: bool
    is_priest: bool
    is_shaman: bool
    is_mercenary: bool
    is_gladiator: bool
    is_guardian_swordsman: bool
    is_explorer: bool
    is_excavator: bool
    is_sniper: bool


@strawberry.interface
class ClassSeaMixin:
    is_armored: bool
    is_big_gun: bool
    is_torpedo: bool
    is_maintenance: bool
    is_assault: bool


@strawberry.interface
class ItemSetMixin:
    item_set_code: Optional[str]
    item_set: Optional["ItemSet"]


@strawberry.interface
class UpgradeRuleMixin:
    upgrade_rule_base_code: Optional[str]
    upgrade_rule: list["UpgradeRule"]


@strawberry.interface
class BaseMixin(RowIDMixin):
    code: str
    name: str
    icon: str
    is_tradable: bool
    is_destroyable: bool
    npc_sell_price: float
    is_sellable: bool
    is_storageable: bool
    grade: enums.ItemGrade
    duration: Optional[int]
    stack_size: int
    npc_buy_price: float


@strawberry.interface
class SkillMixin(EffectMixin, ClassSeaMixin, ClassLandMixin):
    code: str
    reference_code: str
    name: str
    icon: str
    required_level_land: int
    required_level_sea: int
    skill_level: int
    skill_max_level: int
    mana_cost: int
    accuracy: int
    hit_correction: int
    cooldown: float
    cast_time: float
    cast_distance: float
    dash_distance: float
    push_distance: float
    effect_range: float
    effect_angle: int
    is_persistent: bool
    duration: float
    toggle_tick_time: Optional[float]
    toggle_operator: Optional[str]
    toggle_hp_value: Optional[float]
    toggle_mp_value: Optional[float]
    required_weapons: str
    description: str


@strawberry.interface
class WeaponMixin(
    BaseMixin,
    ClassLandMixin,
    EffectMixin,
    ItemSetMixin,
    UpgradeRuleMixin,
    FlorensiaModelMixin,
):
    level_land: int
    level_sea: int
    minimum_physical_damage: int
    maximum_physical_damage: int
    minimum_magical_damage: int
    maximum_magical_damage: int
    attack_speed: float
    attack_range: float
    item_flag: enums.ItemFlag


@strawberry.interface
class ArmorMixin(
    BaseMixin, ClassLandMixin, EffectMixin, ItemSetMixin, FlorensiaModelMixin
):
    level_land: int
    level_sea: int
    physical_defense: int
    magical_defense: int


@strawberry.interface
class EquipmentMixin(BaseMixin, ClassLandMixin, EffectMixin, ItemSetMixin):
    gender: enums.Gender
    level_land: int
    level_sea: int
    item_flag: enums.ItemFlag


@strawberry.interface
class ActorModelMixin(FlorensiaModelMixin):
    model_scale: Optional[float]


@strawberry.interface
class ExtraEquipmentModelMixin(FlorensiaModelMixin):
    model_variant: Optional[list[int]]


@strawberry.interface
class ShipBaseMixin(BaseMixin, ClassSeaMixin, EffectMixin):
    npc_tune_price: int
    level_sea: int
    guns_front: int
    guns_side: int
    crew_size: int
    physical_defense: int
    protection: int
    balance: int
    dp: int
    en: int
    en_usage: int
    en_recovery: int
    acceleration: float
    deceleration: float
    turning_power: float
    favorable_wind: float
    adverse_wind: float
    physical_damage: int
    weapon_range: float
    critical_chance: float
    reload_speed: float
    hit_range: float


@strawberry.interface
class ActorMixin(RowIDMixin, ActorModelMixin):
    code: str
    name: str
    icon: str
    level: int
    grade: enums.ActorGrade
    is_inanimate: bool
    is_sea: bool
    is_ship: bool
    is_air: bool
    is_tameable: bool
    experience: int
    health_points: int
    recovery_rate: float
    minimum_physical_damage: int
    maximum_physical_damage: int
    minimum_magical_damage: int
    maximum_magical_damage: int
    physical_defense: int
    magical_defense: int
    physical_evasion_rate: int
    physical_hit_rate: int
    magical_hit_rate: int
    critical_rate: int
    critical_resistance_rate: int
    sea_attack_aoe_range: float
    ship_guns_count: int
    ship_guns_speed: float
    ship_attack_range: float
    attack_cast_time: float
    attack_cooldown: float
    despawn_delay_time: float
    attack_vision_range: float
    nearby_attack_vision_range: float
    is_ranged: bool
    attack_range: float
    walking_speed: int
    running_speed: int
    turning_speed: int
    messages_code: Optional[str]
    posion_resistance: int
    fire_resistance: int
    cold_resistance: int
    lightning_resistance: int
    holy_resistance: int
    dark_resistance: int
    messages: list["ActorMessage"]


@strawberry.type
class RandomBox(BaseMixin):
    level_land: int
    level_sea: int
    rewards: list["RandomBoxReward"]


@strawberry.type
class RandomBoxReward:
    index: int
    random_box_code: str
    reward_code: str
    quantity: int
    probability: strawberry.Private[float]
    item: "ItemList"


@strawberry.type
class Quest:
    code: str
    is_sea: bool
    level: int
    is_mercenary: bool
    is_saint: bool
    is_noble: bool
    is_explorer: bool
    experience: int
    money: int
    selectable_items_count: int
    title: str
    description: Optional[str]
    pre_dialog: Optional[str]
    start_dialog: Optional[str]
    run_dialog: Optional[str]
    finish_dialog: Optional[str]
    previous_quest_code: Optional[str]
    start_npc_code: Optional[str]
    start_area_code: Optional[str]
    end_npc_code: Optional[str]
    previous_quest: Optional["Quest"]
    start_npc: Optional["Npc"]
    start_area: Optional["MapArea"]
    end_npc: Optional["Npc"]
    give_items: list["QuestGiveItem"]
    reward_items: list["QuestRewardItem"]
    missions: list["QuestMission"]


@strawberry.type
class QuestGiveItem:
    quest_code: str
    item_code: str
    amount: int
    item: "ItemList"


@strawberry.type
class QuestMission:
    index: int
    quest_code: str
    work_type: enums.QuestMissionType
    count: int
    description: str
    map_code: Optional[str]
    x: Optional[float]
    y: Optional[float]
    monster_code: Optional[str]
    item_code: Optional[str]
    quest_item_code: Optional[str]
    npc_code: Optional[str]
    map: Optional["Map"]
    monster: Optional["Monster"]
    item: Optional["ItemList"]
    quest_item: Optional["QuestItem"]
    npc: Optional["Npc"]


@strawberry.type
class QuestRewardItem:
    index: int
    quest_code: str
    item_code: str
    amount: int
    item: "ItemList"


@strawberry.type
class QuestItem(BaseMixin):
    quests_by_mission: list["Quest"]
    quests_by_give_item: list["Quest"]


@strawberry.type
class QuestScroll(BaseMixin):
    quest_code: str
    quest: "Quest"


@strawberry.type
class Monster(ActorMixin):
    skill_1_code: Optional[str]
    skill_1_chance: float
    skill_2_code: Optional[str]
    skill_2_chance: float
    skill_1: Optional["MonsterSkill"]
    skill_2: Optional["MonsterSkill"]
    drops: list["Drop"]
    money: Optional["Money"]
    positions: list["MonsterPosition"]


@strawberry.type
class Npc(ActorMixin):
    positions: list["NpcPosition"]
    quests: list["Quest"]
    store_items: list["NpcStoreItem"]


@strawberry.type
class NpcStoreItem:
    index: int
    section_name: str
    page_name: str
    npc_code: str
    item_code: str
    item: "ItemList"


@strawberry.type
class ActorMessage:
    index: int
    code: Optional[str]
    trigger: enums.MonsterMessageTrigger
    message: str


@strawberry.type
class MonsterSkill(SkillMixin): ...


@strawberry.type
class Drop:
    index: int
    quantity: int
    probability: strawberry.Private[float]
    monster_code: str
    item_code: str
    monster: "Monster"
    item: "ItemList"


@strawberry.type
class Money:
    monster_code: str
    probability: strawberry.Private[float]
    min: int
    max: int
    monster: "Monster"


@strawberry.type
class MonsterPosition:
    index: int
    monster_code: str
    map_code: str
    amount: int
    respawn_time: int
    x: float
    y: float
    z: float
    monster: "Monster"
    map: "Map"


@strawberry.type
class NpcPosition:
    index: int
    npc_code: str
    map_code: str
    x: float
    y: float
    z: float
    npc: "Npc"
    map: "Map"


@strawberry.type
class FishingBait(BaseMixin): ...


@strawberry.type
class FishingMaterial(BaseMixin): ...


@strawberry.type
class Essence(BaseMixin, EffectMixin):
    equip_type: enums.EssenceEquipType
    required_level: int
    is_core: bool


@strawberry.type
class EssenceHelp(BaseMixin):
    description: Optional[str]


@strawberry.type
class Coat(ArmorMixin, UpgradeRuleMixin): ...


@strawberry.type
class Pants(ArmorMixin, UpgradeRuleMixin): ...


@strawberry.type
class Gauntlet(ArmorMixin, UpgradeRuleMixin): ...


@strawberry.type
class Shoes(ArmorMixin, UpgradeRuleMixin): ...


@strawberry.type
class Shield(ArmorMixin): ...


@strawberry.type
class Cariad(WeaponMixin): ...


@strawberry.type
class Dagger(WeaponMixin): ...


@strawberry.type
class Duals(WeaponMixin): ...


@strawberry.type
class FishingRod(WeaponMixin): ...


@strawberry.type
class OneHandedSword(WeaponMixin): ...


@strawberry.type
class Rapier(WeaponMixin): ...


@strawberry.type
class Rifle(WeaponMixin): ...


@strawberry.type
class TwoHandedSword(WeaponMixin): ...


@strawberry.type
class Accessory(EquipmentMixin):
    accessory_type: enums.AccessoryType


@strawberry.type
class Dress(EquipmentMixin, ExtraEquipmentModelMixin): ...


@strawberry.type
class Hat(EquipmentMixin, ExtraEquipmentModelMixin): ...


@strawberry.type
class ShipAnchor(ShipBaseMixin): ...


@strawberry.type
class ShipBody(ShipBaseMixin): ...


@strawberry.type
class ShipFigure(ShipBaseMixin): ...


@strawberry.type
class ShipFlag(ShipBaseMixin): ...


@strawberry.type
class ShipFront(ShipBaseMixin): ...


@strawberry.type
class ShipHeadMast(ShipBaseMixin): ...


@strawberry.type
class ShipMagicStone(ShipBaseMixin): ...


@strawberry.type
class ShipMainMast(ShipBaseMixin): ...


@strawberry.type
class ShipNormalWeapon(ShipBaseMixin): ...


@strawberry.type
class ShipShell(BaseMixin):
    level_sea: int
    physical_damage: int
    explosion_range: float


@strawberry.type
class ShipSpecialWeapon(ShipBaseMixin): ...


@strawberry.type
class Pet(BaseMixin):
    initial_courage: int
    initial_patience: int
    initial_wisdom: int
    is_unlimited: bool


@strawberry.type
class PetCombineHelp(BaseMixin):
    value: float


@strawberry.type
class PetCombineStone(BaseMixin):
    min_value: int
    max_value: int


@strawberry.type
class PetSkill(SkillMixin): ...


@strawberry.type
class PetSkillStone(BaseMixin):
    skill_code: str
    skill: "PetSkill"


@strawberry.type
class RidingPet(BaseMixin):
    description: str


@strawberry.type
class PlayerSkill(SkillMixin):
    required_skills: list["PlayerRequiredSkill"]


@strawberry.type
class SkillBook(BaseMixin):
    skill_code: str
    skill: "PlayerSkill"


@strawberry.type
class PlayerLevelStat:
    base_class: enums.BaseClassType
    level: int
    max_hp: int
    max_mp: int
    avoidance: int
    melee_min_attack: int
    melee_max_attack: int
    melee_hitrate: int
    melee_critical_rate: int
    range_min_attack: int
    range_max_attack: int
    range_hitrate: int
    range_critical_rate: int
    magic_min_attack: int
    magic_max_attack: int
    magic_hitrate: int
    magic_critical_rate: int


@strawberry.type
class PlayerStatusStat:
    base_class: enums.BaseClassType
    point_level: int
    stat_type: enums.StatType
    max_hp_increment: int
    max_mp_increment: int
    avoidance_increment: int
    melee_min_attack_increment: int
    melee_max_attack_increment: int
    melee_hitrate_increment: int
    melee_critical_rate_increment: int
    range_min_attack_increment: int
    range_max_attack_increment: int
    range_hitrate_increment: int
    range_critical_rate_increment: int
    magic_min_attack_increment: int
    magic_max_attack_increment: int
    magic_hitrate_increment: int
    magic_critical_rate_increment: int


@strawberry.type
class Recipe(BaseMixin):
    result_code: str
    result_quantity: int
    result_item: "ItemList"
    required_materials: list["RecipeRequiredMaterial"]


@strawberry.type
class RecipeRequiredMaterial:
    recipe_code: str
    material_code: str
    quantity: int
    item: "ItemList"


@strawberry.type
class Production(RowIDMixin):
    code: str
    type: enums.SecondJobType
    points_required: int
    result_code: str
    result_quantity: int
    result_item: "ItemList"
    required_materials: list["ProductionRequiredMaterial"]


@strawberry.type
class ProductionRequiredMaterial:
    production_code: str
    material_code: str
    quantity: int
    item: "ItemList"


@strawberry.type
class ProductionBook(BaseMixin):
    production_code: str
    production: "Production"


@strawberry.type
class UpgradeHelp(BaseMixin):
    description: Optional[str]


@strawberry.type
class UpgradeStone(BaseMixin):
    description: str


@strawberry.type
class UpgradeCrystal(BaseMixin):
    description: str


@strawberry.type
class UpgradeRule(EffectMixin):
    code: str
    base_code: str
    level: int
    cost: int


@strawberry.type
class SealBreakHelp(BaseMixin):
    description: str


@strawberry.type
class ItemList(ClassLandMixin, ClassSeaMixin, EffectMixin):
    code: str
    tablename: str
    name: str
    icon: str
    grade: enums.ItemGrade
    gender: Optional[enums.Gender]
    duration: Optional[int]
    level_land: Optional[int]
    level_sea: Optional[int]
    model_name: Optional[str]
    model_variant: Optional[list[int]]


@strawberry.type
class PlayerRequiredSkill:
    skill_code: str
    required_skill_code: str
    skill: "PlayerSkill"


@strawberry.type
class Effect:
    index: int
    ref_code: str
    effect_code: enums.EffectCode
    operator: str
    value: float


@strawberry.type
class ItemSet(EffectMixin):
    code: str
    name: str
    items: list["ItemSetItem"]


@strawberry.type
class ItemSetItem:
    set_code: str
    slot: enums.ItemSetSlot
    item_code: str
    item: "ItemList"


@strawberry.type
class Map:
    code: str
    name: str
    left: float
    top: float
    width: float
    height: float
    areas: list["MapArea"]
    monsters: list["MonsterPosition"]
    npcs: list["NpcPosition"]


@strawberry.type
class MapArea:
    map_code: str
    area_code: str
    name: str


@strawberry.type
class Bullet(BaseMixin): ...


@strawberry.type
class Consumable(BaseMixin):
    description: Optional[str]
    level_land: int
    level_sea: int
    cooldown_id: int
    cooldown: float
    cast_time: float
    value: Optional[int]
    skill_code: Optional[str]


@strawberry.type
class Material(BaseMixin): ...


@strawberry.type
class TowerFloor:
    code: str
    floor_number: int
    time: int
    monsters: list["TowerFloorMonster"]


@strawberry.type
class TowerFloorMonster:
    floor_code: str
    monster_code: str
    amount: int
    monster: "Monster"


@strawberry.type
class Available3DModel:
    asset_path: str
    filename: str
    model_name: str
    model_variant: Optional[list[int]]
    animation_name: Optional[str]
    character_class: Optional[enums.Model3DClass]
    gender: Optional[enums.Model3DGender]


@strawberry.type
class FusionHelp(BaseMixin):
    description: Optional[str]
