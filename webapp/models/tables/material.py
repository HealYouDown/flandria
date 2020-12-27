from webapp.extensions import db
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import BaseMixin


class Material(
    db.Model, BaseMixin,
    DroppedByMixin, SoldByMixin, NeededForMixin, ProducedByMixin,
    RandomBoxMixin,
):
    __tablename__ = "material"

    _mapper_utils = {
        "files": {
            "server": [
                "s_StdMaterialItem.bin"
            ],
            "client": [
                "c_StdMaterialItemRes.bin"
            ],
            "string": [
                "StdMaterialItemStr.dat"
            ],
        },
    }

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            **NeededForMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **DroppedByMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
