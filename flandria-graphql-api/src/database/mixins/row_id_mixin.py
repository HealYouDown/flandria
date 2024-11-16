import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.updater.schema import ColumnInfo


class RowIDMixin:
    """Adds a row_id column to the model.

    Used to sort by "added" to the game.
    """

    row_id = orm.mapped_column(
        sa.Integer,
        index=True,
        info=ColumnInfo(key="row_id"),
        nullable=False,
    )
