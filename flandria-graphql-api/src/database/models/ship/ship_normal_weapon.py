from src.database.base import Base
from src.database.mixins import ShipBaseMixin
from src.updater.schema import LoaderInfo


class ShipNormalWeapon(Base, ShipBaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ShipNWeaponItem.bin"],
            client_files=["c_ShipNWeaponItemRes.bin"],
            string_files=["ShipNWeaponItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
