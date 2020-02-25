from sqlalchemy import Column, Integer
from ...extensions import db
from ..mixins import ShipBaseMixin


class ShipFront(db.Model, ShipBaseMixin):
    __tablename__ = "ship_front"
    __bind_key__ = "static_data"

    physical_defense = Column(Integer)
    protection = Column(Integer)
    ability_hp = Column(Integer)
    balance = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "physical_defense": self.physical_defense,
            "protection": self.protection,
            "ability_hp": self.ability_hp,
            "balance": self.balance,
        }
