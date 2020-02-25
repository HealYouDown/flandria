from sqlalchemy import Column, Integer, String
from ...extensions import db
from ..mixins import BaseMixin


class RidingPet(db.Model, BaseMixin):
    __tablename__ = "riding_pet"
    __bind_key__ = "static_data"

    duration = Column(Integer)
    description = Column(String)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            **BaseMixin.to_dict(self, minimal),
            "duration": self.duration,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "description": self.description
        }
