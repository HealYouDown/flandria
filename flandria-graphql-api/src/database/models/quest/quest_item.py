from typing import TYPE_CHECKING

import sqlalchemy.orm as orm
from sqlalchemy.ext.hybrid import hybrid_property

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import LoaderInfo

if TYPE_CHECKING:
    from .quest import Quest


class QuestItem(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_QuestItem.bin"],
            client_files=["c_QuestItemRes.bin"],
            string_files=["QuestItemStr.dat"],
        ),
        include_in_itemlist=True,
    )

    quests_by_mission = orm.relationship(
        "Quest",
        secondary="quest_mission",
        uselist=True,
        viewonly=True,
    )
    quests_by_give_item = orm.relationship(
        "Quest",
        secondary="quest_give_item",
        primaryjoin="QuestGiveItem.item_code == QuestItem.code",
        uselist=True,
        viewonly=True,
    )

    @hybrid_property
    def related_quests(self) -> list["Quest"]:
        return self.quests_by_mission + self.quests_by_give_item
