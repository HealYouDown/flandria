import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import EffectCode
from src.database.base import Base


class Effect(Base):
    index = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    ref_code = orm.mapped_column(
        sa.String(32),
        nullable=False,
        index=True,
    )
    effect_code = orm.mapped_column(
        sa.Enum(EffectCode),
        nullable=False,
        doc="Effect code",
    )
    operator = orm.mapped_column(
        sa.String(4),
        nullable=False,
        doc="Effect operator (+, *, -)",
    )
    value = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Effect value",
    )
