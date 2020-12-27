import os
import typing
import xml.etree.ElementTree as ET
import re

from webapp.models.enums import Area, QuestWorkType

from database_updater.constants import QUESTS_FOLDER


def _parse_mission(
    element: ET.Element,
    quest_code: str
) -> typing.List[dict]:
    """Parses the quest element 'Mission'.

    Args:
        element (ET.Element): The XML element.
        quest_code (str): The quest code.

    Returns:
        typing.List[dict]: List with all defined missions.
    """
    missions = []

    for mission_element in element:
        try:
            work_type = QuestWorkType(int(mission_element.get("WorkType")))
        except ValueError:
            # Unknown or excluded work types are skipped
            continue

        mission = {
            "work_type": work_type,
            "quest_code": quest_code,
            "count": int(mission_element.get("Count")),
        }

        # Parse position (e.g. BF2 2939.00 44808.00")
        work_pos = mission_element.get("WorkPos", None)

        if not work_pos or work_pos.startswith("_no_use"):
            mission.update({
                "map_code": None,
                "x": None,
                "y": None,
            })
        else:
            work_pos_splitted = work_pos.split(" ")

            # remove _1b (or anything like that) from the map code and add _000
            # for map relationships
            map_code = "{0}_000".format(
                work_pos_splitted[0].split("_")[0].upper())

            mission.update({
                "map_code": map_code,
                "x": float(work_pos_splitted[1]),
                "y": float(work_pos_splitted[2])
            })

        # All missions have different goals, like equipping an item, killing
        # monsters. Therefore, different columns are needed and some will be
        # None. By default, we set all to none and only update the ones
        # we need based on the work type.
        # For some work types, all columns stay none.
        mission.update({
            "npc_code": None,
            "item_code": None,
            "monster_code": None,
            "quest_item_code": None,
        })

        work_value = mission_element.get("WorkValue")
        mission["work_value"] = work_value

        if work_type == QuestWorkType.deliver_item:
            mission["item_code"] = work_value

        elif work_type in [QuestWorkType.talk_to_npc,
                           QuestWorkType.convoy_npc,
                           QuestWorkType.talk_to_npc]:
            mission["npc_code"] = work_value

        elif work_type == QuestWorkType.kill_monster:
            mission["monster_code"] = work_value

        elif work_type == QuestWorkType.collect_quest_item:
            mission["quest_item_code"] = work_value

        missions.append(mission)

    return missions


def _parse_reward_desc(
    element: ET.Element,
    quest_code: str
) -> typing.Tuple[dict, list]:
    """Parses quest element 'RewardDesc'.

    Args:
        element (ET.Element): The XML element.
        quest_code (str): The quest code.

    Returns:
        typing.Tuple[dict, list]: Returns a dict with informations
            about the npc, money, exp, etc. as well as a list
            with all items that can be selected, if there are any.
    """
    # Parse the root element tag with reward information
    reward_information = {
        "end_npc_code": element.get("Supplier"),
        "experience": int(element.get("Exp")),
        "money": int(element.get("Money")),
        "selectable_items_count": int(element.get("SelectableCount"))
    }

    # Parse selectable items
    select_items_element = element[0]

    selectable_items = [
        {
            "item_code": item.get("ItemCode"),
            "amount": int(item.get("Amount")),
            "quest_code": quest_code,
        } for item in select_items_element
    ]

    return reward_information, selectable_items


def _parse_give_desc(
    element: ET.Element,
    quest_code: str
) -> typing.List[dict]:
    """Parses quest element 'GiveDesc'.

    Args:
        element (ET.Element): The XML element.
        quest_code (str): The quest code from the main quest, which
            is added to each item to be able to join them to the
            quest later.

    Returns:
        typing.List[dict]: Returns a list with all items that
            have to be delivered to an npc. List can be empty.
    """
    return [
        {
            "item_code": item.get("ItemCode"),
            "amount": int(item.get("Amount")),
            "quest_code": quest_code,
        } for item in element
    ]


def _parse_occur_term(
    element: ET.Element
) -> dict:
    """Parses quest element 'OccurTerm'.

    Args:
        element (ET.Element): The XML element.

    Returns:
        dict: Dict with parsed values.
    """
    res = {}

    # Level
    res["level"] = element.get("Lv")

    # Area
    res["area"] = Area(int(element.get("LvType")))

    # Before quest
    before_quest_code = element.get("BeforeQuest")
    if before_quest_code:
        res["before_quest_code"] = before_quest_code

    # Classes
    # Class0 = Merc, Class1 = Pirate (?), Class2 = Explorer, Class3 = Noble
    # Class4 = Saint
    letters = []
    for i in range(0, 5):
        if i == 1:
            continue

        # Check if attrib is true
        is_quest_for_class = bool(int(element.get(f"Class{i}")))

        if is_quest_for_class:
            letters.append({
                "0": "W",
                "2": "E",
                "3": "N",
                "4": "S"
            }[str(i)])

    res["class_"] = "".join(letters)

    return res


def _parse_quest_file(
    filepath: str,
) -> typing.Dict[str, typing.Union[list, dict]]:
    """[summary]

    Args:
        filepath (str): [description]

    Returns:
        typing.Dict[str, dict]: [description]
    """
    parser = ET.XMLParser(encoding="utf-8")

    # Create element tree from xml file
    tree = ET.parse(filepath, parser=parser)
    root = tree.getroot()

    # Parse root 'Quest' Element
    quest = {
        "code": root.get("QuestCode"),
        "start_npc_code": root.get("SourceObject"),
        "start_area_code": root.get("SourceArea"),
    }

    # Get quest code as it is needed multiple times later
    quest_code = quest.get("code")

    # Parse children tags
    for element in root:
        if element.tag == "OccurTerm":
            quest.update(_parse_occur_term(element))
        elif element.tag == "GiveDesc":
            give_items = _parse_give_desc(element, quest_code)
        elif element.tag == "RewardDesc":
            reward_information, selectable_items = _parse_reward_desc(
                element, quest_code)
            # Update quest data with reward information
            quest.update(reward_information)
        elif element.tag == "Mission":
            missions = _parse_mission(element, quest_code)

    return {
        "quest": quest,
        "give_items": give_items,
        "selectable_items": selectable_items,
        "missions": missions,
    }


def parse_string_data_file(filepath: str, language: str) -> typing.List[dict]:
    """Parses the given quest string file. Adds a language attribute to each
    dict.

    Args:
        filepath (str): The path to the file.
        language (str): Language key to add to each row.

    Returns:
        typing.List[dict]: List with dicts containing the quest description
            data.
    """
    pattern = re.compile(
        r"\[(?P<quest_code>.*)\][\r\n]Title=(?P<title>.*)[\r\n]Mission1=(?P<mission_1>.*)[\r\n]Mission2=(?P<mission_2>.*)[\r\n]Mission3=(?P<mission_3>.*)[\r\n]desc=(?P<description>.*)[\r\n]preDlg=(?P<pre_dialog>.*)[\r\n]startDlg=(?P<start_dialog>.*)[\r\n]runDlg=(?P<run_dialog>.*)[\r\n]finishDlg=(?P<finish_dialog>.*)"  # noqa: E501
    )

    with open(filepath, "r", encoding="utf-16") as fp:
        matches = [match.groupdict()
                   for match in re.finditer(pattern, fp.read())]

    for match in matches:
        for key, value in match.items():
            # All lines with < 3 characters are None. Often times
            # there is just a . to indiate that its empty
            if len(value) < 3:
                match[key] = None
            else:
                match[key] = value.strip()

        # Add language key to each row
        match["language"] = language

    return matches


def parse_quests() -> typing.List[typing.Dict[str, typing.Union[list, dict]]]:
    # We parse QuestIndex.xml to figure out which quests we all want.
    # (There are A LOT of unused quests that break a lot of things..)
    tree = ET.parse(os.path.join(QUESTS_FOLDER, "QuestIndex.xml"),
                    parser=ET.XMLParser(encoding="utf-8"))
    root = tree.getroot()

    quests = [
        _parse_quest_file(os.path.join(QUESTS_FOLDER, f"{element.tag}.xml"))
        for element in root
    ]

    return quests
