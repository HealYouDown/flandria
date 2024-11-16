import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import EffectMixin
from src.updater import strategies
from src.updater.schema import LoaderInfo


class UpgradeRule(Base, EffectMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_UpgradeRule.bin"],
        ),
        loader_strategy=strategies.upgrade_rule,
    )

    code = orm.mapped_column(
        sa.String(32),
        primary_key=True,
        doc="Code for each upgrade level object",
    )
    base_code = orm.mapped_column(
        sa.String(32),
        nullable=False,
        index=True,
        doc="Base code (0th skill level) which is used for linking",
    )
    level = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Upgrade level",
    )
    cost = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Cost for each upgrade try",
    )
