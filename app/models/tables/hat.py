from ...extensions import db
from ..mixins import ExtraEquipmentMixin


class Hat(db.Model, ExtraEquipmentMixin):
    __tablename__ = "hat"
    __bind_key__ = "static_data"

    def to_dict(self, minimal: bool = False) -> dict:
        return ExtraEquipmentMixin.to_dict(self, minimal)
