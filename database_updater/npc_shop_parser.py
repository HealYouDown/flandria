import typing
import os
import xml.etree.ElementTree as ET
from database_updater.constants import TEMP_FOLDER


def parse_npc_shop_data() -> typing.List[dict]:
    # Path to the downloaded .xml file
    filepath = os.path.join(TEMP_FOLDER, "StoreData.xml")

    # Get root element of xml
    xmlp = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(filepath, parser=xmlp)
    root = tree.getroot()

    items = []
    # Parse xml structure
    for npc in list(root):
        for section in list(npc):
            for item in list(section):
                items.append({
                    "npc_code": npc.attrib.get("NpcCode"),
                    "npc_class": int(npc.attrib.get("MerchantClass")),
                    "section_name": section.attrib.get("SectionName"),
                    "section_type": section.attrib.get("SectionType"),
                    "item_code": item.attrib.get("ItemCode"),
                })

    return items
