import json
from typing import List
from app.models import ItemList, Production

from flask import abort, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_optional
from sqlalchemy import or_, and_, not_

from app.api.blueprint import api_bp
from app.api.helpers import get_hidden_item_codes, get_table_cls_from_tablename
from app.constants import DATABASE_TABLENAMES
from app.extensions import cache


@cache.memoize(timeout=0)
def get_response(
    tablename: str,
    table_cls,
    order: str,
    sort: str,
    filter_: str,
    current_page: int,
    location: str,
    bonuses: List[int],
    search: str,
    can_see_hidden: bool,
) -> dict:
    sort_column = sort if sort != "added" else "index"

    query = table_cls.query

    # Exclude hidden items
    if not can_see_hidden:
        query = query.filter(getattr(table_cls, "code").notin_(
            get_hidden_item_codes()
        ))

    # Filter out premium recipes for production
    if tablename == "production":
        query = query.filter(not_(and_(
            table_cls.type == "Essence",
            table_cls.division == 1
            ))
        )

    # Order
    if order == "asc":
        query = query.order_by(getattr(table_cls, sort_column).asc())
    elif order == "desc":
        query = query.order_by(getattr(table_cls, sort_column).desc())

    # Filter
    if filter_.startswith("rating_type"):
        # Filters monster tables rating type.
        desired_rating: int = int(filter_.split(":")[-1])
        query = query.filter(
            getattr(table_cls, "rating_type") == desired_rating)

    elif filter_.startswith("class_land"):
        # Class land
        requested_class = filter_.split(":")[-1]
        query = query.filter(
            getattr(table_cls, "class_land").contains(requested_class))

    elif filter_.startswith("equip"):
        # Essence equip type
        equip_type = int(filter_.split(":")[-1])
        query = query.filter(
            getattr(table_cls, "equip") == equip_type)

    elif filter_.startswith("prod_class"):
        production_class = filter_.split(":")[-1]
        query = query.filter(
            getattr(table_cls, "type").contains(production_class))

    # Location
    location_val = int(location.split(":")[-1])
    if location_val != -1:
        query = query.filter(
            getattr(table_cls, "location") == location_val
        )

    # Bonuses
    if bonuses:
        for bonus in bonuses:
            query = query.filter(
                or_(
                    getattr(table_cls, "bonus_code_1") == bonus,
                    getattr(table_cls, "bonus_code_2") == bonus,
                    getattr(table_cls, "bonus_code_3") == bonus,
                    getattr(table_cls, "bonus_code_4") == bonus,
                    getattr(table_cls, "bonus_code_5") == bonus,
                )
            )

    if search:
        if tablename == "production":
            query = (query.join(ItemList,
                               ItemList.code == Production.result_code)
                     .filter(ItemList.name.contains(search)))
        else:
            query = query.filter(
                table_cls.name.contains(search)
            )

    # 60 Items because we have cols of 1, 2, 3, 4 and 12 is a multiple of all
    # 4 numbers. (= Always have filled out rows) 60 Then seems like a good
    # amount to display
    items_per_page = 60
    pagination_obj = query.paginate(page=current_page, per_page=items_per_page)

    return {
        "items": [item.to_dict(minimal=True) for item in pagination_obj.items],
        "pagination": {
            "has_next": pagination_obj.has_next,
            "has_previous": pagination_obj.has_prev,
            "labels": list(pagination_obj.iter_pages()),
        }
    }


@api_bp.route("/database/<string:tablename>")
@jwt_optional
def overview(tablename: str):
    assert tablename in DATABASE_TABLENAMES, abort(404)

    user = get_jwt_identity()
    can_see_hidden = (True if (user is not None
                               and user["can_see_hidden"]
                               and tablename == "random_box")
                      else False)

    table_cls = get_table_cls_from_tablename(tablename)

    # Args
    current_page = int(request.args.get("page", 1))
    order = request.args.get("order", "asc")
    sort = request.args.get("sort", "added")
    filter_ = request.args.get("filter", "all")
    location = request.args.get("location", "location:-1")
    bonuses = json.loads(request.args.get("bonuses", "[]"))
    search = request.args.get("search", "").strip()

    # Get response object
    response = get_response(
        tablename=tablename,
        table_cls=table_cls,
        order=order,
        sort=sort,
        filter_=filter_,
        location=location,
        bonuses=bonuses,
        search=search,
        can_see_hidden=can_see_hidden,
        current_page=current_page
    )

    return jsonify(response), 200
