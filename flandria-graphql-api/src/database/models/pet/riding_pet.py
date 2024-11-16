import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class RidingPet(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_RidingPetItem.bin"],
            client_files=["c_RidingpetItemRes.bin"],
            string_files=["RidingpetItemStr.dat"],
            description_files=["LandItemSkillActionDesc.dat"],
        ),
        include_in_itemlist=True,
    )

    description = orm.mapped_column(
        sa.Text,
        nullable=False,
        doc="Description for the riding pet",
        info=ColumnInfo.description("스킬코드"),
    )
