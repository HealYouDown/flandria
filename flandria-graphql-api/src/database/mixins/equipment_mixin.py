import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import Gender, ItemFlag
from src.updater.schema import ColumnInfo

from .base_mixin import BaseMixin
from .class_land_mixin import ClassLandMixin
from .effect_mixin import EffectMixin
from .item_set_mixin import ItemSetMixin


class EquipmentMixin(BaseMixin, ClassLandMixin, EffectMixin, ItemSetMixin):
    gender = orm.mapped_column(
        sa.Enum(Gender),
        nullable=False,
        doc="Required gender for the item",
        info=ColumnInfo(
            key="사용성별",
            transforms=[lambda v: Gender(v)],
        ),
    )
    level_land = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Required level on land",
        info=ColumnInfo(key="육상LV"),
    )
    level_sea = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Required level on sea",
        info=ColumnInfo(key="해상LV"),
    )
    item_flag = orm.mapped_column(
        sa.Enum(ItemFlag),
        nullable=False,
        doc="Item type flag like Event or Cash",
        info=ColumnInfo(
            key="타입코드",
            transforms=[lambda v: ItemFlag(v)],
        ),
    )
