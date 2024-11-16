import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import Gender, ItemGrade
from src.database.base import Base
from src.database.column_types import RGB
from src.database.mixins import ClassLandMixin, ClassSeaMixin, EffectMixin

# Technically, we're storing a lot of redundant data in here
# but that's just how life is. Allows for faster queries instead of
# having to do another query to get specific attributes from different tables


class ItemList(Base, ClassLandMixin, ClassSeaMixin, EffectMixin):
    code = orm.mapped_column(
        sa.String(32),
        primary_key=True,
        nullable=False,
    )
    tablename = orm.mapped_column(
        sa.String(128),
        doc="Tablename for the item",
        nullable=False,
    )
    name = orm.mapped_column(
        sa.String(256),
        nullable=False,
        index=True,
        doc="Name of the item",
    )
    icon = orm.mapped_column(
        sa.String(32),
        nullable=False,
        doc="Icon of the item",
    )
    grade = orm.mapped_column(
        sa.Enum(ItemGrade),
        nullable=False,
        doc="Grade of the item",
        default=ItemGrade.BLUE,
    )
    gender = orm.mapped_column(
        sa.Enum(Gender),
        nullable=True,
        doc="Gender for the item, if there is one",
    )
    duration = orm.mapped_column(
        sa.Integer,
        nullable=True,
        doc="Lifespan of the item in minutese",
        default=None,
    )
    level_land = orm.mapped_column(
        sa.Integer,
        nullable=True,
        doc="Item level land, could be None",
    )
    level_sea = orm.mapped_column(
        sa.Integer,
        nullable=True,
        doc="Item level land, could be None",
    )
    model_name = orm.mapped_column(
        sa.String(16),
        nullable=True,
        doc="Model code name",
    )
    model_variant = orm.mapped_column(
        RGB,
        nullable=True,
        doc="Model variant",
    )
