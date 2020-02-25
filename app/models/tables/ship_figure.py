from sqlalchemy import Column, Integer
from ...extensions import db
from ..mixins import ShipBaseMixin


class ShipFigure(db.Model, ShipBaseMixin):
    __tablename__ = "ship_figure"
    __bind_key__ = "static_data"

    balance = Column(Integer)
    protection = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "balance": self.balance,
            "protection": self.protection
        }
