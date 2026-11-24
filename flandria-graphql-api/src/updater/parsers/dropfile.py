import sys
from typing import cast

from loguru import logger
from lxml import etree

from src.core.enums import DropDistribution
from src.updater.transforms import probability_to_float


def get_item_probability(element: etree._Element, total: int = 10_000) -> float:
    # typos are nice, wonder how florensia handles them (:
    keys = ["Probapility", "Probability"]

    for key in keys:
        if key in element.attrib:
            value = int(cast(str, element.get(key)))
            return probability_to_float(value, total=total)
    else:
        logger.error("Missing probability key on element")
        sys.exit(1)


def parse_dropfile(path: str, monster_code: str):
    xml_parser = etree.XMLParser(encoding="utf-8")
    tree = etree.parse(path, xml_parser)

    drops: list[dict] = []
    money: dict | None = None

    section_counter = 0
    for element in tree.getroot():
        if element.tag == "Money":
            assert "LeastMoney" in element.attrib and "MaxMoney" in element.attrib

            assert money is None  # Duplicate money tags? lol
            money = {
                "monster_code": monster_code,
                "min": int(float(cast(str, element.get("LeastMoney")))),
                "max": int(float(cast(str, element.get("MaxMoney")))),
                "probability": get_item_probability(element),
            }
        else:  # WearItems, AccessoryItems, Materials, BossItems1, ... (any name)
            assert "MainProbability" in element.attrib

            # In a guaranteed section every item drops, probabilities are ignored
            guaranteed = element.get("Guaranteed", "0") != "0"

            for child in element:
                assert "ItemCode" in child.attrib and "Amount" in child.attrib

                item_code = cast(str, child.get("ItemCode"))
                max_per_player = int(child.get("MaxPerPlayer", "0"))
                drops.append(
                    {
                        "monster_code": monster_code,
                        "item_code": item_code,
                        "quantity": int(cast(str, child.get("Amount"))),
                        "section_id": section_counter,
                        "section_guaranteed": guaranteed,
                        "section_probability": 1.0
                        if guaranteed
                        else probability_to_float(
                            int(cast(str, element.get("MainProbability")))
                        ),
                        "item_probability": 1.0
                        if guaranteed
                        else get_item_probability(child),
                        "distribution": DropDistribution(
                            int(child.get("Distribution", "0"))
                        ),
                        "max_per_player": max_per_player or None,
                        "bypass_level": child.get("BypassLevel", "0") != "0",
                    }
                )

            section_counter += 1

    return drops, money
