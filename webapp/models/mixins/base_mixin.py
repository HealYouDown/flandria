from database_updater.conversions import convert_integer
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.transforms import MAX_INT


class BaseMixin:
    @declared_attr
    def index(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def code(cls):
        return CustomColumn(String(32), primary_key=True, nullable=False,
                            mapper_key="코드")

    @declared_attr
    def name(cls):
        return CustomColumn(String(256), nullable=False, mapper_key="_name")

    @declared_attr
    def icon(cls):
        return CustomColumn(String(32), nullable=False, mapper_key="_icon")

    @declared_attr
    def tradable(cls):
        return CustomColumn(Boolean, nullable=False, mapper_key="교환가능")

    @declared_attr
    def destroyable(cls):
        return CustomColumn(Boolean, nullable=False, mapper_key="버림가능")

    @declared_attr
    def sellable(cls):
        return CustomColumn(Boolean, nullable=False, mapper_key="매매가능")

    @declared_attr
    def storagable(cls):
        return CustomColumn(Boolean, nullable=False, mapper_key="보관가능")

    @declared_attr
    def rare_grade(cls):
        return CustomColumn(Integer, nullable=False, default=0,
                            mapper_key="가치")

    @declared_attr
    def duration(cls):
        return CustomColumn(
            Integer, mapper_key="기간제타임",
            # duration is either None or the time in minutes.
            transform=lambda v: v if v != MAX_INT else None)

    @declared_attr
    def stack_size(cls):
        # Baits and Shells have another attribute instead of stack
        # size. Means the same though...
        key = ("최대중복개수" if cls.__tablename__ in ["bait", "ship_shell"]
               else "중복가능수")

        return CustomColumn(Integer, nullable=False, mapper_key=key,
                            default=1)

    @declared_attr
    def npc_buy_price(cls):
        # Ship tables have a different key for buy price
        if cls.__tablename__ in ["ship_anchor", "ship_body", "ship_figure",
                                 "ship_flag", "ship_front", "ship_head_mast",
                                 "ship_magic_stone", "ship_main_mast",
                                 "ship_normal_weapon", "ship_special_weapon"]:
            key = "기준가격"
        else:
            key = "판매가격"
        return CustomColumn(Integer, nullable=False, mapper_key=key,
                            transform=convert_integer)

    @declared_attr
    def npc_sell_price(cls):
        return CustomColumn(Integer, nullable=False, mapper_key="처분가격",
                            transform=convert_integer)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            "code": self.code,
            "name": self.name,
            "icon": self.icon,
            "rare_grade": self.rare_grade,
            "duration": self.duration,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "tradable": self.tradable,
            "destroyable": self.destroyable,
            "sellable": self.sellable,
            "storagable": self.storagable,
            "stack_size": self.stack_size,
            "npc_buy_price": self.npc_buy_price,
            "npc_sell_price": self.npc_sell_price,
        }
