from src.database.base import Base
from src.database.mixins import WeaponMixin
from src.updater.schema import LoaderInfo


class OneHandedSword(Base, WeaponMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_KnifeItem.bin"],
            client_files=["c_KnifeItemRes.bin"],
            string_files=["KnifeItemStr.dat"],
        ),
        row_filters=[lambda row: row["무기타입"] == "S"],
        include_in_itemlist=True,
    )
