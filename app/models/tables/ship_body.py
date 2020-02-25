from sqlalchemy import Column, Integer
from ...extensions import db
from ..mixins import ShipBaseMixin


class ShipBody(db.Model, ShipBaseMixin):
    __tablename__ = "ship_body"
    __bind_key__ = "static_data"

    ship_defense = Column(Integer)
    ship_guns_front = Column(Integer)
    ship_guns_side = Column(Integer)
    ship_guns_speed = Column(Integer)
    ship_hitrange = Column(Integer)
    physical_defense = Column(Integer)
    protection = Column(Integer)
    ability_hp = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "ship_defense": self.ship_defense,
            "ship_guns_front": self.ship_guns_front,
            "ship_guns_side": self.ship_guns_side,
            "ship_guns_speed": self.ship_guns_speed,
            "ship_hitrange": self.ship_hitrange,
            "physical_defense": self.physical_defense,
            "protection": self.protection,
            "ability_hp": self.ability_hp,
        }
