import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import DropDistribution
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
    section_guaranteed = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        default=False,
        doc="Every item of a guaranteed section drops (probabilities are set to 1)",
    )
    item_probability = orm.mapped_column(
        sa.Float,
        nullable=False,
    )
    distribution = orm.mapped_column(
        sa.Enum(DropDistribution),
        nullable=False,
        default=DropDistribution.DEFAULT,
        doc="How the item is distributed in a party",
    )
    max_per_player = orm.mapped_column(
        sa.Integer,
        nullable=True,
        doc="Cap per party member for shared drops, None if uncapped",
    )
    bypass_level = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        default=False,
        doc="Party members in range receive the item regardless of the level rule",
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
