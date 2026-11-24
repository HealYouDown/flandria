import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import ActorGrade
from src.updater.schema import ColumnInfo
from src.updater.transforms import ms_to_seconds

from .florensia_model_mixin import ActorModelMixin
from .row_id_mixin import RowIDMixin


class ActorMixin(RowIDMixin, ActorModelMixin):
    code = orm.mapped_column(
        sa.String(32),
        primary_key=True,
        doc="Unique code of the actor",
        info=ColumnInfo.code(),
    )

    name = orm.mapped_column(
        sa.String(256),
        nullable=False,
        index=True,
        doc="Name of the actor",
        info=ColumnInfo.name(),
    )

    icon = orm.mapped_column(
        sa.String(32),
        nullable=False,
        doc="Icon for the actor",
        info=ColumnInfo.icon("ModelCode"),
    )

    level = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Level of the actor",
        info=ColumnInfo(key="Level"),
    )

    grade = orm.mapped_column(
        sa.Enum(ActorGrade),
        nullable=False,
        doc="The grade of the actor",
        info=ColumnInfo(
            key="MonsterGrade",
            transforms=[lambda v: ActorGrade(v)],
        ),
    )

    is_inanimate = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the actor is alive and moves around or is just in-place",
        info=ColumnInfo(key="IsLifeless"),
    )

    is_sea = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the actor is on land or sea",
        info=ColumnInfo(key="FieldType"),
    )

    is_ship = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the actor is a ship",
        info=ColumnInfo(key="IsShip"),
    )

    is_air = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the actor is flying",
        info=ColumnInfo(key="IsAir"),
    )

    is_tameable = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the actor can be tamed",
        info=ColumnInfo(key="IsTameable"),
    )

    experience = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="The experience rewarded on kill",
        info=ColumnInfo(key="Experience"),
    )

    health_points = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Health Points",
        info=ColumnInfo(key="HP"),
    )

    recovery_rate = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc=(
            "The percentage that is recovered each tick if "
            "the actor was not attacked recently"
        ),
        info=ColumnInfo(key="HPRecoveryPerTick"),
    )

    minimum_physical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Minimum physical attack damage",
        info=ColumnInfo(key="MinPhysicalAttack"),
    )

    maximum_physical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Maximum physical attack damage",
        info=ColumnInfo(key="MaxPhysicalAttack"),
    )

    minimum_magical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Minimum magical attack damage",
        info=ColumnInfo(key="MinMagicAttack"),
    )

    maximum_magical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Maximum magical attack damage",
        info=ColumnInfo(key="MaxMagicAttack"),
    )

    physical_defense = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Physical defense",
        info=ColumnInfo(key="PhysicalDefense"),
    )

    magical_defense = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Magical defense",
        info=ColumnInfo(key="MagicDefense"),
    )

    physical_evasion_rate = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Physical evasion rate",
        info=ColumnInfo(key="Avoidance"),
    )

    physical_hit_rate = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Physical hit rate",
        info=ColumnInfo(key="PhysicalHit"),
    )

    magical_hit_rate = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Magical hit rate",
        info=ColumnInfo(key="MagicHit"),
    )

    critical_rate = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Critical hit rate",
        info=ColumnInfo(key="CritHitRate"),
    )

    critical_resistance_rate = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Critical resistance rate",
        info=ColumnInfo(key="CritDefense"),
    )

    sea_attack_aoe_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Area in florensia units affected by physical attack of sea monsters",
        info=ColumnInfo(key="PhysicalAttackRange"),
    )

    ship_guns_count = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Number of ship guns",
        info=ColumnInfo(key="MobCannonCount"),
    )

    ship_guns_speed = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Attack speed for ship guns",
        info=ColumnInfo(
            key="MobCannonSpeed",
            transforms=[ms_to_seconds],
        ),
    )

    ship_attack_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Ship attack range in florensia units",
        info=ColumnInfo(key="MobCannonSpreadRange"),
    )

    attack_cooldown = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Cooldown before attacking again",
        info=ColumnInfo(
            key="PhysicalAttackCooldownMs",
            transforms=[ms_to_seconds],
        ),
    )

    despawn_delay_time = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Time until body disappears after death",
        info=ColumnInfo(
            key="DespawnDelayMs",
            transforms=[ms_to_seconds],
        ),
    )

    attack_vision_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Range in florensia units in which the actor will attack a player",
        info=ColumnInfo(key="AggroRange"),
    )

    nearby_attack_vision_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Range in florensia units in which the actor will attack if nearby actors are in battle",
        info=ColumnInfo(key="AskHelpRange"),
    )

    is_ranged = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the actor is melee or ranged",
        info=ColumnInfo(key="AttackType"),
    )

    attack_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Attack range in florensia units",
        info=ColumnInfo(key="MaxAttackRange"),
    )

    walking_speed = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Movement speed when out of combat",
        info=ColumnInfo(key="WalkSpeed"),
    )

    running_speed = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Movement speed when in combat",
        info=ColumnInfo(key="RunSpeed"),
    )

    turning_speed = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Turning speed for ships on sea",
        info=ColumnInfo(key="TurnSpeed"),
    )

    messages_code = orm.mapped_column(
        sa.String,
        nullable=True,
        doc="Code for linking messages",
        info=ColumnInfo(key="BalloonMessageKey"),
    )

    @orm.declared_attr
    def messages(cls):
        cls_name = cls.__name__  # type: ignore
        return orm.relationship(
            "ActorMessage",
            primaryjoin=(f"foreign(ActorMessage.code) == {cls_name}.messages_code"),
            uselist=True,
            viewonly=True,
        )

    posion_resistance = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Posion resistance",
        info=ColumnInfo(key="AttributePoisonResistance"),
    )

    fire_resistance = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Fire resistance",
        info=ColumnInfo(key="AttributeFireResistance"),
    )

    cold_resistance = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Cold resistance",
        info=ColumnInfo(key="AttributeIceResistance"),
    )

    lightning_resistance = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Lightning resistance",
        info=ColumnInfo(key="AttributeLightningResistance"),
    )

    holy_resistance = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Holy resistance",
        info=ColumnInfo(key="AttributeHolyResistance"),
    )

    dark_resistance = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Dark resistance",
        info=ColumnInfo(key="AttributeDarkResistance"),
    )
