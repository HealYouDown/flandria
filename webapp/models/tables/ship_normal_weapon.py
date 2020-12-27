from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import ShipBaseMixin
from webapp.models.transforms import (florensia_sea_meter_transform,
                                      florensia_time_transform)


class ShipNormalWeapon(
    db.Model, ShipBaseMixin,
    DroppedByMixin, SoldByMixin, RandomBoxMixin, ProducedByMixin,
    NeededForMixin,
):
    __tablename__ = "ship_normal_weapon"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ShipNWeaponItem.bin"
            ],
            "client": [
                "c_ShipNWeaponItemRes.bin"
            ],
            "string": [
                "ShipNWeaponItemStr.dat"
            ],
        },
    }

    damage = CustomColumn(db.Integer, nullable=False, mapper_key="공격력")

    range = CustomColumn(db.Float, nullable=False, mapper_key="최대거리",
                         transform=florensia_sea_meter_transform)

    critical = CustomColumn(db.Integer, nullable=False, mapper_key="크리티컬")

    reloadspeed = CustomColumn(db.Float, nullable=False, mapper_key="장전속도",
                               transform=florensia_time_transform)

    hitrange = CustomColumn(db.Float, nullable=False, mapper_key="집탄범위",
                            transform=florensia_sea_meter_transform)

    balance = CustomColumn(db.Integer, nullable=False, default=-2)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "damage": self.damage,
            "range": self.range,
            "critical": self.critical,
            "reloadspeed": self.reloadspeed,
            "hitrange": self.hitrange,
            "balance": self.balance,
            **DroppedByMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **NeededForMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
