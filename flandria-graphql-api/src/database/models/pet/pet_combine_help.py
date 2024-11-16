import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class PetCombineHelp(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_PetCombineHelpItem.bin"],
            client_files=["c_PetCombineHelpItemRes.bin"],
            string_files=["PetCombineHelpItemStr.dat"],
        ),
        include_in_itemlist=True,
    )

    value = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Value of the pet combine help item in percent",
        info=ColumnInfo(
            key="성공확률보정",
            transforms=[lambda v: v / 100],
        ),
    )
