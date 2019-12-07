import app.database.models as db_models
from sqlalchemy.sql.expression import or_
from app.extensions import db
from sqlalchemy.exc import OperationalError
from app.auth.models import User
from app.decorators import catch_errors

tables = {
    "monster": [
        "quests", "drops",
    ],
    "cariad": [
        "upgrade_data", "random_boxes", "dropped_by", "produced_by_recipe",
        "produced_by_second_job", "needed_for_recipe", "needed_for_second_job",
    ],
    "rapier": [
        "upgrade_data", "random_boxes", "dropped_by", "produced_by_recipe",
        "produced_by_second_job", "needed_for_recipe", "needed_for_second_job",
    ],
    "dagger": [
        "upgrade_data", "random_boxes", "dropped_by", "produced_by_recipe",
        "produced_by_second_job", "needed_for_recipe", "needed_for_second_job",
    ],
    "one_handed_sword": [
        "upgrade_data", "random_boxes", "dropped_by", "produced_by_recipe",
        "produced_by_second_job", "needed_for_recipe", "needed_for_second_job",
    ],
    "two_handed_sword": [
        "upgrade_data", "random_boxes", "dropped_by", "produced_by_recipe",
        "produced_by_second_job", "needed_for_recipe", "needed_for_second_job",
    ],
    "rifle": [
        "upgrade_data", "random_boxes", "dropped_by", "produced_by_recipe",
        "produced_by_second_job", "needed_for_recipe", "needed_for_second_job",
    ],
    "duals": [
        "upgrade_data", "random_boxes", "dropped_by", "produced_by_recipe",
        "produced_by_second_job", "needed_for_recipe", "needed_for_second_job",
    ],
    "shield": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "coat": [
        "upgrade_data", "random_boxes", "dropped_by", "produced_by_recipe",
        "produced_by_second_job", "needed_for_recipe", "needed_for_second_job",
    ],
    "pants": [
        "upgrade_data", "random_boxes", "dropped_by", "produced_by_recipe",
        "produced_by_second_job", "needed_for_recipe", "needed_for_second_job",
    ],
    "gauntlet": [
        "upgrade_data", "random_boxes", "dropped_by", "produced_by_recipe",
        "produced_by_second_job", "needed_for_recipe", "needed_for_second_job",
    ],
    "shoes": [
        "upgrade_data", "random_boxes", "dropped_by", "produced_by_recipe",
        "produced_by_second_job", "needed_for_recipe", "needed_for_second_job",
    ],
    "quest_scroll": [
        "dropped_by", "quests_by_item",
    ],
    "quest_item": [
        "quests", "dropped_by", "quests_by_item",
    ],
    "hat": [
        "dropped_by", "random_boxes",
    ],
    "dress": [
        "dropped_by", "random_boxes",
    ],
    "accessory": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "recipe": [
        "dropped_by", "random_boxes",
    ],
    "material": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "bullet": [
        "dropped_by",
    ],
    "ship_flag": [
        "dropped_by",
    ],
    "shell": [
        "dropped_by",
    ],
    "consumable": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "random_box": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "ship_anchor": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "ship_body": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "ship_figure": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "ship_head_mast": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "ship_main_mast": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "ship_magic_stone": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "ship_front": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "ship_normal_weapon": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "ship_special_weapon": [
        "random_boxes", "dropped_by", "produced_by_recipe", "produced_by_second_job",
        "needed_for_recipe", "needed_for_second_job",
    ],
    "pet_combine_help": [
        "random_boxes", "dropped_by",
    ],
    "pet_combine_stone": [
        "random_boxes", "dropped_by",
    ],
    "pet_skill_stone": [
        "random_boxes", "dropped_by",
    ],
    "pet": [
        "random_boxes", "dropped_by",
    ],
    "seal_break_help": [
        "random_boxes", "dropped_by",
    ],
    "upgrade_help": [
        "random_boxes", "dropped_by",
    ],
    "upgrade_crystal": [
        "random_boxes", "dropped_by",
    ],
    "upgrade_stone": [
        "random_boxes", "dropped_by",
    ],
    "fishing_rod": [
        "random_boxes",
    ],
    "riding_pet": [
        "random_boxes",
    ],
    "fishing_material": [
        "produced_by_recipe", "produced_by_second_job", "needed_for_recipe",
        "needed_for_second_job",
    ],
    "quest": [
        "after_quests", "quest_scrolls",
    ],
    "product_book": [],
    "fishing_bait": [],
}


@catch_errors
def get_hidden_codes():
    return [o.code for o in db.session.query(db_models.HiddenItem).all()]


@catch_errors
def get_excluded_codes():
    return [o.code for o in db.session.query(db_models.ExcludedItem).all()]


@catch_errors
def search_itemlist(string: str, user):
    query = db.session.query(db_models.ItemList)\
        .filter(or_(db_models.ItemList.name.contains(string),
                    db_models.ItemList.code.contains(string)
                    ),
                db_models.ItemList.code.notin_(get_excluded_codes())
                )

    if user is None or not user.can_see_hidden:
        query = query.filter(db_models.ItemList.code.notin_(
            get_hidden_codes(user=None)))

    includes = ["code", "table", "name", "icon", "rare_grade"]
    return [i.to_dict(includes=includes) for i in query.limit(50).all()]


@catch_errors
def get_upgrade_data(upgrade_code):
    return [
        u.to_dict() for u in db.session.query(db_models.UpgradeRule)
        .filter(db_models.UpgradeRule.upgrade_code == upgrade_code)
        .order_by(db_models.UpgradeRule.upgrade_level)
        .all()
    ]


@catch_errors
def get_random_boxes(code):
    includes = ["code", "name", "icon", "rare_grade"]
    return [
        r.to_dict(includes=includes) for r in db.session.query(db_models.RandomBox)
        .filter(or_(
            db_models.RandomBox.item_0_code == code, db_models.RandomBox.item_1_code == code,
            db_models.RandomBox.item_2_code == code, db_models.RandomBox.item_3_code == code,
            db_models.RandomBox.item_4_code == code, db_models.RandomBox.item_5_code == code,
            db_models.RandomBox.item_6_code == code, db_models.RandomBox.item_7_code == code,
            db_models.RandomBox.item_8_code == code, db_models.RandomBox.item_9_code == code,
            db_models.RandomBox.item_10_code == code, db_models.RandomBox.item_11_code == code,
            db_models.RandomBox.item_12_code == code, db_models.RandomBox.item_13_code == code,
            db_models.RandomBox.item_14_code == code, db_models.RandomBox.item_15_code == code,
            db_models.RandomBox.item_16_code == code, db_models.RandomBox.item_17_code == code,
            db_models.RandomBox.item_18_code == code, db_models.RandomBox.item_19_code == code,
            db_models.RandomBox.item_20_code == code, db_models.RandomBox.item_21_code == code,
            db_models.RandomBox.item_22_code == code, db_models.RandomBox.item_23_code == code,
            db_models.RandomBox.item_24_code == code, db_models.RandomBox.item_25_code == code,
            db_models.RandomBox.item_26_code == code, db_models.RandomBox.item_27_code == code,
            db_models.RandomBox.item_28_code == code, db_models.RandomBox.item_29_code == code,
            db_models.RandomBox.item_30_code == code, db_models.RandomBox.item_31_code == code,
            db_models.RandomBox.item_32_code == code, db_models.RandomBox.item_33_code == code,
            db_models.RandomBox.item_34_code == code, db_models.RandomBox.item_35_code == code,
            db_models.RandomBox.item_36_code == code, db_models.RandomBox.item_37_code == code,
            db_models.RandomBox.item_38_code == code, db_models.RandomBox.item_39_code == code,
            db_models.RandomBox.item_40_code == code, db_models.RandomBox.item_41_code == code,
            db_models.RandomBox.item_42_code == code, db_models.RandomBox.item_43_code == code,
            db_models.RandomBox.item_44_code == code, db_models.RandomBox.item_45_code == code,
            db_models.RandomBox.item_46_code == code, db_models.RandomBox.item_47_code == code,
            db_models.RandomBox.item_48_code == code, db_models.RandomBox.item_49_code == code,
            db_models.RandomBox.item_50_code == code, db_models.RandomBox.item_51_code == code,
            db_models.RandomBox.item_52_code == code, db_models.RandomBox.item_53_code == code,
            db_models.RandomBox.item_54_code == code, db_models.RandomBox.item_55_code == code,
            db_models.RandomBox.item_56_code == code, db_models.RandomBox.item_57_code == code,
            db_models.RandomBox.item_58_code == code, db_models.RandomBox.item_59_code == code,
            db_models.RandomBox.item_60_code == code
            )
        )
        .all()
    ]


@catch_errors
def get_drops(code):
    includes = ["item.code", "item.icon", "item.table", "item.name", "item.rare_grade", "quantity"]
    return [
        d.to_dict(includes=includes) for d in db.session.query(db_models.Drop)
        .filter(db_models.Drop.monster_code == code)
        .all()
    ]


@catch_errors
def get_dropped_by(code):
    includes = ["monster.code", "monster.name", "monster.icon", "monster.rating_type"]
    return [
        d.to_dict(includes=includes)["monster"] for d in db.session.query(db_models.Drop)
        .filter(db_models.Drop.item_code == code)
        .all()
    ]


@catch_errors
def get_produced_by_recipe(code):
    includes = ["code", "name", "icon", "rare_grade"]
    return [
        r.to_dict(includes=includes) for r in db.session.query(db_models.Recipe)
        .filter(db_models.Recipe.result_code == code)
        .all()
    ]


@catch_errors
def get_produced_by_second_job(code):
    includes = ["code", "name", "icon", "rare_grade"]
    return [
        r.to_dict(includes=includes) for r in db.session.query(db_models.ProductBook)
        .join(db_models.Production)
        .filter(db_models.Production.result_code == code)
        .all()
    ]


@catch_errors
def get_needed_for_recipe(code):
    includes = ["code", "name", "icon", "rare_grade"]
    return [
        r.to_dict(includes=includes) for r in db.session.query(db_models.Recipe)
        .filter(or_(
            db_models.Recipe.material_1_code == code,
            db_models.Recipe.material_2_code == code,
            db_models.Recipe.material_3_code == code,
            db_models.Recipe.material_4_code == code,
            db_models.Recipe.material_5_code == code,
            db_models.Recipe.material_6_code == code
            )
        )
        .all()
    ]


@catch_errors
def get_needed_for_second_job(code):
    includes = ["code", "name", "icon", "rare_grade"]
    return [
        r.to_dict(includes=includes) for r in db.session.query(db_models.ProductBook)
        .join(db_models.Production)
        .filter(or_(
            db_models.Production.material_1_code == code,
            db_models.Production.material_2_code == code,
            db_models.Production.material_3_code == code,
            db_models.Production.material_4_code == code,
            db_models.Production.material_5_code == code,
            db_models.Production.material_6_code == code
            )
        )
        .all()
    ]


@catch_errors
def get_quests_by_item(code):
    includes = ["code", "name", "icon"]
    return [
        q.to_dict(includes=includes) for q in db.session.query(db_models.Quest)
        .join(db_models.QuestMission)
        .filter(db_models.QuestMission.quest_item_code == code)
        .all()
    ]


@catch_errors
def get_quest_scrolls(code):
    includes = ["code", "name", "icon", "rare_grade"]
    return [
        s.to_dict(includes=includes) for s in db.session.query(db_models.QuestScroll)
        .filter(db_models.QuestScroll.quest_code == code)
        .all()
    ]


@catch_errors
def get_after_quests(code):
    includes = ["code", "name"]
    return [
        q.to_dict(includes=includes) for q in db.session.query(db_models.Quest)
        .filter(db_models.Quest.before_quest_code == code)
        .all()
    ]


@catch_errors
def get_quests(code):
    includes = ["code", "name"]
    q = [q.to_dict(includes=includes) for q in db.session.query(db_models.Quest)
         .join(db_models.QuestMission)
         .filter(db_models.QuestMission.monster_code == code)
         .all()
         ]
    q += [q.to_dict(includes=includes) for q in db.session.query(db_models.Quest)
          .join(db_models.QuestLootDescription)
          .filter(db_models.QuestLootDescription.monster_code == code)
          .all()
          ]
    return q
