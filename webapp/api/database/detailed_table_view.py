from flask_restx import Resource, abort
from webapp.api.database.constants import ALLOWED_DATABASE_TABLES
from webapp.api.database.utils import get_model_from_tablename
from webapp.extensions import cache


class DetailedTableView(Resource):
    def get(self, table: str, code: str):
        if table not in ALLOWED_DATABASE_TABLES:
            abort(404, "Table does not exist.")

        resp = self._get_response(table, code)

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(self, table: str, code: str) -> dict:
        model = get_model_from_tablename(table)
        item = model.query.get_or_404(code)

        return item.to_dict()
