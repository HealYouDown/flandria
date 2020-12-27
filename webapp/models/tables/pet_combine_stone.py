from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import DroppedByMixin, RandomBoxMixin
from webapp.models.mixins import BaseMixin


class PetCombineStone(
    db.Model, BaseMixin,
    DroppedByMixin, RandomBoxMixin,
):
    __tablename__ = "pet_combine_stone"

    _mapper_utils = {
        "files": {
            "server": [
                "s_PetCombineItem.bin"
            ],
            "client": [
                "c_PetCombineItemRes.bin"
            ],
            "string": [
                "PetCombineItemStr.dat"
            ],
        },
    }

    efficiency_minimal = CustomColumn(db.Integer, nullable=False,
                                      mapper_key="성공확률보정")

    efficiency_maximal = CustomColumn(db.Integer, nullable=False,
                                      mapper_key="증가최대값")

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "efficiency_minimal": self.efficiency_minimal,
            "efficiency_maximal": self.efficiency_maximal,
            **DroppedByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
