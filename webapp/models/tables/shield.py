from webapp.extensions import db
from webapp.models.declarative_mixins import (DroppedByMixin, ItemSetMixin,
                                              NeededForMixin, ProducedByMixin,
                                              RandomBoxMixin, SoldByMixin)
from webapp.models.mixins import ArmorEquipmentMixin


class Shield(
    db.Model, ArmorEquipmentMixin,
    ItemSetMixin, DroppedByMixin, ProducedByMixin, NeededForMixin,
    RandomBoxMixin, SoldByMixin,
):
    __tablename__ = "shield"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ShieldItem.bin"
            ],
            "client": [
                "c_ShieldItemRes.bin"
            ],
            "string": [
                "ShieldItemStr.dat"
            ],
        },
    }

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ArmorEquipmentMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            **ItemSetMixin.to_dict(self),
            **DroppedByMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **NeededForMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
