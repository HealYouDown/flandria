from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import LoaderInfo


class Bullet(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_BulletItem.bin"],
            client_files=["c_BulletItemRes.bin"],
            string_files=["BulletItemStr.dat"],
        ),
        include_in_itemlist=True,
    )
