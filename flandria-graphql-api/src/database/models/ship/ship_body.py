from src.database.base import Base
from src.database.mixins import ShipBaseMixin
from src.updater.schema import LoaderInfo


class ShipBody(Base, ShipBaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShipBodyItem.bin"],
            client_files=["c_ShipBodyItemRes.bin"],
            string_files=["ShipBodyItemStr.dat"],
        ),
        include_in_itemlist=True,
    )