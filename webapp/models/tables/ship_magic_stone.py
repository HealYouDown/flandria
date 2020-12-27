from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import ShipBaseMixin


class ShipMagicStone(
    db.Model, ShipBaseMixin,
    DroppedByMixin, SoldByMixin, NeededForMixin, ProducedByMixin,
    RandomBoxMixin,
):
    __tablename__ = "ship_magic_stone"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ShipMagicStoneItem.bin"
            ],
            "client": [
                "c_ShipMagicStoneItemRes.bin"
            ],
            "string": [
                "ShipMagicStoneItemStr.dat"
            ],
        },
    }

    en = CustomColumn(db.Integer, nullable=False, mapper_key="EN")

    en_recovery = CustomColumn(db.Integer, nullable=False, mapper_key="EN소모")

    balance = CustomColumn(db.Integer, nullable=False, mapper_key="벨런스")

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "en": self.en,
            "en_recovery": self.en_recovery,
            "balance": self.balance,
            **DroppedByMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **NeededForMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
