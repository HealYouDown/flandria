from src.database.base import Base
from src.database.mixins import ShipBaseMixin
from src.updater.schema import LoaderInfo


class ShipSpecialWeapon(Base, ShipBaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShipCWeaponItem.bin"],
            client_files=["c_ShipCWeaponItemRes.bin"],
            string_files=["ShipCWeaponItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
