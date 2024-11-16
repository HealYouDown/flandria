import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class PetCombineStone(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_PetCombineItem.bin"],
            client_files=["c_PetCombineItemRes.bin"],
            string_files=["PetCombineItemStr.dat"],
        ),
        include_in_itemlist=True,
    )

    min_value = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Minimum increment value (0 - 10.000)",
        info=ColumnInfo(key="성공확률보정"),
    )
    max_value = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Maximum increment value (0 - 10.000)",
        info=ColumnInfo(key="증가최대값"),
    )
