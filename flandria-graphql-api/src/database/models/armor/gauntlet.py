from src.database.base import Base
from src.database.mixins import ArmorMixin, UpgradeRuleMixin
from src.updater.schema import LoaderInfo


class Gauntlet(Base, ArmorMixin, UpgradeRuleMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_GauntletItem.bin"],
            client_files=["c_GauntletItemRes.bin"],
            string_files=["GauntletItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
