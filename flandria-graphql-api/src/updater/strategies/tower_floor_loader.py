from typing import TYPE_CHECKING

from src.updater.file_data import FileData
from src.updater.helpers import map_row_to_model

if TYPE_CHECKING:
    from src.database.types import ModelCls
    from src.updater.schema import LoaderInfo

    from .types import T_STRATEGY_RETURN


def tower_floor(
    model_cls: "ModelCls",
    loader_info: "LoaderInfo",
) -> "T_STRATEGY_RETURN":
    from src.database.models import TowerFloorMonster

    data = FileData.from_files(loader_info.files)

    tower_floors: list[dict] = []
    tower_floor_monsters: list[dict] = []
    for row in data.server_data:
        pk, obj = map_row_to_model(model_cls, row, data)

        for i in range(1, 11):
            monster_code = row[f"몬스터KEY_{i}"]
            amount = row[f"몬스터갯수_{i}"]

            if monster_code is not None:
                tower_floor_monsters.append(
                    {
                        "floor_code": pk,
                        "monster_code": monster_code,
                        "amount": amount,
                    }
                )

        tower_floors.append(obj)

    return [
        (model_cls, tower_floors),
        (TowerFloorMonster, tower_floor_monsters),
    ]
