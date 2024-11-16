from src.database.base import Base
from src.database.mixins import ArmorMixin, UpgradeRuleMixin
from src.updater.schema import LoaderInfo


class Coat(Base, ArmorMixin, UpgradeRuleMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_UpperItem.bin"],
            client_files=["c_UpperItemRes.bin"],
            string_files=["UpperItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
