from typing import cast

import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class ProductionBook(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ProductBook.bin"],
            client_files=["c_ProductRes.bin"],
            string_files=["ProductStr.dat"],
        ),
        include_in_itemlist=True,
        row_filters=[
            # Filters out all essence production books, that weren't actually used
            # in the end.
            lambda row: not cast(str, row["대상코드"]).startswith("rbessc"),
        ],
    )

    production_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("production.code"),
        nullable=False,
        index=True,
        doc="Code for the production that is learned by using the book.",
        info=ColumnInfo(key="대상코드"),
    )
    production = orm.relationship(
        "Production",
        foreign_keys=[production_code],
        uselist=False,
        viewonly=True,
        doc="The production that belongs to the book",
    )
