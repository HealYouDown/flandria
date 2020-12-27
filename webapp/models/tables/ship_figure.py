from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import ShipBaseMixin


class ShipFigure(
    db.Model, ShipBaseMixin,
    DroppedByMixin, SoldByMixin, NeededForMixin, ProducedByMixin,
    RandomBoxMixin,
):
    __tablename__ = "ship_figure"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ShipFigureItem.bin"
            ],
            "client": [
                "c_ShipFigureItemRes.bin"
            ],
            "string": [
                "ShipFigureItemStr.dat"
            ],
        },
    }

    protection = CustomColumn(db.Integer, nullable=False, mapper_key="방탄력")

    balance = CustomColumn(db.Integer, nullable=False, mapper_key="벨런스")

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "protection": self.protection,
            "balance": self.balance,
            **DroppedByMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **NeededForMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
