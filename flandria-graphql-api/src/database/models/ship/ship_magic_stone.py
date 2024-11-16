from src.database.base import Base
from src.database.mixins import ShipBaseMixin
from src.updater.schema import LoaderInfo


class ShipMagicStone(Base, ShipBaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShipMagicStoneItem.bin"],
            client_files=["c_ShipMagicStoneItemRes.bin"],
            string_files=["ShipMagicStoneItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
