import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import ActorMixin
from src.updater.schema import ColumnInfo, LoaderInfo
from src.updater.transforms import probability_to_float


class Monster(Base, ActorMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_MonsterChar.bin"],
            client_files=["c_MonsterCharRes.bin"],
            string_files=["MonsterCharStr.dat"],
        )
    )

    # TODO: n:m for skills
    skill_1_code = orm.mapped_column(
        sa.String,
        sa.ForeignKey("monster_skill.code"),
        index=True,
        nullable=True,
        doc="Code for skill object #1",
        info=ColumnInfo(key="부가Action1코드"),
    )

    skill_1_chance = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Chance to use skill #1",
        info=ColumnInfo(
            key="부가Action1선택율",
            transforms=[probability_to_float],
        ),
    )

    @orm.declared_attr
    def skill_1(cls):
        return orm.relationship(
            "MonsterSkill",
            uselist=False,
            viewonly=True,
            foreign_keys=[cls.skill_1_code],
        )

    skill_2_code = orm.mapped_column(
        sa.String,
        sa.ForeignKey("monster_skill.code"),
        index=True,
        nullable=True,
        doc="Code for skill object #2",
        info=ColumnInfo(key="부가Action2코드"),
    )

    skill_2_chance = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Chance to use skill #2",
        info=ColumnInfo(
            key="부가Action2선택율",
            transforms=[probability_to_float],
        ),
    )

    @orm.declared_attr
    def skill_2(cls):
        return orm.relationship(
            "MonsterSkill",
            uselist=False,
            viewonly=True,
            foreign_keys=[cls.skill_2_code],
        )

    drops = orm.relationship(
        "Drop",
        viewonly=True,
        uselist=True,
    )
    money = orm.relationship(
        "Money",
        viewonly=True,
        uselist=False,
    )

    positions = orm.relationship(
        "MonsterPosition",
        viewonly=True,
        uselist=True,
    )
