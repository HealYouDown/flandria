from ...extensions import db
from ..mixins import WeaponMixin


class TwoHandedSword(db.Model, WeaponMixin):
    __tablename__ = "two_handed_sword"
    __bind_key__ = "static_data"

    def to_dict(self, minimal: bool = False) -> dict:
        return WeaponMixin.to_dict(self, minimal)
