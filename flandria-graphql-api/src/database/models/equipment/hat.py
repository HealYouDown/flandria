from src.database.base import Base
from src.database.mixins import EquipmentMixin, ExtraEquipmentModelMixin
from src.updater.schema import LoaderInfo


class Hat(Base, EquipmentMixin, ExtraEquipmentModelMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_HatItem.bin"],
            client_files=["c_HatItemRes.bin"],
            string_files=["HatItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
