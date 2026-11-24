import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class SealExtend(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_SealExtendItem.bin"],
            client_files=["c_SealExtendItemRes.bin"],
            string_files=["SealExtendItemStr.dat"],
            description_files=["SealExtendItemDesc.dat"],
        ),
        include_in_itemlist=True,
    )

    description = orm.mapped_column(
        sa.Text,
        nullable=True,
        doc="Item description",
        info=ColumnInfo.description(),
    )
    is_random = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc=(
            "False: adds `seal_count` seals. True: rerolls the seal count to "
            "`min_seals` - `max_seals`. The result is capped at 5 seals and all seals end up closed."
        ),
        info=ColumnInfo(key="Mode", transforms=[lambda v: v == 1]),
    )
    seal_count = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Seals added to the item (only if not random)",
        info=ColumnInfo(key="SealCount"),
    )
    min_seals = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Lowest seal count the reroll can land on (only if random)",
        info=ColumnInfo(key="MinSeals"),
    )
    max_seals = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Highest seal count the reroll can land on (only if random)",
        info=ColumnInfo(key="MaxSeals"),
    )
    for_armor = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Usable on coats, pants, gloves and shoes",
        info=ColumnInfo(key="ForArmor"),
    )
    for_weapons = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Usable on weapons",
        info=ColumnInfo(key="ForWeapons"),
    )
    for_accessories = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Usable on accessories",
        info=ColumnInfo(key="ForAccessories"),
    )
    min_item_level = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Lowest required level of the target item",
        info=ColumnInfo(key="MinLv"),
    )
    max_item_level = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Highest required level of the target item",
        info=ColumnInfo(key="MaxLv"),
    )
