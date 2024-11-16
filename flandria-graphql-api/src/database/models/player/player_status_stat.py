import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import BaseClassType, StatType
from src.database.base import Base


class PlayerStatusStat(Base):
    __table_args__ = (
        sa.PrimaryKeyConstraint("base_class", "point_level", "stat_type"),
    )

    base_class = orm.mapped_column(sa.Enum(BaseClassType), nullable=False)
    point_level = orm.mapped_column(sa.Integer, nullable=False)
    stat_type = orm.mapped_column(sa.Enum(StatType), nullable=False)

    # Increments are relative to level stats
    # In the end, to get the total stat, we calculate level stats + status stats
    max_hp_increment = orm.mapped_column(sa.Integer, nullable=False)
    max_mp_increment = orm.mapped_column(sa.Integer, nullable=False)
    avoidance_increment = orm.mapped_column(sa.Integer, nullable=False)

    melee_min_attack_increment = orm.mapped_column(sa.Integer, nullable=False)
    melee_max_attack_increment = orm.mapped_column(sa.Integer, nullable=False)
    melee_hitrate_increment = orm.mapped_column(sa.Integer, nullable=False)
    melee_critical_rate_increment = orm.mapped_column(sa.Integer, nullable=False)

    range_min_attack_increment = orm.mapped_column(sa.Integer, nullable=False)
    range_max_attack_increment = orm.mapped_column(sa.Integer, nullable=False)
    range_hitrate_increment = orm.mapped_column(sa.Integer, nullable=False)
    range_critical_rate_increment = orm.mapped_column(sa.Integer, nullable=False)

    magic_min_attack_increment = orm.mapped_column(sa.Integer, nullable=False)
    magic_max_attack_increment = orm.mapped_column(sa.Integer, nullable=False)
    magic_hitrate_increment = orm.mapped_column(sa.Integer, nullable=False)
    magic_critical_rate_increment = orm.mapped_column(sa.Integer, nullable=False)
