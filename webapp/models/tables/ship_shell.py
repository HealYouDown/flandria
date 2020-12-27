from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import DroppedByMixin, SoldByMixin
from webapp.models.mixins import BaseMixin
from webapp.models.transforms import florensia_sea_meter_transform


class ShipShell(
    db.Model, BaseMixin,
    DroppedByMixin, SoldByMixin
):
    __tablename__ = "ship_shell"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ShellItem.bin"
            ],
            "client": [
                "c_ShellItemRes.bin"
            ],
            "string": [
                "ShellItemStr.dat"
            ],
        },
    }

    level = CustomColumn(db.Integer, nullable=False, mapper_key="제한레벨")

    damage = CustomColumn(db.Integer, nullable=False, mapper_key="물공력")

    explosion_range = CustomColumn(db.Float, nullable=False, mapper_key="폭발반경",
                                   transform=florensia_sea_meter_transform)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "level": self.level,
            "damage": self.damage,
            "explosion_range": self.explosion_range,
            **DroppedByMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
        }
