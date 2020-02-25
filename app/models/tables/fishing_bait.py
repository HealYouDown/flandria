from ...extensions import db
from ..mixins import BaseMixin


class FishingBait(db.Model, BaseMixin):
    __tablename__ = "fishing_bait"
    __bind_key__ = "static_data"

    def to_dict(self, minimal: bool = False) -> dict:
        return BaseMixin.to_dict(self, minimal)
