import strawberry

from src.api import types
from src.api.resolvers import (
    resolve_available_as_quest_reward,
    resolve_available_in_randombox,
    resolve_dropped_by,
    resolve_needed_for,
    resolve_produced_by,
    resolve_sold_by_npc,
)


@strawberry.type
class HelpersQuery:
    @strawberry.field
    def dropped_by(self, info: strawberry.Info, code: str) -> list[types.Drop]:
        return resolve_dropped_by(info=info, item_code=code)

    @strawberry.field
    def produced_by(
        self, info: strawberry.Info, code: str
    ) -> list[types.Recipe | types.Production]:
        return resolve_produced_by(info=info, item_code=code)

    @strawberry.field
    def needed_for(
        self, info: strawberry.Info, code: str
    ) -> list[types.Recipe | types.Production]:
        return resolve_needed_for(info=info, item_code=code)

    @strawberry.field
    def available_in_randombox(
        self, info: strawberry.Info, code: str
    ) -> list[types.RandomBox]:
        return resolve_available_in_randombox(info=info, item_code=code)

    @strawberry.field
    def available_as_quest_reward(
        self, info: strawberry.Info, code: str
    ) -> list[types.Quest]:
        return resolve_available_as_quest_reward(info=info, item_code=code)

    @strawberry.field
    def sold_by_npc(self, info: strawberry.Info, code: str) -> list[types.Npc]:
        return resolve_sold_by_npc(info=info, item_code=code)
