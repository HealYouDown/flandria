from itertools import batched
from typing import TYPE_CHECKING, cast

from src.updater.file_data import FileData
from src.updater.helpers import get_effects

if TYPE_CHECKING:
    from src.database.types import ModelCls
    from src.updater.schema import LoaderInfo

    from .types import T_STRATEGY_RETURN


"""
Reference:
----------
{
    "Code": "ruoh0100",
    "InternalName": "한손검 LV1 근공 0 강화LV0",
    "UpgradeLevel": 0,
    "Effect0Code": 6,
    "Effect0Operator": "+",
    "Effect0Value": 0.0,
    "Effect1Code": 7,
    "Effect1Operator": "+",
    "Effect1Value": 0.0,
    "Effect2Code": -1,
    "Effect2Operator": "+",
    "Effect2Value": 0.0,
    "Effect3Code": -1,
    "Effect3Operator": "+",
    "Effect3Value": 0.0,
    "UpgradeCost": 0,
},
{
    "Code": "ruoh0101",
    "InternalName": "한손검 LV1 근공 0 강화LV1",
    "UpgradeLevel": 1,
    "Effect0Code": 6,
    "Effect0Operator": "+",
    "Effect0Value": 1.0,
    "Effect1Code": 7,
    "Effect1Operator": "+",
    "Effect1Value": 1.0,
    "Effect2Code": -1,
    "Effect2Operator": "+",
    "Effect2Value": 0.0,
    "Effect3Code": -1,
    "Effect3Operator": "+",
    "Effect3Value": 0.0,
    "UpgradeCost": 0,
},
{
    "Code": "ruoh0102",
    "InternalName": "한손검 LV1 근공 0 강화LV2",
    "UpgradeLevel": 2,
    "Effect0Code": 6,
    "Effect0Operator": "+",
    "Effect0Value": 2.0,
    "Effect1Code": 7,
    "Effect1Operator": "+",
    "Effect1Value": 2.0,
    "Effect2Code": -1,
    "Effect2Operator": "+",
    "Effect2Value": 0.0,
    "Effect3Code": -1,
    "Effect3Operator": "+",
    "Effect3Value": 0.0,
    "UpgradeCost": 0,
},
...
"""


def upgrade_rule(
    model_cls: "ModelCls",
    loader_info: "LoaderInfo",
) -> "T_STRATEGY_RETURN":
    from src.database.models import Effect

    data = FileData.from_files(loader_info.files)

    objects: list[dict] = []
    effects: list[dict] = []

    for rules in batched(data.server_data, 16):
        # used so that we can query all upgrade rules for a specific item
        base_code = cast(str, rules[0]["Code"])

        for row in rules:
            upgrade_rule_code = cast(str, row["Code"])
            level = row["UpgradeLevel"]
            cost = row["UpgradeCost"]

            objects.append(
                {
                    "code": upgrade_rule_code,
                    "base_code": base_code,
                    "level": level,
                    "cost": cost,
                }
            )
            effects.extend(get_effects(row, "upgrade_rule", upgrade_rule_code))

    return [
        (model_cls, objects),
        (Effect, effects),
    ]
