from src.database.base import Base
from src.database.mixins import ShipBaseMixin
from src.updater.schema import LoaderInfo


class ShipFlag(Base, ShipBaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShipFlagItem.bin"],
            client_files=["c_ShipFlagItemRes.bin"],
            string_files=["ShipFlagItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
