import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo

# There are lots of unused upgrade stones that just clutter the view,
# so we remove them. They aren't used for anything anyways
EXCLUDE_CODES = [
    "usnew0001",
    "usnew0002",
    "usnew0003",
    "usnew0004",
    "usnew0005",
    "usnew0006",
    "usnew0007",
    "usnew0008",
    "usnew0009",
    "usnew0010",
    "usnew0011",
    "usnew0012",
    "usnew0013",
    "usnew0014",
    "usnew0015",
    "usnew0016",
    "usnew0017",
    "usnew0018",
    "usnew0019",
    "usnew0020",
    "usnew0021",
    "usnew0022",
    "usnew0023",
    "usnew0024",
    "usnew0025",
    "usnew0026",
    "usnew0027",
    "usnew0028",
    "usnew0029",
    "usnew0030",
    "usnew0031",
    "usnew0032",
    "usnew0033",
    "usnew0034",
    "usnew0035",
    "usnew0036",
    "usnew0037",
    "usnew0038",
    "usnew0039",
    "usnew0040",
    "usnew0041",
    "usnew0042",
    "usnew0043",
    "usnew0044",
    "usnew0045",
]


class UpgradeStone(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_UpgradeStoneItem.bin"],
            client_files=["c_UpgradeStoneItemRes.bin"],
            string_files=["UpgradeStoneItemStr.dat"],
            description_files=["UpgradeStoneItemDesc.dat"],
        ),
        row_filters=[lambda row: row["코드"] not in EXCLUDE_CODES],
        include_in_itemlist=True,
    )

    description = orm.mapped_column(
        sa.Text,
        nullable=False,
        doc="Item description",
        info=ColumnInfo.description(),
    )
