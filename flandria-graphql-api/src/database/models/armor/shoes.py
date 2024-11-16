from src.database.base import Base
from src.database.mixins import ArmorMixin, UpgradeRuleMixin
from src.updater.schema import LoaderInfo


class Shoes(Base, ArmorMixin, UpgradeRuleMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShoeItem.bin"],
            client_files=["c_ShoeItemRes.bin"],
            string_files=["ShoeItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
