from src.database.base import Base
from src.database.mixins import ShipBaseMixin
from src.updater.schema import LoaderInfo


class ShipFront(Base, ShipBaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShipFrontItem.bin"],
            client_files=["c_ShipFrontItemRes.bin"],
            string_files=["ShipFrontItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
