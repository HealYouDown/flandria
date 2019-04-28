from distutils import util

from flask import Blueprint, jsonify, render_template, request, abort
from flask_login import login_required
from webapp.decorators import check_can_edit_drops

from webapp.database.helpers import *
from webapp.utils import get_locale

database = Blueprint("database", __name__, url_prefix="/database")


@database.route("/")
def index():
    return render_template("database/index.html", active_header="items", title="Items")


@database.route("/<table>")
def listview(table):
    assert table in TABLENAMES, abort(404)

    kws = {}
    kws["filtered"] = bool(util.strtobool(
        request.args.get("filtered", "True")))
    kws["table"] = table

    if kws["filtered"] and table in ["dress", "hat"]:
        kws["data"] = get_filtered_table_items(table)
    else:
        kws["data"] = get_table_items(table)
    kws["subs"] = get_subs(table)
    kws["options"] = get_options(table)
    kws["order"] = "desc" if table in INIT_DESC_ORDER else "asc"

    if table == "monster":
        kws["active_header"] = "monsters"
    elif table == "quest":
        kws["active_header"] = "quests"
        kws["init_sort_name"] = "level"
    else:
        kws["active_header"] = "items"

    return render_template("database/listview.html", **kws, title=tablename_to_title(table))


@database.route("/<table>/<code>")
def single_page(table, code):  # TODO: Refactor
    assert table in TABLENAMES, abort(404)

    kws = {}
    kws["data"] = get_data(table, code)
    kws["active_header"] = "items" # gets overwritten by monster and quest table

    if table == "monster":
        kws["active_header"] = "monsters"
        drops = get_drops(code)
        quests = get_quests(code)

        kws.update({"drops": drops, "quests": quests})
        template = "monster"

    elif table in WEAPON_TABLES or table in ARMOR_TABLES:
        dropped_by = get_dropped_by(code)
        try:
            upgrade_data = get_upgrade_data(kws["data"].upgrade_code)
        except AttributeError:
            upgrade_data = None
        produced_by_recipe = get_produced_by_recipe(code)
        produced_by_second_job = get_produced_by_second_job(code)
        needed_for_recipe = get_needed_for_recipe(code)
        needed_for_second_job = get_needed_for_second_job(code)
        random_boxes = get_avaiable_in_randombox(code)

        type_ = "weapon" if table in WEAPON_TABLES else "armor"

        kws.update({"dropped_by": dropped_by,
                    "upgrade_data": upgrade_data, "table": table,
                    "produced_by_recipe_data": produced_by_recipe, "produced_by_second_job_data": produced_by_second_job,
                    "needed_for_recipe_data": needed_for_recipe, "needed_for_second_job_data": needed_for_second_job,
                    "random_boxes": random_boxes, "type": type_})
        template = "weapon_and_armor"

    elif table == "quest_scroll":
        dropped_by = get_dropped_by(code)

        kws.update({"dropped_by": dropped_by})
        template = "quest_scroll"

    elif table == "quest_item":
        dropped_by = get_dropped_by(code)
        quests = get_quests_by_quest_item(code)

        kws.update({"dropped_by": dropped_by, "quests": quests})
        template = "quest_item"

    elif table in ["dress", "hat"]:
        dropped_by = get_dropped_by(code)
        random_boxes = get_avaiable_in_randombox(code)

        kws.update({"dropped_by": dropped_by, "random_boxes": random_boxes})
        template = "dress_and_hat"

    elif table == "accessory":
        dropped_by = get_dropped_by(code)
        produced_by_recipe = get_produced_by_recipe(code)
        produced_by_second_job = get_produced_by_second_job(code)
        needed_for_recipe = get_needed_for_recipe(code)
        needed_for_second_job = get_needed_for_second_job(code)
        random_boxes = get_avaiable_in_randombox(code)

        kws.update({"dropped_by": dropped_by,
                    "produced_by_recipe_data": produced_by_recipe, "produced_by_second_job_data": produced_by_second_job,
                    "needed_for_recipe_data": needed_for_recipe, "needed_for_second_job_data": needed_for_second_job,
                    "random_boxes": random_boxes})
        template = "accessory"

    elif table == "recipe":
        dropped_by = get_dropped_by(code)
        random_boxes = get_avaiable_in_randombox(code)

        kws.update({"dropped_by": dropped_by, "random_boxes": random_boxes})
        template = "recipe"

    elif table == "material":
        dropped_by = get_dropped_by(code)
        produced_by_recipe = get_produced_by_recipe(code)
        produced_by_second_job = get_produced_by_second_job(code)
        needed_for_recipe = get_needed_for_recipe(code)
        needed_for_second_job = get_needed_for_second_job(code)
        random_boxes = get_avaiable_in_randombox(code)

        kws.update({"dropped_by": dropped_by,
                    "produced_by_recipe_data": produced_by_recipe, "produced_by_second_job_data": produced_by_second_job,
                    "needed_for_recipe_data": needed_for_recipe, "needed_for_second_job_data": needed_for_second_job,
                    "random_boxes": random_boxes})
        template = "material"

    elif table == "product_book":
        produced_by_recipe = get_produced_by_recipe(code)
        produced_by_second_job = get_produced_by_second_job(code)
        needed_for_recipe = get_needed_for_recipe(code)
        needed_for_second_job = get_needed_for_second_job(code)

        kws.update({"produced_by_recipe_data": produced_by_recipe, "produced_by_second_job_data": produced_by_second_job,
                    "needed_for_recipe_data": needed_for_recipe, "needed_for_second_job_data": needed_for_second_job})
        template = "product_book"

    elif table in ["pet_combine_stone", "pet_combine_help"]:
        dropped_by = get_dropped_by(code)
        random_boxes = get_avaiable_in_randombox(code)

        kws.update({"dropped_by": dropped_by,
                    "random_boxes": random_boxes, "table": table})
        template = "pet_combine"

    elif table == "pet_skill_stone":
        dropped_by = get_dropped_by(code)
        random_boxes = get_avaiable_in_randombox(code)

        kws.update({"dropped_by": dropped_by, "random_boxes": random_boxes})
        template = "pet_skill_stone"

    elif table == "pet":
        dropped_by = get_dropped_by(code)
        random_boxes = get_avaiable_in_randombox(code)

        kws.update({"dropped_by": dropped_by, "random_boxes": random_boxes})
        template = "pet"

    elif table == "riding_pet":
        random_boxes = get_avaiable_in_randombox(code)

        kws.update({"random_boxes": random_boxes})
        template = "riding_pet"

    elif table in ["seal_break_help", "upgrade_help", "upgrade_crystal", "upgrade_stone"]:
        dropped_by = get_dropped_by(code)
        random_boxes = get_avaiable_in_randombox(code)

        kws.update({"dropped_by": dropped_by,
                    "random_boxes": random_boxes, "table": table})
        template = "enhancing"

    elif table == "fishing_rod":
        random_boxes = get_avaiable_in_randombox(code)

        kws.update({"random_boxes": random_boxes})
        template = "fishing_rod"

    elif table == "fishing_material":
        produced_by_recipe = get_produced_by_recipe(code)
        produced_by_second_job = get_produced_by_second_job(code)
        needed_for_recipe = get_needed_for_recipe(code)
        needed_for_second_job = get_needed_for_second_job(code)

        kws.update({"produced_by_recipe_data": produced_by_recipe, "produced_by_second_job_data": produced_by_second_job,
                    "needed_for_recipe_data": needed_for_recipe, "needed_for_second_job_data": needed_for_second_job})
        template = "fishing_material"

    elif table == "fishing_bait":
        template = "fishing_bait"

    elif table == "random_box":
        dropped_by = get_dropped_by(code)
        produced_by_recipe = get_produced_by_recipe(code)
        produced_by_second_job = get_produced_by_second_job(code)
        needed_for_recipe = get_needed_for_recipe(code)
        needed_for_second_job = get_needed_for_second_job(code)

        kws.update({"dropped_by": dropped_by, "produced_by_recipe_data": produced_by_recipe, "produced_by_second_job_data": produced_by_second_job,
                    "needed_for_recipe_data": needed_for_recipe, "needed_for_second_job_data": needed_for_second_job})
        template = "random_box"

    elif table == "consumable":
        dropped_by = get_dropped_by(code)
        random_boxes = get_avaiable_in_randombox(code)
        produced_by_recipe = get_produced_by_recipe(code)
        produced_by_second_job = get_produced_by_second_job(code)
        needed_for_recipe = get_needed_for_recipe(code)
        needed_for_second_job = get_needed_for_second_job(code)

        kws.update({"random_boxes": random_boxes, "dropped_by": dropped_by, "produced_by_recipe_data": produced_by_recipe, "produced_by_second_job_data": produced_by_second_job,
                    "needed_for_recipe_data": needed_for_recipe, "needed_for_second_job_data": needed_for_second_job})
        template = "consumable"

    elif table == "bullet":
        dropped_by = get_dropped_by(code)

        kws.update({"dropped_by": dropped_by})
        template = "bullet"

    elif table == "shell":
        dropped_by = get_dropped_by(code)

        kws.update({"dropped_by": dropped_by})
        template = "shell"

    elif table in ["ship_anchor", "ship_body", "ship_figure", "ship_head_mast", "ship_main_mast", "ship_magic_stone", "ship_front", "ship_normal_weapon", "ship_special_weapon"]:
        dropped_by = get_dropped_by(code)
        produced_by_recipe = get_produced_by_recipe(code)
        produced_by_second_job = get_produced_by_second_job(code)
        needed_for_recipe = get_needed_for_recipe(code)
        needed_for_second_job = get_needed_for_second_job(code)

        kws.update({"dropped_by": dropped_by, "produced_by_recipe_data": produced_by_recipe, "produced_by_second_job_data": produced_by_second_job,
                    "needed_for_recipe_data": needed_for_recipe, "needed_for_second_job_data": needed_for_second_job, "table": table})
        template = "ship"

    elif table == "quest":
        kws["active_header"] = "quests"
        after_quest = get_after_quest(code)
        quest_scroll = get_quest_scroll(code)

        _local = get_locale()
        # FIXME: 10/10 nice way to get only selected language description
        description = [dd for dd in kws["data"].descriptions if dd.language_code == _local][0]

        kws.update({"after_quest": after_quest, "quest_scroll": quest_scroll, "description": description})
        template = "quest"

    return render_template("database/single_pages/{0}.html".format(template), **kws, title=kws["data"].name)


@database.route("/monster/<code>/edit")
@login_required
@check_can_edit_drops
def edit_monster(code):
    kws = {}
    kws["data"] = get_data("monster", code)
    kws["drops"] = get_drops(code)
    kws["active_header"] = "monsters"
    kws["title"] = "Edit: " + kws["data"].name 
    return render_template("database/edit_monster.html", **kws)


@database.route("/search", methods=["GET"])
def search_item():
    string = request.args.get("s")
    items = search_itemlist(string)
    items_json = [item._asdict() for item in items]
    return jsonify(items_json)


@database.route("/delete_drop", methods=["DELETE"])
@login_required
@check_can_edit_drops
def delete_drop_view():
    data = request.json
    success, code, message = delete_drop(monster_code=data["monster_code"], item_code=data["item_code"])
    return jsonify({"success": success, "message": message}), code


@database.route("/add_drop", methods=["PUT"])
@login_required
@check_can_edit_drops
def add_drop_view():
    data = request.json
    success, code, message = add_drop(monster_code=data["monster_code"], item_code=data["item_code"])
    return jsonify({"success": success, "message": message}), code


@database.route("/add_drop_message", methods=["PUT"])
def add_drop_message_view():
    data = request.json
    success, code, message = add_drop_message(monster_code=data["monster_code"], message=data["message"])
    return jsonify({"success": success, "message": message}), code
