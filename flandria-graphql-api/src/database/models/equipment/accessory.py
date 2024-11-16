import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import AccessoryType
from src.database.base import Base
from src.database.mixins import EquipmentMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class Accessory(Base, EquipmentMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_AccessoryItem.bin"],
            client_files=["c_AccessoryItemRes.bin"],
            string_files=["AccessoryItemStr.dat"],
        ),
        include_in_itemlist=True,
    )

    accessory_type = orm.mapped_column(
        sa.Enum(AccessoryType),
        nullable=False,
        doc="Type of the accessory (e.g. Ring, Necklace or Earrings)",
        info=ColumnInfo(
            key="구분코드",
            transforms=[lambda v: AccessoryType(v)],
        ),
    )
