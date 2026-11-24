import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.updater import strategies
from src.updater.schema import LoaderInfo


class NpcExchangeMaterial(Base):
    index = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    exchange_index = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("npc_exchange_item.index"),
        index=True,
        nullable=False,
    )
    item_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_list.code"),
        index=True,
        nullable=False,
    )
    quantity = orm.mapped_column(sa.Integer, nullable=False)

    item = orm.relationship(
        "ItemList",
        foreign_keys=[item_code],
        uselist=False,
        viewonly=True,
    )


class NpcExchangeItem(Base):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            extra_files=["ExchangeData.xml", "Keyword_En.dat"],
        ),
        loader_strategy=strategies.npc_exchange_item,
    )

    # Set by the loader, so that materials can reference it
    index = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=False,
    )
    section_name = orm.mapped_column(
        sa.String(256),
        nullable=False,
        doc="Section name",
    )
    page_name = orm.mapped_column(
        sa.String(256),
        nullable=False,
        doc="Page name inside a section",
    )
    npc_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("npc.code"),
        index=True,
        nullable=False,
    )
    item_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_list.code"),
        index=True,
        nullable=False,
    )
    quantity = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Amount of the item you receive",
    )
    gelt = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Gelt required in addition to the materials",
    )

    item = orm.relationship(
        "ItemList",
        foreign_keys=[item_code],
        uselist=False,
        viewonly=True,
    )
    npc = orm.relationship(
        "Npc",
        foreign_keys=[npc_code],
        uselist=False,
        viewonly=True,
    )
    materials = orm.relationship(
        "NpcExchangeMaterial",
        uselist=True,
        viewonly=True,
    )
