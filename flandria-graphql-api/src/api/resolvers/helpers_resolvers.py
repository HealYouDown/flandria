import sqlalchemy as sa
import strawberry

from src.api import types
from src.database import Session, models

from .helpers import coerce_orm_to_strawberry, parse_nested_keys_from_selections
from .sqla_helpers import apply_join_options


def _get_nks(info: strawberry.Info):
    return parse_nested_keys_from_selections(info.selected_fields)[
        info._raw_info.field_name
    ]


def resolve_dropped_by(*, info: strawberry.Info, item_code: str) -> list[types.Drop]:
    nks = _get_nks(info)
    query = sa.select(models.Drop).where(models.Drop.item_code == item_code)
    query = apply_join_options(query, models.Drop, nks)

    with Session() as session:
        result = session.scalars(query).all()
        return [coerce_orm_to_strawberry(r, types.Drop, nks) for r in result]


def resolve_produced_by(
    *, info: strawberry.Info, item_code: str
) -> list[types.Recipe | types.Production]:
    nks = _get_nks(info)

    recipe_query = sa.select(models.Recipe).where(
        models.Recipe.result_code == item_code
    )
    recipe_query = apply_join_options(recipe_query, models.Recipe, nks)

    production_query = sa.select(models.Production).where(
        models.Production.result_code == item_code
    )
    production_query = apply_join_options(production_query, models.Production, nks)

    with Session() as session:
        recipes = session.scalars(recipe_query).all()
        productions = session.scalars(production_query).all()

        return [
            *[coerce_orm_to_strawberry(r, types.Recipe, nks) for r in recipes],
            *[coerce_orm_to_strawberry(r, types.Production, nks) for r in productions],
        ]


def resolve_needed_for(
    *, info: strawberry.Info, item_code: str
) -> list[types.Recipe | types.Production]:
    nks = _get_nks(info)

    recipe_query = (
        sa.select(models.Recipe)
        .join(models.Recipe.required_materials)
        .where(models.RecipeRequiredMaterial.material_code == item_code)
    )
    recipe_query = apply_join_options(recipe_query, models.Recipe, nks)

    production_query = (
        sa.select(models.Production)
        .join(models.Production.required_materials)
        .where(models.ProductionRequiredMaterial.material_code == item_code)
    )
    production_query = apply_join_options(production_query, models.Production, nks)

    with Session() as session:
        recipes = session.scalars(recipe_query).all()
        productions = session.scalars(production_query).all()

        return [
            *[coerce_orm_to_strawberry(r, types.Recipe, nks) for r in recipes],
            *[coerce_orm_to_strawberry(r, types.Production, nks) for r in productions],
        ]


def resolve_available_in_randombox(
    *, info: strawberry.Info, item_code: str
) -> list[types.RandomBox]:
    nks = _get_nks(info)
    query = (
        sa.select(models.RandomBox)
        .join(models.RandomBox.rewards)
        .where(models.RandomBoxReward.reward_code == item_code)
    )
    query = apply_join_options(query, models.RandomBox, nks)

    with Session() as session:
        result = session.scalars(query).all()
        return [coerce_orm_to_strawberry(r, types.RandomBox, nks) for r in result]


def resolve_available_as_quest_reward(
    *, info: strawberry.Info, item_code: str
) -> list[types.Quest]:
    nks = _get_nks(info)
    query = (
        sa.select(models.Quest)
        .join(models.Quest.reward_items)
        .where(models.QuestRewardItem.item_code == item_code)
    )
    query = apply_join_options(query, models.Quest, nks)

    with Session() as session:
        result = session.scalars(query).all()
        return [coerce_orm_to_strawberry(r, types.Quest, nks) for r in result]


def resolve_sold_by_npc(*, info: strawberry.Info, item_code: str) -> list[types.Npc]:
    nks = _get_nks(info)
    query = (
        sa.select(models.Npc)
        .join(models.Npc.store_items)
        .where(models.NpcStoreItem.item_code == item_code)
    )
    query = apply_join_options(query, models.Npc, nks)

    with Session() as session:
        result = session.scalars(query).all()
        return [coerce_orm_to_strawberry(r, types.Npc, nks) for r in result]
