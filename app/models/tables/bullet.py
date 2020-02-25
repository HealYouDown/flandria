from ...extensions import db
from ..mixins import BaseMixin


class Bullet(db.Model, BaseMixin):
    __tablename__ = "bullet"
    __bind_key__ = "static_data"

    def to_dict(self, minimal: bool = False) -> dict:
        return BaseMixin.to_dict(self, minimal)
