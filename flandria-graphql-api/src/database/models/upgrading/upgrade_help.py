import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class UpgradeHelp(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_UpgradeHelpItem.bin"],
            client_files=["c_UpgradeHelpItemRes.bin"],
            string_files=["UpgradeHelpItemStr.dat"],
            description_files=["UpgradeHelpItemDesc.dat"],
        ),
        include_in_itemlist=True,
    )

    description = orm.mapped_column(
        sa.Text,
        nullable=True,
        doc="Item description",
        info=ColumnInfo.description(),
    )
