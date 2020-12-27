import copy

from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declared_attr
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.mixins import (CLASS_LAND_COLUMN, LEVEL_LAND_COLUMN,
                                  LEVEL_SEA_COLUMN, BaseMixin, BonusMixin)


class ArmorEquipmentMixin(BaseMixin, BonusMixin):
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
    def physical_defense(cls):
        return CustomColumn(Integer, nullable=False, mapper_key="물방력")

    @declared_attr
    def magic_defense(cls):
        return CustomColumn(Integer, nullable=False, mapper_key="마항력")

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
            "physical_defense": self.physical_defense,
            "magic_defense": self.magic_defense,
        }
