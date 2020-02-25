from sqlalchemy import Column, String, Integer
from ...extensions import db
from ..mixins import BaseMixin


class PetSkillStone(db.Model, BaseMixin):
    __tablename__ = "pet_skill_stone"
    __bind_key__ = "static_data"

    description = Column(String)
    cooldown = Column(Integer)
    casttime = Column(Integer)
    level = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            **BaseMixin.to_dict(self, minimal),
            "level": self.level,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "description": self.description,
            "cooldown": self.cooldown,
            "casttime": self.casttime
        }
