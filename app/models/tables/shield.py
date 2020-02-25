from ...extensions import db
from ..mixins import ArmorMixin


class Shield(db.Model, ArmorMixin):
    __tablename__ = "shield"
    __bind_key__ = "static_data"

    def to_dict(self, minimal: bool = False) -> dict:
        return ArmorMixin.to_dict(self, minimal)
