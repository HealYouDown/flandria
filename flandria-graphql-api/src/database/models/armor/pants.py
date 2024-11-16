from src.database.base import Base
from src.database.mixins import ArmorMixin, UpgradeRuleMixin
from src.updater.schema import LoaderInfo


class Pants(Base, ArmorMixin, UpgradeRuleMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_LowerItem.bin"],
            client_files=["c_LowerItemRes.bin"],
            string_files=["LowerItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
