from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import RandomBoxMixin
from webapp.models.mixins import BaseMixin


class RidingPet(
    db.Model, BaseMixin,
    RandomBoxMixin,
):
    __tablename__ = "riding_pet"

    _mapper_utils = {
        "files": {
            "server": [
                "s_RidingPetItem.bin"
            ],
            "client": [
                "c_RidingpetItemRes.bin"
            ],
            "string": [
                "RidingpetItemStr.dat"
            ],
            "description": [
                "LandItemSkillActionDesc.dat"
            ],
        },
        "options": {
            "description_key": "스킬코드",
        }
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
            **RandomBoxMixin.to_dict(self),
        }
