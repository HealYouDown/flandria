import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class EssenceHelp(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ArtifactManagItem.bin"],
            client_files=["c_ArtifactManagItemRes.bin"],
            string_files=["ArtifactManagItemStr.dat"],
            description_files=["ArtifactManagItemDesc.dat"],
        ),
        include_in_itemlist=True,
    )

    description = orm.mapped_column(
        sa.Text,
        nullable=True,
        doc="Description of the item",
        info=ColumnInfo.description(),
    )
