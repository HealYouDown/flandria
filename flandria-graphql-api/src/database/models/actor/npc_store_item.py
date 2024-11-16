import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.updater import strategies
from src.updater.schema import LoaderInfo


class NpcStoreItem(Base):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            extra_files=["StoreData.xml", "Keyword_En.dat"],
        ),
        loader_strategy=strategies.npc_store_item,
    )

    index = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    section_name = orm.mapped_column(
        sa.String(256),
        nullable=False,
        doc="Section name",
    )
    page_name = orm.mapped_column(
        sa.String(256),
        doc="Page name inside a section",
        nullable=False,
    )
    npc_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("npc.code"),
        index=True,
        nullable=False,
    )
    # npc_class = orm.mapped_column(
    #     sa.Integer,
    #     doc="idk, 1 for everyone",
    #     nullable=False,
    # )
    item_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_list.code"),
        index=True,
        nullable=False,
    )

    item = orm.relationship(
        "ItemList",
        foreign_keys=[item_code],
        uselist=False,
        viewonly=True,
    )
