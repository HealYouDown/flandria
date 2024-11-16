import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class UpgradeCrystal(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_UpgradeMustItem.bin"],
            client_files=["c_UpgradeMustItemRes.bin"],
            string_files=["UpgradeMustItemStr.dat"],
            description_files=["UpgradeMustItemDesc.dat"],
        ),
        include_in_itemlist=True,
    )

    description = orm.mapped_column(
        sa.Text,
        nullable=False,
        doc="Item description",
        info=ColumnInfo.description(),
    )
