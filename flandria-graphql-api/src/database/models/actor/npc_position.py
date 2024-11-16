import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base


class NpcPosition(Base):
    index = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )

    npc_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("npc.code"),
        index=True,
        nullable=False,
    )
    npc = orm.relationship(
        "Npc",
        foreign_keys=[npc_code],
        uselist=False,
        viewonly=True,
    )

    map_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("map.code"),
        index=True,
        nullable=False,
    )
    map = orm.relationship(
        "Map",
        foreign_keys=[map_code],
        uselist=False,
        viewonly=True,
    )

    x = orm.mapped_column(sa.Float, nullable=False)
    y = orm.mapped_column(sa.Float, nullable=False)
    z = orm.mapped_column(sa.Float, nullable=False)
