import strawberry

from src.api import enums, types
from src.api.resolvers import resolve_player_level_stats, resolve_player_status_stats


@strawberry.type
class PlayerStatsQuery:
    @strawberry.field
    def player_level_stats(
        self,
        info: strawberry.Info,
        base_class: enums.BaseClassType,
        level_min: int = 1,
        level_max: int = 105,
    ) -> list[types.PlayerLevelStat]:
        return resolve_player_level_stats(
            info=info,
            class_=base_class,
            level_min=level_min,
            level_max=level_max,
        )

    @strawberry.field
    def player_stats(
        self,
        info: strawberry.Info,
        base_class: enums.BaseClassType,
        max_points: int = 700,
    ) -> list[types.PlayerStatusStat]:
        return resolve_player_status_stats(
            info=info,
            class_=base_class,
            max_points=max_points,
        )
