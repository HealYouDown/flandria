import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class ShipShell(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShellItem.bin"],
            client_files=["c_ShellItemRes.bin"],
            string_files=["ShellItemStr.dat"],
        ),
        include_in_itemlist=True,
    )

    level_sea = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Sea level required to use",
        info=ColumnInfo(key="제한레벨"),
    )
    physical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Physical damage dealt",
        info=ColumnInfo(key="물공력"),
    )
    explosion_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Explosion radius in florensia units",
        info=ColumnInfo(key="폭발반경"),
    )
