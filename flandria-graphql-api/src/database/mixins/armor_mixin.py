import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.updater.schema import ColumnInfo

from .base_mixin import BaseMixin
from .class_land_mixin import ClassLandMixin
from .effect_mixin import EffectMixin
from .florensia_model_mixin import FlorensiaModelMixin
from .item_set_mixin import ItemSetMixin


class ArmorMixin(
    BaseMixin,
    ClassLandMixin,
    EffectMixin,
    ItemSetMixin,
    FlorensiaModelMixin,
):
    level_land = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Land level required to use the weapon",
        info=ColumnInfo(key="LevelLand"),
    )

    level_sea = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Land sea required to use the weapon",
        info=ColumnInfo(key="LevelSea"),
    )

    physical_defense = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Physical defense of armor piece",
        info=ColumnInfo(key="PhysicalDefense"),
    )

    magical_defense = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Magical defense of armor piece",
        info=ColumnInfo(key="MagicDefense"),
    )
