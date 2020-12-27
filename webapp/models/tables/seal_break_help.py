from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import DroppedByMixin, RandomBoxMixin
from webapp.models.mixins import BaseMixin


class SealBreakHelp(
    db.Model, BaseMixin,
    DroppedByMixin, RandomBoxMixin,
):
    __tablename__ = "seal_break_help"

    _mapper_utils = {
        "files": {
            "server": [
                "s_SealHelpBreakItem.bin"
            ],
            "client": [
                "c_SealHelpBreakItemRes.bin"
            ],
            "string": [
                "SealHelpBreakItemStr.dat"
            ],
            "description": [
                "SealHelpBreakItemDesc.dat"
            ],
        },
        "options": {
            "description_key": "코드"
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
            **DroppedByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
