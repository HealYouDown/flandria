import typing

from sqlalchemy import Enum, Float, String
from sqlalchemy.ext.declarative import declared_attr
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.enums import EffectCode
from webapp.models.transforms import MAX_INT, bonus_value_transform


class BonusMixin:
    # 1
    @declared_attr
    def bonus_1_code(cls):
        return CustomColumn(
            Enum(EffectCode), mapper_key="효과코드_1",
            transform=lambda v: EffectCode(v) if v != MAX_INT else None)

    @declared_attr
    def bonus_1_operator(cls):
        return CustomColumn(
            String(4), mapper_key="수치연산자_1",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def bonus_1_value(cls):
        return CustomColumn(
            Float, mapper_key="효과값_1",
            transform=bonus_value_transform)

    # 2
    @declared_attr
    def bonus_2_code(cls):
        return CustomColumn(
            Enum(EffectCode), mapper_key="효과코드_2",
            transform=lambda v: EffectCode(v) if v != MAX_INT else None)

    @declared_attr
    def bonus_2_operator(cls):
        return CustomColumn(
            String(4), mapper_key="수치연산자_2",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def bonus_2_value(cls):
        return CustomColumn(
            Float, mapper_key="효과값_2",
            transform=bonus_value_transform)

    # 3
    @declared_attr
    def bonus_3_code(cls):
        return CustomColumn(
            Enum(EffectCode), mapper_key="효과코드_3",
            transform=lambda v: EffectCode(v) if v != MAX_INT else None)

    @declared_attr
    def bonus_3_operator(cls):
        return CustomColumn(
            String(4), mapper_key="수치연산자_3",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def bonus_3_value(cls):
        return CustomColumn(
            Float, mapper_key="효과값_3",
            transform=bonus_value_transform)

    # 4
    @declared_attr
    def bonus_4_code(cls):
        return CustomColumn(
            Enum(EffectCode), mapper_key="효과코드_4",
            transform=lambda v: EffectCode(v) if v != MAX_INT else None)

    @declared_attr
    def bonus_4_operator(cls):
        return CustomColumn(
            String(4), mapper_key="수치연산자_4",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def bonus_4_value(cls):
        return CustomColumn(
            Float, mapper_key="효과값_4",
            transform=bonus_value_transform)

    # 5
    @declared_attr
    def bonus_5_code(cls):
        return CustomColumn(
            Enum(EffectCode), mapper_key="효과코드_5",
            transform=lambda v: EffectCode(v) if v != MAX_INT else None)

    @declared_attr
    def bonus_5_operator(cls):
        return CustomColumn(
            String(4), mapper_key="수치연산자_5",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def bonus_5_value(cls):
        return CustomColumn(
            Float, mapper_key="효과값_5",
            transform=bonus_value_transform)

    def to_dict(self) -> typing.Dict[str, typing.List[dict]]:
        effects = []
        for i in range(1, 6):
            effect_code = getattr(self, f"bonus_{i}_code")
            if effect_code:
                effects.append({
                    "code": effect_code.to_dict(),
                    "operator": getattr(self, f"bonus_{i}_operator"),
                    "value": getattr(self, f"bonus_{i}_value"),
                })

        return {
            "effects": effects,
        }
