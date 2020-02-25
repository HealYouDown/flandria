from sqlalchemy import Column, Integer
from ...extensions import db
from ..mixins import BaseMixin


class PetCombineStone(db.Model, BaseMixin):
    __tablename__ = "pet_combine_stone"
    __bind_key__ = "static_data"

    increment_min = Column(Integer)
    increment_max = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "increment_min": self.increment_min,
            "increment_max": self.increment_max,
        }
