from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, ItemSetMixin,
                                              NeededForMixin, ProducedByMixin,
                                              RandomBoxMixin, SoldByMixin)
from webapp.models.enums import AccessoryType
from webapp.models.mixins import ExtraEquipmentMixin


class Accessory(
    db.Model, ExtraEquipmentMixin,
    ItemSetMixin, DroppedByMixin, ProducedByMixin, NeededForMixin,
    RandomBoxMixin, SoldByMixin,
):
    __tablename__ = "accessory"

    _mapper_utils = {
        "files": {
            "server": [
                "s_AccessoryItem.bin"
            ],
            "client": [
                "c_AccessoryItemRes.bin"
            ],
            "string": [
                "AccessoryItemStr.dat"
            ],
        },
    }

    accessory_type = CustomColumn(
        db.Enum(AccessoryType), nullable=False,
        mapper_key="구분코드", transform=lambda v: AccessoryType(v))

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            **ExtraEquipmentMixin.to_dict(self, minimal),
            "accessory_type": self.accessory_type.to_dict(),
        }

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
