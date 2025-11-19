import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base


class Drop(Base):
    index = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )

    quantity = orm.mapped_column(
        sa.Integer,
        nullable=False,
    )

    section_id = orm.mapped_column(sa.Integer, nullable=False)
    section_probability = orm.mapped_column(
        sa.Float,
        nullable=False,
    )
    item_probability = orm.mapped_column(
        sa.Float,
        nullable=False,
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

    item_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_list.code"),
        index=True,
        nullable=False,
    )
    item = orm.relationship(
        "ItemList",
        foreign_keys=[item_code],
        uselist=False,
        viewonly=True,
    )
