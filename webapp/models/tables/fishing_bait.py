from webapp.extensions import db
from webapp.models.declarative_mixins import SoldByMixin
from webapp.models.mixins import BaseMixin


class FishingBait(
    db.Model, BaseMixin,
    SoldByMixin
):
    __tablename__ = "fishing_bait"

    _mapper_utils = {
        "files": {
            "server": [
                "s_BaitItem.bin"
            ],
            "client": [
                "c_BaitItemRes.bin"
            ],
            "string": [
                "BaitItemStr.dat"
            ],
        },
    }

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            **SoldByMixin.to_dict(self),
        }
