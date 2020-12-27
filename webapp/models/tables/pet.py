from webapp.extensions import db
from webapp.models.declarative_mixins import DroppedByMixin, RandomBoxMixin
from webapp.models.mixins import BaseMixin
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.transforms import MAX_INT


class Pet(
    db.Model, BaseMixin,
    DroppedByMixin, RandomBoxMixin,
):
    __tablename__ = "pet"

    _mapper_utils = {
        "files": {
            "server": [
                "s_PetItem.bin"
            ],
            "client": [
                "c_PetItemRes.bin"
            ],
            "string": [
                "PetItemStr.dat"
            ],
        },
    }

    inital_courage = CustomColumn(
        db.Integer, mapper_key="용기",
        transform=lambda v: v if v != MAX_INT else 0)

    inital_patience = CustomColumn(
        db.Integer, mapper_key="인내",
        transform=lambda v: v if v != MAX_INT else 0)

    inital_wisdom = CustomColumn(
        db.Integer, mapper_key="지혜",
        transform=lambda v: v if v != MAX_INT else 0)

    # Whether the pet needs pocket watches (False)
    # or not (True)
    is_unlimited = CustomColumn(
        db.Boolean, mapper_key="펫봉인타임",
        transform=lambda v: True if v == MAX_INT else False)

    strength = CustomColumn(db.Integer, mapper_key="str")
    dexterity = CustomColumn(db.Integer, mapper_key="dex")
    constitution = CustomColumn(db.Integer, mapper_key="con")
    intelligence = CustomColumn(db.Integer, mapper_key="int")
    wisdom = CustomColumn(db.Integer, mapper_key="wis")

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "inital_courage": self.inital_courage,
            "inital_patience": self.inital_patience,
            "inital_wisdom": self.inital_wisdom,
            "is_unlimited": self.is_unlimited,
            **DroppedByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
