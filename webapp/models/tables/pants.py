import copy

from webapp.extensions import db
from webapp.models.declarative_mixins import (DroppedByMixin, ItemSetMixin,
                                              NeededForMixin, ProducedByMixin,
                                              RandomBoxMixin, SoldByMixin,
                                              UpgradeRuleMixin)
from webapp.models.mixins import UPGRADE_CODE_COLUMN, ArmorEquipmentMixin


class Pants(
    db.Model, ArmorEquipmentMixin,
    ItemSetMixin, DroppedByMixin, UpgradeRuleMixin, ProducedByMixin,
    NeededForMixin, RandomBoxMixin, SoldByMixin,
):
    __tablename__ = "pants"

    _mapper_utils = {
        "files": {
            "server": [
                "s_LowerItem.bin"
            ],
            "client": [
                "c_LowerItemRes.bin"
            ],
            "string": [
                "LowerItemStr.dat"
            ],
        },
    }

    upgrade_code = copy.deepcopy(UPGRADE_CODE_COLUMN)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = ArmorEquipmentMixin.to_dict(self, minimal)

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
