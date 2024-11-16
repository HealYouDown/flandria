from typing import TYPE_CHECKING, cast

from src.core.constants import LANGUAGE
from src.core.enums import ItemSetSlot
from src.updater.file_data import FileData
from src.updater.helpers import get_effects

if TYPE_CHECKING:
    from src.database.types import ModelCls
    from src.updater.schema import LoaderInfo

    from .types import T_STRATEGY_RETURN


def item_set(
    model_cls: "ModelCls",
    loader_info: "LoaderInfo",
) -> "T_STRATEGY_RETURN":
    from src.database.models import Effect, ItemSetItem

    data = FileData.from_files(loader_info.files)

    item_code_keys: list[tuple[str, ItemSetSlot]] = [
        ("무기", ItemSetSlot.WEAPON),
        ("상의", ItemSetSlot.COAT),
        ("하의", ItemSetSlot.PANTS),
        ("신발", ItemSetSlot.SHOES),
        ("장갑", ItemSetSlot.GAUNTLET),
        ("방패", ItemSetSlot.SHIELD),
        ("목걸이", ItemSetSlot.NECKLACE),
        ("귀걸이", ItemSetSlot.EARRING),
        ("반지1", ItemSetSlot.RING1),
        ("반지2", ItemSetSlot.RING2),
        ("옷", ItemSetSlot.DRESS),
        ("모자", ItemSetSlot.HAT),
    ]

    item_sets: list[dict] = []
    item_set_items: list[dict] = []
    effects: list[dict] = []

    for row in data.server_data:
        set_code = cast(str, row["코드"])
        name = data.string_lookup[set_code][LANGUAGE]

        item_sets.append(
            {
                "code": set_code,
                "name": name,
            }
        )
        effects.extend(get_effects(row, "item_set", set_code))

        for item_code_key, slot in item_code_keys:
            item_code = row[item_code_key]
            if item_code is not None:
                item_set_items.append(
                    {
                        "set_code": set_code,
                        "slot": slot,
                        "item_code": item_code,
                    }
                )

    return [
        (model_cls, item_sets),
        (ItemSetItem, item_set_items),
        (Effect, effects),
    ]
