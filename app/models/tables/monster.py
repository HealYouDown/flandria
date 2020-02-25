from sqlalchemy import Column, String, Integer
from ...extensions import db


class Monster(db.Model):
    __tablename__ = "monster"
    __bind_key__ = "static_data"

    index = Column(Integer)
    code = Column(String, primary_key=True)
    name = Column(String)
    icon = Column(String)
    rating_type = Column(Integer)
    level = Column(Integer)
    hp = Column(Integer)
    range = Column(String)
    location = Column(Integer)
    required_hitrate = Column(Integer)
    experience = Column(Integer)
    min_dmg = Column(Integer)
    max_dmg = Column(Integer)
    physical_defense = Column(Integer)
    magical_defense = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            "code": self.code,
            "name": self.name,
            "icon": self.icon,
            "rating_type": self.rating_type,
            "level": self.level,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "hp": self.hp,
            "range": self.range,
            "location": self.location,
            "required_hitrate": self.required_hitrate,
            "experience": self.experience,
            "min_dmg": self.min_dmg,
            "max_dmg": self.max_dmg,
            "physical_defense": self.physical_defense,
            "magical_defense": self.magical_defense,
        }
