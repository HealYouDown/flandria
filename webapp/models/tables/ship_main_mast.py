from database_updater.conversions import convert_integer
from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import ShipBaseMixin
from webapp.models.transforms import florensia_sea_meter_transform


class ShipMainMast(
    db.Model, ShipBaseMixin,
    DroppedByMixin, SoldByMixin, NeededForMixin, ProducedByMixin,
    RandomBoxMixin,
):
    __tablename__ = "ship_main_mast"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ShipMainmastItem.bin"
            ],
            "client": [
                "c_ShipMainMastItemRes.bin"
            ],
            "string": [
                "ShipMainMastItemStr.dat"
            ],
        },
    }

    favorable_wind = CustomColumn(db.Integer, nullable=False,
                                  mapper_key="횡범성능")

    adverse_wind = CustomColumn(db.Integer, nullable=False,
                                mapper_key="종범성능")

    turning_power = CustomColumn(db.Float, nullable=False,
                                 mapper_key="선회력",
                                 transform=convert_integer)

    acceleration = CustomColumn(
        db.Float, nullable=False, mapper_key="가속력",
        # Converted value is e.g. 56, ingame value is
        # # displayed as 5.6 ?
        transform=lambda v: florensia_sea_meter_transform(
            convert_integer(v)))

    deceleration = CustomColumn(
        db.Float, nullable=False, mapper_key="정선력",
        transform=lambda v: florensia_sea_meter_transform(
            convert_integer(v)))

    balance = CustomColumn(db.Integer, nullable=False,
                           mapper_key="벨런스",)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "favorable_wind": self.favorable_wind,
            "adverse_wind": self.adverse_wind,
            "turning_power": self.turning_power,
            "acceleration": self.acceleration,
            "deceleration": self.deceleration,
            "balance": self.balance,
            **DroppedByMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **NeededForMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
