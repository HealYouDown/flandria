from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import LoaderInfo


class FishingBait(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_BaitItem.bin"],
            client_files=["c_BaitItemRes.bin"],
            string_files=["BaitItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
