import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class QuestScroll(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_QuestScrollItem.bin"],
            client_files=["c_QuestScrollItemRes.bin"],
            string_files=["QuestScrollItemStr.dat"],
        ),
        include_in_itemlist=True,
    )

    quest_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("quest.code"),
        index=True,
        nullable=False,
        doc="Quest code",
        info=ColumnInfo(key="대상코드"),
    )
    quest = orm.relationship(
        "Quest",
        uselist=False,
        viewonly=True,
        foreign_keys=[quest_code],
    )
