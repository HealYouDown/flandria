from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin)
from webapp.models.mixins import BaseMixin, BonusMixin
from webapp.models.enums import EssenceEquipType


class Essence(
    db.Model, BaseMixin, BonusMixin,
    DroppedByMixin, NeededForMixin, ProducedByMixin, RandomBoxMixin,
):
    __tablename__ = "essence"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ArtifactItem.bin"
            ],
            "client": [
                "c_ArtifactRes.bin"
            ],
            "string": [
                "ArtifactStr.dat"
            ],
        },
    }

    equip_type = CustomColumn(db.Enum(EssenceEquipType), nullable=False,
                              mapper_key="장착대상",
                              transform=lambda v: EssenceEquipType(int(v)))

    required_weapon_level = CustomColumn(db.Integer, nullable=False,
                                         mapper_key="육상LV")

    is_core_essence = CustomColumn(db.Boolean, nullable=False,
                                   mapper_key="AtI타입")

    mounting_cost = CustomColumn(db.Integer, nullable=False,
                                 mapper_key="고정비용")

    mounting_item_level_cost = CustomColumn(db.Integer, nullable=False,
                                            mapper_key="LV비용")

    mounting_unit_cost = CustomColumn(db.Integer, nullable=False,
                                      mapper_key="비용단위")

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            **BaseMixin.to_dict(self, minimal),
            **BonusMixin.to_dict(self),
            "equip_type": self.equip_type.to_dict(),
            "is_core_essence": self.is_core_essence,
            "required_weapon_level": self.required_weapon_level,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            **DroppedByMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **NeededForMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
