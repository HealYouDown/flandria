from flask_restx import Resource
from webapp.extensions import cache
from webapp.models import Map


class MapView(Resource):
    def get(self, code: str):
        resp = self._get_response(code)

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(self, code: str) -> dict:
        map_ = Map.query.get_or_404(code.strip())

        return map_.to_dict()
