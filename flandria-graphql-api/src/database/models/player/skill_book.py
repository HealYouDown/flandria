import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class SkillBook(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_SkillBookItem.bin"],
            client_files=["c_SkillBookItemRes.bin"],
            string_files=["SkillBookItemStr.dat"],
        ),
        include_in_itemlist=True,
    )

    skill_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("player_skill.code"),
        index=True,
        nullable=False,
        doc="Player skill code",
        info=ColumnInfo(key="대상코드"),
    )
    skill = orm.relationship(
        "PlayerSkill",
        uselist=False,
        viewonly=True,
        foreign_keys=[skill_code],
    )
