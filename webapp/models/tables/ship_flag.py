from webapp.extensions import db
from webapp.models.declarative_mixins import DroppedByMixin, SoldByMixin
from webapp.models.mixins import ShipBaseMixin


class ShipFlag(
    db.Model, ShipBaseMixin,
    DroppedByMixin, SoldByMixin,
):
    __tablename__ = "ship_flag"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ShipFlagItem.bin"
            ],
            "client": [
                "c_ShipFlagItemRes.bin"
            ],
            "string": [
                "ShipFlagItemStr.dat"
            ],
        },
    }

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ShipBaseMixin.to_dict(self)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            **DroppedByMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
