import sys
from typing import cast

from loguru import logger
from lxml import etree

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
        else:  # WearItems, AccessoryItems, StuffItems, EventItems
            assert "MainProbability" in element.attrib

            for child in element:
                assert "ItemCode" in child.attrib and "Amount" in child.attrib

                item_code = cast(str, child.get("ItemCode"))
                drops.append(
                    {
                        "monster_code": monster_code,
                        "item_code": item_code,
                        "quantity": int(cast(str, child.get("Amount"))),
                        "section_id": section_counter,
                        "section_probability": probability_to_float(
                            int(cast(str, element.get("MainProbability")))
                        ),
                        "item_probability": get_item_probability(child),
                    }
                )

            section_counter += 1

    return drops, money
