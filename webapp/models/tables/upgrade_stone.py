from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import BaseMixin

EXCLUDES = [
    "usnew0001", "usnew0002", "usnew0003", "usnew0004", "usnew0005",
    "usnew0006", "usnew0007", "usnew0008", "usnew0009", "usnew0010",
    "usnew0011", "usnew0012", "usnew0013", "usnew0014", "usnew0015",
    "usnew0016", "usnew0017", "usnew0018", "usnew0019", "usnew0020",
    "usnew0021", "usnew0022", "usnew0023", "usnew0024", "usnew0025",
    "usnew0026", "usnew0027", "usnew0028", "usnew0029", "usnew0030",
    "usnew0031", "usnew0032", "usnew0033", "usnew0034", "usnew0035",
    "usnew0036", "usnew0037", "usnew0038", "usnew0039", "usnew0040",
    "usnew0041", "usnew0042", "usnew0043", "usnew0044", "usnew0045",
]


class UpgradeStone(
    db.Model, BaseMixin,
    DroppedByMixin, SoldByMixin, RandomBoxMixin,
):
    __tablename__ = "upgrade_stone"

    _mapper_utils = {
        "files": {
            "server": [
                "s_UpgradeStoneItem.bin"
            ],
            "client": [
                "c_UpgradeStoneItemRes.bin"
            ],
            "string": [
                "UpgradeStoneItemStr.dat"
            ],
            "description": [
                "UpgradeStoneItemDesc.dat"
            ],
        },
        "options": {
            "description_key": "코드"
        },
        "filter": lambda row: row["코드"] not in EXCLUDES,
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
            **SoldByMixin.to_dict(self),
            **DroppedByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
