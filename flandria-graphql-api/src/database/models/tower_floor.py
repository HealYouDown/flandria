import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.updater import strategies
from src.updater.schema import ColumnInfo, LoaderInfo


class TowerFloorMonster(Base):
    __table_args__ = (sa.PrimaryKeyConstraint("floor_code", "monster_code"),)

    floor_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("tower_floor.code"),
        index=True,
        nullable=False,
        doc="Code of the tower floor",
    )
    monster_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("monster.code"),
        index=True,
        nullable=False,
        doc="Monster code",
    )
    monster = orm.relationship(
        "Monster",
        uselist=False,
        viewonly=True,
        foreign_keys=[monster_code],
    )
    amount = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="How many of those monsters are on the floor",
    )


class TowerFloor(Base):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_floorDungeonData.bin"],
        ),
        loader_strategy=strategies.tower_floor,
    )

    code = orm.mapped_column(
        sa.String(32),
        primary_key=True,
        doc="Tower floor code",
        info=ColumnInfo.code(),
    )
    floor_number = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Tower floor, 0-indexed",
        info=ColumnInfo(
            key="코드",
            # step00001 -> int("00001") -> 1
            transforms=[lambda v: int(v[4:])],
        ),
    )
    time = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Available time to clear the floor (in seconds)",
        info=ColumnInfo(key="시간"),
    )
    monsters = orm.relationship(
        "TowerFloorMonster",
        uselist=True,
        viewonly=True,
    )
