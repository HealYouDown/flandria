from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import LoaderInfo


class Material(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_StdMaterialItem.bin"],
            client_files=["c_StdMaterialItemRes.bin"],
            string_files=["StdMaterialItemStr.dat"],
        ),
        include_in_itemlist=True,
    )