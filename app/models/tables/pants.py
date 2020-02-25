from sqlalchemy import Column, String
from ...extensions import db
from ..mixins import ArmorMixin


class Pants(db.Model, ArmorMixin):
    __tablename__ = "pants"
    __bind_key__ = "static_data"

    upgrade_code = Column(String)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ArmorMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "upgrade_code": self.upgrade_code
        }
