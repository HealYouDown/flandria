import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import ActorMixin
from src.updater.schema import LoaderInfo


class Npc(Base, ActorMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=[
                "s_MerchantChar.bin",
                "s_GuardChar.bin",
                "s_CitizenChar.bin",
            ],
            client_files=[
                "c_MerchantCharRes.bin",
                "c_GuardCharRes.bin",
                "c_CitizenCharRes.bin",
            ],
            string_files=[
                "MerchantCharStr.dat",
                "GuardCharStr.dat",
                "CitizenCharStr.dat",
            ],
        ),
    )

    positions = orm.relationship(
        "NpcPosition",
        viewonly=True,
        uselist=True,
    )

    quests = orm.relationship(
        "Quest",
        foreign_keys="Quest.start_npc_code",
        viewonly=True,
        uselist=True,
    )

    store_items = orm.relationship(
        "NpcStoreItem",
        viewonly=True,
        uselist=True,
    )
