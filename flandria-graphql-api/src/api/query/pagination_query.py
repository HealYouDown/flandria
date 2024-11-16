# pyright: reportAssignmentType=false
from typing import TYPE_CHECKING, Callable

import strawberry
from strawberry.tools import create_type

# the exec() call below needs the imports in the global namespace,
# so we have to keep them, even if they are unused and ruff wants to remove them.
from src.api import inputs  # noqa: F401
from src.api import types as strawberry_types  # noqa: F401
from src.api.resolvers import resolve_pagination  # noqa: F401
from src.api.settings import DEFAULT_PAGESIZE  # noqa: F401
from src.database import models  # noqa: F401

if TYPE_CHECKING:
    from strawberry.types.field import StrawberryField


# @strawberry.type
# class PaginationQuery:
#     @strawberry.field
#     def all_monsters(
#         self,
#         info: strawberry.Info,
#         offset: int = 0,
#         limit: int = DEFAULT_PAGESIZE,
#         filter: inputs.MonsterFilter | None = strawberry.UNSET,
#     ) -> strawberry_types.PageInfo[strawberry_types.Monster]:
#         return resolve_pagination(
#             info=info,
#             model_cls=models.Monster,
#             object_cls=strawberry_types.Monster,
#             limit=limit,
#             offset=offset,
#             filter=filter,
#         )


# I can't be arsed to write the same resolve function for each class (see above)
# so yea.. this abomination was born
to_evaluate = [
    # Actors
    ("all_monsters", "Monster"),
    ("all_npcs", "Npc"),
    ("all_npc_store_items", "NpcStoreItem"),
    ("all_actor_messages", "ActorMessage"),
    ("all_monster_skills", "MonsterSkill"),
    ("all_drops", "Drop"),
    ("all_money_drops", "Money"),
    ("all_monster_positions", "MonsterPosition"),
    ("all_npc_positions", "NpcPosition"),
    # Quests
    ("all_quests", "Quest"),
    ("all_quest_give_items", "QuestGiveItem"),
    ("all_quest_mission", "QuestMission"),
    ("all_quest_reward_items", "QuestRewardItem"),
    ("all_quest_items", "QuestItem"),
    ("all_quest_scrolls", "QuestScroll"),
    # RandomBox
    ("all_random_boxes", "RandomBox"),
    ("all_random_box_rewards", "RandomBoxReward"),
    # Fishing
    ("all_fishing_baits", "FishingBait"),
    ("all_fishing_materials", "FishingMaterial"),
    # Essence
    ("all_essences", "Essence"),
    ("all_essence_help_items", "EssenceHelp"),
    # Armor
    ("all_coats", "Coat"),
    ("all_pants", "Pants"),
    ("all_gauntlets", "Gauntlet"),
    ("all_shoes", "Shoes"),
    ("all_shields", "Shield"),
    # Weapons
    ("all_cariads", "Cariad"),
    ("all_daggers", "Dagger"),
    ("all_duals", "Duals"),
    ("all_fishing_rods", "FishingRod"),
    ("all_one_handed_swords", "OneHandedSword"),
    ("all_rapiers", "Rapier"),
    ("all_rifles", "Rifle"),
    ("all_two_handed_swords", "TwoHandedSword"),
    # Extra equipment
    ("all_accessories", "Accessory"),
    ("all_dresses", "Dress"),
    ("all_hats", "Hat"),
    # Ship
    ("all_ship_anchors", "ShipAnchor"),
    ("all_ship_bodies", "ShipBody"),
    ("all_ship_figures", "ShipFigure"),
    ("all_ship_flags", "ShipFlag"),
    ("all_ship_fronts", "ShipFront"),
    ("all_ship_head_masts", "ShipHeadMast"),
    ("all_ship_magic_stones", "ShipMagicStone"),
    ("all_ship_main_masts", "ShipMainMast"),
    ("all_ship_normal_weapons", "ShipNormalWeapon"),
    ("all_ship_shells", "ShipShell"),
    ("all_ship_special_weapons", "ShipSpecialWeapon"),
    # Pets
    ("all_pets", "Pet"),
    ("all_pet_combine_help_items", "PetCombineHelp"),
    ("all_pet_combine_stones", "PetCombineStone"),
    ("all_pet_skills", "PetSkill"),
    ("all_pet_skill_stones", "PetSkillStone"),
    ("all_riding_pets", "RidingPet"),
    # Player
    ("all_player_skills", "PlayerSkill"),
    ("all_skill_books", "SkillBook"),
    # Crafting
    ("all_recipes", "Recipe"),
    ("all_recipe_required_materials", "RecipeRequiredMaterial"),
    ("all_productions", "Production"),
    ("all_production_required_material", "ProductionRequiredMaterial"),
    ("all_production_books", "ProductionBook"),
    # Upgrading
    ("all_upgrade_help_items", "UpgradeHelp"),
    ("all_upgrade_stones", "UpgradeStone"),
    ("all_upgrade_crystals", "UpgradeCrystal"),
    ("all_upgrade_rules", "UpgradeRule"),
    # Seals
    ("all_seal_break_help_items", "SealBreakHelp"),
    # Others
    ("all_fusion_help_items", "FusionHelp"),
    ("all_player_required_skills", "PlayerRequiredSkill"),
    ("all_effects", "Effect"),
    ("all_item_sets", "ItemSet"),
    ("all_item_set_items", "ItemSetItem"),
    ("all_maps", "Map"),
    ("all_map_areas", "MapArea"),
    ("all_bullets", "Bullet"),
    ("all_consumables", "Consumable"),
    ("all_materials", "Material"),
    ("all_tower_floors", "TowerFloor"),
    ("all_tower_floor_monsters", "TowerFloorMonster"),
]

fields: list["StrawberryField"] = []
for query_name, cls_name in to_evaluate:
    exec(f"""
def {query_name}(
    self,
    info: strawberry.Info,
    offset: int = 0,
    limit: int = DEFAULT_PAGESIZE,
    filter: inputs.{cls_name}Filter | None = strawberry.UNSET,
    order_by: list[inputs.{cls_name}Sort] | None = strawberry.UNSET
) -> strawberry_types.PageInfo[strawberry_types.{cls_name}]:
    return resolve_pagination(
        info=info,
        model_cls=models.{cls_name},
        object_cls=strawberry_types.{cls_name},
        limit=limit,
        offset=offset,
        filter=filter,
        order_by=order_by,
    )
""")
    resolver: Callable = locals().get(query_name)
    fields.append(strawberry.field(resolver=resolver, name=query_name))

PaginationQuery = create_type("PaginationQuery", fields)
