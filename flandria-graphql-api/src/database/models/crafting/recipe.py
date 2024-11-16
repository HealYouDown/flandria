import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import BaseMixin
from src.updater import strategies
from src.updater.schema import ColumnInfo, LoaderInfo


class RecipeRequiredMaterial(Base):
    __table_args__ = (sa.PrimaryKeyConstraint("recipe_code", "material_code"),)

    recipe_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("recipe.code"),
        nullable=False,
        doc="Recipe code",
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
        viewonly=True,
        uselist=False,
        doc="The item object",
    )


class Recipe(Base, BaseMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_RecipeItem.bin"],
            client_files=["c_RecipeItemRes.bin"],
            string_files=["RecipeItemStr.dat"],
        ),
        loader_strategy=strategies.recipe,
        include_in_itemlist=True,
    )

    result_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_list.code"),
        nullable=False,
        index=True,
        info=ColumnInfo(key="결과물코드"),
        doc="Result code for the item that is crafted",
    )
    result_quantity = orm.mapped_column(
        sa.Integer,
        nullable=False,
        info=ColumnInfo(key="결과물수량"),
        doc="Quantity of the result item",
    )
    result_item = orm.relationship(
        "ItemList",
        uselist=False,
        viewonly=True,
        foreign_keys=[result_code],
        doc="The result item",
    )
    required_materials = orm.relationship(
        "RecipeRequiredMaterial",
        uselist=True,
        viewonly=True,
    )
