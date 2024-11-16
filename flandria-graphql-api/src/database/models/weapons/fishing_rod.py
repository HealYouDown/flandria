from src.database.base import Base
from src.database.mixins import WeaponMixin
from src.updater.schema import LoaderInfo

EXCLUDE_CODES = [
    "fiyang000",
    "fiyang001",
    "fiyang002",
    "fiyang003",
    "fiyang004",
    "fiyang005",
    "fiyang006",
    "fiyang007",
    "fiyang008",
    "fiyang009",
    "fiyang010",
    "fiyang011",
    "fiyang012",
    "fiyang013",
    "fiyang014",
    "fiyang015",
    "fiyang016",
    "fiyang017",
]


class FishingRod(Base, WeaponMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_FishingItem.bin"],
            client_files=["c_FishingItemRes.bin"],
            string_files=["FishingItemStr.dat"],
        ),
        include_in_itemlist=True,
        row_filters=[lambda row: row["코드"] not in EXCLUDE_CODES],
    )
