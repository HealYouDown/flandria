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


def _load_keywords() -> CaseInsensitiveDict[str]:
    # Maps keywords to their english translation
    keyword_fpath = os.path.join(UPDATER_DATA_PATH, "Keyword_En.dat")
    return CaseInsensitiveDict(
        data={
            row["key"]: row["value"]
            for row in parse_dat(
                keyword_fpath,
                headers=["index", "type", "key", "value"],
            )
        }
    )


def npc_exchange_item(
    model_cls: "ModelCls",
    _: "LoaderInfo",
) -> "T_STRATEGY_RETURN":
    from src.database.models import NpcExchangeMaterial

    exchange_fpath = os.path.join(UPDATER_DATA_PATH, "ExchangeData.xml")
    keywords = _load_keywords()

    xml_parser = etree.XMLParser(encoding="utf-8")
    tree = etree.parse(exchange_fpath, parser=xml_parser)

    exchanges: list[dict] = []
    materials: list[dict] = []
    for npc_element in tree.getroot():
        npc_code = npc_element.get("NpcCode")
        for section_element in npc_element:
            section_name = section_element.get("SectionName")
            page_name = section_element.get("SectionType")

            for item_element in section_element:
                index = len(exchanges)
                exchanges.append(
                    {
                        "index": index,
                        "npc_code": npc_code,
                        "section_name": keywords.get(
                            cast(str, section_name), section_name
                        ),
                        "page_name": keywords.get(cast(str, page_name), page_name),
                        "item_code": item_element.get("ItemCode"),
                        "quantity": int(item_element.get("Amount", "1")),
                        "gelt": int(item_element.get("Gelt", "0")),
                    }
                )
                materials += [
                    {
                        "exchange_index": index,
                        "item_code": material_element.get("ItemCode"),
                        "quantity": int(material_element.get("Amount", "1")),
                    }
                    for material_element in item_element
                ]

    return [(model_cls, exchanges), (NpcExchangeMaterial, materials)]


def npc_store_item(
    model_cls: "ModelCls",
    _: "LoaderInfo",
) -> "T_STRATEGY_RETURN":
    store_fpath = os.path.join(UPDATER_DATA_PATH, "StoreData.xml")
    keywords = _load_keywords()

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
