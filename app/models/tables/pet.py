from sqlalchemy import Column, Integer
from ...extensions import db
from ..mixins import BaseMixin


class Pet(db.Model, BaseMixin):
    __tablename__ = "pet"
    __bind_key__ = "static_data"

    duration = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        return {
            **BaseMixin.to_dict(self, minimal),
            "duration": self.duration,
        }
