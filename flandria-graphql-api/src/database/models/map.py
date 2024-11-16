import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.updater import strategies
from src.updater.schema import LoaderInfo


class Map(Base):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_Area.bin"],
            string_files=["AreaStr.dat"],
        ),
        loader_strategy=strategies.map,
    )

    code = orm.mapped_column(
        sa.String(32),
        primary_key=True,
        doc="Code of the map",
    )
    name = orm.mapped_column(
        sa.String(256),
        nullable=False,
        doc="Name of the map",
    )
    left = orm.mapped_column(
        sa.Float,
        nullable=False,
    )
    top = orm.mapped_column(
        sa.Float,
        nullable=False,
    )
    width = orm.mapped_column(
        sa.Float,
        nullable=False,
    )
    height = orm.mapped_column(
        sa.Float,
        nullable=False,
    )

    areas = orm.relationship(
        "MapArea",
        uselist=True,
        viewonly=True,
    )

    monsters = orm.relationship(
        "MonsterPosition",
        uselist=True,
        viewonly=True,
    )
    npcs = orm.relationship(
        "NpcPosition",
        uselist=True,
        viewonly=True,
    )


class MapArea(Base):
    __table_args__ = (sa.PrimaryKeyConstraint("map_code", "area_code"),)

    map_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("map.code"),
        index=True,
        doc="Parent map code",
        nullable=False,
    )
    area_code = orm.mapped_column(
        sa.String(32),
        doc="Area code",
        nullable=False,
    )
    name = orm.mapped_column(
        sa.String(256),
        doc="Area name",
        nullable=False,
    )
