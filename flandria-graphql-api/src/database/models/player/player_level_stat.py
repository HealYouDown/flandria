import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import BaseClassType
from src.database.base import Base


class PlayerLevelStat(Base):
    """Stores accumulated stats data for each level."""

    __table_args__ = (sa.PrimaryKeyConstraint("base_class", "level"),)

    base_class = orm.mapped_column(sa.Enum(BaseClassType), nullable=False)
    level = orm.mapped_column(sa.Integer, nullable=False)

    max_hp = orm.mapped_column(sa.Integer, nullable=False)
    max_mp = orm.mapped_column(sa.Integer, nullable=False)
    avoidance = orm.mapped_column(sa.Integer, nullable=False)

    melee_min_attack = orm.mapped_column(sa.Integer, nullable=False)
    melee_max_attack = orm.mapped_column(sa.Integer, nullable=False)
    melee_hitrate = orm.mapped_column(sa.Integer, nullable=False)
    melee_critical_rate = orm.mapped_column(sa.Integer, nullable=False)

    range_min_attack = orm.mapped_column(sa.Integer, nullable=False)
    range_max_attack = orm.mapped_column(sa.Integer, nullable=False)
    range_hitrate = orm.mapped_column(sa.Integer, nullable=False)
    range_critical_rate = orm.mapped_column(sa.Integer, nullable=False)

    magic_min_attack = orm.mapped_column(sa.Integer, nullable=False)
    magic_max_attack = orm.mapped_column(sa.Integer, nullable=False)
    magic_hitrate = orm.mapped_column(sa.Integer, nullable=False)
    magic_critical_rate = orm.mapped_column(sa.Integer, nullable=False)
