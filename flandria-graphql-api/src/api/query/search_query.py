import strawberry

from src.api import types
from src.api.resolvers import resolve_search

SearchResultType = types.Monster | types.Npc | types.Quest | types.ItemList


@strawberry.type
class SearchQuery:
    @strawberry.field
    def search(
        self,
        info: strawberry.Info,
        s: str,
        limit: int = 20,
    ) -> list[SearchResultType]:
        return resolve_search(info=info, s=s, limit=limit)
