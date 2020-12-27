import copy

from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declared_attr
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.mixins import (CLASS_LAND_COLUMN, LEVEL_LAND_COLUMN,
                                  LEVEL_SEA_COLUMN, UPGRADE_CODE_COLUMN,
                                  BaseMixin, BonusMixin)
from webapp.models.transforms import florensia_meter_transform


class WeaponEquipmentMixin(BaseMixin, BonusMixin):
    @declared_attr
    def class_land(cls):
        return copy.deepcopy(CLASS_LAND_COLUMN)

    @declared_attr
    def level_land(cls):
        return copy.deepcopy(LEVEL_LAND_COLUMN)

    @declared_attr
    def level_sea(cls):
        return copy.deepcopy(LEVEL_SEA_COLUMN)

    @declared_attr
    def minimal_physical_attack(cls):
        return CustomColumn(Integer, nullable=False, mapper_key="최소물공력")

    @declared_attr
    def maximal_physical_attack(cls):
        return CustomColumn(Integer, nullable=False, mapper_key="최대물공력")

    @declared_attr
    def minimal_magic_attack(cls):
        return CustomColumn(Integer, nullable=False, mapper_key="최소마공력")

    @declared_attr
    def maximal_magic_attack(cls):
        return CustomColumn(Integer, nullable=False, mapper_key="최대마공력")

    @declared_attr
    def attack_speed(cls):
        return CustomColumn(Integer, nullable=False, mapper_key="물공쿨타임밀초")

    @declared_attr
    def attack_range(cls):
        return CustomColumn(
            Integer, nullable=False, mapper_key="물공최대거리",
            transform=florensia_meter_transform)

    @declared_attr
    def upgrade_code(cls):
        return copy.deepcopy(UPGRADE_CODE_COLUMN)

    def to_dict(self, minimal: bool = False) -> dict:
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
            "minimal_physical_attack": self.minimal_physical_attack,
            "maximal_physical_attack": self.maximal_physical_attack,
            "minimal_magic_attack": self.minimal_magic_attack,
            "maximal_magic_attack": self.maximal_magic_attack,
            "attack_speed": self.attack_speed,
            "attack_range": self.attack_range,
        }
