from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import BaseMixin
from webapp.models.transforms import MAX_INT, florensia_time_transform


class Consumable(
    db.Model, BaseMixin,
    DroppedByMixin, SoldByMixin, RandomBoxMixin, ProducedByMixin,
    NeededForMixin,
):
    __tablename__ = "consumable"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ConsumeItem.bin"
            ],
            "client": [
                "c_ConsumeItemRes.bin"
            ],
            "string": [
                "ConsumeItemStr.dat"
            ],
            "description": [
                "SeaItemSkillActionDesc.dat",
                "LandItemSkillActionDesc.dat",
            ],
        },
        "options": {
            "description_key": "스킬코드"
        }
    }

    level_land = CustomColumn(db.Integer, nullable=False,
                              mapper_key="육상최소레벨")

    level_sea = CustomColumn(db.Integer, nullable=False,
                             mapper_key="해상최소레벨")

    # id that links items that have the same (shared) cooldown
    cooldown_type = CustomColumn(db.Integer, nullable=False,
                                 mapper_key="쿨타임계열")

    cooldown = CustomColumn(db.Float, nullable=False,
                            mapper_key="쿨타임밀초",
                            transform=florensia_time_transform)

    cast_time = CustomColumn(db.Integer, nullable=False,
                             mapper_key="캐스팅시간밀초")

    efficiency = CustomColumn(db.Integer, mapper_key="성능",
                              transform=lambda v: v if v != MAX_INT else None)

    skill_code = CustomColumn(db.String(32), mapper_key="스킬코드",
                              transform=lambda v: v if v != "#" else None)

    description = CustomColumn(db.Text(2048), mapper_key="_description")

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "level_land": self.level_land,
            "level_sea": self.level_sea,
            "cooldown": self.cooldown,
            "cast_time": self.cast_time,
            "efficiency": self.efficiency,
            "description": self.description,
            **NeededForMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **DroppedByMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
