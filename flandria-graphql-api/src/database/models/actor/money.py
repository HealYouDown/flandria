import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base


class Money(Base):
    monster_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("monster.code"),
        primary_key=True,
        nullable=False,
    )
    monster = orm.relationship(
        "Monster",
        foreign_keys=[monster_code],
        uselist=False,
        viewonly=True,
    )
    probability = orm.mapped_column(
        sa.Float,
        nullable=False,
    )

    min = orm.mapped_column(
        sa.Integer,
        nullable=False,
    )
    max = orm.mapped_column(
        sa.Integer,
        nullable=False,
    )
