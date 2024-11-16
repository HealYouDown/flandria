import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.updater.schema import ColumnInfo
from src.updater.transforms import ms_to_seconds

from .base_mixin import BaseMixin
from .class_sea_mixin import ClassSeaMixin
from .effect_mixin import EffectMixin


# TODO: SHIP TYPE: 타입: SMBG
# Ship type is most often in the name itself, so the
# field isn't that much needed
class ShipBaseMixin(BaseMixin, ClassSeaMixin, EffectMixin):
    npc_tune_price = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Price to tune this piece in the dock",
        info=ColumnInfo(key="튜닝가격"),
    )

    level_sea = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Required level on sea to use the ship piece",
        info=ColumnInfo(key="해상LV"),
    )

    guns_front = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Number of guns on the front",
        info=ColumnInfo(key="전포수"),
    )

    guns_side = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Number of guns on the side",
        info=ColumnInfo(key="측포수"),
    )

    crew_size = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Number of possible crew members",
        info=ColumnInfo(key="필요선원수"),
    )

    # What the fuck is the difference between physical defense and protection though?
    physical_defense = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Physical stat",
        info=ColumnInfo(key="물방력"),
    )

    protection = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Protection stat",
        info=ColumnInfo(key="방탄력"),
    )

    balance = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Balance stat",
        info=ColumnInfo(key="벨런스"),
    )

    dp = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Health points (DP)",
        info=ColumnInfo(key="HP"),
    )

    en = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Mana (EN)",
        info=ColumnInfo(key="EN"),
    )

    en_usage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="EN usage (weapons only)",
        info=ColumnInfo(key="EN소모"),
    )

    en_recovery = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Amount of EN restored per regeneration tick",
        info=ColumnInfo(key="EN회복"),
    )

    acceleration = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Acceleration stat in Florensia units/s",
        info=ColumnInfo(key="가속력"),
    )

    deceleration = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Deceleration stat in Florensia units/s",
        info=ColumnInfo(key="정선력"),
    )

    turning_power = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Turning power stat",
        info=ColumnInfo(key="선회력"),
    )

    favorable_wind = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Favorable wind stat",
        info=ColumnInfo(key="횡범성능"),
    )

    adverse_wind = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Adverse wind stat",
        info=ColumnInfo(key="종범성능"),
    )

    physical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Physical damage (of weapons)",
        info=ColumnInfo(key="공격력"),
    )

    weapon_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Weapon range in florensia units",
        info=ColumnInfo(key="최대거리"),
    )

    critical_chance = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Critical chance in % (0-1.0)",
        info=ColumnInfo(key="크리티컬", transforms=[lambda v: v / 100]),
    )

    reload_speed = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Reload speed in seconds",
        info=ColumnInfo(key="장전속도", transforms=[ms_to_seconds]),
    )

    hit_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Hit range in florensia units",
        info=ColumnInfo(key="집탄범위"),
    )
