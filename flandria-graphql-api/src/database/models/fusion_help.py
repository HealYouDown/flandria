import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class FusionHelp(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_FusionHelpBreakItem.bin"],
            client_files=["c_FusionHelpRes.bin"],
            string_files=["FusionHelpStr.dat"],
            description_files=["FusionHelpBreakItemDesc.dat"],
        ),
        # Fusion items aren't ingame anymore, we just keep this model due to completeness
        include_in_itemlist=False,
    )

    description = orm.mapped_column(
        sa.Text,
        nullable=True,
        doc="Item description",
        info=ColumnInfo.description(),
    )
