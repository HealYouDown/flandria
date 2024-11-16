from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import ItemGrade
from src.updater.schema import ColumnInfo
from src.updater.transforms import value_if_not_equal

from .row_id_mixin import RowIDMixin

if TYPE_CHECKING:
    pass


class BaseMixin(RowIDMixin):
    code = orm.mapped_column(
        sa.String(32),
        primary_key=True,
        doc="Code of the item",
        info=ColumnInfo.code(),
    )

    name = orm.mapped_column(
        sa.String(256),
        nullable=False,
        doc="Name of the item",
        info=ColumnInfo.name(),
    )

    icon = orm.mapped_column(
        sa.String(16),
        nullable=False,
        doc="Icon of the item",
        info=ColumnInfo.icon(),
    )

    is_tradable = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the item can be traded",
        info=ColumnInfo(key="교환가능"),
    )

    is_destroyable = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the item can be destroyed",
        info=ColumnInfo(key="버림가능"),
    )

    @orm.declared_attr
    def is_sellable(cls):
        info = ColumnInfo(key="매매가능")
        tablename: str = cls.__tablename__  # type: ignore
        if tablename in {"quest_item"}:
            info = {}

        return orm.mapped_column(
            sa.Boolean,
            nullable=False,
            doc="Whether the item can be sold",
            default=False,
            info=info,
        )

    @orm.declared_attr
    def is_storageable(cls):
        info = ColumnInfo(key="보관가능")
        tablename: str = cls.__tablename__  # type: ignore

        if tablename in {"quest_item"}:
            info = {}

        return orm.mapped_column(
            sa.Boolean,
            nullable=False,
            doc="Whether the item can be stored",
            default=False,
            info=info,
        )

    @orm.declared_attr
    def grade(cls):
        info = ColumnInfo(
            key="가치",
            transforms=[lambda v: ItemGrade(v)],
        )

        # Some tables do not have a grade value, so they default to 1
        tablename: str = cls.__tablename__  # type: ignore
        if tablename in {
            "ship_shell",
            "bullet",
            "consumable",
            "fishing_bait",
            "fishing_material",
            "fusion_help",
            "pet",
            "riding_pet",
            "pet_combine_help",
            "pet_combine_stone",
            "pet_skill_stone",
            "quest_item",
            "upgrade_stone",
            "upgrade_help",
            "upgrade_crystal",
            "seal_break_help",
        }:
            info = {}

        return orm.mapped_column(
            sa.Enum(ItemGrade),
            nullable=False,
            doc="Grade of the item",
            info=info,
            default=ItemGrade.BLUE,
        )

    @orm.declared_attr
    def duration(cls):
        info = ColumnInfo(
            key="기간제타임",
            transforms=[lambda v: value_if_not_equal(v, -1)],
        )
        tablename: str = cls.__tablename__  # type: ignore
        if tablename in {"essence", "random_box"}:
            info = {}

        return orm.mapped_column(
            sa.Integer,
            nullable=True,
            doc="Duration of the item in minutes",
            info=info,
            default=None,
        )

    @orm.declared_attr
    def stack_size(cls):
        # Bait, bullets and ship shells have a different name for stack size
        key = "중복가능수"
        tablename: str = cls.__tablename__  # type: ignore

        if tablename in {"fishing_bait", "ship_shell", "bullet"}:
            key = "최대중복개수"
        # Some tables don't have a stack size, so the default (of 1) is used instead
        elif tablename in {
            "ship_anchor",
            "ship_body",
            "ship_figure",
            "ship_flag",
            "ship_front",
            "ship_head_mast",
            "ship_main_mast",
            "ship_magic_stone",
            "ship_normal_weapon",
            "ship_special_weapon",
            "pet_skill_stone",
            "production_book",
            "quest_scroll",
            "skill_book",
        }:
            key = None

        info = ColumnInfo(key=key) if key is not None else {}

        return orm.mapped_column(
            sa.Integer,
            nullable=False,
            doc="Stack size of the item",
            info=info,
            default=1,
        )

    @orm.declared_attr
    def npc_buy_price(cls):
        key = "판매가격"
        tablename: str = cls.__tablename__  # type: ignore

        if tablename in {
            "ship_anchor",
            "ship_body",
            "ship_figure",
            "ship_flag",
            "ship_front",
            "ship_head_mast",
            "ship_magic_stone",
            "ship_main_mast",
            "ship_normal_weapon",
            "ship_special_weapon",
        }:
            key = "기준가격"
        elif tablename == "quest_item":
            key = None

        info = ColumnInfo(key=key) if key is not None else {}

        return orm.mapped_column(
            sa.Float,
            nullable=False,
            doc="Price for which you can buy the item from NPCs",
            info=info,
            default=0,
        )

    npc_sell_price = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Price for which you can sell the item to NPCs",
        info=ColumnInfo(key="처분가격"),
    )
