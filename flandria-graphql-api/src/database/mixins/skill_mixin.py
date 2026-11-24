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
        info=ColumnInfo(key="OriginalSkillCode"),
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
        info=ColumnInfo.icon("IconCode"),
    )

    required_level_land = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Required level on land",
        info=ColumnInfo(key="RequiredLandLevel"),
    )

    required_level_sea = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Required level on sea",
        info=ColumnInfo(key="RequiredSeaLevel"),
    )

    @orm.declared_attr
    def description(cls):
        info = ColumnInfo.description("Code")

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
        info=ColumnInfo(key="SkillLevel"),
    )

    skill_max_level = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Max level for the skill",
        info=ColumnInfo(key="MaxSkillLevel"),
    )

    mana_cost = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Mana cost to use the skill",
        info=ColumnInfo(key="MPCost"),
    )

    accuracy = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Accuracy, but not sure how its used.",
        info=ColumnInfo(key="HitRate"),
    )

    hit_correction = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Same as accuracy",
        info=ColumnInfo(key="HitCorrection"),
    )

    cooldown = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Cooldown in seconds",
        info=ColumnInfo(key="Cooldown", transforms=[ms_to_seconds]),
    )

    cast_time = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Cast time in seconds",
        info=ColumnInfo(key="CastTime", transforms=[ms_to_seconds]),
    )

    cast_distance = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Max cast distance in Florensia units",
        info=ColumnInfo(key="MaxCastRange"),
    )

    dash_distance = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="??",
        info=ColumnInfo(key="DashDistance"),
    )

    push_distance = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="??",
        info=ColumnInfo(key="PushDistance"),
    )

    effect_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Range in which skills affect actors in Florensia units",
        info=ColumnInfo(key="PushDistance"),
    )

    effect_angle = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Effect angle for skills. (0 means 360° only if effect range is not None.)",
        info=ColumnInfo(key="EffectAngle"),
    )

    is_persistent = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether (de-)buff stays after death",
        info=ColumnInfo(key="EffectsLastAfterDeath"),
    )

    duration = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Duration for (de-)buffs in seconds",
        info=ColumnInfo(key="ActiveEffectDuration", transforms=[ms_to_seconds]),
    )

    toggle_tick_time = orm.mapped_column(
        sa.Float,
        nullable=True,
        doc=("How often toggle skills (like PoM) trigger in seconds"),
        info=ColumnInfo(
            key="ToggleTickTime",
            transforms=[lambda v: ms_to_seconds(v) if v != 0 else None],
        ),
    )

    toggle_operator = orm.mapped_column(
        sa.String(4),
        nullable=True,
        doc="Toggle operator (+, -, *)",
        info=ColumnInfo(
            key="ToggleOperator",
            transforms=[lambda v: value_if_not_equal(v, "#")],
        ),
    )

    toggle_hp_value = orm.mapped_column(
        sa.Float,
        nullable=True,
        doc="HP value that is used per toggle tick",
        info=ColumnInfo(
            key="ToggleHPCost",
            transforms=[lambda v: value_if_not_equal(v, 0)],
        ),
    )

    toggle_mp_value = orm.mapped_column(
        sa.Float,
        nullable=True,
        doc="MP value that is used per toggle tick",
        info=ColumnInfo(
            key="ToggleMPCost",
            transforms=[lambda v: value_if_not_equal(v, 0)],
        ),
    )

    # Not gonna bother with a 1:n relationship for that, frontend can deal with it
    required_weapons = orm.mapped_column(
        sa.String(32),
        nullable=False,
        doc="A key list of weapons that can use this skill.",
        info=ColumnInfo(key="WeaponType"),
    )

    # TODO: Additional skill data (damage?)
    # - Data values
    # - Passive values
    # but we don't know what they mean anyways
