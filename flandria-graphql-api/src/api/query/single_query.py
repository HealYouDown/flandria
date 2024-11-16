# pyright: reportAssignmentType=false
from typing import TYPE_CHECKING, Callable

import sqlalchemy as sa
import strawberry
from strawberry.tools import create_type

# the exec() call below needs the imports in the global namespace,
# so we have to keep them, even if they are unused and ruff wants to remove them.
from src.api import types as strawberry_types  # noqa: F401
from src.api.resolvers import resolve_single  # noqa: F401
from src.database import models  # noqa: F401

if TYPE_CHECKING:
    from strawberry.types.field import StrawberryField

    from src.database.types import ModelCls


to_evaluate = [
    # Actors
    ("monster", "Monster"),
    ("npc", "Npc"),
    # Quests
    ("quest", "Quest"),
    ("quest_item", "QuestItem"),
    ("quest_scroll", "QuestScroll"),
    # RandomBox
    ("random_box", "RandomBox"),
    # Fishing
    ("fishing_bait", "FishingBait"),
    ("fishing_material", "FishingMaterial"),
    # Essence
    ("essence", "Essence"),
    ("essence_help_item", "EssenceHelp"),
    # Armor
    ("coat", "Coat"),
    ("pants", "Pants"),
    ("gauntlets", "Gauntlet"),
    ("shoes", "Shoes"),
    ("shield", "Shield"),
    # Weapons
    ("cariad", "Cariad"),
    ("dagger", "Dagger"),
    ("duals", "Duals"),
    ("fishing_rod", "FishingRod"),
    ("one_handed_sword", "OneHandedSword"),
    ("rapier", "Rapier"),
    ("rifle", "Rifle"),
    ("two_handed_sword", "TwoHandedSword"),
    # Extra equipment
    ("accessory", "Accessory"),
    ("dress", "Dress"),
    ("hat", "Hat"),
    # Ship
    ("ship_anchor", "ShipAnchor"),
    ("ship_body", "ShipBody"),
    ("ship_figure", "ShipFigure"),
    ("ship_flag", "ShipFlag"),
    ("ship_front", "ShipFront"),
    ("ship_head_mast", "ShipHeadMast"),
    ("ship_magic_stone", "ShipMagicStone"),
    ("ship_main_mast", "ShipMainMast"),
    ("ship_normal_weapon", "ShipNormalWeapon"),
    ("ship_shell", "ShipShell"),
    ("ship_special_weapon", "ShipSpecialWeapon"),
    # Pets
    ("pet", "Pet"),
    ("pet_combine_help_item", "PetCombineHelp"),
    ("pet_combine_stone", "PetCombineStone"),
    ("pet_skill", "PetSkill"),
    ("pet_skill_stone", "PetSkillStone"),
    ("riding_pet", "RidingPet"),
    # Player
    ("player_skill", "PlayerSkill"),
    ("skill_book", "SkillBook"),
    # Crafting
    ("recipe", "Recipe"),
    ("production", "Production"),
    ("production_book", "ProductionBook"),
    # Upgrading
    ("upgrade_help_item", "UpgradeHelp"),
    ("upgrade_stone", "UpgradeStone"),
    ("upgrade_crystal", "UpgradeCrystal"),
    # Seals
    ("seal_break_help_item", "SealBreakHelp"),
    # Others
    # ("fusion_help_item", "FusionHelp"),
    ("map", "Map"),
    ("bullet", "Bullet"),
    ("consumable", "Consumable"),
    ("material", "Material"),
    ("tower_floor", "TowerFloor"),
]

fields: list["StrawberryField"] = []
for query_name, cls_name in to_evaluate:
    model_cls: "ModelCls" = getattr(models, cls_name)
    insp = sa.inspect(model_cls)
    pks = [(c.name, c.type.python_type.__name__) for c in insp.primary_key]

    # technically, all of our models have only one pk called "code"
    # but this way, we can support any composite pks as well!
    pk_params = ",".join([f"{key}: {type_}" for key, type_ in pks])
    pk_arguments_resolver = (
        "{" + ",".join(f'"{key}": {key}' for key in [j[0] for j in pks]) + "}"
    )

    exec(f"""
def {query_name}(
    self,
    info: strawberry.Info,
    {pk_params}
) -> strawberry_types.{cls_name} | None:
    return resolve_single(
        info=info,
        model_cls=models.{cls_name},
        object_cls=strawberry_types.{cls_name},
        pk={pk_arguments_resolver},
    )
""")
    resolver: Callable = locals().get(query_name)
    fields.append(strawberry.field(resolver=resolver, name=query_name))

SingleQuery = create_type("SingleQuery", fields)
