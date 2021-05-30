from flask_restx import Resource, abort
from webapp.models import RankingPlayer
from webapp.models.enums import Server
from webapp.extensions import cache


class PlayerDetailedView(Resource):
    def get(self, server: str, name: str):
        resp = self._get_response(
            server=server,
            name=name,
        )

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(
        self,
        server: str,
        name: str,
    ) -> dict:
        server_value = 0 if server == "luxplena" else 1
        player = RankingPlayer.query.filter(
            RankingPlayer.server == Server(server_value),
            RankingPlayer.name == name,
        ).first()

        if not player:
            abort(404, "Player not found.")

        return player.to_dict()
