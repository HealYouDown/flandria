from ...extensions import db
from ..mixins import ShipBaseMixin


class ShipFlag(db.Model, ShipBaseMixin):
    __tablename__ = "ship_flag"
    __bind_key__ = "static_data"

    def to_dict(self, minimal: bool = False) -> dict:
        return ShipBaseMixin.to_dict(self, minimal)
