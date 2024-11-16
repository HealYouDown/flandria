import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base


class MonsterPosition(Base):
    index = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )

    monster_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("monster.code"),
        index=True,
        nullable=False,
    )
    monster = orm.relationship(
        "Monster",
        foreign_keys=[monster_code],
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

    amount = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Amount of monsters at this spawn point",
    )

    respawn_time = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Respawn time at this location in minutes",
    )

    x = orm.mapped_column(sa.Float, nullable=False)
    y = orm.mapped_column(sa.Float, nullable=False)
    z = orm.mapped_column(sa.Float, nullable=False)
