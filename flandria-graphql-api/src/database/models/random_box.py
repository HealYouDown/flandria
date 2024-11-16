import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater import strategies
from src.updater.schema import ColumnInfo, LoaderInfo
from src.updater.transforms import value_if_not_equal


class RandomBoxReward(Base):
    # Some randomboxes have the same item multiple times,
    # so we need an autoincrement pk :'(
    index = orm.mapped_column(
        sa.Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    random_box_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("random_box.code"),
        index=True,
        nullable=False,
        doc="Code of the random box",
    )
    reward_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_list.code"),
        index=True,
        nullable=False,
        doc="Reward item code",
    )
    quantity = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Quantity of the reward",
    )
    probability = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Probability (0-1.0) for the reward",
    )
    item = orm.relationship(
        "ItemList",
        foreign_keys=[reward_code],
        uselist=False,
        viewonly=True,
        doc="The item",
    )


class RandomBox(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_RandomBoxItem.bin"],
            client_files=["c_RandomBoxItemRes.bin"],
            string_files=["RandomBoxItemStr.dat"],
        ),
        loader_strategy=strategies.random_box,
        include_in_itemlist=True,
    )

    level_land = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Land level required to open the randombox",
        info=ColumnInfo(
            key="육상LV",
            transforms=[lambda v: value_if_not_equal(v, -1, 1)],
        ),
    )
    level_sea = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Sea level required to open the randombox",
        info=ColumnInfo(
            key="해상LV",
            transforms=[lambda v: value_if_not_equal(v, -1, 1)],
        ),
    )
    rewards = orm.relationship(
        "RandomBoxReward",
        uselist=True,
        cascade="all, delete-orphan",
    )
