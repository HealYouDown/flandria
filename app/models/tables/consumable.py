from sqlalchemy import Column, String, Integer
from ...extensions import db
from ..mixins import BaseMixin


class Consumable(db.Model, BaseMixin):
    __tablename__ = "consumable"
    __bind_key__ = "static_data"

    class_land = Column(String)
    cooltime = Column(Integer)
    efficiency = Column(Integer)
    description = Column(String)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            # "class_land": self.class_land,
            "cooltime": self.cooltime,
            "efficiency": self.efficiency,
            "description": self.description
        }
