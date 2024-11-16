from typing import TYPE_CHECKING

import sqlalchemy as sa
import strawberry

from src.api import types
from src.database import Session, models

from .helpers import coerce_orm_to_strawberry, parse_nested_keys_from_selections

if TYPE_CHECKING:
    from src.api.query.search_query import SearchResultType


def resolve_search(
    *,
    info: strawberry.Info,
    s: str,
    limit: int,
) -> list["SearchResultType"]:
    nested_keys = parse_nested_keys_from_selections(info.selected_fields)[
        info._raw_info.field_name
    ]

    monsters_query = (
        sa.select(models.Monster)
        .where(sa.or_(models.Monster.name.icontains(s), models.Monster.code == s))
        .limit(limit)
    )
    npcs_query = (
        sa.select(models.Npc)
        .where(sa.or_(models.Npc.name.icontains(s), models.Npc.code == s))
        .limit(limit)
    )
    quests_query = (
        sa.select(models.Quest)
        .where(sa.or_(models.Quest.title.icontains(s), models.Quest.code == s))
        .limit(limit)
    )
    items_query = (
        sa.select(models.ItemList)
        .where(sa.or_(models.ItemList.name.icontains(s), models.ItemList.code == s))
        .limit(limit)
    )

    with Session() as session:
        monsters = session.scalars(monsters_query).all()
        npcs = session.scalars(npcs_query).all()
        quests = session.scalars(quests_query).all()
        items = session.scalars(items_query).all()

        return [
            *[
                coerce_orm_to_strawberry(o, types.Monster, nested_keys)
                for o in monsters
            ],
            *[coerce_orm_to_strawberry(o, types.Npc, nested_keys) for o in npcs],
            *[coerce_orm_to_strawberry(o, types.Quest, nested_keys) for o in quests],
            *[coerce_orm_to_strawberry(o, types.ItemList, nested_keys) for o in items],
        ]
