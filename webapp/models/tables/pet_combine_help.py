from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import DroppedByMixin, RandomBoxMixin
from webapp.models.mixins import BaseMixin


class PetCombineHelp(
    db.Model, BaseMixin,
    DroppedByMixin, RandomBoxMixin,
):
    __tablename__ = "pet_combine_help"

    _mapper_utils = {
        "files": {
            "server": [
                "s_PetCombineHelpItem.bin"
            ],
            "client": [
                "c_PetCombineHelpItemRes.bin"
            ],
            "string": [
                "PetCombineHelpItemStr.dat"
            ],
        },
    }

    efficiency = CustomColumn(db.Integer, nullable=False,
                              mapper_key="성공확률보정")

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "efficiency": self.efficiency,
            **DroppedByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
