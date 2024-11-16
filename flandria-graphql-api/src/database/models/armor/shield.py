from src.database.base import Base
from src.database.mixins import ArmorMixin
from src.updater.schema import LoaderInfo


class Shield(Base, ArmorMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShieldItem.bin"],
            client_files=["c_ShieldItemRes.bin"],
            string_files=["ShieldItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
