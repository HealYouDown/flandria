from webapp.extensions import db
from webapp.models.declarative_mixins import DroppedByMixin
from webapp.models.custom_sql_classes import CustomColumn


class QuestItem(
    db.Model,
    DroppedByMixin
):
    __tablename__ = "quest_item"

    _mapper_utils = {
        "files": {
            "server": [
                "s_QuestItem.bin"
            ],
            "client": [
                "c_QuestItemRes.bin"
            ],
            "string": [
                "QuestItemStr.dat"
            ],
        },
    }

    index = db.Column(db.Integer, nullable=False)

    code = CustomColumn(db.String(32), primary_key=True, nullable=False,
                        mapper_key="코드")

    name = CustomColumn(db.String(256), nullable=False, mapper_key="_name")

    icon = CustomColumn(db.String(32), nullable=False, mapper_key="_icon")

    stack_size = CustomColumn(db.Integer, nullable=False, mapper_key="중복가능수")

    quest_missions = db.relationship(
        "QuestMission",
        primaryjoin="foreign(QuestMission.quest_item_code) == QuestItem.code",
        viewonly=True,
    )

    quest_give_items = db.relationship(
        "QuestGiveItem",
        primaryjoin="foreign(QuestGiveItem.item_code) == QuestItem.code",
        viewonly=True,
    )

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            "code": self.code,
            "name": self.name,
            "icon": self.icon,
        }

        if minimal:
            return minimal_dict

        quest_objectives = self.quest_missions + self.quest_give_items

        return {
            **minimal_dict,
            "stack_size": self.stack_size,
            "quests": [quest_objective.quest.to_dict(minimal=True)
                       for quest_objective in quest_objectives],
            **DroppedByMixin.to_dict(self),
        }
