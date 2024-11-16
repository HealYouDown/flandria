import sys
from functools import reduce
from typing import TYPE_CHECKING, Any, cast

from loguru import logger

from src.core.constants import (
    FALLBACK_ACTOR_ICON,
    FALLBACK_ITEM_ICON,
    FALLBACK_NAME,
    FALLBACK_SKILL_ICON,
    LANGUAGE,
)
from src.core.enums import EffectCode
from src.updater.file_data import FileData

if TYPE_CHECKING:
    from sqlalchemy import Column

    from src.database.types import ModelCls
    from src.updater.file_data import FileData
    from src.updater.transforms.types import T_TRANSFORM_FUNCTION


def get_effects(row: dict, tablename: str, ref_code: str) -> list[dict]:
    if tablename.startswith("ship"):
        code_key = "효과코드_{i}"
        operator_key = None
        value_key = "효과값_{i}"
        range_ = (1, 6)
    elif tablename in {"monster_skill", "player_skill", "pet_skill"}:
        code_key = "지속코드{i}"
        operator_key = "지속수치연산자{i}"
        value_key = "지속값{i}"
        range_ = (1, 5)
    elif tablename == "upgrade_rule":
        code_key = "효과코드{i}"
        operator_key = "연산자{i}"
        value_key = "효과값{i}"
        range_ = (0, 4)
    elif tablename == "item_set":
        code_key = "효과코드_{i}"
        operator_key = "수치연산자_{i}"
        value_key = "효과값_{i}"
        range_ = (1, 13)
    else:
        code_key = "효과코드_{i}"
        operator_key = "수치연산자_{i}"
        value_key = "효과값_{i}"
        range_ = (1, 6)

    effects = []
    for i in range(*range_):
        effect_code = row[code_key.format(i=i)]
        if effect_code == -1:
            continue

        if operator_key is None:  # ships
            effect_operator = "+"
        else:
            effect_operator = cast(str, row[operator_key.format(i=i)])
            if effect_operator is None:
                effect_operator = "+"

        # Workaround for negative values that are stored as + with a negative value
        effect_value = row[value_key.format(i=i)]
        if effect_value < 0 and effect_operator == "+":
            effect_value *= -1
            effect_operator = "-"

        effects.append(
            {
                "ref_code": ref_code,
                "effect_code": EffectCode(effect_code),
                "operator": effect_operator,
                "value": effect_value,
            }
        )

    return effects


def get_required_skills(row: dict, skill_code: str) -> list[dict]:
    required_skills = []

    key = "필요스킬코드{i}"
    for i in range(1, 6):
        required_skill_code = row[key.format(i=i)]
        if required_skill_code != "*":
            # required skill code, by default, is the lv 1 skill code
            # to make the frontend work easier, we just set the lv 0 skill as required
            required_skill_code = required_skill_code[:-1] + "0"

            required_skills.append(
                {
                    "skill_code": skill_code,
                    "required_skill_code": required_skill_code,
                }
            )

    return required_skills


def get_class_land(row: dict, tablename: str) -> dict[str, bool]:
    key = (
        "사용직업1"
        if tablename in {"pet_skill", "monster_skill", "player_skill"}
        else "사용직업"
    )
    value: str | None = row[key]
    if value is None:
        return {}

    # Filter out P for Pirate in accessories
    if tablename == "accessory":
        value = value.replace("P", "")

    mapping = {
        "N": "is_noble",
        "K": "is_magic_knight",
        "M": "is_court_magician",
        "W": "is_mercenary",
        "G": "is_gladiator",
        "D": "is_guardian_swordsman",
        "S": "is_saint",
        "P": "is_priest",
        "A": "is_shaman",
        "E": "is_explorer",
        "B": "is_excavator",
        "H": "is_sniper",
    }

    return {mapping[char]: True for char in value if char in mapping}


def get_class_sea(row: dict, tablename: str) -> dict[str, bool]:
    key = (
        "사용직업2"
        if tablename in {"pet_skill", "monster_skill", "player_skill"}
        else "클래스"
    )
    value: str | None = row[key]
    if value is None:
        return {}

    mapping = {
        "A": "is_armored",
        "G": "is_big_gun",
        "H": "is_torpedo",
        "M": "is_maintenance",
        "R": "is_assault",
    }

    return {mapping[char]: True for char in value if char in mapping}


def get_model_info(pk: str, data: "FileData") -> dict:
    try:
        client_row = data.client_lookup[pk]
    except KeyError:
        logger.warning(f"No model reference found for item {pk!r}")
        return {}

    return {"model_name": client_row["모델명"]}


def get_extra_equipment_model_info(pk: str, data: "FileData") -> dict:
    try:
        client_row = data.client_lookup[pk]
    except KeyError:
        logger.warning(f"No model reference found for dress/hat {pk!r}")
        return {}

    def _parse_variant(variant: str) -> tuple[int, int, int] | None:
        if variant == "fff":
            return None

        # splits 255,255,255 into tuple
        parts = variant.split(",")
        if not len(parts) == 3:
            return None

        if not all(str.isdigit(p) for p in parts):
            return None

        r, g, b = [int(p) for p in parts]
        return (r, g, b)

    return {
        "model_name": client_row["모델명"],
        "model_variant": _parse_variant(client_row["그라운드아이템"]),
    }


def get_actor_model_info(pk: str, data: "FileData") -> dict:
    try:
        client_row = data.client_lookup[pk]
    except KeyError:
        logger.warning(f"No model reference found for actor {pk!r}")
        return {}

    return {
        "model_name": client_row["모델명"],
        "model_scale": client_row["스케일"] / 100,
    }


def map_row_to_model(
    model_cls: "ModelCls",
    row: dict[str, Any],
    data: "FileData",
) -> tuple[Any, dict[str, Any]]:
    # Columns like __name, __icon, ... which are done after everything was mapped
    columns = model_cls.__mapper__.columns
    special_columns: list[tuple[dict, "Column[Any]"]] = []

    # tablename is required for some specific workarounds and checks
    tablename = model_cls.__tablename__

    obj: dict[str, Any] = {}
    for column in columns:
        column_info = column.info
        key = cast(str | None, column_info.get("key", None))
        transforms: list["T_TRANSFORM_FUNCTION"] = column_info.get("transforms", [])

        # Column is not mapped via a key
        if key is None:
            continue

        # Column is a special column, which will be handled in another
        # loop, as it requires the pk to get the related data
        if key.startswith("__"):
            special_columns.append((column_info, column))
            continue

        try:
            value = row[key]
        except KeyError:
            logger.critical(
                f"{key!r} wasn't found in server data for " f"column {column.name!r}"
            )
            sys.exit(1)

        # apply transformations to the value
        value = reduce(lambda v, transform: transform(v), transforms, value)

        obj[column.name] = value

    pk_columns = [
        column for column in model_cls.__mapper__.columns if column.primary_key
    ]
    if len(pk_columns) != 1:
        raise ValueError(
            f"Expected exactly one primary key column in {model_cls!r}, got {len(pk_columns)!r}"
        )

    pk_value: str = obj[pk_columns[0].name]

    for column_info, column in special_columns:
        key = column_info.get("key")

        if key == "__name":
            try:
                name = data.string_lookup[pk_value][LANGUAGE]
            except KeyError:
                logger.debug(
                    f"No name found for {model_cls!r} {pk_value!r}, using fallback value"
                )
                name = FALLBACK_NAME

            obj[column.name] = name

        elif key == "__icon":
            icon_key = column_info.get("icon_key", None)
            if icon_key is None:
                raise ValueError(
                    f"Expected an icon key for {column!r} in {model_cls!r}"
                )

            try:
                icon_name = cast(str, data.client_lookup[pk_value][icon_key])
            except KeyError:
                logger.debug(
                    f"No icon found for {model_cls!r} {pk_value!r}, using fallback value"
                )
                icon_name = {
                    "monster": FALLBACK_ACTOR_ICON,
                    "npc": FALLBACK_ACTOR_ICON,
                    "pet_skill": FALLBACK_SKILL_ICON,
                    "player_skill": FALLBACK_SKILL_ICON,
                    "monster_skill": FALLBACK_SKILL_ICON,
                }.get(tablename, FALLBACK_ITEM_ICON)
                obj[column.name] = icon_name
                continue

            if model_cls.__tablename__ in ("monster", "npc"):
                icon_name = f"{icon_name}.png"
            else:
                # Fix icon names so that it always fits the
                # format "<palette><size?>_\d{3}.png" format.
                # Somehow some icon names are fucked
                palette_name = icon_name[:3]
                number = int(icon_name[3:])

                # Workaround for monster skill icons which only have a smn24 palette
                # with 24px icons, instead of the default smn palette with 32px icons.
                if palette_name == "smn":
                    palette_name = "smn24"

                icon_name = f"{palette_name}_{number:0>3}.png"

            obj[column.name] = icon_name

        elif key == "__description":
            description_key = column_info.get("description_key", None)
            if description_key is None:
                raise ValueError(
                    f"Expected an description key for {column!r} in {model_cls!r}"
                )

            try:
                description_key_value = row[description_key]
                description = data.description_lookup[description_key_value][LANGUAGE]
            except KeyError:
                description = None

            obj[column.name] = description

    return pk_value, obj
