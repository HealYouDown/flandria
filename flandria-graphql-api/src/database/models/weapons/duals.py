from src.database.base import Base
from src.database.mixins import WeaponMixin
from src.updater.schema import LoaderInfo


class Duals(Base, WeaponMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_GunItem.bin"],
            client_files=["c_GunItemRes.bin"],
            string_files=["GunItemStr.dat"],
        ),
        row_filters=[lambda row: row["무기타입"] == "P"],
        include_in_itemlist=True,
    )
