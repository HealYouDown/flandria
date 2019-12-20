from app.base_model import BaseModel
from app.extensions import db

bonus_includes = [
    "bonus_code_1", "bonus_operator_1", "bonus_1",
    "bonus_code_2", "bonus_operator_2", "bonus_2",
    "bonus_code_3", "bonus_operator_3", "bonus_3",
    "bonus_code_4", "bonus_operator_4", "bonus_4",
    "bonus_code_5", "bonus_operator_5", "bonus_5",
]


class _Base:
    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)

    tradable = db.Column(db.Boolean)

    rare_grade = db.Column(db.Integer, default=0)

    npc_price = db.Column(db.Integer)
    npc_price_disposal = db.Column(db.Integer)


class _Bonus:
    bonus_code_1 = db.Column(db.Integer)
    bonus_operator_1 = db.Column(db.String)
    bonus_1 = db.Column(db.Float)

    bonus_code_2 = db.Column(db.Integer)
    bonus_operator_2 = db.Column(db.String)
    bonus_2 = db.Column(db.Float)

    bonus_code_3 = db.Column(db.Integer)
    bonus_operator_3 = db.Column(db.String)
    bonus_3 = db.Column(db.Float)

    bonus_code_4 = db.Column(db.Integer)
    bonus_operator_4 = db.Column(db.String)
    bonus_4 = db.Column(db.Float)

    bonus_code_5 = db.Column(db.Integer)
    bonus_operator_5 = db.Column(db.String)
    bonus_5 = db.Column(db.Float)


# Item list #

class ItemList(BaseModel):
    __tablename__ = "item_list"
    __bind_key__ = "static_florensia_data"

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)

    table = db.Column(db.String)
    rare_grade = db.Column(db.Integer, default=None)


# Monster #

class Monster(BaseModel):
    __tablename__ = "monster"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rating_type", "level", "hp", "location", "experience",
        "min_dmg", "max_dmg",
    ]

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)
    rating_type = db.Column(db.Integer)

    level = db.Column(db.Integer)
    hp = db.Column(db.Integer)

    range = db.Column(db.String)
    location = db.Column(db.Integer)
    required_hitrate = db.Column(db.Integer)
    experience = db.Column(db.Integer)

    min_dmg = db.Column(db.Integer)
    max_dmg = db.Column(db.Integer)

    physical_defense = db.Column(db.Integer)
    magical_defense = db.Column(db.Integer)


# Extra Equipment #

class _ExtraEquipment(_Base, _Bonus):
    gender = db.Column(db.String)

    class_land = db.Column(db.String)
    level_land = db.Column(db.Integer)
    level_sea = db.Column(db.Integer)

    duration = db.Column(db.Integer)


class Accessory(_ExtraEquipment, BaseModel):
    __tablename__ = "accessory"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade", "duration", "level_land", *bonus_includes
    ]


class Dress(_ExtraEquipment, BaseModel):
    __tablename__ = "dress"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade", "duration", *bonus_includes
    ]


class Hat(_ExtraEquipment, BaseModel):
    __tablename__ = "hat"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade", "duration", "level_land", *bonus_includes
    ]


# Weapons #

class _Weapon(_Base, _Bonus):  # TODO: Relationship UpgradeData
    itemtype = db.Column(db.String)

    _include_fields = [
        "code", "name", "icon", "class_land", "level_land", "level_sea", "rare_grade", *bonus_includes
    ]

    class_land = db.Column(db.String)
    level_land = db.Column(db.Integer)
    level_sea = db.Column(db.Integer)

    physical_attack_min = db.Column(db.Integer)
    magical_attack_min = db.Column(db.Integer)
    physical_attack_max = db.Column(db.Integer)
    magical_attack_max = db.Column(db.Integer)

    attack_range = db.Column(db.Integer)
    attack_speed = db.Column(db.Integer)

    upgrade_code = db.Column(db.String)


class Cariad(_Weapon, BaseModel):
    __tablename__ = "cariad"
    __bind_key__ = "static_florensia_data"


class Dagger(_Weapon, BaseModel):
    __tablename__ = "dagger"
    __bind_key__ = "static_florensia_data"


class Duals(_Weapon, BaseModel):
    __tablename__ = "duals"
    __bind_key__ = "static_florensia_data"


class Rifle(_Weapon, BaseModel):
    __tablename__ = "rifle"
    __bind_key__ = "static_florensia_data"


class OneHandedSword(_Weapon, BaseModel):
    __tablename__ = "one_handed_sword"
    __bind_key__ = "static_florensia_data"


class TwoHandedSword(_Weapon, BaseModel):
    __tablename__ = "two_handed_sword"
    __bind_key__ = "static_florensia_data"


class Rapier(_Weapon, BaseModel):
    __tablename__ = "rapier"
    __bind_key__ = "static_florensia_data"


# Armor #

class _Armor(_Base, _Bonus):  # TODO: Relation UpgradeData
    _include_fields = [
        "code", "name", "icon", "class_land", "level_land", "level_sea", "rare_grade", *bonus_includes
    ]

    itemtype = db.Column(db.String)

    physical_defense = db.Column(db.Integer)
    magic_defense = db.Column(db.Integer)

    class_land = db.Column(db.String)
    level_land = db.Column(db.Integer)
    level_sea = db.Column(db.Integer)


class Shield(_Armor, BaseModel):
    __tablename__ = "shield"
    __bind_key__ = "static_florensia_data"


class Gauntlet(_Armor, BaseModel):
    __tablename__ = "gauntlet"
    __bind_key__ = "static_florensia_data"
    upgrade_code = db.Column(db.Integer)


class Coat(_Armor, BaseModel):
    __tablename__ = "coat"
    __bind_key__ = "static_florensia_data"
    upgrade_code = db.Column(db.Integer)


class Pants(_Armor, BaseModel):
    __tablename__ = "pants"
    __bind_key__ = "static_florensia_data"
    upgrade_code = db.Column(db.Integer)


class Shoes(_Armor, BaseModel):
    __tablename__ = "shoes"
    __bind_key__ = "static_florensia_data"
    upgrade_code = db.Column(db.Integer)


# Fishing stuff #

class FishingBait(_Base, BaseModel):
    __tablename__ = "fishing_bait"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade",
    ]


class FishingMaterial(_Base, BaseModel):
    __tablename__ = "fishing_material"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade",
    ]


class FishingRod(_Base, _Bonus, BaseModel):
    __tablename__ = "fishing_rod"
    __bind_key__ = "static_florensia_data"

    itemtype = db.Column(db.String)

    class_land = db.Column(db.String)
    level_land = db.Column(db.Integer)
    level_sea = db.Column(db.Integer)

    _include_fields = [
        "code", "name", "icon", "rare_grade", *bonus_includes
    ]


# Material #

class Material(_Base, BaseModel):
    __tablename__ = "material"
    __bind_key__ = "static_florensia_data"

    produced_by_code = db.Column(db.String, db.ForeignKey('recipe.code'))
    produced_by = db.relationship("Recipe", lazy="joined")

    _include_fields = [
        "code", "name", "icon", "rare_grade",
    ]


class Recipe(_Base, BaseModel):
    __tablename__ = "recipe"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade",
    ]

    result_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    result_quantity = db.Column(db.Integer)
    result_item = db.relationship("ItemList", foreign_keys=[result_code], lazy="joined")

    material_1_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    material_1_quantity = db.Column(db.Integer)
    material_1 = db.relationship("ItemList", foreign_keys=[material_1_code], lazy="joined")

    material_2_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    material_2_quantity = db.Column(db.Integer)
    material_2 = db.relationship("ItemList", foreign_keys=[material_2_code], lazy="joined")

    material_3_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    material_3_quantity = db.Column(db.Integer)
    material_3 = db.relationship("ItemList", foreign_keys=[material_3_code], lazy="joined")

    material_4_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    material_4_quantity = db.Column(db.Integer)
    material_4 = db.relationship("ItemList", foreign_keys=[material_4_code], lazy="joined")

    material_5_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    material_5_quantity = db.Column(db.Integer)
    material_5 = db.relationship("ItemList", foreign_keys=[material_5_code], lazy="joined")

    material_6_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    material_6_quantity = db.Column(db.Integer)
    material_6 = db.relationship("ItemList", foreign_keys=[material_6_code], lazy="joined")


class ProductBook(_Base, BaseModel):
    __tablename__ = "product_book"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "rare_grade", "target.code", "target.type",
        "target.result_item.icon", "target.result_item.rare_grade"
    ]

    target_code = db.Column(db.String, db.ForeignKey("production.code"))
    target = db.relationship("Production", foreign_keys=[target_code], lazy="joined")


class Production(BaseModel):
    __tablename__ = "production"
    __bind_key__ = "static_florensia_data"

    code = db.Column(db.String, primary_key=True)
    type = db.Column(db.Integer)
    points_needed = db.Column(db.Integer)
    division = db.Column(db.Integer)

    result_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    result_quantity = db.Column(db.Integer)
    result_item = db.relationship("ItemList", foreign_keys=[result_code], lazy="joined")

    material_1_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    material_1_quantity = db.Column(db.Integer)
    material_1 = db.relationship("ItemList", foreign_keys=[material_1_code], lazy="joined")

    material_2_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    material_2_quantity = db.Column(db.Integer)
    material_2 = db.relationship("ItemList", foreign_keys=[material_2_code], lazy="joined")

    material_3_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    material_3_quantity = db.Column(db.Integer)
    material_3 = db.relationship("ItemList", foreign_keys=[material_3_code], lazy="joined")

    material_4_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    material_4_quantity = db.Column(db.Integer)
    material_4 = db.relationship("ItemList", foreign_keys=[material_4_code], lazy="joined")

    material_5_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    material_5_quantity = db.Column(db.Integer)
    material_5 = db.relationship("ItemList", foreign_keys=[material_5_code], lazy="joined")

    material_6_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    material_6_quantity = db.Column(db.Integer)
    material_6 = db.relationship("ItemList", foreign_keys=[material_6_code], lazy="joined")


# Pets #

class PetCombineHelp(_Base, BaseModel):
    __tablename__ = "pet_combine_help"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade",
    ]

    efficiency = db.Column(db.Integer)


class PetCombineStone(_Base, BaseModel):
    __tablename__ = "pet_combine_stone"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade",
    ]

    increment_min = db.Column(db.Integer)
    increment_max = db.Column(db.Integer)


class PetSkillStone(_Base, BaseModel):
    __tablename__ = "pet_skill_stone"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade", "level",
    ]

    cooldown = db.Column(db.Integer)
    casttime = db.Column(db.Integer)
    level = db.Column(db.Integer)
    description = db.Column(db.Text)


class Pet(_Base, BaseModel):  # TODO: Stats
    __tablename__ = "pet"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade", "duration"
    ]

    duration = db.Column(db.Integer)


class RidingPet(_Base, BaseModel):
    __tablename__ = "riding_pet"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade", "duration",
    ]

    duration = db.Column(db.Integer)
    description = db.Column(db.Text)


# Ship stuff #

class _ShipBase(_Base):
    _include_fields = [
        "code", "name", "icon", "rare_grade", "class_sea", "level_sea",
    ]

    npc_price_tuning = db.Column(db.Integer)

    class_sea = db.Column(db.String)
    level_sea = db.Column(db.Integer)


class Shell(_Base, BaseModel):
    __tablename__ = "shell"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade", "level_sea",
    ]

    level_sea = db.Column(db.Integer)
    damage = db.Column(db.Integer)


class ShipAnchor(_ShipBase, BaseModel):
    __tablename__ = "ship_anchor"
    __bind_key__ = "static_florensia_data"

    ship_deceleration = db.Column(db.Integer)
    ship_turnpower = db.Column(db.Integer)
    balance = db.Column(db.Integer)


class ShipBody(_ShipBase, BaseModel):
    __tablename__ = "ship_body"
    __bind_key__ = "static_florensia_data"

    ship_defense = db.Column(db.Integer)
    ship_guns_front = db.Column(db.Integer)
    ship_guns_side = db.Column(db.Integer)
    ship_guns_speed = db.Column(db.Integer)
    ship_hitrange = db.Column(db.Integer)
    physical_defense = db.Column(db.Integer)
    protection = db.Column(db.Integer)
    ability_hp = db.Column(db.Integer)


class ShipFigure(_ShipBase, BaseModel):
    __tablename__ = "ship_figure"
    __bind_key__ = "static_florensia_data"

    balance = db.Column(db.Integer)
    protection = db.Column(db.Integer)


class ShipFlag(_ShipBase, BaseModel):
    __tablename__ = "ship_flag"
    __bind_key__ = "static_florensia_data"


class ShipFront(_ShipBase, BaseModel):
    __tablename__ = "ship_front"
    __bind_key__ = "static_florensia_data"

    physical_defense = db.Column(db.Integer)
    protection = db.Column(db.Integer)
    ability_hp = db.Column(db.Integer)
    balance = db.Column(db.Integer)


class ShipHeadMast(_ShipBase, BaseModel):
    __tablename__ = "ship_head_mast"
    __bind_key__ = "static_florensia_data"

    ship_wind_favorable = db.Column(db.Integer)
    ship_wind_adverse = db.Column(db.Integer)
    ship_acceleration = db.Column(db.Integer)
    ship_deceleration = db.Column(db.Integer)
    ship_turnpower = db.Column(db.Integer)
    balance = db.Column(db.Integer)


class ShipMagicStone(_ShipBase, BaseModel):
    __tablename__ = "ship_magic_stone"
    __bind_key__ = "static_florensia_data"

    ability_en = db.Column(db.Integer)
    ability_en_recovery = db.Column(db.Integer)


class ShipMainMast(_ShipBase, BaseModel):
    __tablename__ = "ship_main_mast"
    __bind_key__ = "static_florensia_data"

    ship_wind_favorable = db.Column(db.Integer)
    ship_wind_adverse = db.Column(db.Integer)
    ship_acceleration = db.Column(db.Integer)
    ship_deceleration = db.Column(db.Integer)
    ship_turnpower = db.Column(db.Integer)
    balance = db.Column(db.Integer)


class ShipNormalWeapon(_ShipBase, BaseModel):
    __tablename__ = "ship_normal_weapon"
    __bind_key__ = "static_florensia_data"

    ship_defense = db.Column(db.Integer)
    ship_range = db.Column(db.Integer)
    critical = db.Column(db.Integer)
    ship_reloadspeed = db.Column(db.Integer)
    ship_guns_front = db.Column(db.Integer)
    ship_guns_side = db.Column(db.Integer)
    ship_guns_speed = db.Column(db.Integer)
    ship_hitrange = db.Column(db.Integer)


class ShipSpecialWeapon(_ShipBase, BaseModel):
    __tablename__ = "ship_special_weapon"
    __bind_key__ = "static_florensia_data"

    ship_defense = db.Column(db.Integer)
    ship_range = db.Column(db.Integer)
    critical = db.Column(db.Integer)
    ship_reloadspeed = db.Column(db.Integer)
    ship_guns_speed = db.Column(db.Integer)
    ship_hitrange = db.Column(db.Integer)
    ability_en_usage = db.Column(db.Integer)


# Enhancing stuff #

class _Enhancing(_Base):
    _include_fields = [
        "code", "name", "icon", "rare_grade",
    ]

    description = db.Column(db.Text)


class UpgradeCrystal(_Enhancing, BaseModel):
    __tablename__ = "upgrade_crystal"
    __bind_key__ = "static_florensia_data"


class UpgradeHelp(_Enhancing, BaseModel):
    __tablename__ = "upgrade_help"
    __bind_key__ = "static_florensia_data"

    description = db.Column(db.Text)


class UpgradeStone(_Enhancing, BaseModel):
    __tablename__ = "upgrade_stone"
    __bind_key__ = "static_florensia_data"

    description = db.Column(db.Text)


class SealBreakHelp(_Enhancing, BaseModel):
    __tablename__ = "seal_break_help"
    __bind_key__ = "static_florensia_data"

    description = db.Column(db.Text)


class UpgradeRule(BaseModel):
    __tablename__ = "upgrade_rule"
    __bind_key__ = "static_florensia_data"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)

    upgrade_code = db.Column(db.String)
    upgrade_level = db.Column(db.Integer)
    gelt = db.Column(db.Integer)

    code_0 = db.Column(db.Integer)
    operator_0 = db.Column(db.String)
    value_0 = db.Column(db.Integer)

    code_1 = db.Column(db.Integer)
    operator_1 = db.Column(db.String)
    value_1 = db.Column(db.Integer)

    code_2 = db.Column(db.Integer)
    operator_2 = db.Column(db.String)
    value_2 = db.Column(db.Integer)

    code_3 = db.Column(db.Integer)
    operator_3 = db.Column(db.String)
    value_3 = db.Column(db.Integer)


# Other stuff #

class RandomBox(_Base, BaseModel):
    __tablename__ = "random_box"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade",
    ]

    item_0_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_0_quantity = db.Column(db.Integer)
    item_0_probability = db.Column(db.Float)
    item_0 = db.relationship("ItemList", foreign_keys=[item_0_code], lazy="joined")
    item_1_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_1_quantity = db.Column(db.Integer)
    item_1_probability = db.Column(db.Float)
    item_1 = db.relationship("ItemList", foreign_keys=[item_1_code], lazy="joined")
    item_2_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_2_quantity = db.Column(db.Integer)
    item_2_probability = db.Column(db.Float)
    item_2 = db.relationship("ItemList", foreign_keys=[item_2_code], lazy="joined")
    item_3_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_3_quantity = db.Column(db.Integer)
    item_3_probability = db.Column(db.Float)
    item_3 = db.relationship("ItemList", foreign_keys=[item_3_code], lazy="joined")
    item_4_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_4_quantity = db.Column(db.Integer)
    item_4_probability = db.Column(db.Float)
    item_4 = db.relationship("ItemList", foreign_keys=[item_4_code], lazy="joined")
    item_5_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_5_quantity = db.Column(db.Integer)
    item_5_probability = db.Column(db.Float)
    item_5 = db.relationship("ItemList", foreign_keys=[item_5_code], lazy="joined")
    item_6_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_6_quantity = db.Column(db.Integer)
    item_6_probability = db.Column(db.Float)
    item_6 = db.relationship("ItemList", foreign_keys=[item_6_code], lazy="joined")
    item_7_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_7_quantity = db.Column(db.Integer)
    item_7_probability = db.Column(db.Float)
    item_7 = db.relationship("ItemList", foreign_keys=[item_7_code], lazy="joined")
    item_8_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_8_quantity = db.Column(db.Integer)
    item_8_probability = db.Column(db.Float)
    item_8 = db.relationship("ItemList", foreign_keys=[item_8_code], lazy="joined")
    item_9_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_9_quantity = db.Column(db.Integer)
    item_9_probability = db.Column(db.Float)
    item_9 = db.relationship("ItemList", foreign_keys=[item_9_code], lazy="joined")
    item_10_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_10_quantity = db.Column(db.Integer)
    item_10_probability = db.Column(db.Float)
    item_10 = db.relationship("ItemList", foreign_keys=[item_10_code], lazy="joined")
    item_11_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_11_quantity = db.Column(db.Integer)
    item_11_probability = db.Column(db.Float)
    item_11 = db.relationship("ItemList", foreign_keys=[item_11_code], lazy="joined")
    item_12_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_12_quantity = db.Column(db.Integer)
    item_12_probability = db.Column(db.Float)
    item_12 = db.relationship("ItemList", foreign_keys=[item_12_code], lazy="joined")
    item_13_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_13_quantity = db.Column(db.Integer)
    item_13_probability = db.Column(db.Float)
    item_13 = db.relationship("ItemList", foreign_keys=[item_13_code], lazy="joined")
    item_14_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_14_quantity = db.Column(db.Integer)
    item_14_probability = db.Column(db.Float)
    item_14 = db.relationship("ItemList", foreign_keys=[item_14_code], lazy="joined")
    item_15_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_15_quantity = db.Column(db.Integer)
    item_15_probability = db.Column(db.Float)
    item_15 = db.relationship("ItemList", foreign_keys=[item_15_code], lazy="joined")
    item_16_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_16_quantity = db.Column(db.Integer)
    item_16_probability = db.Column(db.Float)
    item_16 = db.relationship("ItemList", foreign_keys=[item_16_code], lazy="joined")
    item_17_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_17_quantity = db.Column(db.Integer)
    item_17_probability = db.Column(db.Float)
    item_17 = db.relationship("ItemList", foreign_keys=[item_17_code], lazy="joined")
    item_18_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_18_quantity = db.Column(db.Integer)
    item_18_probability = db.Column(db.Float)
    item_18 = db.relationship("ItemList", foreign_keys=[item_18_code], lazy="joined")
    item_19_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_19_quantity = db.Column(db.Integer)
    item_19_probability = db.Column(db.Float)
    item_19 = db.relationship("ItemList", foreign_keys=[item_19_code], lazy="joined")
    item_20_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_20_quantity = db.Column(db.Integer)
    item_20_probability = db.Column(db.Float)
    item_20 = db.relationship("ItemList", foreign_keys=[item_20_code], lazy="joined")
    item_21_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_21_quantity = db.Column(db.Integer)
    item_21_probability = db.Column(db.Float)
    item_21 = db.relationship("ItemList", foreign_keys=[item_21_code], lazy="joined")
    item_22_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_22_quantity = db.Column(db.Integer)
    item_22_probability = db.Column(db.Float)
    item_22 = db.relationship("ItemList", foreign_keys=[item_22_code], lazy="joined")
    item_23_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_23_quantity = db.Column(db.Integer)
    item_23_probability = db.Column(db.Float)
    item_23 = db.relationship("ItemList", foreign_keys=[item_23_code], lazy="joined")
    item_24_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_24_quantity = db.Column(db.Integer)
    item_24_probability = db.Column(db.Float)
    item_24 = db.relationship("ItemList", foreign_keys=[item_24_code], lazy="joined")
    item_25_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_25_quantity = db.Column(db.Integer)
    item_25_probability = db.Column(db.Float)
    item_25 = db.relationship("ItemList", foreign_keys=[item_25_code], lazy="joined")
    item_26_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_26_quantity = db.Column(db.Integer)
    item_26_probability = db.Column(db.Float)
    item_26 = db.relationship("ItemList", foreign_keys=[item_26_code], lazy="joined")
    item_27_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_27_quantity = db.Column(db.Integer)
    item_27_probability = db.Column(db.Float)
    item_27 = db.relationship("ItemList", foreign_keys=[item_27_code], lazy="joined")
    item_28_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_28_quantity = db.Column(db.Integer)
    item_28_probability = db.Column(db.Float)
    item_28 = db.relationship("ItemList", foreign_keys=[item_28_code], lazy="joined")
    item_29_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_29_quantity = db.Column(db.Integer)
    item_29_probability = db.Column(db.Float)
    item_29 = db.relationship("ItemList", foreign_keys=[item_29_code])
    item_30_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_30_quantity = db.Column(db.Integer)
    item_30_probability = db.Column(db.Float)
    item_30 = db.relationship("ItemList", foreign_keys=[item_30_code], lazy="joined")
    item_31_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_31_quantity = db.Column(db.Integer)
    item_31_probability = db.Column(db.Float)
    item_31 = db.relationship("ItemList", foreign_keys=[item_31_code], lazy="joined")
    item_32_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_32_quantity = db.Column(db.Integer)
    item_32_probability = db.Column(db.Float)
    item_32 = db.relationship("ItemList", foreign_keys=[item_32_code], lazy="joined")
    item_33_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_33_quantity = db.Column(db.Integer)
    item_33_probability = db.Column(db.Float)
    item_33 = db.relationship("ItemList", foreign_keys=[item_33_code], lazy="joined")
    item_34_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_34_quantity = db.Column(db.Integer)
    item_34_probability = db.Column(db.Float)
    item_34 = db.relationship("ItemList", foreign_keys=[item_34_code], lazy="joined")
    item_35_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_35_quantity = db.Column(db.Integer)
    item_35_probability = db.Column(db.Float)
    item_35 = db.relationship("ItemList", foreign_keys=[item_35_code])
    item_36_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_36_quantity = db.Column(db.Integer)
    item_36_probability = db.Column(db.Float)
    item_36 = db.relationship("ItemList", foreign_keys=[item_36_code], lazy="joined")
    item_37_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_37_quantity = db.Column(db.Integer)
    item_37_probability = db.Column(db.Float)
    item_37 = db.relationship("ItemList", foreign_keys=[item_37_code], lazy="joined")
    item_38_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_38_quantity = db.Column(db.Integer)
    item_38_probability = db.Column(db.Float)
    item_38 = db.relationship("ItemList", foreign_keys=[item_38_code], lazy="joined")
    item_39_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_39_quantity = db.Column(db.Integer)
    item_39_probability = db.Column(db.Float)
    item_39 = db.relationship("ItemList", foreign_keys=[item_39_code], lazy="joined")
    item_40_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_40_quantity = db.Column(db.Integer)
    item_40_probability = db.Column(db.Float)
    item_40 = db.relationship("ItemList", foreign_keys=[item_40_code], lazy="joined")
    item_41_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_41_quantity = db.Column(db.Integer)
    item_41_probability = db.Column(db.Float)
    item_41 = db.relationship("ItemList", foreign_keys=[item_41_code], lazy="joined")
    item_42_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_42_quantity = db.Column(db.Integer)
    item_42_probability = db.Column(db.Float)
    item_42 = db.relationship("ItemList", foreign_keys=[item_42_code], lazy="joined")
    item_43_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_43_quantity = db.Column(db.Integer)
    item_43_probability = db.Column(db.Float)
    item_43 = db.relationship("ItemList", foreign_keys=[item_43_code], lazy="joined")
    item_44_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_44_quantity = db.Column(db.Integer)
    item_44_probability = db.Column(db.Float)
    item_44 = db.relationship("ItemList", foreign_keys=[item_44_code], lazy="joined")
    item_45_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_45_quantity = db.Column(db.Integer)
    item_45_probability = db.Column(db.Float)
    item_45 = db.relationship("ItemList", foreign_keys=[item_45_code], lazy="joined")
    item_46_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_46_quantity = db.Column(db.Integer)
    item_46_probability = db.Column(db.Float)
    item_46 = db.relationship("ItemList", foreign_keys=[item_46_code], lazy="joined")
    item_47_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_47_quantity = db.Column(db.Integer)
    item_47_probability = db.Column(db.Float)
    item_47 = db.relationship("ItemList", foreign_keys=[item_47_code], lazy="joined")
    item_48_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_48_quantity = db.Column(db.Integer)
    item_48_probability = db.Column(db.Float)
    item_48 = db.relationship("ItemList", foreign_keys=[item_48_code], lazy="joined")
    item_49_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_49_quantity = db.Column(db.Integer)
    item_49_probability = db.Column(db.Float)
    item_49 = db.relationship("ItemList", foreign_keys=[item_49_code], lazy="joined")
    item_50_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_50_quantity = db.Column(db.Integer)
    item_50_probability = db.Column(db.Float)
    item_50 = db.relationship("ItemList", foreign_keys=[item_50_code], lazy="joined")
    item_51_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_51_quantity = db.Column(db.Integer)
    item_51_probability = db.Column(db.Float)
    item_51 = db.relationship("ItemList", foreign_keys=[item_51_code], lazy="joined")
    item_52_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_52_quantity = db.Column(db.Integer)
    item_52_probability = db.Column(db.Float)
    item_52 = db.relationship("ItemList", foreign_keys=[item_52_code], lazy="joined")
    item_53_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_53_quantity = db.Column(db.Integer)
    item_53_probability = db.Column(db.Float)
    item_53 = db.relationship("ItemList", foreign_keys=[item_53_code], lazy="joined")
    item_54_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_54_quantity = db.Column(db.Integer)
    item_54_probability = db.Column(db.Float)
    item_54 = db.relationship("ItemList", foreign_keys=[item_54_code], lazy="joined")
    item_55_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_55_quantity = db.Column(db.Integer)
    item_55_probability = db.Column(db.Float)
    item_55 = db.relationship("ItemList", foreign_keys=[item_55_code], lazy="joined")
    item_56_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_56_quantity = db.Column(db.Integer)
    item_56_probability = db.Column(db.Float)
    item_56 = db.relationship("ItemList", foreign_keys=[item_56_code], lazy="joined")
    item_57_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_57_quantity = db.Column(db.Integer)
    item_57_probability = db.Column(db.Float)
    item_57 = db.relationship("ItemList", foreign_keys=[item_57_code], lazy="joined")
    item_58_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_58_quantity = db.Column(db.Integer)
    item_58_probability = db.Column(db.Float)
    item_58 = db.relationship("ItemList", foreign_keys=[item_58_code], lazy="joined")
    item_59_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_59_quantity = db.Column(db.Integer)
    item_59_probability = db.Column(db.Float)
    item_59 = db.relationship("ItemList", foreign_keys=[item_59_code], lazy="joined")
    item_60_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item_60_quantity = db.Column(db.Integer)
    item_60_probability = db.Column(db.Float)
    item_60 = db.relationship("ItemList", foreign_keys=[item_60_code], lazy="joined")


class Consumable(_Base, BaseModel):
    __tablename__ = "consumable"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade",
    ]

    class_land = db.Column(db.Integer)
    cooltime = db.Column(db.Integer)
    efficiency = db.Column(db.Integer)
    description = db.Column(db.Text)


class Bullet(_Base, BaseModel):
    __tablename__ = "bullet"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade",
    ]


# Maps & NPCs #

class Map(BaseModel):
    __tablename__ = "map"
    __bind_key__ = "static_florensia_data"

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)


class NPC(BaseModel):
    __tablename__ = "npc"
    __bind_key__ = "static_florensia_data"

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)


# Quest #

class QuestItem(BaseModel):
    __tablename__ = "quest_item"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade",
    ]

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)
    rare_grade = db.Column(db.Integer, default=0)


class QuestScroll(BaseModel):  # TODO Description
    __tablename__ = "quest_scroll"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "icon", "rare_grade",
    ]

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)
    rare_grade = db.Column(db.Integer, default=0)
    quest_code = db.Column(db.String, db.ForeignKey("quest.code"))
    quest = db.relationship("Quest", foreign_keys=[quest_code], lazy="joined")


class QuestMission(BaseModel):
    __tablename__ = "quest_mission"
    __bind_key__ = "static_florensia_data"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quest_code = db.Column(db.String, db.ForeignKey('quest.code'))

    work_type = db.Column(db.Integer)
    work_value = db.Column(db.String)
    count = db.Column(db.Integer)

    # 0
    item_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item = db.relationship("ItemList", foreign_keys=[item_code])

    # 1, 4, 17
    npc_code = db.Column(db.String, db.ForeignKey("npc.code"))
    npc = db.relationship("NPC", foreign_keys=[npc_code])

    # 2
    monster_code = db.Column(db.String, db.ForeignKey("monster.code"))
    monster = db.relationship("Monster", foreign_keys=[monster_code])

    # 3
    quest_item_code = db.Column(db.String, db.ForeignKey("quest_item.code"))
    quest_item = db.relationship("QuestItem", foreign_keys=[quest_item_code])


class QuestGiveDescription(BaseModel):
    __tablename__ = "quest_give_description"
    __bind_key__ = "static_florensia_data"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quest_code = db.Column(db.String, db.ForeignKey('quest.code'))

    item_code = db.Column(db.String, db.ForeignKey("quest_item.code"))
    item = db.relationship("QuestItem", foreign_keys=[item_code])

    amount = db.Column(db.Integer)


class QuestLootDescription(BaseModel):
    __tablename__ = "quest_loot_description"
    __bind_key__ = "static_florensia_data"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quest_code = db.Column(db.String, db.ForeignKey('quest.code'))

    monster_code = db.Column(db.String, db.ForeignKey("monster.code"))
    monster = db.relationship("Monster", foreign_keys=[monster_code])

    item_code = db.Column(db.String, db.ForeignKey("quest_item.code"))
    item = db.relationship("QuestItem", foreign_keys=[item_code])

    rate = db.Column(db.Integer)


class QuestSelectableItem(BaseModel):
    __tablename__ = "quest_selectable_item"
    __bind_key__ = "static_florensia_data"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quest_code = db.Column(db.String, db.ForeignKey('quest.code'))

    item_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item = db.relationship("ItemList", foreign_keys=[item_code])

    amount = db.Column(db.Integer)


class QuestDescription(BaseModel):
    __tablename__ = "quest_description"
    __bind_key__ = "static_florensia_data"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)

    quest_code = db.Column(db.String, db.ForeignKey("quest.code"))
    language_code = db.Column(db.String)

    title = db.Column(db.String)
    mission_1 = db.Column(db.Text)
    mission_2 = db.Column(db.Text)
    mission_3 = db.Column(db.Text)
    desc = db.Column(db.Text)
    pre_dialog = db.Column(db.Text)
    start_dialog = db.Column(db.Text)
    run_dialog = db.Column(db.Text)
    finish_dialog = db.Column(db.Text)


class Quest(BaseModel):
    __tablename__ = "quest"
    __bind_key__ = "static_florensia_data"

    _include_fields = [
        "code", "name", "level", "location",
    ]

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    level = db.Column(db.Integer)
    player_class = db.Column(db.String)
    exp_reward = db.Column(db.String)
    money_reward = db.Column(db.String)
    location = db.Column(db.Integer)

    before_quest_code = db.Column(db.String, db.ForeignKey("quest.code"))
    before_quest = db.relation("Quest", remote_side=[code])

    source_object_code = db.Column(db.String, db.ForeignKey("npc.code"))
    source_object = db.relationship("NPC", foreign_keys=[source_object_code])

    source_area_code = db.Column(db.String, db.ForeignKey("map.code"))
    source_area = db.relationship("Map", foreign_keys=[source_area_code])

    supplier_code = db.Column(db.String, db.ForeignKey("npc.code"))
    supplier = db.relationship("NPC", foreign_keys=[supplier_code])

    give_descriptions = db.relationship("QuestGiveDescription")
    loot_descriptions = db.relationship("QuestLootDescription")
    selectable_items = db.relationship("QuestSelectableItem")
    missions = db.relationship("QuestMission")
    descriptions = db.relationship("QuestDescription")


class ExcludedItem(BaseModel):
    __tablename__ = "excluded_item"
    __bind_key__ = "unstatic_florensia_data"

    code = db.Column(db.String, primary_key=True)


class HiddenItem(BaseModel):
    __tablename__ = "hidden_item"
    __bind_key__ = "unstatic_florensia_data"

    code = db.Column(db.String, primary_key=True)


class Drop(BaseModel):
    __tablename__ = "drop"
    __bind_key__ = "unstatic_florensia_data"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, default=1)

    monster_code = db.Column(db.String, db.ForeignKey("monster.code"))
    monster = db.relationship("Monster", foreign_keys=[monster_code])

    item_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item = db.relationship("ItemList", foreign_keys=[item_code])
