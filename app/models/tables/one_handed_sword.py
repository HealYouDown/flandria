from ...extensions import db
from ..mixins import WeaponMixin


class OneHandedSword(db.Model, WeaponMixin):
    __tablename__ = "one_handed_sword"
    __bind_key__ = "static_data"

    def to_dict(self, minimal: bool = False) -> dict:
        return WeaponMixin.to_dict(self, minimal)
