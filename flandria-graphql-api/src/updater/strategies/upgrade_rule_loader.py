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
    "코드": "ruoh0100",
    "이름": "한손검 LV1 근공 0 강화LV0",
    "업그레이드레벨": 0,
    "효과코드0": 6,
    "연산자0": "+",
    "효과값0": 0.0,
    "효과코드1": 7,
    "연산자1": "+",
    "효과값1": 0.0,
    "효과코드2": -1,
    "연산자2": "+",
    " 효과값2": 0.0,
    "효과코드3": -1,
    "연산자3": "+",
    "효과값3": 0.0,
    "강화소모gelt": 0,
},
{
    "코드": "ruoh0101",
    "이름": "한손검 LV1 근공 0 강화LV1",
    "업그레이드레벨": 1,
    "효과코드0": 6,
    "연산자0": "+",
    "효과값0": 1.0,
    "효과코드1": 7,
    "연산자1": "+",
    "효과값1": 1.0,
    "효과코드2": -1,
    "연산자2": "+",
    "효과값2": 0.0,
    "효과코드3": -1,
    "연산자3": "+",
    "효과값3": 0.0,
    "강화소모gelt": 0,
},
{
    "코드": "ruoh0102",
    "이름": "한손검 LV1 근공 0 강화LV2",
    "업그레이드레벨": 2,
    "효과코드0": 6,
    "연산자0": "+",
    "효과값0": 2.0,
    "효과코드1": 7,
    "연산자1": "+",
    "효과값1": 2.0,
    "효과코드2": -1,
    "연산자2": "+",
    " 효과값2": 0.0,
    "효과코드3": -1,
    "연산자3": "+",
    "효과값3": 0.0,
    "강화소모gelt": 0,
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
    for row in data.server_data:
        upgrade_rule_code = cast(str, row["코드"])

        # used so that we can query all upgrade rules for a specific item
        base_code = f"{upgrade_rule_code[:-2]}00"
        level = row["업그레이드레벨"]
        cost = row["강화소모gelt"]

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
