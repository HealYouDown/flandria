from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import LoaderInfo


class FishingMaterial(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_FishMaterialItem.bin"],
            client_files=["c_FishMaterialItemRes.bin"],
            string_files=["FishMaterialItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
