import typing

from flask_restx import Resource
from sqlalchemy import func
from webapp.api.utils import get_url_parameter
from webapp.models import RankingPlayer
from webapp.models.enums import Server
from webapp.extensions import cache


class GuildOverviewView(Resource):
    def get(self):
        page = get_url_parameter("page", int, 1)
        per_page = get_url_parameter("limit", int, 60)
        server = get_url_parameter(
            "server", str, "both",
            lambda v: v in ["bergruen", "luxplena", "both"])

        resp = self._get_response(
            server=server,
            page=page,
            per_page=per_page,
        )

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(
        self,
        page: int,
        per_page: int,
        server: typing.Optional[str] = None,
    ) -> typing.List[dict]:
        query = (
            RankingPlayer.query
            .with_entities(
                RankingPlayer.guild,
                RankingPlayer.server,
                func.count(RankingPlayer.guild).label("member_count"),
                func.avg(RankingPlayer.level_land).label("avg_level_land"),
                func.avg(RankingPlayer.level_sea).label("avg_level_sea"),
                func.avg(RankingPlayer.rank).label("avg_rank"),
            ).filter(
                RankingPlayer.guild.isnot(None),
            ).group_by(
                RankingPlayer.guild,
            )
        )

        # Apply server filter, if server is given
        if server != "both":
            server_value = 0 if server == "luxplena" else 1
            query = query.filter(RankingPlayer.server == Server(server_value))

        # Create pagination based on query and return in
        pagination_obj = query.paginate(page=page, per_page=per_page)

        return {
            "items": [
                {
                    "name": item.guild,
                    "server": item.server.to_dict(),
                    "member_count": int(item.member_count),
                    "avg_level_land": float(item.avg_level_land),
                    "avg_level_sea": float(item.avg_level_sea),
                    "avg_rank": float(item.avg_rank),
                } for item in pagination_obj.items
            ],
            "pagination": {
                "has_next": pagination_obj.has_next,
                "has_previous": pagination_obj.has_prev,
                "labels": list(pagination_obj.iter_pages()),
            }
        }
