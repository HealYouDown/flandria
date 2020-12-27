from webapp.extensions import db
from webapp.models.declarative_mixins import (DroppedByMixin, ItemSetMixin,
                                              ProducedByMixin, RandomBoxMixin)
from webapp.models.mixins import ExtraEquipmentMixin


class Dress(
    db.Model, ExtraEquipmentMixin,
    DroppedByMixin, RandomBoxMixin, ProducedByMixin, ItemSetMixin,
):
    __tablename__ = "dress"

    _mapper_utils = {
        "files": {
            "server": [
                "s_CloakItem.bin"
            ],
            "client": [
                "c_CloakItemRes.bin"
            ],
            "string": [
                "CloakItemStr.dat"
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
