from src.database.base import Base
from src.database.mixins import ShipBaseMixin
from src.updater.schema import LoaderInfo


class ShipHeadMast(Base, ShipBaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShipHeadMastItem.bin"],
            client_files=["c_ShipHeadMastItemRes.bin"],
            string_files=["ShipHeadMastItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
