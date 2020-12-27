from webapp.extensions import db
from webapp.models.declarative_mixins import DroppedByMixin, SoldByMixin
from webapp.models.mixins import BaseMixin


class Bullet(
    db.Model, BaseMixin,
    DroppedByMixin, SoldByMixin
):
    __tablename__ = "bullet"

    _mapper_utils = {
        "files": {
            "server": [
                "s_BulletItem.bin"
            ],
            "client": [
                "c_BulletItemRes.bin"
            ],
            "string": [
                "BulletItemStr.dat"
            ],
        },
    }

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            **DroppedByMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
