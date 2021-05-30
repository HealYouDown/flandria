
from database_updater.conversions import convert_integer
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declared_attr
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.mixins import BaseMixin


class ShipBaseMixin(BaseMixin):
    @declared_attr
    def npc_price_tuning(cls):
        return CustomColumn(Integer, mapper_key="튜닝가격",
                            nullable=False, transform=convert_integer)

    @declared_attr
    def class_sea(cls):
        return CustomColumn(String(255), nullable=False, mapper_key="클래스")

    @declared_attr
    def level_sea(cls):
        return CustomColumn(Integer, nullable=False, mapper_key="해상LV")

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "class_sea": self.class_sea,
            "level_sea": self.level_sea,
            "npc_tuning_price": self.npc_price_tuning
        }
