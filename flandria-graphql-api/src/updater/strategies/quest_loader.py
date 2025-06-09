import configparser
import os
from typing import TYPE_CHECKING, Any, cast

from loguru import logger
from lxml import etree

from src.core.constants import UPDATER_DATA_PATH
from src.core.enums import QuestMissionType
from src.updater.transforms import probability_to_float

if TYPE_CHECKING:
    from src.database.types import ModelCls
    from src.updater.schema import LoaderInfo

    from .types import T_STRATEGY_RETURN


def quest(
    model_cls: "ModelCls",
    loader_info: "LoaderInfo",
) -> "T_STRATEGY_RETURN":
    from src.database.models import (
        Drop,
        QuestGiveItem,
        QuestMission,
        QuestRewardItem,
    )

    quest_index_fpath = os.path.join(
        UPDATER_DATA_PATH,
        loader_info.files.extra_files[0],
    )
    quest_description_fpath = os.path.join(
        UPDATER_DATA_PATH,
        loader_info.files.extra_files[1],
    )

    quest_descriptions: dict[str, dict[str, str | None]] = {}

    description_parser = configparser.ConfigParser(allow_no_value=True, strict=False)
    description_parser.read(quest_description_fpath, encoding="utf-16")

    for quest_code in description_parser:
        if quest_code == description_parser.default_section:
            continue

        descriptions = {}
        for key in (
            "Title",
            "Mission1",
            "Mission2",
            "Mission3",
            "desc",
            "preDlg",
            "startDlg",
            "runDlg",
            "finishDlg",
        ):
            value = description_parser[quest_code][key]
            value = value.strip()
            # Strings with less than 3 chars are set as None
            # Sometimes a '.' is used as a filler character, so we
            # want to ignore those (and empty descriptions)
            value = value if len(value) > 3 else None
            descriptions[key] = value
        quest_descriptions[quest_code] = descriptions

    xml_parser = etree.XMLParser(encoding="utf-8")

    # Parse the QuestIndex.xml file to get all quest filenames
    index_tree = etree.parse(quest_index_fpath, xml_parser)
    quest_codes: list[str] = [element.tag for element in index_tree.getroot()]

    quests: list[dict] = []
    give_items: list[dict] = []
    reward_items: list[dict] = []
    missions: list[dict] = []
    drops: list[dict] = []
    for quest_code in quest_codes:
        quest_fpath = os.path.join(UPDATER_DATA_PATH, f"{quest_code}.xml")
        if not os.path.exists(quest_fpath):
            logger.warning(f"Missing quest file for {quest_code!r} (skipped)")
            continue

        if quest_code not in quest_descriptions:
            logger.warning(f"Missing quest descriptions for {quest_code!r} (skipped)")
            continue

        tree = etree.parse(quest_fpath, parser=xml_parser)
        root = tree.getroot()

        quest_description = quest_descriptions[quest_code]
        quest_obj: dict[str, Any] = {
            "code": quest_code,
            "start_npc_code": root.get("SourceObject"),
            "start_area_code": root.get("SourceArea"),
            "title": quest_description["Title"],
            "description": quest_description["desc"],
            "pre_dialog": quest_description["preDlg"],
            "start_dialog": quest_description["startDlg"],
            "run_dialog": quest_description["runDlg"],
            "finish_dialog": quest_description["finishDlg"],
        }

        for element in root:
            if element.tag == "OccurTerm":
                required_keys = {"Lv", "LvType", "Class0", "Class2", "Class3", "Class4"}
                if not all(key in element.keys() for key in required_keys):
                    logger.warning(
                        f"Missing required key on tag {element.tag!r} in {quest_code!r}"
                    )

                quest_obj.update(
                    {
                        # previous quest code sometimes is a "empty" string, but with some spaces, so ternary it is
                        "previous_quest_code": (
                            element.get("BeforeQuest", None)
                            if element.get("BeforeQuest", None)
                            else None
                        ),
                        "level": int(cast(str, element.get("Lv"))),
                        "is_sea": bool(int(cast(str, element.get("LvType")))),
                        "is_mercenary": bool(int(cast(str, element.get("Class0")))),
                        # probably pirate
                        # "pirate": bool(int(element.get("Class1"))),
                        "is_explorer": bool(int(cast(str, element.get("Class2")))),
                        "is_noble": bool(int(cast(str, element.get("Class3")))),
                        "is_saint": bool(int(cast(str, element.get("Class4")))),
                    }
                )

            elif element.tag == "GiveDesc":
                for give_item in element:
                    required_keys = {"ItemCode", "Amount"}
                    if not all(key in give_item.keys() for key in required_keys):
                        logger.warning(
                            f"Missing required key on tag GiveDesc-Item in {quest_code!r}"
                        )

                    give_items.append(
                        {
                            "quest_code": quest_code,
                            "item_code": cast(str, give_item.get("ItemCode")),
                            "amount": int(cast(str, give_item.get("Amount"))),
                        }
                    )

            elif element.tag == "RewardDesc":
                required_keys = {"Exp", "Money", "SelectableCount"}
                if not all(key in element.keys() for key in required_keys):
                    logger.warning(
                        f"Missing required key on tag {element.tag!r} in {quest_code!r}"
                    )

                quest_obj.update(
                    {
                        "end_npc_code": element.get("Supplier", None),
                        "experience": int(cast(str, element.get("Exp"))),
                        "money": int(cast(str, element.get("Money"))),
                        "selectable_items_count": int(
                            cast(str, element.get("SelectableCount"))
                        ),
                    }
                )

                select_items = element.find("SelectItems")
                if select_items is not None:
                    for select_item in select_items:
                        required_keys = {"ItemCode", "Amount"}
                        if not all(key in select_item.keys() for key in required_keys):
                            logger.warning(
                                f"Missing required key on tag SelectItems-Item in {quest_code!r}"
                            )

                        reward_items.append(
                            {
                                "quest_code": quest_code,
                                "item_code": select_item.get("ItemCode"),
                                "amount": int(cast(str, select_item.get("Amount"))),
                            }
                        )

            elif element.tag == "LootDesc":
                required_keys = {"MonsterCode", "Rate", "ItemCode"}
                for loot in element:
                    if not all(key in loot.keys() for key in required_keys):
                        logger.warning(
                            f"Missing required key on tag LootDesc-Loot in {quest_code!r}"
                        )
                        continue

                    monster_code = loot.get("MonsterCode")
                    drop_rate = int(cast(int, loot.get("Rate")))
                    item_code = loot.get("ItemCode")

                    drops.append(
                        {
                            "quantity": 1,
                            "probability": probability_to_float(drop_rate),
                            "monster_code": monster_code,
                            "item_code": item_code,
                        }
                    )

            elif element.tag == "RunTerm":
                # XXX: Maybe whether the quest requires 50% kill participation
                # idk?
                pass

            elif element.tag == "CheckItemDesc":
                # idk, empty tag
                pass

            elif element.tag == "Mission":
                mission_descriptions = [
                    quest_description["Mission1"],
                    quest_description["Mission2"],
                    quest_description["Mission3"],
                ]
                for mission, description in zip(element, mission_descriptions):
                    required_keys = {"WorkType", "WorkValue", "Count"}
                    if "WorkType" not in mission.keys():
                        logger.warning(
                            f"Missing required key on mission in {quest_code!r}"
                        )
                        continue

                    mission_obj = {
                        "quest_code": quest_code,
                        "count": int(cast(str, mission.get("Count"))),
                        "description": description,
                    }

                    work_type_value = int(cast(str, mission.get("WorkType")))
                    if work_type_value not in QuestMissionType._value2member_map_:
                        logger.warning(
                            f"Found excluded mission work type {work_type_value!r} for quest {quest_code!r}"
                        )
                        continue

                    work_type = QuestMissionType(work_type_value)
                    mission_obj["work_type"] = work_type

                    work_pos = mission.get("WorkPos")
                    if work_pos is None or work_pos.lower().startswith("_no_use"):
                        mission_obj.update({"x": None, "y": None, "map_code": None})
                    else:
                        # value e.g. BF2_1b 2939.00 44808.00"
                        map_code, x_str, y_str = work_pos.split(" ")
                        mission_obj.update(
                            {
                                "map_code": f"{map_code.split('_')[0]}_000".upper(),
                                "x": float(x_str),
                                "y": float(y_str),
                            }
                        )

                    work_value_key = {
                        QuestMissionType.DELIVER_ITEM: "item_code",
                        QuestMissionType.KILL_MONSTER: "monster_code",
                        QuestMissionType.COLLECT_QUEST_ITEM: "quest_item_code",
                        QuestMissionType.TALK_TO_NPC: "npc_code",
                        QuestMissionType.PROTECT_NPC: "npc_code",
                        QuestMissionType.LISTEN_TO_NPC: "npc_code",
                    }.get(work_type, None)
                    if work_value_key is not None:
                        mission_obj[work_value_key] = cast(
                            str, mission.get("WorkValue")
                        )

                    missions.append(mission_obj)
            else:
                logger.error(f"Unhandeled tag in quest {quest_code!r}: {element.tag!r}")

        quests.append(quest_obj)

    return [
        (model_cls, quests),
        (QuestRewardItem, reward_items),
        (QuestGiveItem, give_items),
        (QuestMission, missions),
        (Drop, drops),
    ]
