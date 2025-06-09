import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.updater.schema import ColumnInfo
from src.updater.transforms import (
    ms_to_seconds,
    value_if_not_equal,
)

from .class_land_mixin import ClassLandMixin
from .class_sea_mixin import ClassSeaMixin
from .effect_mixin import EffectMixin


class SkillMixin(EffectMixin, ClassSeaMixin, ClassLandMixin):
    code = orm.mapped_column(
        sa.String(32),
        primary_key=True,
        doc="Code of the skill",
        info=ColumnInfo.code(),
    )

    reference_code = orm.mapped_column(
        sa.String(32),
        nullable=False,
        doc="Base Skill Code",
        info=ColumnInfo(key="원형코드"),
    )

    name = orm.mapped_column(
        sa.String(256),
        nullable=False,
        doc="Name of the skill",
        info=ColumnInfo.name(),
    )

    icon = orm.mapped_column(
        sa.String(16),
        nullable=False,
        doc="Icon of the skill",
        info=ColumnInfo.icon("아이콘코드"),
    )

    required_level_land = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Required level on land",
        info=ColumnInfo(key="습득가능레벨_육전"),
    )

    required_level_sea = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Required level on sea",
        info=ColumnInfo(key="습득가능레벨_해전"),
    )

    @orm.declared_attr
    def description(cls):
        info = ColumnInfo.description("코드")

        return orm.mapped_column(
            sa.Text,
            nullable=False,
            doc="Description of the skill",
            info=info,
        )

    skill_level = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Level of the skill (e.g. player skills have level 0-15)",
        info=ColumnInfo(key="레벨"),
    )

    skill_max_level = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Max level for the skill",
        info=ColumnInfo(key="마스터레벨"),
    )

    mana_cost = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Mana cost to use the skill",
        info=ColumnInfo(key="소모ACT"),
    )

    accuracy = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Accuracy, but not sure how its used.",
        info=ColumnInfo(key="명중률"),
    )

    hit_correction = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Same as accuracy",
        info=ColumnInfo(key="명중보정"),
    )

    cooldown = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Cooldown in seconds",
        info=ColumnInfo(key="쿨타임밀초", transforms=[ms_to_seconds]),
    )

    cast_time = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Cast time in seconds",
        info=ColumnInfo(key="캐스팅시간밀초", transforms=[ms_to_seconds]),
    )

    cast_distance = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Max cast distance in Florensia units",
        info=ColumnInfo(key="시전유효최대거리"),
    )

    dash_distance = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="??",
        info=ColumnInfo(key="데쉬거리"),
    )

    push_distance = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="??",
        info=ColumnInfo(key="푸쉬거리"),
    )

    effect_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Range in which skills affect actors in Florensia units",
        info=ColumnInfo(key="푸쉬거리"),
    )

    effect_angle = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Effect angle for skills. (0 means 360° only if effect range is not None.)",
        info=ColumnInfo(key="영향각도"),
    )

    is_persistent = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether (de-)buff stays after death",
        info=ColumnInfo(key="지속사망후유지"),
    )

    duration = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Duration for (de-)buffs in seconds",
        info=ColumnInfo(key="적용시간밀리초", transforms=[ms_to_seconds]),
    )

    toggle_tick_time = orm.mapped_column(
        sa.Float,
        nullable=True,
        doc=("How often toggle skills (like PoM) trigger in seconds"),
        info=ColumnInfo(
            key="토글주기밀리초",
            transforms=[lambda v: ms_to_seconds(v) if v != 0 else None],
        ),
    )

    toggle_operator = orm.mapped_column(
        sa.String(4),
        nullable=True,
        doc="Toggle operator (+, -, *)",
        info=ColumnInfo(
            key="토글지속소모량연산자",
            transforms=[lambda v: value_if_not_equal(v, "#")],
        ),
    )

    toggle_hp_value = orm.mapped_column(
        sa.Float,
        nullable=True,
        doc="HP value that is used per toggle tick",
        info=ColumnInfo(
            key="토글지속필요HP",
            transforms=[lambda v: value_if_not_equal(v, 0)],
        ),
    )

    toggle_mp_value = orm.mapped_column(
        sa.Float,
        nullable=True,
        doc="MP value that is used per toggle tick",
        info=ColumnInfo(
            key="토글지속필요MP",
            transforms=[lambda v: value_if_not_equal(v, 0)],
        ),
    )

    # Not gonna bother with a 1:n relationship for that, frontend can deal with it
    required_weapons = orm.mapped_column(
        sa.String(32),
        nullable=False,
        doc="A key list of weapons that can use this skill.",
        info=ColumnInfo(key="사용가능무기타입"),
    )

    # TODO: Additional skill data (damage?)
    # - Data values
    # - Passive values
    # but we don't know what they mean anyways
