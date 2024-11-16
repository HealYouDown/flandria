import sqlalchemy as sa
import strawberry

from src.api import enums, types
from src.database import models
from src.database.engine import Session

from .helpers import coerce_orm_to_strawberry, parse_nested_keys_from_selections

# Technically, neither level nor status stats have any nested keys, so we could pass [] to coerce
# Future proofing anyways :)


def resolve_player_level_stats(
    *,
    info: strawberry.Info,
    class_: enums.BaseClassType,
    level_min: int,
    level_max: int,
):
    nested_keys = parse_nested_keys_from_selections(info.selected_fields)[
        info._raw_info.field_name
    ]

    if class_ == enums.BaseClassType.SHIP:
        return []

    with Session() as session:
        query = sa.select(models.PlayerLevelStat).where(
            models.PlayerLevelStat.base_class == class_,
            models.PlayerLevelStat.level.between(level_min, level_max),
        )
        result = session.scalars(query)
        return [
            coerce_orm_to_strawberry(
                o,
                types.PlayerLevelStat,
                nested_keys,
            )
            for o in result
        ]


def resolve_player_status_stats(
    *,
    info: strawberry.Info,
    class_: enums.BaseClassType,
    max_points: int,
):  # -> list[Any] | list[PlayerStatusStat]:
    nested_keys = parse_nested_keys_from_selections(info.selected_fields)[
        info._raw_info.field_name
    ]

    if class_ == enums.BaseClassType.SHIP:
        return []

    with Session() as session:
        query = sa.select(models.PlayerStatusStat).where(
            models.PlayerStatusStat.base_class == class_,
            models.PlayerStatusStat.point_level <= max_points,
        )
        result = session.scalars(query)
        return [
            coerce_orm_to_strawberry(
                o,
                types.PlayerStatusStat,
                nested_keys,
            )
            for o in result
        ]
