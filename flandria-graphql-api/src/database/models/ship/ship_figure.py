from src.database.base import Base
from src.database.mixins import ShipBaseMixin
from src.updater.schema import LoaderInfo


class ShipFigure(Base, ShipBaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShipFigureItem.bin"],
            client_files=["c_ShipFigureItemRes.bin"],
            string_files=["ShipFigureItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
