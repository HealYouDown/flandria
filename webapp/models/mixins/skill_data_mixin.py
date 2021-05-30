from database_updater.conversions import convert_integer
from sqlalchemy import Boolean, Enum, Float, Integer, String, Text
from sqlalchemy.ext.declarative import declared_attr
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.enums import EffectCode
from webapp.models.transforms import (MAX_INT, florensia_meter_transform,
                                      florensia_time_transform)


class SkillDataMixin:
    @declared_attr
    def code(cls):
        return CustomColumn(String(32), primary_key=True,
                            nullable=False, mapper_key="코드")

    @declared_attr
    def name(cls):
        return CustomColumn(String(128), nullable=False,
                            mapper_key="_name")

    @declared_attr
    def icon(cls):
        return CustomColumn(String(32), nullable=False,
                            mapper_key="_icon")

    @declared_attr
    def description(cls):
        return CustomColumn(Text(1024), nullable=False,
                            mapper_key="_description")

    @declared_attr
    def reference_code(cls):
        return CustomColumn(String(32), nullable=False,
                            mapper_key="원형코드")

    @declared_attr
    def skill_level(cls):
        return CustomColumn(Integer, mapper_key="레벨")

    @declared_attr
    def max_level(cls):
        return CustomColumn(Integer, mapper_key="마스터레벨")

    @declared_attr
    def mana_cost(cls):
        return CustomColumn(Integer, mapper_key="소모ACT")

    @declared_attr
    def required_level_land(cls):
        return CustomColumn(Integer, mapper_key="습득가능레벨_육전",
                            nullable=False,
                            transform=lambda v: v if v != MAX_INT else 0)

    @declared_attr
    def required_level_sea(cls):
        return CustomColumn(Integer, mapper_key="습득가능레벨_해전",
                            nullable=False,
                            transform=lambda v: v if v != MAX_INT else 0)

    @declared_attr
    def required_weapons(cls):
        return CustomColumn(String(32), mapper_key="사용가능무기타입")

    @declared_attr
    def required_skill_1_code(cls):
        return CustomColumn(String(32), mapper_key="필요스킬코드1",
                            transform=(lambda v: f"{v[:-1]}0" if v != "*"
                                       else None))

    @declared_attr
    def required_skill_2_code(cls):
        return CustomColumn(String(32), mapper_key="필요스킬코드2",
                            transform=(lambda v: f"{v[:-1]}0" if v != "*"
                                       else None))

    @declared_attr
    def required_skill_3_code(cls):
        return CustomColumn(String(32), mapper_key="필요스킬코드3",
                            transform=(lambda v: f"{v[:-1]}0" if v != "*"
                                       else None))

    @declared_attr
    def required_skill_4_code(cls):
        return CustomColumn(String(32), mapper_key="필요스킬코드4",
                            transform=(lambda v: f"{v[:-1]}0" if v != "*"
                                       else None))

    @declared_attr
    def required_skill_5_code(cls):
        return CustomColumn(String(32), mapper_key="필요스킬코드5",
                            transform=(lambda v: f"{v[:-1]}0" if v != "*"
                                       else None))

    @declared_attr
    def class_land(cls):
        return CustomColumn(String(32), mapper_key="사용직업1",
                            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def class_sea(cls):
        return CustomColumn(String(32), mapper_key="사용직업2",
                            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def accuracy(cls):
        return CustomColumn(Integer, nullable=False,
                            mapper_key="명중률")

    @declared_attr
    def hit_compensation(cls):
        return CustomColumn(Integer, nullable=False,
                            mapper_key="명중보정")

    @declared_attr
    def cooldown(cls):
        return CustomColumn(
            Float, mapper_key="쿨타임밀초",
            transform=(lambda v: florensia_time_transform(v)
                       if v != MAX_INT else None))

    @declared_attr
    def cast_time(cls):
        return CustomColumn(
            Float, mapper_key="캐스팅시간밀초",
            transform=(lambda v: florensia_time_transform(v)
                       if v != MAX_INT else None))

    @declared_attr
    def cast_distance(cls):
        return CustomColumn(
            Float, mapper_key="시전유효최대거리",
            transform=(lambda v: florensia_meter_transform(v) if v != MAX_INT
                       else None))

    @declared_attr
    def dash_distance(cls):
        return CustomColumn(
            Float, mapper_key="데쉬거리",
            transform=(lambda v: florensia_meter_transform(v) if v != 0
                       else None))

    @declared_attr
    def push_distance(cls):
        return CustomColumn(
            Float, mapper_key="푸쉬거리",
            transform=(lambda v: florensia_meter_transform(v) if v != 0
                       else None))

    @declared_attr
    def effect_range(cls):
        return CustomColumn(
            Float, mapper_key="영향범위",
            transform=(lambda v: florensia_meter_transform(v) if v != MAX_INT
                       else None))

    @declared_attr
    def effect_angle(cls):
        # 360° are stored as 0, same as point-and-click spells of monsters.
        # The only difference is that a 360° skill has an effect range, while a
        # close up point and click spell do not.
        return CustomColumn(Float, nullable=False, mapper_key="영향각도")

    @declared_attr
    def stays_after_death(cls):
        return CustomColumn(Boolean, nullable=False,
                            mapper_key="지속사망후유지")

    @declared_attr
    def duration(cls):
        return CustomColumn(
            Integer, mapper_key="적용시간밀리초",
            transform=(lambda v: florensia_time_transform(v) if v != 0
                       else None))

    @declared_attr
    def toggle_cycle(cls):
        # How often the toggle effect triggers
        return CustomColumn(
            Float, mapper_key="토글주기밀리초",
            transform=(lambda v: florensia_time_transform(v) if v != 0
                       else None))

    @declared_attr
    def toggle_operator(cls):
        # * calculates based on max mp/hp
        return CustomColumn(
            String(4), mapper_key="토글지속소모량연산자",
            transform=lambda v: v if v != "#" else None
        )

    @declared_attr
    def toggle_mp_value(cls):
        return CustomColumn(
            Float, mapper_key="토글지속필요MP",
            transform=lambda v: convert_integer(v) if v != 0 else None
        )

    @declared_attr
    def toggle_hp_value(cls):
        return CustomColumn(
            Float, mapper_key="토글지속필요HP",
            transform=lambda v: convert_integer(v) if v != 0 else None
        )

    # Data 1
    @declared_attr
    def data_1_code(cls):
        return CustomColumn(
            Integer, mapper_key="일시코드1",
            transform=lambda v: v if v != MAX_INT else None)

    @declared_attr
    def data_1_operator(cls):
        return CustomColumn(
            String(4), mapper_key="일시수치연산자1",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def data_1_value(cls):
        return CustomColumn(
            Float, mapper_key="일시값1",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    @declared_attr
    def data_1_correction_1(cls):
        return CustomColumn(
            Float, mapper_key="지능보정1_1",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    @declared_attr
    def data_1_correction_2(cls):
        return CustomColumn(
            Float, mapper_key="지능보정2_1",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    # Data 2
    @declared_attr
    def data_2_code(cls):
        return CustomColumn(
            Integer, mapper_key="일시코드2",
            transform=lambda v: v if v != MAX_INT else None)

    @declared_attr
    def data_2_operator(cls):
        return CustomColumn(
            String(4), mapper_key="일시수치연산자2",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def data_2_value(cls):
        return CustomColumn(
            Float, mapper_key="일시값2",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    @declared_attr
    def data_2_correction_1(cls):
        return CustomColumn(
            Float, mapper_key="지능보정1_2",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    @declared_attr
    def data_2_correction_2(cls):
        return CustomColumn(
            Float, mapper_key="지능보정2_2",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    # Effect 1
    @declared_attr
    def effect_1_code(cls):
        return CustomColumn(
            Enum(EffectCode), mapper_key="지속코드1",
            transform=lambda v: EffectCode(v) if v != MAX_INT else None)

    @declared_attr
    def effect_1_operator(cls):
        return CustomColumn(
            String(4), mapper_key="지속수치연산자1",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def effect_1_value(cls):
        return CustomColumn(
            Float, mapper_key="지속값1",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    # Effect 2
    @declared_attr
    def effect_2_code(cls):
        return CustomColumn(
            Enum(EffectCode), mapper_key="지속코드2",
            transform=lambda v: EffectCode(v) if v != MAX_INT else None)

    @declared_attr
    def effect_2_operator(cls):
        return CustomColumn(
            String(4), mapper_key="지속수치연산자2",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def effect_2_value(cls):
        return CustomColumn(
            Float, mapper_key="지속값2",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    # Effect 3
    @declared_attr
    def effect_3_code(cls):
        return CustomColumn(
            Enum(EffectCode), mapper_key="지속코드3",
            transform=lambda v: EffectCode(v) if v != MAX_INT else None)

    @declared_attr
    def effect_3_operator(cls):
        return CustomColumn(
            String(4), mapper_key="지속수치연산자3",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def effect_3_value(cls):
        return CustomColumn(
            Float, mapper_key="지속값3",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    # Effect 4
    @declared_attr
    def effect_4_code(cls):
        return CustomColumn(
            Enum(EffectCode), mapper_key="지속코드4",
            transform=lambda v: EffectCode(v) if v != MAX_INT else None)

    @declared_attr
    def effect_4_operator(cls):
        return CustomColumn(
            String(4), mapper_key="지속수치연산자4",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def effect_4_value(cls):
        return CustomColumn(
            Float, mapper_key="지속값4",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    # Passive Effect 1
    @declared_attr
    def passive_1_code(cls):
        return CustomColumn(
            Enum(EffectCode), mapper_key="패시브코드1",
            transform=lambda v: EffectCode(v) if v != MAX_INT else None)

    @declared_attr
    def passive_1_operator(cls):
        return CustomColumn(
            String(4), mapper_key="패시브수치연산자1",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def passive_1_value(cls):
        return CustomColumn(
            Float, mapper_key="패시브값1",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    # Passive Effect 2
    @declared_attr
    def passive_2_code(cls):
        return CustomColumn(
            Enum(EffectCode), mapper_key="패시브코드2",
            transform=lambda v: EffectCode(v) if v != MAX_INT else None)

    @declared_attr
    def passive_2_operator(cls):
        return CustomColumn(
            String(4), mapper_key="패시브수치연산자2",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def passive_2_value(cls):
        return CustomColumn(
            Float, mapper_key="패시브값2",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    # Passive Effect 3
    @declared_attr
    def passive_3_code(cls):
        return CustomColumn(
            Enum(EffectCode), mapper_key="패시브코드3",
            transform=lambda v: EffectCode(v) if v != MAX_INT else None)

    @declared_attr
    def passive_3_operator(cls):
        return CustomColumn(
            String(4), mapper_key="패시브수치연산자3",
            transform=lambda v: v if v != "#" else None)

    @declared_attr
    def passive_3_value(cls):
        return CustomColumn(
            Float, mapper_key="패시브값3",
            transform=lambda v: convert_integer(v) if v != 0 else None)

    def to_dict(self, minimal: bool = False) -> dict:
        required_skills = []
        for i in range(1, 6):
            required_skill_code = getattr(self, f"required_skill_{i}_code")
            if required_skill_code:
                required_skills.append(required_skill_code)

        minimal_dict = {
            "code": self.code,
            "name": self.name,
            "icon": self.icon,
            "description": self.description,
            "reference_code": self.reference_code,
            "skill_level": self.skill_level,
            "max_level": self.max_level,
            "mana_cost": self.mana_cost,
            "required_level_land": self.required_level_land,
            "required_level_sea": self.required_level_sea,
            "required_weapons": self.required_weapons,
            "class_land": self.class_land,
            "class_sea": self.class_sea,
            "cooldown": self.cooldown,
            "cast_time": self.cast_time,
            "accuracy": self.accuracy,
            "hit_compensation": self.hit_compensation,
            "cast_distance": self.cast_distance,
            "effect_range": self.effect_range,
            "effect_angle": self.effect_angle,
            "required_skills": required_skills,
        }

        if minimal:
            return minimal_dict

        # Data
        data = []
        for i in range(1, 3):
            data_code = getattr(self, f"data_{i}_code")
            if data_code:
                data.append({
                    "code": data_code,
                    "operator": getattr(self, f"data_{i}_operator"),
                    "value": getattr(self, f"data_{i}_value"),
                    "correction_1": getattr(self, f"data_{i}_correction_1"),
                    "correction_2": getattr(self, f"data_{i}_correction_2"),
                })

        # Effects
        effects = []
        for i in range(1, 5):
            effect_code = getattr(self, f"effect_{i}_code")
            if effect_code:
                effects.append({
                    "code": effect_code.to_dict(),
                    "operator": getattr(self, f"effect_{i}_operator"),
                    "value": getattr(self, f"effect_{i}_value"),
                })

        # Passives
        passives = []
        for i in range(1, 4):
            passive_code = getattr(self, f"passive_{i}_code")
            if passive_code:
                passives.append({
                    "code": passive_code.to_dict(),
                    "operator": getattr(self, f"passive_{i}_operator"),
                    "value": getattr(self, f"passive_{i}_value"),
                })

        return {
            **minimal_dict,
            "dash_distance": self.dash_distance,
            "push_distance:": self.push_distance,
            "stays_after_death": self.stays_after_death,
            "duration": self.duration,
            "toggle_cycle": self.toggle_cycle,
            "toggle_operator": self.toggle_operator,
            "toggle_mp_value": self.toggle_mp_value,
            "toggle_hp_value": self.toggle_hp_value,
            "data": data,
            "effects": effects,
            "passives": passives,
        }
