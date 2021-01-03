import json
import os
import re
import typing

from flask import current_app
from flask_sqlalchemy.model import DefaultMeta
from webapp.extensions import db
from webapp.models import (ItemList, Map, Quest, QuestDescription,
                           QuestGiveItem, QuestMission, QuestSelectableItem,
                           StatusData)
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.enums import ProductionType, SealOptionType

from database_updater.constants import LANGUAGE, QUESTS_FOLDER, TEMP_FOLDER
from database_updater.converter import bin2list, dat2list
from database_updater.json_encoder import CustomJsonEncoder
from database_updater.model_lists import ITEMLIST_MODELS, MODELS
from database_updater.npc_shop_parser import parse_npc_shop_data
from database_updater.quest_parser import parse_quests, parse_string_data_file
from database_updater.update_icons import get_icon_name
from database_updater.status_points_parser import parse_status_points


def get_mapping_from_model(model: DefaultMeta) -> typing.Dict[str, dict]:
    """Creates a mapping from the defined model columns.
    Mapping looks like that:
    {
        mapper_key: {
            name: column_name,
            transform: function or None
        }
    }

    Args:
        model (DefaultMeta): The model.

    Returns:
        typing.Dict[str, dict]: The mapping in form of a dict.
    """
    mapping = {}

    for column in list(model.__table__.columns):
        if not isinstance(column, CustomColumn):
            continue

        mapping[column.mapper_key] = {
            "name": column.name,
            "transform": getattr(column, "transform", None)
        }

    return mapping


def update_database(tables: typing.Tuple[str]) -> None:
    # TODO / FIXME: Split loops into functions

    # Determine what tables have to be created based on
    # the given argument
    models_to_create = MODELS

    if tables:
        models_to_create = [
            model for model in MODELS
            if model.__tablename__ in tables]

    # Clear itemlist table
    ItemList.query.delete()

    # Insert status data
    current_app.logger.info("Inserting status data.")
    data = parse_status_points()
    StatusData.query.delete()

    db.session.bulk_insert_mappings(StatusData, data)

    # Insert quests
    if not tables or "quest" in tables:
        current_app.logger.info("Inserting quests.")
        # Clear models
        QuestDescription.query.delete()
        Quest.query.delete()
        QuestGiveItem.query.delete()
        QuestMission.query.delete()
        QuestSelectableItem.query.delete()

        # Insert description data
        files = [
            ("StringData_EN.ini", "en"),
            ("StringData_CN.ini", "cn"),
            ("StringData_ESP.ini", "es"),
            ("StringData_FR.ini", "fr"),
            ("StringData_GER.ini", "de"),
            ("StringData_IT.ini", "it"),
            ("StringData_JP.ini", "jp"),
            ("StringData_KR.ini", "kr"),
            ("StringData_PT.ini", "pt"),
            ("StringData_TR.ini", "tr"),
            ("StringData_TW.ini", "tw"),
        ]

        # Dict is used to map quests a title.
        quest_code_to_title = {}

        for fname, local in files:
            # Create path and parse file
            path = os.path.join(QUESTS_FOLDER, fname)
            descriptions = parse_string_data_file(path, local)

            if local == "en":
                for desc in descriptions:
                    quest_code_to_title[desc["quest_code"]] = desc["title"]

            # Insert
            db.session.bulk_insert_mappings(QuestDescription, descriptions)

        # Insert quests
        quests = []
        missions = []
        give_items = []
        selectable_items = []

        for index, quest_obj in enumerate(parse_quests()):
            for key, value in quest_obj.items():
                if key == "quest":
                    # Add title to quest, if no title was found
                    # we skip this one.
                    quest_code = value["code"]
                    quest_title = quest_code_to_title.get(quest_code, None)

                    if quest_title:
                        value["title"] = quest_title
                        value["index"] = index
                        quests.append(value)
                    else:
                        current_app.logger.warning((
                            f"Skipped quest.{quest_code} because "
                            "no title was found."))
                        break

                elif key == "give_items" and value:
                    give_items.extend(value)
                elif key == "missions" and value:
                    missions.extend(value)
                elif key == "selectable_items":
                    selectable_items.extend(value)

        db.session.bulk_insert_mappings(Quest, quests)
        db.session.bulk_insert_mappings(QuestMission, missions)
        db.session.bulk_insert_mappings(QuestSelectableItem, selectable_items)
        db.session.bulk_insert_mappings(QuestGiveItem, give_items)

    for index, model in enumerate(models_to_create):
        # Log process
        msg = (f"Creating table {model.__tablename__} "
               f"({index+1}/{len(models_to_create)}).")
        current_app.logger.info(msg)

        # Get tablename
        tablename = model.__tablename__

        # Options for the specific model
        options = model._mapper_utils.get("options", {})
        image_key = options.get("image_key", "아이콘")
        description_key = options.get("description_key", None)

        # Filters to filter out item rows (e.g. only Rapiers, ..)
        model_filter = model._mapper_utils.get("filter", None)

        # Get mapping of model, e.g. {'코드': {'name': 'code', 'transform': None}
        # to map the file content to the specific column
        mapping = get_mapping_from_model(model)

        # Load and store given files inside model declaration
        server_data = []
        client_data = []
        string_data = []
        skill_data = []
        description_data = []

        for key, filenames in model._mapper_utils["files"].items():
            for fname in filenames:
                fpath = os.path.join(TEMP_FOLDER, fname)
                if fname.endswith(".bin"):
                    data = bin2list(fpath)
                elif fname.endswith(".dat"):
                    data = dat2list(fpath)

                if key == "server":
                    server_data.extend(data)
                elif key == "client":
                    client_data.extend(data)
                elif key == "string":
                    string_data.extend(data)
                elif key == "skill":
                    skill_data.extend(data)
                elif key == "description":
                    description_data.extend(data)

        # Create dicts from server_data and mapping configuration
        items: typing.List[dict] = []

        # Some tables need some specific things to be done, everything
        # else is done through the same algorithm to map files to models.
        if tablename == "monster_message":
            # Monster messages are mapped by client file to string file
            for row in client_data:
                item = {}

                for key, value in row.items():
                    column_mapping_config = mapping[key]

                    column_name = column_mapping_config["name"]
                    if column_name == "code":
                        item[column_name] = value

                    else:
                        # Parse the string file for the message
                        # value is here the row key to map to.
                        # e.g. obchpld00 or None, if there are no
                        # messages.
                        if not value:
                            continue

                        message_row = [row for row in string_data
                                       if row["Code"] == value]

                        if message_row:
                            item[column_name] = message_row[0][LANGUAGE]

                items.append(item)

        elif tablename == "npc_shop_item":
            items = parse_npc_shop_data()

        elif tablename == "map":
            items = [Map._parse_row(row) for row in string_data]

        else:
            # Standard algorithm to map files to model
            for index, row in enumerate(server_data):
                # Item dict to store information in. Tablename is
                # always given, but not always used. Only in ItemList.
                item = {
                    "table": tablename
                }

                # If a filter is defined and the row does not pass the
                # given filter, it is skipped.
                if model_filter is not None and not model_filter(row):
                    continue

                # Go through all data of the item defined in the file
                for key, value in row.items():
                    # Skip data that we are not interested in
                    if key not in mapping:
                        continue

                    # Get the configuration for specific column
                    column_mapping_config = mapping[key]

                    # If a transform function is given, apply it
                    transform_function = column_mapping_config["transform"]
                    transform_function: typing.Union[None, typing.Callable]

                    if transform_function:
                        value = transform_function(value)

                    item[column_mapping_config["name"]] = value

                # Now only _name, _icon (and _description) are left that have
                # to be dealt with. Maybe some other keys that have some
                # specific function.
                for key in mapping:
                    if key == "_name":
                        # Get the code (key that links string data and server
                        # data) and make it all lowercase for easier comparing
                        code = item["code"].lower()

                        # Get the name row from string data that contains the
                        # code
                        name_row = [row for row in string_data
                                    if row["Code"].lower() == code]

                        if name_row:
                            # Add name to item dict
                            item["name"] = name_row[0][LANGUAGE]
                        else:
                            # Skip item and log an error
                            current_app.logger.warning((
                                f"Skipped {tablename}.{code} because "
                                "no name was found."))
                            break

                    elif key == "_icon":
                        # Same as for _name but with client_data
                        code = item["code"].lower()

                        icon_row = [row for row in client_data
                                    if row["코드"].lower() == code]

                        if icon_row:
                            if tablename in ["monster", "npc"]:
                                # Monster and NPC icons are formatted right
                                item["icon"] = f"{icon_row[0][image_key]}.png"
                            else:
                                # Convert icons like abc12 to abc012, ...
                                icon_match = re.match(
                                    r"^(\D*)(\d*)$",
                                    f"{icon_row[0][image_key]}")
                                icon_name = icon_match.group(1)
                                icon_num = int(icon_match.group(2))

                                item["icon"] = get_icon_name(icon_name,
                                                             icon_num)
                        else:
                            current_app.logger.warning((
                                f"Skipped {tablename}.{code} because "
                                "no icon was found."))
                            break

                    elif key == "_description":
                        # Same as for _name but with description_data
                        code = row[description_key].lower()

                        desc_row = [row for row in description_data
                                    if row["Code"].lower() == code]

                        # Not all items have description, so we do not skip
                        # the item if it doesn't.
                        if desc_row:
                            item["description"] = desc_row[0][LANGUAGE]

                    elif key == "_premium_essence":
                        # Premium essences are all listed in division 1
                        if (item["production_type"] == ProductionType.essence
                                and item["division"] == 1):
                            item["is_premium_essence"] = True
                        else:
                            item["is_premium_essence"] = False

                    elif key == "_seal_option_type":
                        item["seal_option_type"] = SealOptionType(item["code"])

                else:
                    # If loop was not stopped by break (that means skip the
                    # item), we add the item to the list.
                    item["index"] = index
                    items.append(item)

            # After everything is done, some tables need a bit of cleanup
            # which cannot be done in the above loops.
            if tablename == "seal_option":
                # Remove option_codes if there is no chance for them
                # to even appear
                # Reason: If tables are joined loaded later this will
                # reduce the amount of relationships that have to be
                # initalized. (I think, idk. Sounds logically to me though)
                for item in items:
                    for i in range(0, 63):
                        if item[f"option_{i}_chance"] is None:
                            item[f"option_{i}_code"] = None

        # Clear table
        model.query.delete()

        # (Re-)popuplate table
        db.session.bulk_insert_mappings(model, items)

        # Add to item_list if model should be included
        if model in ITEMLIST_MODELS:
            # Update itemlist items to include themselves as data
            # with the basic keys like code, name etc. filtered out
            # to reduce size.
            for item in items:
                item["item_data"] = json.dumps({
                    key: value for key, value in item.items()
                    if key not in ["code", "name", "icon", "table",
                                   "rare_grade", "duration"]
                }, cls=CustomJsonEncoder)

            db.session.bulk_insert_mappings(ItemList, items)

    # Commit to save changes
    db.session.commit()
