import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo
from src.updater.transforms import ms_to_seconds, value_if_not_equal


class Consumable(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ConsumeItem.bin"],
            client_files=["c_ConsumeItemRes.bin"],
            string_files=["ConsumeItemStr.dat"],
            description_files=[
                "SeaItemSkillActionDesc.dat",
                "LandItemSkillActionDesc.dat",
            ],
        ),
        include_in_itemlist=True,
    )

    description = orm.mapped_column(
        sa.Text,
        nullable=True,
        doc="Description of the consume item",
        info=ColumnInfo.description("스킬코드"),
    )
    level_land = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Land level required to use the item",
        info=ColumnInfo(
            key="육상최소레벨",
            transforms=[lambda v: value_if_not_equal(v, 0, 1)],
        ),
    )
    level_sea = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Sea level required to use the item",
        info=ColumnInfo(
            key="해상최소레벨",
            transforms=[lambda v: value_if_not_equal(v, 0, 1)],
        ),
    )
    cooldown_id = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="All consumables with the same id share their cooldown",
        info=ColumnInfo(key="쿨타임계열"),
    )
    cooldown = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Cooldown in seconds",
        info=ColumnInfo(
            key="쿨타임밀초",
            transforms=[ms_to_seconds],
        ),
    )
    cast_time = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Cast time in seconds",
        info=ColumnInfo(
            key="캐스팅시간밀초",
            transforms=[ms_to_seconds],
        ),
    )
    value = orm.mapped_column(
        sa.Integer,
        nullable=True,
        doc="Could be how much HP or MP is restored, how much def " "you get, ...",
        info=ColumnInfo(
            key="성능",
            transforms=[lambda v: value_if_not_equal(v, -1)],
        ),
    )
    # TODO: Skill ForeignKey and Relationship
    skill_code = orm.mapped_column(
        sa.String(32),
        index=True,
        nullable=True,
        doc=(
            "Skill code of the effect which you may get "
            "(not all consumables have a skill)"
        ),
        info=ColumnInfo(key="스킬코드"),
    )
