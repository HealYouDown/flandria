import os
from typing import TYPE_CHECKING, cast

from lxml import etree

from src.core.case_insensitive_dict import CaseInsensitiveDict
from src.core.constants import UPDATER_DATA_PATH
from src.updater.parsers import parse_dat

if TYPE_CHECKING:
    from src.database.types import ModelCls
    from src.updater.schema import LoaderInfo

    from .types import T_STRATEGY_RETURN


def npc_store_item(
    model_cls: "ModelCls",
    _: "LoaderInfo",
) -> "T_STRATEGY_RETURN":
    store_fpath = os.path.join(UPDATER_DATA_PATH, "StoreData.xml")
    keyword_fpath = os.path.join(UPDATER_DATA_PATH, "Keyword_En.dat")

    # Maps keywords to their english translation
    keywords: CaseInsensitiveDict[str] = CaseInsensitiveDict(
        data={
            row["key"]: row["value"]
            for row in parse_dat(
                keyword_fpath,
                headers=["index", "type", "key", "value"],
            )
        }
    )

    xml_parser = etree.XMLParser(encoding="utf-8")
    tree = etree.parse(store_fpath, parser=xml_parser)

    objects: list[dict] = []
    for npc_element in tree.getroot():
        npc_code = npc_element.get("NpcCode")
        # npc_class = int(npc_element.get("MerchantClass"))
        for section_element in npc_element:
            section_name = keywords.get(
                cast(str, section_element.get("SectionName")),
                section_element.get("SectionName"),
            )
            page_name = keywords.get(
                cast(str, section_element.get("SectionType")),
                section_element.get("SectionType"),
            )

            for item_element in section_element:
                item_code = item_element.get("ItemCode")

                objects.append(
                    {
                        "npc_code": npc_code,
                        # "npc_class": npc_class,
                        "section_name": section_name,
                        "page_name": page_name,
                        "item_code": item_code,
                    }
                )

    return [(model_cls, objects)]
