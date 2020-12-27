from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin)
from webapp.models.mixins import BaseMixin


class EssenceHelp(
    db.Model, BaseMixin,
    DroppedByMixin, NeededForMixin, ProducedByMixin, RandomBoxMixin,
):
    __tablename__ = "essence_help"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ArtifactManagItem.bin"
            ],
            "client": [
                "c_ArtifactManagItemRes.bin"
            ],
            "string": [
                "ArtifactManagItemStr.dat"
            ],
            "description": [
                "ArtifactManagItemDesc.dat"
            ],
        },
        "options": {
            "description_key": "코드",
        },
    }

    description = CustomColumn(db.Text, nullable=False,
                               mapper_key="_description")

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "description": self.description,
            **DroppedByMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **NeededForMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
