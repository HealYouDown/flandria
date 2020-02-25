from sqlalchemy import Column, Integer
from ...extensions import db
from ..mixins import ShipBaseMixin


class ShipMainMast(db.Model, ShipBaseMixin):
    __tablename__ = "ship_main_mast"
    __bind_key__ = "static_data"

    ship_wind_favorable = Column(Integer)
    ship_wind_adverse = Column(Integer)
    ship_acceleration = Column(Integer)
    ship_deceleration = Column(Integer)
    ship_turnpower = Column(Integer)
    balance = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "ship_wind_favorable": self.ship_wind_favorable,
            "ship_wind_adverse": self.ship_wind_adverse,
            "ship_acceleration": self.ship_acceleration,
            "ship_deceleration": self.ship_deceleration,
            "ship_turnpower": self.ship_turnpower,
            "balance": self.balance
        }
