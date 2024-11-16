import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import ItemSetSlot
from src.database.base import Base
from src.database.mixins import EffectMixin
from src.updater import strategies
from src.updater.schema import LoaderInfo


class ItemSetItem(Base):
    __table_args__ = (sa.PrimaryKeyConstraint("set_code", "slot", "item_code"),)

    # There are some duplicates allowed for each set (even if they don't make sense)
    # SELECT
    #   set_code, name, item_code, slot
    # FROM item_set_item
    # JOIN item_set
    #   ON item_set.code = item_set_item.set_code
    # WHERE set_code IN (
    #   SELECT set_code FROM item_set_item GROUP BY item_code HAVING count(item_code) > 1
    # )

    set_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_set.code"),
        nullable=False,
        doc="Set code",
    )
    slot = orm.mapped_column(
        sa.Enum(ItemSetSlot),
        nullable=False,
        doc="Slot the item applies to for the set",
    )
    item_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_list.code"),
        index=True,
        doc="Item code",
        nullable=False,
    )
    item = orm.relationship(
        "ItemList",
        foreign_keys=[item_code],
        uselist=False,
        viewonly=True,
    )


# TODO: how to know how many set pieces are needed for x effect?
class ItemSet(Base, EffectMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_SetItemData.bin"],
            string_files=["SetNameStr.dat"],
        ),
        loader_strategy=strategies.item_set,
    )

    code = orm.mapped_column(
        sa.String(32),
        primary_key=True,
        doc="Set code",
    )
    name = orm.mapped_column(
        sa.String(128),
        nullable=False,
        doc="Name of the set",
    )
    items = orm.relationship(
        "ItemSetItem",
        uselist=True,
        viewonly=True,
    )
