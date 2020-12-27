from webapp.extensions import db
from webapp.models.declarative_mixins import (DroppedByMixin, ItemSetMixin,
                                              NeededForMixin, ProducedByMixin,
                                              RandomBoxMixin, SoldByMixin,
                                              UpgradeRuleMixin)
from webapp.models.enums import WeaponType
from webapp.models.mixins import WeaponEquipmentMixin


class Rifle(
    db.Model, WeaponEquipmentMixin,
    ItemSetMixin, DroppedByMixin, UpgradeRuleMixin, ProducedByMixin,
    NeededForMixin, RandomBoxMixin, SoldByMixin,
):
    __tablename__ = "rifle"

    _mapper_utils = {
        "files": {
            "server": [
                "s_GunItem.bin"
            ],
            "client": [
                "c_GunItemRes.bin"
            ],
            "string": [
                "GunItemStr.dat"
            ],
        },
        "filter": lambda row: (
            WeaponType(row["무기타입"]) == WeaponType.rifle),
    }

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = WeaponEquipmentMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            **UpgradeRuleMixin.to_dict(self),
            **ItemSetMixin.to_dict(self),
            **DroppedByMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **NeededForMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
