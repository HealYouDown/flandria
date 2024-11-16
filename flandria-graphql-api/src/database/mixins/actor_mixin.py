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
        info=ColumnInfo.icon("모델명"),
    )

    level = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Level of the actor",
        info=ColumnInfo(key="기준레벨"),
    )

    grade = orm.mapped_column(
        sa.Enum(ActorGrade),
        nullable=False,
        doc="The grade of the actor",
        info=ColumnInfo(
            key="몬스터등급타입",
            transforms=[lambda v: ActorGrade(v)],
        ),
    )

    is_inanimate = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the actor is alive and moves around or is just in-place",
        info=ColumnInfo(key="무생물"),
    )

    is_sea = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the actor is on land or sea",
        info=ColumnInfo(key="필드구분"),
    )

    is_ship = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the actor is a ship",
        info=ColumnInfo(key="함선형"),
    )

    is_air = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the actor is flying",
        info=ColumnInfo(key="공중유닛"),
    )

    is_tameable = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the actor can be tamed",
        info=ColumnInfo(key="테이밍"),
    )

    experience = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="The experience rewarded on kill",
        info=ColumnInfo(key="보상경험치"),
    )

    health_points = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Health Points",
        info=ColumnInfo(key="기준최대HP"),
    )

    recovery_rate = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc=(
            "The percentage that is recovered each tick if "
            "the actor was not attacked recently"
        ),
        info=ColumnInfo(key="회복속도"),
    )

    minimum_physical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Minimum physical attack damage",
        info=ColumnInfo(key="최소물공력"),
    )

    maximum_physical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Maximum physical attack damage",
        info=ColumnInfo(key="최대물공력"),
    )

    minimum_magical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Minimum magical attack damage",
        info=ColumnInfo(key="최소마공력"),
    )

    maximum_magical_damage = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Maximum magical attack damage",
        info=ColumnInfo(key="최대마공력"),
    )

    physical_defense = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Physical defense",
        info=ColumnInfo(key="물방력"),
    )

    magical_defense = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Magical defense",
        info=ColumnInfo(key="마항력"),
    )

    physical_evasion_rate = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Physical evasion rate",
        info=ColumnInfo(key="물공피"),
    )

    physical_hit_rate = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Physical hit rate",
        info=ColumnInfo(key="물공명"),
    )

    magical_hit_rate = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Magical hit rate",
        info=ColumnInfo(key="마공명"),
    )

    critical_rate = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Critical hit rate",
        info=ColumnInfo(key="크리성공"),
    )

    critical_resistance_rate = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Critical resistance rate",
        info=ColumnInfo(key="크리저항"),
    )

    sea_attack_aoe_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Area in florensia units affected by physical attack of sea monsters",
        info=ColumnInfo(key="물리공격범위"),
    )

    ship_guns_count = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Number of ship guns",
        info=ColumnInfo(key="몹함포갯수"),
    )

    ship_guns_speed = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Attack speed for ship guns",
        info=ColumnInfo(
            key="몹함포속도",
            transforms=[ms_to_seconds],
        ),
    )

    ship_attack_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Ship attack range in florensia units",
        info=ColumnInfo(key="몹함포집탄범위"),
    )

    attack_cast_time = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Time it takes from casting to dealing damage",
        info=ColumnInfo(
            key="물리공격캐스팅타임밀초",
            transforms=[ms_to_seconds],
        ),
    )

    attack_cooldown = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Cooldown before attacking again",
        info=ColumnInfo(
            key="물리공격쿨타임밀초",
            transforms=[ms_to_seconds],
        ),
    )

    despawn_delay_time = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Time until body disappears after death",
        info=ColumnInfo(
            key="소멸지연타임밀초",
            transforms=[ms_to_seconds],
        ),
    )

    attack_vision_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Range in florensia units in which the actor will attack a player",
        info=ColumnInfo(key="선공시야"),
    )

    nearby_attack_vision_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Range in florensia units in which the actor will attack if nearby actors are in battle",
        info=ColumnInfo(key="요청시야"),
    )

    is_ranged = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the actor is melee or ranged",
        info=ColumnInfo(key="공격거리타입"),
    )

    attack_range = orm.mapped_column(
        sa.Float,
        nullable=False,
        doc="Attack range in florensia units",
        info=ColumnInfo(key="기본사정거리"),
    )

    walking_speed = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Movement speed when out of combat",
        info=ColumnInfo(key="걷기속도"),
    )

    running_speed = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Movement speed when in combat",
        info=ColumnInfo(key="뛰기속도"),
    )

    turning_speed = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Turning speed for ships on sea",
        info=ColumnInfo(key="선회력"),
    )

    messages_code = orm.mapped_column(
        sa.String,
        nullable=True,
        doc="Code for linking messages",
        info=ColumnInfo(key="오브젝트채팅"),
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
        info=ColumnInfo(key="독속성저항력"),
    )

    fire_resistance = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Fire resistance",
        info=ColumnInfo(key="화염속성저항력"),
    )

    cold_resistance = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Cold resistance",
        info=ColumnInfo(key="냉기속성저항력"),
    )

    lightning_resistance = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Lightning resistance",
        info=ColumnInfo(key="전격속성저항력"),
    )

    holy_resistance = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Holy resistance",
        info=ColumnInfo(key="신성속성저항력"),
    )

    dark_resistance = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Dark resistance",
        info=ColumnInfo(key="암흑속성저항력"),
    )
