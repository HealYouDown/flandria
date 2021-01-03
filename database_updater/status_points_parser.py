import json
import os

from webapp.models.enums import CharacterClass

from database_updater.constants import PERSISTENT_DATA_FOLDER

CLASSES_INITIAL_POINTS = {
    # Explorer
    "E": {
        "strength": 19,
        "dexterity": 18,
        "constitution": 16,
        "intelligence": 13,
        "wisdom": 10,
        "will": 17,
    },
    # Noble
    "N": {
        "strength": 11,
        "dexterity": 16,
        "constitution": 12,
        "intelligence": 21,
        "wisdom": 19,
        "will": 14,
    },
    # Saint
    "S": {
        "strength": 14,
        "dexterity": 14,
        "constitution": 14,
        "intelligence": 16,
        "wisdom": 19,
        "will": 16,
    },
    # Mercenary
    "W": {
        "strength": 21,
        "dexterity": 15,
        "constitution": 22,
        "intelligence": 8,
        "wisdom": 10,
        "will": 17,
    }
}


def load_json_file(fpath: str) -> dict:
    with open(fpath, "r") as fp:
        return json.load(fp)


def parse_status_points():
    increments = []

    for character_class, base_status_values in CLASSES_INITIAL_POINTS.items():
        status_data = load_json_file(os.path.join(
            PERSISTENT_DATA_FOLDER, f"{character_class}.json"
        ))

        level_data = load_json_file(os.path.join(
            PERSISTENT_DATA_FOLDER, f"{character_class}_level.json"
        ))

        level_1_stats = level_data[0]

        # Go through level data and calculate all increments offset by level 0
        for level, stats in enumerate(level_data, start=1):
            stats["point_type"] = "level"
            stats["level"] = level
            stats["character_class"] = CharacterClass(character_class)
            increments.append(stats)

        # Do the same for each key in status data
        keys = ["Strength", "Dexterity", "Constitution",
                "Intelligence", "Wisdom", "Will"]

        for stat_key in keys:
            key_stats = status_data[stat_key]
            initial_points = CLASSES_INITIAL_POINTS[
                character_class][stat_key.lower()]

            for level, stats in enumerate(key_stats, start=initial_points):
                # Calculate offset from level 1 stats
                for key, value in level_1_stats.items():
                    if key in stats:
                        stats[key] -= value

                stats["point_type"] = stat_key.lower()
                stats["level"] = level
                stats["character_class"] = CharacterClass(character_class)

                increments.append(stats)

    return increments
