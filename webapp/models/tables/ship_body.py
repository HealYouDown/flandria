from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import ShipBaseMixin


class ShipBody(
    db.Model, ShipBaseMixin,
    DroppedByMixin, SoldByMixin, NeededForMixin, ProducedByMixin,
    RandomBoxMixin,
):
    __tablename__ = "ship_body"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ShipBodyItem.bin",
            ],
            "client": [
                "c_ShipBodyItemRes.bin",
            ],
            "string": [
                "ShipBodyItemStr.dat",
            ],
        },
    }

    physical_defense = CustomColumn(db.Integer, nullable=False,
                                    mapper_key="물방력")

    protection = CustomColumn(db.Integer, nullable=False, mapper_key="방탄력")

    dp = CustomColumn(db.Integer, nullable=False, mapper_key="HP")

    guns_front = CustomColumn(db.Integer, nullable=False, mapper_key="전포수")

    guns_side = CustomColumn(db.Integer, nullable=False, mapper_key="측포수")

    crew_size = CustomColumn(db.Integer, nullable=False, mapper_key="필요선원수")

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "physical_defense": self.physical_defense,
            "protection": self.protection,
            "dp": self.dp,
            "guns_front": self.guns_front,
            "guns_side": self.guns_side,
            "crew_size": self.crew_size,
            **DroppedByMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **NeededForMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
