from webapp.extensions import db
from webapp.models.declarative_mixins import (DroppedByMixin, ItemSetMixin,
                                              ProducedByMixin, RandomBoxMixin)
from webapp.models.mixins import ExtraEquipmentMixin


class Hat(
    db.Model, ExtraEquipmentMixin,
    DroppedByMixin, RandomBoxMixin, ProducedByMixin, ItemSetMixin,
):
    __tablename__ = "hat"

    _mapper_utils = {
        "files": {
            "server": [
                "s_HatItem.bin"
            ],
            "client": [
                "c_HatItemRes.bin"
            ],
            "string": [
                "HatItemStr.dat"
            ],
        },
    }

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ExtraEquipmentMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            **DroppedByMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
