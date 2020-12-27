from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import ShipBaseMixin


class ShipFront(
    db.Model, ShipBaseMixin,
    DroppedByMixin, SoldByMixin, NeededForMixin, ProducedByMixin,
    RandomBoxMixin,
):
    __tablename__ = "ship_front"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ShipFrontItem.bin"
            ],
            "client": [
                "c_ShipFrontItemRes.bin"
            ],
            "string": [
                "ShipFrontItemStr.dat"
            ],
        },
    }

    physical_defense = CustomColumn(db.Integer, nullable=False,
                                    mapper_key="물방력")

    protection = CustomColumn(db.Integer, nullable=False, mapper_key="방탄력")

    dp = CustomColumn(db.Integer, nullable=False, mapper_key="HP")

    # All ship fronts appear to have balance = -1
    balance = CustomColumn(db.Integer, default=-1)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "physical_defense": self.physical_defense,
            "protection": self.protection,
            "dp": self.dp,
            "balance": self.balance,
            **DroppedByMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **NeededForMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
