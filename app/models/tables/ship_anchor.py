from sqlalchemy import Column, Integer
from ...extensions import db
from ..mixins import ShipBaseMixin


class ShipAnchor(db.Model, ShipBaseMixin):
    __tablename__ = "ship_anchor"
    __bind_key__ = "static_data"

    ship_deceleration = Column(Integer)
    ship_turnpower = Column(Integer)
    balance = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "ship_deceleration": self.ship_deceleration,
            "ship_turnpower": self.ship_turnpower,
            "balance": self.balance,
        }
