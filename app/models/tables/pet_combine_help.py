from sqlalchemy import Column, Integer
from ...extensions import db
from ..mixins import BaseMixin


class PetCombineHelp(db.Model, BaseMixin):
    __tablename__ = "pet_combine_help"
    __bind_key__ = "static_data"

    efficiency = Column(Integer)

    def to_dict(self, minimal: bool = False):
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "efficiency": self.efficiency
        }
