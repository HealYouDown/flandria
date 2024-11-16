from src.database.base import Base
from src.database.mixins import WeaponMixin
from src.updater.schema import LoaderInfo


class Cariad(Base, WeaponMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_MagicBallItem.bin"],
            client_files=["c_MagicBallItemRes.bin"],
            string_files=["MagicBallItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
