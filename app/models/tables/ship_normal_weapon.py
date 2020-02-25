from sqlalchemy import Column, Integer
from ...extensions import db
from ..mixins import ShipBaseMixin


class ShipNormalWeapon(db.Model, ShipBaseMixin):
    __tablename__ = "ship_normal_weapon"
    __bind_key__ = "static_data"

    ship_defense = Column(Integer)
    ship_range = Column(Integer)
    critical = Column(Integer)
    ship_reloadspeed = Column(Integer)
    ship_guns_front = Column(Integer)
    ship_guns_side = Column(Integer)
    ship_guns_speed = Column(Integer)
    ship_hitrange = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "ship_defense": self.ship_defense,
            "ship_range": self.ship_range,
            "critical": self.critical,
            "ship_reloadspeed": self.ship_reloadspeed,
            "ship_guns_front": self.ship_guns_front,
            "ship_guns_side": self.ship_guns_side,
            "ship_guns_speed": self.ship_guns_speed,
            "ship_hitrange": self.ship_hitrange
        }
