import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.updater.schema import ColumnInfo


class ItemSetMixin:
    item_set_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_set.code"),
        index=True,
        nullable=True,
        doc="Code of the item set",
        info=ColumnInfo(key="세트코드"),
    )

    @orm.declared_attr
    def item_set(cls):
        return orm.relationship(
            "ItemSet",
            foreign_keys=[cls.item_set_code],
            uselist=False,
            viewonly=True,
        )
