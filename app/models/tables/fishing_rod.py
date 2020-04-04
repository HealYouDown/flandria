from sqlalchemy import Column, String, Integer, Float
from ...extensions import db
from ..mixins import BonusMixin, BaseMixin


class FishingRod(db.Model, BaseMixin, BonusMixin):
    __tablename__ = "fishing_rod"
    __bind_key__ = "static_data"

    class_land = Column(String)
    itemtype = Column(String)
    level_land = Column(Integer)
    level_sea = Column(Integer)
    duration = Column(Float)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            **BaseMixin.to_dict(self, minimal),
            **BonusMixin.to_dict(self),
            "duration": self.duration,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "class_land": self.class_land,
            # "itemtype": self.itemtype,
            "level_land": self.level_land,
            "level_sea": self.level_sea
        }
