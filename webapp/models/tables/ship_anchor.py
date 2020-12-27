from database_updater.conversions import convert_integer
from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import ShipBaseMixin
from webapp.models.transforms import florensia_sea_meter_transform


class ShipAnchor(
    db.Model, ShipBaseMixin,
    DroppedByMixin, SoldByMixin, NeededForMixin, ProducedByMixin,
    RandomBoxMixin,
):
    __tablename__ = "ship_anchor"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ShipAnchorItem.bin"
            ],
            "client": [
                "c_ShipAnchorItemRes.bin"
            ],
            "string": [
                "ShipAnchorItemStr.dat"
            ],
        },
    }

    turning_power = CustomColumn(db.Float, nullable=False,
                                 mapper_key="선회력",
                                 transform=convert_integer)

    deceleration = CustomColumn(
        db.Float, nullable=False, mapper_key="정선력",
        transform=lambda v: florensia_sea_meter_transform(convert_integer(v)))

    balance = CustomColumn(db.Integer, nullable=False,
                           mapper_key="벨런스",)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "turning_power": self.turning_power,
            "deceleration": self.deceleration,
            "balance": self.balance,
            **DroppedByMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **NeededForMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
