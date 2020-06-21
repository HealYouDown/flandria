from sqlalchemy import Column, String, Integer, Float, Boolean
from app.extensions import db
from app.models.mixins import BonusMixin, BaseMixin


class Essence(db.Model, BaseMixin, BonusMixin):
    __tablename__ = "essence"
    __bind_key__ = "static_data"

    level_land = Column(Integer)
    level_sea = Column(Integer)
    core_essence = Column(Boolean)
    equip = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            **BaseMixin.to_dict(self, minimal),
            **BonusMixin.to_dict(self),
            "equip": self.equip,
            "level": self.level_land,
            "core_essence": self.core_essence,
        }

        return minimal_dict
