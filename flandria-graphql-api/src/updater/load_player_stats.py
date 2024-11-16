import json
import os
from typing import Literal, NotRequired, TypedDict

import sqlalchemy as sa

from src.core.enums import BaseClassType, StatType
from src.database.engine import Session
from src.database.models import PlayerLevelStat, PlayerStatusStat

CLASSES_INITIAL_POINTS = {
    "explorer": {
        "strength": 19,
        "dexterity": 18,
        "constitution": 16,
        "intelligence": 13,
        "wisdom": 10,
        "will": 17,
    },
    "noble": {
        "strength": 11,
        "dexterity": 16,
        "constitution": 12,
        "intelligence": 21,
        "wisdom": 19,
        "will": 14,
    },
    "saint": {
        "strength": 14,
        "dexterity": 14,
        "constitution": 14,
        "intelligence": 16,
        "wisdom": 19,
        "will": 16,
    },
    "mercenary": {
        "strength": 21,
        "dexterity": 15,
        "constitution": 22,
        "intelligence": 8,
        "wisdom": 10,
        "will": 17,
    },
}


class BaseStatsDictType(TypedDict):
    max_hp: int
    max_mp: int
    avoidance: int
    melee_min_attack: int
    melee_max_attack: int
    melee_hitrate: int
    melee_critical_rate: int
    range_min_attack: int
    range_max_attack: int
    range_hitrate: int
    range_critical_rate: int
    magic_min_attack: int
    magic_max_attack: int
    magic_hitrate: int
    magic_critical_rate: int


class LevelStatsORMDictType(BaseStatsDictType):
    level: NotRequired[int]
    base_class: NotRequired[BaseClassType]


class StatsORMDictType(TypedDict):
    max_hp_increment: int
    max_mp_increment: int
    avoidance_increment: int
    melee_min_attack_increment: int
    melee_max_attack_increment: int
    melee_hitrate_increment: int
    melee_critical_rate_increment: int
    range_min_attack_increment: int
    range_max_attack_increment: int
    range_hitrate_increment: int
    range_critical_rate_increment: int
    magic_min_attack_increment: int
    magic_max_attack_increment: int
    magic_hitrate_increment: int
    magic_critical_rate_increment: int

    point_level: NotRequired[int]
    base_class: NotRequired[BaseClassType]
    stat_type: NotRequired[StatType]


def load_player_stats(stats_folder_path: str) -> None:
    classes = ["explorer", "mercenary", "saint", "noble"]

    level_orm_mappings: list[LevelStatsORMDictType] = []
    stats_orm_mappings: list[StatsORMDictType] = []
    for class_ in classes:
        with open(
            os.path.join(stats_folder_path, f"{class_}_level.json"),
            "r",
            encoding="utf-8",
        ) as fp:
            level_data: list[BaseStatsDictType] = json.load(fp)
            level_1_data = level_data[0]

        with open(
            os.path.join(stats_folder_path, f"{class_}_stats.json"),
            "r",
            encoding="utf-8",
        ) as fp:
            stats_data: dict[
                Literal[
                    "Strength",
                    "Dexterity",
                    "Constitution",
                    "Intelligence",
                    "Wisdom",
                    "Will",
                ],
                list[BaseStatsDictType],
            ] = json.load(fp)

        for i, stats in enumerate(level_data, start=1):
            level_orm_mappings.append(
                {
                    **stats,
                    "level": i,
                    "base_class": BaseClassType[class_.upper()],
                }
            )

        for stat_key, stat_values in stats_data.items():
            start = CLASSES_INITIAL_POINTS[class_][stat_key.lower()]

            for point_level, stats in enumerate(stat_values, start=start):
                stats_orm_mappings.append(
                    {
                        # offset the stats by the level 1 stats, as all stats
                        # were recorded on level 1 characters.
                        **{
                            f"{k}_increment": v - level_1_data[k]
                            for k, v in stats.items()
                        },  # type: ignore
                        "point_level": point_level,
                        "base_class": BaseClassType[class_.upper()],
                        "stat_type": StatType[stat_key.upper()],
                    }
                )

    with Session() as session:
        # Clear models
        session.query(PlayerLevelStat).delete(synchronize_session=False)
        session.query(PlayerStatusStat).delete(synchronize_session=False)

        session.execute(sa.insert(PlayerLevelStat), level_orm_mappings)
        session.execute(sa.insert(PlayerStatusStat), stats_orm_mappings)

        session.commit()
