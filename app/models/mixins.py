from sqlalchemy import Boolean, Column, Float, Integer, String


class BaseMixin:
    index = Column(Integer)

    code = Column(String, primary_key=True)
    name = Column(String)
    icon = Column(String)

    tradable = Column(Boolean)

    rare_grade = Column(Integer, default=0)

    npc_price = Column(Integer)
    npc_price_disposal = Column(Integer)

    def to_dict(self, minimal: bool) -> dict:
        minimal_dict = {
                "code": self.code,
                "name": self.name,
                "icon": self.icon,
                "rare_grade": self.rare_grade,
            }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "tradable": self.tradable,
            "npc_price": self.npc_price,
            "npc_price_disposal": self.npc_price_disposal
        }


class BonusMixin:
    bonus_code_1 = Column(Integer)
    bonus_operator_1 = Column(String)
    bonus_1 = Column(Float)

    bonus_code_2 = Column(Integer)
    bonus_operator_2 = Column(String)
    bonus_2 = Column(Float)

    bonus_code_3 = Column(Integer)
    bonus_operator_3 = Column(String)
    bonus_3 = Column(Float)

    bonus_code_4 = Column(Integer)
    bonus_operator_4 = Column(String)
    bonus_4 = Column(Float)

    bonus_code_5 = Column(Integer)
    bonus_operator_5 = Column(String)
    bonus_5 = Column(Float)

    def to_dict(self) -> dict:
        return {
            "bonus_code_1": self.bonus_code_1,
            "bonus_operator_1": self.bonus_operator_1,
            "bonus_1": self.bonus_1,
            "bonus_code_2": self.bonus_code_2,
            "bonus_operator_2": self.bonus_operator_2,
            "bonus_2": self.bonus_2,
            "bonus_code_3": self.bonus_code_3,
            "bonus_operator_3": self.bonus_operator_3,
            "bonus_3": self.bonus_3,
            "bonus_code_4": self.bonus_code_4,
            "bonus_operator_4": self.bonus_operator_4,
            "bonus_4": self.bonus_4,
            "bonus_code_5": self.bonus_code_5,
            "bonus_operator_5": self.bonus_operator_5,
            "bonus_5": self.bonus_5,
        }


class ExtraEquipmentMixin(BaseMixin, BonusMixin):
    gender = Column(String)

    class_land = Column(String)
    level_land = Column(Integer)
    level_sea = Column(Integer)

    duration = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        return {
            **BaseMixin.to_dict(self, minimal),
            **BonusMixin.to_dict(self),
            "gender": self.gender,
            "class_land": self.class_land,
            "level_land": self.level_land,
            "level_sea": self.level_sea,
            "duration": self.duration
        }


class WeaponMixin(BaseMixin, BonusMixin):
    itemtype = Column(String)

    class_land = Column(String)
    level_land = Column(Integer)
    level_sea = Column(Integer)

    physical_attack_min = Column(Integer)
    magical_attack_min = Column(Integer)
    physical_attack_max = Column(Integer)
    magical_attack_max = Column(Integer)

    attack_range = Column(Integer)
    attack_speed = Column(Integer)

    upgrade_code = Column(String)

    def to_dict(self, minimal: bool) -> dict:
        minimal_dict = {
            **BaseMixin.to_dict(self, minimal),
            **BonusMixin.to_dict(self),
            "class_land": self.class_land,
            "level_land": self.level_land,
            "level_sea": self.level_sea,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            # "itemtype": self.itemtype,
            "physical_attack_min": self.physical_attack_min,
            "magical_attack_min": self.magical_attack_min,
            "physical_attack_max": self.physical_attack_max,
            "magical_attack_max": self.magical_attack_max,
            "attack_range": self.attack_range,
            "attack_speed": self.attack_speed,
            "upgrade_code": self.upgrade_code,
        }


class ArmorMixin(BaseMixin, BonusMixin):
    itemtype = Column(String)

    physical_defense = Column(Integer)
    magic_defense = Column(Integer)

    class_land = Column(String)
    level_land = Column(Integer)
    level_sea = Column(Integer)

    def to_dict(self, minimal: bool) -> dict:
        minimal_dict = {
            **BaseMixin.to_dict(self, minimal),
            **BonusMixin.to_dict(self),
            "class_land": self.class_land,
            "level_land": self.level_land,
            "level_sea": self.level_sea,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            # "itemtype": self.itemtype,
            "physical_defense": self.physical_defense,
            "magic_defense": self.magic_defense
        }


class ShipBaseMixin(BaseMixin):
    npc_price_tuning = Column(Integer)

    class_sea = Column(String)
    level_sea = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            **BaseMixin.to_dict(self, minimal),
            "class_sea": self.class_sea,
            "level_sea": self.level_sea,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "npc_price_tuning": self.npc_price_tuning
        }


class PlayerSkillMixin:
    code = Column(String, primary_key=True)
    name = Column(String)
    icon = Column(String)

    class_land = Column(String)
    skill_code = Column(String)
    skill_level = Column(Integer)

    required_level = Column(Integer)
    required_weapon = Column(String)
    max_level = Column(Integer)

    mana_consumption = Column(Integer)
    cooldown = Column(Integer)
    description = Column(String)

    required_skill_1 = Column(String)
    required_skill_2 = Column(String)
    required_skill_3 = Column(String)
    required_skill_4 = Column(String)
    required_skill_5 = Column(String)

    def to_dict(self) -> dict:
        required_skills = []
        for i in range(1, 6):
            req_skill = getattr(self, f"required_skill_{i}")
            if req_skill != "*":
                required_skills.append(req_skill)

        return {
            "code": self.code,
            "name": self.name,
            "icon": self.icon,
            "class_land": self.class_land,
            "skill_code": self.skill_code,
            "skill_level": self.skill_level,
            "max_level": self.max_level,
            "required_level": self.required_level,
            "required_weapon": self.required_weapon,
            "required_skills": required_skills,
            "mana_consumption": self.mana_consumption,
            "cooldown": self.cooldown,
            "description": self.description,
        }
