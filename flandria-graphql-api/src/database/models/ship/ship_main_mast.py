from src.database.base import Base
from src.database.mixins import ShipBaseMixin
from src.updater.schema import LoaderInfo


class ShipMainMast(Base, ShipBaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShipMainMastItem.bin"],
            client_files=["c_ShipMainMastItemRes.bin"],
            string_files=["ShipMainMastItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
