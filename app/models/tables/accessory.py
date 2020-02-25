from ...extensions import db
from ..mixins import ExtraEquipmentMixin


class Accessory(db.Model, ExtraEquipmentMixin):
    __tablename__ = "accessory"
    __bind_key__ = "static_data"

    def to_dict(self, minimal: bool = False) -> dict:
        return ExtraEquipmentMixin.to_dict(self, minimal)
