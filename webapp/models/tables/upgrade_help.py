from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import BaseMixin


class UpgradeHelp(
    db.Model, BaseMixin,
    DroppedByMixin, SoldByMixin, RandomBoxMixin,
):
    __tablename__ = "upgrade_help"

    _mapper_utils = {
        "files": {
            "server": [
                "s_UpgradeHelpItem.bin"
            ],
            "client": [
                "c_UpgradeHelpItemRes.bin"
            ],
            "string": [
                "UpgradeHelpItemStr.dat"
            ],
            "description": [
                "UpgradeHelpItemDesc.dat"
            ],
        },
        "options": {
            "description_key": "코드"
        }
    }

    description = CustomColumn(db.Text, mapper_key="_description")

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "description": self.description,
            **SoldByMixin.to_dict(self),
            **DroppedByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
