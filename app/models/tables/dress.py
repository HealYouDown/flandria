from ...extensions import db
from ..mixins import ExtraEquipmentMixin


class Dress(db.Model, ExtraEquipmentMixin):
    __tablename__ = "dress"
    __bind_key__ = "static_data"

    def to_dict(self, minimal: bool = False) -> dict:
        return ExtraEquipmentMixin.to_dict(self, minimal)
