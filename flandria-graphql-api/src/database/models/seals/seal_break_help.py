import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class SealBreakHelp(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_SealHelpBreakItem.bin"],
            client_files=["c_SealHelpBreakItemRes.bin"],
            string_files=["SealHelpBreakItemStr.dat"],
            description_files=["SealHelpBreakItemDesc.dat"],
        ),
        include_in_itemlist=True,
    )

    description = orm.mapped_column(
        sa.Text,
        nullable=False,
        doc="Item description",
        info=ColumnInfo.description(),
    )
