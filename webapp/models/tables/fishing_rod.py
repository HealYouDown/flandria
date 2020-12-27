from webapp.extensions import db
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import WeaponEquipmentMixin


class FishingRod(
    db.Model, WeaponEquipmentMixin,
    RandomBoxMixin, SoldByMixin, ProducedByMixin, NeededForMixin,
    DroppedByMixin,
):
    __tablename__ = "fishing_rod"

    _mapper_utils = {
        "files": {
            "server": [
                "s_FishingItem.bin"
            ],
            "client": [
                "c_FishingItemRes.bin"
            ],
            "string": [
                "FishingItemStr.dat"
            ],
        },
    }

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = WeaponEquipmentMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            **ProducedByMixin.to_dict(self),
            **NeededForMixin.to_dict(self),
            **DroppedByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
