import re
import typing

from flask_restx import Resource, abort
from sqlalchemy import or_
from webapp.api.database.constants import ALLOWED_DATABASE_TABLES
from webapp.api.database.utils import get_model_from_tablename
from webapp.api.utils import get_url_parameter
from webapp.extensions import cache
from webapp.models.enums import (Area, EffectCode, EssenceEquipType,
                                 ProductionType, RatingType)


class TableView(Resource):
    def get(self, table: str):
        if table not in ALLOWED_DATABASE_TABLES:
            abort(404, "Table does not exist.")

        # Get filter from url parameters
        current_page = get_url_parameter("page", int, 1)
        order = get_url_parameter("order", str, "asc",
                                  lambda v: v in ["asc", "desc"])
        per_page = get_url_parameter("limit", int, 60)
        sort_by = get_url_parameter("sort", str, "index")
        area = get_url_parameter("area", int, -1,
                                 lambda v: v in [-1, 0, 1])
        filter_ = get_url_parameter("filter", str, "all")
        minimal = get_url_parameter("minimal", bool, True)
        effects = get_url_parameter("effects", list, [])

        resp = self._get_response(
            table=table,
            current_page=current_page,
            order=order,
            per_page=per_page,
            sort_by=sort_by,
            area=area,
            filter_=filter_,
            minimal=minimal,
            effects=effects
        )

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(
        self,
        table: str,
        current_page: int,
        order: str,
        per_page: int,
        sort_by: str,
        area: int,
        filter_: str,
        minimal: bool,
        effects: typing.List[int],
    ) -> dict:
        # Create query for model
        model = get_model_from_tablename(table)
        query = model.query

        # Apply all sorts of filters, ordering etc.
        query = self._apply_order(query, model, order, sort_by)
        if area != -1:
            query = self._apply_area(query, model, area)
        if filter_ != "all":
            query = self._apply_filter(query, model, filter_)
        if effects:
            query = self._apply_effects(query, model, effects)

        # Create pagination based on query and return in
        pagination_obj = query.paginate(page=current_page,
                                        per_page=per_page)

        return {
            "items": [item.to_dict(minimal=minimal)
                      for item in pagination_obj.items],
            "pagination": {
                "has_next": pagination_obj.has_next,
                "has_previous": pagination_obj.has_prev,
                "labels": list(pagination_obj.iter_pages()),
            }
        }

    def _apply_filter(self, query, model, filter_: str):
        # Filter rating type for monsters
        if match := re.match(r"rating:(\d)$", filter_):
            rating = int(match.group(1))
            return query.filter(model.rating_type == RatingType(rating))

        # Filter class land
        elif match := re.match(r"class_land:(\w)$", filter_):
            class_land = match.group(1)
            return query.filter(model.class_land.contains(class_land))

        # Filter class sea
        elif match := re.match(r"class_sea:(\w)$", filter_):
            class_sea = match.group(1)
            return query.filter(model.class_sea.contains(class_sea))

        # Filter core essences
        elif match := re.match(r"core_essence:(\d)$", filter_):
            core_essence = bool(int(match.group(1)))
            return query.filter(model.is_core_essence == core_essence)

        # Filter essence equip type essences
        elif match := re.match(r"essence_equip:(\d)$", filter_):
            equip_type = EssenceEquipType(int(match.group(1)))
            return query.filter(model.equip_type == equip_type)

        # Filter production type
        elif match := re.match(r"production:(\d)$", filter_):
            production = int(match.group(1))
            return query.filter(
                model.production_type == ProductionType(production))

        # If no filter was matched, but it was not all, just return the query
        # again :shrug:
        return query

    def _apply_effects(self, query, model, effects):
        # Applies a or filter for each bonus code
        for effect_code in effects:
            effect = EffectCode(effect_code)

            query = query.filter(
                or_(
                    model.bonus_1_code == effect,
                    model.bonus_2_code == effect,
                    model.bonus_3_code == effect,
                    model.bonus_4_code == effect,
                    model.bonus_5_code == effect,
                )
            )

        return query

    def _apply_area(self, query, model, area: int):
        try:
            return query.filter(model.area == Area(area))
        except AttributeError:
            return query

    def _apply_order(self, query, model, order: str, sort_by: str):
        try:
            column = getattr(model, sort_by)
        except AttributeError:
            column = getattr(model, "index")

        if order == "asc":
            return query.order_by(column.asc())
        elif order == "desc":
            return query.order_by(column.desc())
