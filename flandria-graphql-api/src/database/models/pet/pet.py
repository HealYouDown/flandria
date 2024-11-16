import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo
from src.updater.transforms import value_if_not_equal


class Pet(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_PetItem.bin"],
            client_files=["c_PetItemRes.bin"],
            string_files=["PetItemStr.dat"],
        ),
        include_in_itemlist=True,
    )

    initial_courage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Courage value the pet starts with",
        info=ColumnInfo(
            key="용기",
            transforms=[lambda v: value_if_not_equal(v, -1, 0)],
        ),
    )
    initial_patience = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Patience value the pet starts with",
        info=ColumnInfo(
            key="인내",
            transforms=[lambda v: value_if_not_equal(v, -1, 0)],
        ),
    )
    initial_wisdom = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Wisdom value the pet starts with",
        info=ColumnInfo(
            key="인내",
            transforms=[lambda v: value_if_not_equal(v, -1, 0)],
        ),
    )
    is_unlimited = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the pet needs pocketwatches",
        info=ColumnInfo(
            key="펫봉인타임",
            transforms=[lambda v: v == -1],
        ),
    )

    # TODO: Pet Stats
