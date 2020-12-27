from sqlalchemy import Enum, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.enums import Gender
from webapp.models.mixins import BaseMixin, BonusMixin


class ExtraEquipmentMixin(BaseMixin, BonusMixin):
    @declared_attr
    def gender(cls):
        return CustomColumn(
            Enum(Gender), nullable=False, mapper_key="사용성별",
            transform=lambda val: Gender(val))

    @declared_attr
    def class_land(cls):
        return CustomColumn(
            String(8), nullable=False, mapper_key="사용직업",
            # Accessories have "WPENS"  (P = Pirate?) instead
            # of just WENS. To keep it the same and allow for
            # easier filtering later, WPENS is exchanged with
            # WENS.
            transform=(lambda v: v if v != "WPENS" else "WENS"))

    @declared_attr
    def level_land(cls):
        return CustomColumn(Integer, nullable=False, mapper_key="육상LV")

    @declared_attr
    def level_sea(cls):
        return CustomColumn(Integer, nullable=False, mapper_key="해상LV")

    def to_dict(self, minimal: bool = False) -> dict:
        return {
            **BaseMixin.to_dict(self, minimal),
            **BonusMixin.to_dict(self),
            "gender": self.gender.to_dict(),
            "class_land": self.class_land,
            "level_land": self.level_land,
            "level_sea": self.level_sea,
        }
