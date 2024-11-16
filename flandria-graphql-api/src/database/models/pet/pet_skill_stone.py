import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class PetSkillStone(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_PetSkillStoneItem.bin"],
            client_files=["c_PetSkillStoneItemRes.bin"],
            string_files=["PetSkillStoneItemStr.dat"],
        ),
        include_in_itemlist=True,
    )

    skill_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("pet_skill.code"),
        nullable=False,
        index=True,
        doc="Skill code",
        info=ColumnInfo(key="대상코드"),
    )
    skill = orm.relationship(
        "PetSkill",
        uselist=False,
        viewonly=True,
        foreign_keys=[skill_code],
    )
