from flask_babel import gettext
from flask_login import current_user
from sqlalchemy.sql.expression import or_
from flask import abort
import webapp.database.models as models
import webapp.database.models_2 as models_2
from webapp import db
from webapp.auth.models import DropLog
from webapp.database.options import OPTIONS

WEAPON_TABLES = [
    "cariad", "rapier", "dagger", "one_handed_sword",
    "two_handed_sword", "shield", "rifle", "duals",
]

ARMOR_TABLES = [
    "coat", "pants", "gauntlet", "shoes",
]

SHIP_STUFF_TABLES = [
    "shell", "ship_anchor", "ship_body", "ship_figure", "ship_head_mast",
    "ship_main_mast", "ship_magic_stone", "ship_front", "ship_normal_weapon", "ship_special_weapon",
]

# shows these tables with descending order as default
INIT_DESC_ORDER = [
    "dress", "hat", "recipe", "material", "random_box", "consumable"
]

TABLENAMES = [
    "monster",
    *WEAPON_TABLES,
    *ARMOR_TABLES,
    "hat", "dress", "accessory",
    "recipe", "material", "product_book",
    *SHIP_STUFF_TABLES,
    "pet_combine_help", "pet_combine_stone", "pet_skill_stone", "pet", "riding_pet",
    "seal_break_help", "upgrade_help", "upgrade_crystal", "upgrade_stone",
    "fishing_rod", "fishing_material", "fishing_bait",
    "random_box", "consumable", "bullet",
    "quest", "quest_scroll", "quest_item",
]


def tablename_to_class_name(tablename: str):
    parts = [part.title() for part in tablename.split('_')]
    return ''.join(part for part in parts)


def tablename_to_title(tablename: str):
    return " ".join(tablename.split("_")).title()


def get_subs(table: str):
    if table == "monster":
        subs = {
            gettext("Level:"): "level"
        }

    elif table in WEAPON_TABLES:
        subs = {
            gettext("Level:"): ["level_land", "level_sea"],
            gettext("Class:"): "class_land",
        }

    elif table in ARMOR_TABLES:
        subs = {
            gettext("Level:"): ["level_land", "level_sea"],
            gettext("Class:"): "class_land",
        }

    elif table == "accessory":
        subs = {
            gettext("Level:"): "level_land"
        }

    elif table == "quest":
        subs = {
            gettext("Level:"): "level",
        }

    elif table in SHIP_STUFF_TABLES:
        subs = {
            gettext("Level:"): "level_sea",
            gettext("Ship:"): "class_sea"
        }

    elif table == "pet_skill_stone":
        subs = {
            gettext("Level:"): "level",
        }

    else:
        subs = {}

    return subs


def get_options(table: str):
    return OPTIONS[table]


# DB queries


def get_exclude_item_codes():
    if current_user.is_authenticated and current_user.can_see_excludes:
        return []
    return [item.item_code for item in models_2.ExcludeFromView.query.all()]


def search_itemlist(string):
    return db.session.query(
        models.ItemList.code, models.ItemList.name, models.ItemList.table, models.ItemList.icon).filter(
        models.ItemList.name.contains(string), models.ItemList.code.notin_(get_exclude_item_codes())).all()


def get_table_items(table):
    table_cls = getattr(models, tablename_to_class_name(table))
    return db.session.query(table_cls).filter(table_cls.code.notin_(get_exclude_item_codes())).all()


def get_filtered_table_items(table):
    table_cls = getattr(models, tablename_to_class_name(table))
    return db.session.query(table_cls).filter(table_cls.included_in_filtered_view == True, table_cls.code.notin_(get_exclude_item_codes())).all()


def get_data(table, code):
    if code in get_exclude_item_codes():
        abort(403)

    return db.session.query(
        getattr(models, tablename_to_class_name(table))).get_or_404(code)


def get_drops(code):
    return db.session.query(models_2.Drop).filter(models_2.Drop.monster_code == code).all()


def get_dropped_by(code):
    return db.session.query(models_2.Drop).filter(models_2.Drop.item_code == code).all()


def get_quests(code):
    q = db.session.query(models.Quest).join(models.QuestMission).filter(models.QuestMission.monster_code == code).all()
    q += db.session.query(models.Quest).join(models.QuestLootDescription).filter(models.QuestLootDescription.monster_code == code).all()

    # Does not return all quests. # TODO
    #v = db.session.query(models.Quest).join(models.QuestMission, models.QuestLootDescription).filter(
    #    or_(models.QuestMission.monster_code == code, models.QuestLootDescription.monster_code == code)).all()

    return q


def get_quests_by_quest_item(code):
    return db.session.query(models.Quest).join(models.QuestMission).filter(models.QuestMission.quest_item_code == code).all()


def get_produced_by_recipe(code):
    return db.session.query(models.Recipe).filter(models.Recipe.result_code == code).all()


def get_produced_by_second_job(code):
    return db.session.query(models.ProductBook).join(
        models.Production).filter(models.Production.result_code == code).all()


def get_needed_for_recipe(code):
    return db.session.query(models.Recipe).filter(or_(models.Recipe.material_1_code == code, models.Recipe.material_2_code == code, models.Recipe.material_3_code ==
                                                      code, models.Recipe.material_4_code == code, models.Recipe.material_5_code == code, models.Recipe.material_6_code == code)).all()


def get_needed_for_second_job(code):
    return db.session.query(models.ProductBook).join(models.Production).filter(or_(models.Production.material_1_code == code, models.Production.material_2_code == code,
                                                                                   models.Production.material_3_code == code, models.Production.material_4_code == code,
                                                                                   models.Production.material_5_code == code, models.Production.material_6_code == code)).all()


def get_upgrade_data(upgrade_code):
    return db.session.query(models.UpgradeRule).filter(models.UpgradeRule.upgrade_code == upgrade_code).order_by(models.UpgradeRule.upgrade_level).all()


def get_avaiable_in_randombox(code):
    return db.session.query(models.RandomBox).filter(or_(
        models.RandomBox.item_0_code == code, models.RandomBox.item_1_code == code, models.RandomBox.item_2_code == code, models.RandomBox.item_3_code == code,
        models.RandomBox.item_4_code == code, models.RandomBox.item_5_code == code, models.RandomBox.item_6_code == code, models.RandomBox.item_7_code == code,
        models.RandomBox.item_8_code == code, models.RandomBox.item_9_code == code, models.RandomBox.item_10_code == code, models.RandomBox.item_11_code == code,
        models.RandomBox.item_12_code == code, models.RandomBox.item_13_code == code, models.RandomBox.item_14_code == code, models.RandomBox.item_15_code == code,
        models.RandomBox.item_16_code == code, models.RandomBox.item_17_code == code, models.RandomBox.item_18_code == code, models.RandomBox.item_19_code == code,
        models.RandomBox.item_20_code == code, models.RandomBox.item_21_code == code, models.RandomBox.item_22_code == code, models.RandomBox.item_23_code == code,
        models.RandomBox.item_24_code == code, models.RandomBox.item_25_code == code, models.RandomBox.item_26_code == code, models.RandomBox.item_27_code == code,
        models.RandomBox.item_28_code == code, models.RandomBox.item_29_code == code, models.RandomBox.item_30_code == code, models.RandomBox.item_31_code == code,
        models.RandomBox.item_32_code == code, models.RandomBox.item_33_code == code, models.RandomBox.item_34_code == code, models.RandomBox.item_35_code == code,
        models.RandomBox.item_36_code == code, models.RandomBox.item_37_code == code, models.RandomBox.item_38_code == code, models.RandomBox.item_39_code == code,
        models.RandomBox.item_40_code == code, models.RandomBox.item_41_code == code, models.RandomBox.item_42_code == code, models.RandomBox.item_43_code == code,
        models.RandomBox.item_44_code == code, models.RandomBox.item_45_code == code, models.RandomBox.item_46_code == code, models.RandomBox.item_47_code == code,
        models.RandomBox.item_48_code == code, models.RandomBox.item_49_code == code, models.RandomBox.item_50_code == code, models.RandomBox.item_51_code == code,
        models.RandomBox.item_52_code == code, models.RandomBox.item_53_code == code, models.RandomBox.item_54_code == code, models.RandomBox.item_55_code == code,
        models.RandomBox.item_56_code == code, models.RandomBox.item_57_code == code, models.RandomBox.item_58_code == code, models.RandomBox.item_59_code == code,
        models.RandomBox.item_60_code == code)).all()


def get_after_quest(code):
    return db.session.query(models.Quest).filter(models.Quest.before_quest_code == code).first()


def get_quest_scroll(code):
    return db.session.query(models.QuestScroll).filter(models.QuestScroll.quest_code == code).first()


def delete_drop(monster_code, item_code):
    # check if codes are valid
    item = db.session.query(models.ItemList).get(item_code)
    monster = db.session.query(models.Monster).get(monster_code)

    if item is None or monster is None:
        return False, 404, "Item or Monster does not exist"

    # delete drop
    db.session.query(models_2.Drop).filter(models_2.Drop.item_code == item_code, models_2.Drop.monster_code == monster_code).delete()
    
    log = DropLog(action="del", user_id=current_user.id, item_code=item_code, monster_code=monster_code)
    db.session.add(log)
    
    db.session.commit()

    return True, 200, "Drop was deleted succesfully"


def add_drop(monster_code, item_code):
    # check if codes are valid
    item = db.session.query(models.ItemList).get(item_code)
    monster = db.session.query(models.Monster).get(monster_code)

    if item is None or monster is None:
        return False, 404, "Item or Monster does not exist"

    # check if drop does not exist
    _drop = db.session.query(models_2.Drop).filter(models_2.Drop.item_code == item_code, models_2.Drop.monster_code == monster_code).first()
    
    if _drop is not None:
        return False, 404, "Drop does already exist"
    
    # add drop
    drop = models_2.Drop(item_code=item_code, monster_code=monster_code)
    db.session.add(drop)

    log = DropLog(action="add", user_id=current_user.id, item_code=item_code, monster_code=monster_code)
    db.session.add(log)

    db.session.commit()

    return True, 200, "Drop was added successfully"


def add_drop_message(monster_code, message):
    # check if codes are valid
    monster = db.session.query(models.Monster).get(monster_code)

    if not monster:
        return False, 404, "Item or Monster does not exist"

    # include user if user is logged in
    if current_user.is_authenticated:
        message = models_2.DropMessage(monster_code=monster_code, message=message, user_id=current_user.id)
    else:
        message = models_2.DropMessage(monster_code=monster_code, message=message)
    
    db.session.add(message)
    db.session.commit()

    return True, 200, "Drop message was sent successfully"
