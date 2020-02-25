from sqlalchemy import Column, Integer
from ...extensions import db
from ..mixins import ShipBaseMixin


class ShipMagicStone(db.Model, ShipBaseMixin):
    __tablename__ = "ship_magic_stone"
    __bind_key__ = "static_data"

    ability_en_recovery = Column(Integer)
    ability_en = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "ability_en_recovery": self.ability_en_recovery,
            "ability_en": self.ability_en
        }
