import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import SecondJobType
from src.database.base import Base
from src.database.mixins import RowIDMixin
from src.updater import strategies
from src.updater.schema import ColumnInfo, LoaderInfo


class ProductionRequiredMaterial(Base):
    __table_args__ = (sa.PrimaryKeyConstraint("production_code", "material_code"),)

    production_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("production.code"),
        nullable=False,
        doc="Production code",
    )
    material_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_list.code"),
        index=True,
        nullable=False,
        doc="Material item code",
    )
    quantity = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Quantity required",
    )
    item = orm.relationship(
        "ItemList",
        foreign_keys=[material_code],
        uselist=False,
        viewonly=True,
        doc="The item object",
    )


class Production(Base, RowIDMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_Production.bin"],
        ),
        loader_strategy=strategies.production,
    )

    code = orm.mapped_column(
        sa.String(32),
        nullable=False,
        primary_key=True,
        doc="Code of the item",
        info=ColumnInfo(key="코드"),
    )
    type = orm.mapped_column(
        sa.Enum(SecondJobType),
        nullable=False,
        info=ColumnInfo(
            key="타입",
            transforms=[lambda v: SecondJobType(v)],
        ),
        doc="Second job type",
    )
    points_required = orm.mapped_column(
        sa.Integer,
        nullable=False,
        info=ColumnInfo(key="필요숙련도"),
        doc="The required points to craft the item",
    )
    result_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_list.code"),
        index=True,
        nullable=False,
        info=ColumnInfo(key="결과물코드"),
        doc="Result code for the item that is crafted",
    )
    result_item = orm.relationship(
        "ItemList",
        foreign_keys=[result_code],
        uselist=False,
        viewonly=True,
        doc="The result item",
    )
    result_quantity = orm.mapped_column(
        sa.Integer,
        nullable=False,
        info=ColumnInfo(key="결과물수량"),
        doc="Quantity of the result item",
    )
    required_materials = orm.relationship(
        "ProductionRequiredMaterial",
        uselist=True,
        viewonly=True,
    )
