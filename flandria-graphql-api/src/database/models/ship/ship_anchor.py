from src.database.base import Base
from src.database.mixins import ShipBaseMixin
from src.updater.schema import LoaderInfo


class ShipAnchor(Base, ShipBaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShipAnchorItem.bin"],
            client_files=["c_ShipAnchorItemRes.bin"],
            string_files=["ShipAnchorItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
