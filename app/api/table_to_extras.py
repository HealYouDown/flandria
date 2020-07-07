from sqlalchemy import or_, not_, and_
from sqlalchemy import func
from app.extensions import db
from typing import List

import app.models as models

TABLE_TO_EXTRA = {
    "monster": [
        "quests",
        "drops",
        "maps",
    ],
    "cariad": [
        "upgrade_data",
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "rapier": [
        "upgrade_data",
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "dagger": [
        "upgrade_data",
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "one_handed_sword": [
        "upgrade_data",
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "two_handed_sword": [
        "upgrade_data",
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "rifle": [
        "upgrade_data",
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "duals": [
        "upgrade_data",
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "shield": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "coat": [
        "upgrade_data",
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "pants": [
        "upgrade_data",
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "gauntlet": [
        "upgrade_data",
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "shoes": [
        "upgrade_data",
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "quest_scroll": [
        "dropped_by",
        "quests_by_scroll",
        "sold_by",
    ],
    "quest_item": [
        "dropped_by",
        "quests_by_item",
    ],
    "hat": [
        "dropped_by",
        "random_boxes",
        "produced_by",
    ],
    "dress": [
        "dropped_by",
        "random_boxes",
        "produced_by",
    ],
    "accessory": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
    ],
    "recipe": [
        "dropped_by",
        "random_boxes",
        "sold_by",
    ],
    "material": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "bullet": [
        "dropped_by",
        "sold_by",
    ],
    "ship_flag": [
        "dropped_by",
        "sold_by",
    ],
    "shell": [
        "dropped_by",
        "sold_by",
    ],
    "consumable": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "random_box": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "ship_anchor": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "ship_body": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "ship_figure": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "ship_head_mast": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "ship_main_mast": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "ship_magic_stone": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "ship_front": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "ship_normal_weapon": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "ship_special_weapon": [
        "random_boxes",
        "dropped_by",
        "produced_by",
        "needed_for",
        "sold_by",
    ],
    "pet_combine_help": [
        "random_boxes",
        "dropped_by",
    ],
    "pet_combine_stone": [
        "random_boxes",
        "dropped_by",
    ],
    "pet_skill_stone": [
        "random_boxes",
        "dropped_by",
        "sold_by",
    ],
    "pet": [
        "random_boxes",
        "dropped_by",
    ],
    "seal_break_help": [
        "random_boxes",
        "dropped_by",
        "sold_by",
    ],
    "upgrade_help": [
        "random_boxes",
        "dropped_by",
        "sold_by",
    ],
    "upgrade_crystal": [
        "random_boxes",
        "dropped_by",
        "sold_by",
    ],
    "upgrade_stone": [
        "random_boxes",
        "dropped_by",
        "sold_by",
    ],
    "fishing_rod": [
        "random_boxes",
        "sold_by",
    ],
    "riding_pet": [
        "random_boxes",
    ],
    "fishing_material": [
        "produced_by",
        "needed_for",
    ],
    "quest": [
        "after_quest",
        "quest_scrolls",
    ],
    "production": [
        "premium_essence_recipe",
    ],
    "fishing_bait": [
        "sold_by",
    ],
    "essence": [
        "dropped_by",
        "produced_by",
        "needed_for",
    ],
    "essence_help_item": [
        "dropped_by"
    ]
}


def get_maps(monster_code: str) -> list:
    query = (db.session.query(models.MapPoint)
             .filter(models.MapPoint.monster_code == monster_code))

    objects = []
    for point in query.all():
        if point.map.to_dict() not in objects:
            objects.append(point.map.to_dict())

    return objects


def get_drops(monster_code: str) -> list:
    query = models.Drop.query.filter_by(monster_code=monster_code)

    return [obj.to_dict(exclude_monster=True)
            for obj in query.all()]


def get_quests(monster_code: str) -> list:
    query1 = models.Quest.query\
        .join(models.QuestLootDescription)\
        .filter_by(monster_code=monster_code)

    query2 = models.Quest.query\
        .join(models.QuestMission)\
        .filter_by(monster_code=monster_code)

    objects = [*query1.all(), *query2.all()]
    return [obj.to_dict(minimal=True) for obj in objects]


def get_dropped_by(item_code: str) -> list:
    query = models.Drop.query.filter_by(item_code=item_code)

    return [obj.to_dict(exclude_item=True)
            for obj in query.all()]


def get_upgrade_data(upgrade_code: str) -> list:
    query = models.UpgradeRule.query\
        .filter_by(upgrade_code=upgrade_code)\
        .order_by(models.UpgradeRule.upgrade_level.asc())

    return [obj.to_dict() for obj in query.all()]


def get_quests_by_item(item_code: str) -> list:
    query = models.Quest.query\
        .join(models.QuestMission)\
        .filter(models.QuestMission.quest_item_code == item_code)

    return [obj.to_dict(minimal=True) for obj in query.all()]


def get_quests_by_scroll(scroll_quest_code: str) -> list:
    query = (models.Quest.query
             .filter(models.Quest.code == scroll_quest_code))

    return [obj.to_dict(minimal=True) for obj in query.all()]


def get_random_boxes(item_code: str) -> list:
    query = models.RandomBox.query\
        .filter(or_(
            getattr(models.RandomBox, f"item_{i}_code") == item_code
            for i in range(0, 61)
        ))

    return [obj.to_dict(minimal=True) for obj in query.all()]


def get_needed_for(item_code: str) -> dict:
    result = {}

    # Recipe
    query = models.Recipe.query\
        .filter(or_(
            getattr(models.Recipe, f"material_{i}_code") == item_code
            for i in range(1, 7)
        ))

    result["recipe"] = [
        obj.to_dict(minimal=True) for obj in query.all()]

    # Second job
    query = (models.Production.query
             .filter(
                 or_(getattr(models.Production,
                             f"material_{i}_code") == item_code
                     for i in range(1, 7)
                     ),
                 not_(and_(
                         models.Production.type == "Essence",
                         models.Production.division == 1
                         )
                      )
                 )
             )

    result["second_job"] = [
        obj.to_dict(minimal=True) for obj in query.all()]

    return result


def get_produced_by(item_code: str) -> dict:
    result = {}

    # Recipe
    query = models.Recipe.query\
        .filter(models.Recipe.result_code == item_code)

    result["recipe"] = [obj.to_dict(minimal=True) for obj in query.all()]

    # Second Job
    query = (models.Production.query
             .filter(models.Production.result_code == item_code,
                     not_(and_(
                         models.Production.type == "Essence",
                         models.Production.division == 1
                         )
                     )))

    result["second_job"] = [
        obj.to_dict(minimal=True) for obj in query.all()]

    return result


def get_after_quest(quest_code: str) -> dict:
    query = models.Quest.query\
        .filter_by(before_quest_code=quest_code)

    quest = query.first()
    if quest is None:
        return None

    return quest.to_dict(minimal=True)


def get_quest_scrolls(quest_code: str) -> list:
    query = models.QuestScroll.query\
        .filter_by(quest_code=quest_code)

    return [obj.to_dict(minimal=True) for obj in query.all()]


def get_premium_essence_recipe(result_code: str) -> dict:
    query = (models.Production.query
             .filter(models.Production.division == 1,
                     models.Production.result_code == result_code))

    production = query.first()

    if production is None:
        return None

    return production.to_dict()


def get_sold_by(item_code: str) -> List[dict]:
    query = (models.NPC.query
             .join(models.NPCShop)
             .filter(
                 models.NPCShop.item_code == item_code
             ))

    return [npc.to_dict() for npc in query.all()]