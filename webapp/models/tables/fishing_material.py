from webapp.extensions import db
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, SoldByMixin,
                                              RandomBoxMixin)
from webapp.models.mixins import BaseMixin


class FishingMaterial(
    db.Model, BaseMixin,
    DroppedByMixin, SoldByMixin, ProducedByMixin, NeededForMixin,
    RandomBoxMixin,
):
    __tablename__ = "fishing_material"

    _mapper_utils = {
        "files": {
            "server": [
                "s_FishMaterialItem.bin"
            ],
            "client": [
                "c_FishMaterialItemRes.bin"
            ],
            "string": [
                "FishMaterialItemStr.dat"
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
