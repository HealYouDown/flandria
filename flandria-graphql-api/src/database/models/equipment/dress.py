from src.database.base import Base
from src.database.mixins import EquipmentMixin, ExtraEquipmentModelMixin
from src.updater.schema import LoaderInfo


class Dress(Base, EquipmentMixin, ExtraEquipmentModelMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_CloakItem.bin"],
            client_files=["c_CloakItemRes.bin"],
            string_files=["CloakItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
