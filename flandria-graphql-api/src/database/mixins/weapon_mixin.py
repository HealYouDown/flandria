import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import ItemFlag
from src.updater.schema import ColumnInfo
from src.updater.transforms import ms_to_seconds

from .base_mixin import BaseMixin
from .class_land_mixin import ClassLandMixin
from .effect_mixin import EffectMixin
from .florensia_model_mixin import FlorensiaModelMixin
from .item_set_mixin import ItemSetMixin
from .upgrade_rule_mixin import UpgradeRuleMixin


class WeaponMixin(
    BaseMixin,
    ClassLandMixin,
    EffectMixin,
    ItemSetMixin,
    UpgradeRuleMixin,
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

    minimum_physical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Minimum physical damage of the weapon",
        info=ColumnInfo(key="MinPhysicalAttack"),
    )

    maximum_physical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Maximum physical damage of the weapon",
        info=ColumnInfo(key="MaxPhysicalAttack"),
    )

    minimum_magical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Minimum magical damage of the weapon",
        info=ColumnInfo(key="MinMagicAttack"),
    )

    maximum_magical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Maximum magical damage of the weapon",
        info=ColumnInfo(key="MaxMagicAttack"),
    )

    attack_speed = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Attack speed of the weapon in seconds",
        info=ColumnInfo(key="AttackSpeed", transforms=[ms_to_seconds]),
    )

    attack_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Attack range of the weapon in meters",
        info=ColumnInfo(key="MaxAttackDistance"),
    )

    item_flag = orm.mapped_column(
        sa.Enum(ItemFlag),
        nullable=False,
        doc="Item flag type like 'Event' or 'Cash'",
        info=ColumnInfo(
            key="ItemType",
            transforms=[
                lambda v: ItemFlag(v),
            ],
        ),
    )
