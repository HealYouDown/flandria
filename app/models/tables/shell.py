from sqlalchemy import Column, Integer
from ...extensions import db
from ..mixins import BaseMixin


class Shell(db.Model, BaseMixin):
    __tablename__ = "shell"
    __bind_key__ = "static_data"

    level_sea = Column(Integer)
    damage = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            **BaseMixin.to_dict(self, minimal),
            "level_sea": self.level_sea
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "damage": self.damage
        }
