from webapp.extensions import db
from webapp.models.declarative_mixins import DroppedByMixin, SoldByMixin
from webapp.models.mixins import BaseMixin
from webapp.models.custom_sql_classes import CustomColumn


class QuestScroll(
    db.Model, BaseMixin,
    DroppedByMixin, SoldByMixin,
):
    __tablename__ = "quest_scroll"

    _mapper_utils = {
        "files": {
            "server": [
                "s_QuestScrollItem.bin"
            ],
            "client": [
                "c_QuestScrollItemRes.bin"
            ],
            "string": [
                "QuestScrollItemStr.dat"
            ],
        },
    }

    quest_code = CustomColumn(db.String(32), db.ForeignKey("quest.code"),
                              nullable=False, mapper_key="대상코드")

    quest = db.relationship("Quest", foreign_keys=[quest_code],
                            uselist=False, viewonly=True,)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "quest": self.quest.to_dict(minimal=True) if self.quest else None,
            **SoldByMixin.to_dict(self),
            **DroppedByMixin.to_dict(self),
        }
