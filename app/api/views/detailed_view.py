from flask import abort, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_optional

from app.api.blueprint import api_bp
from app.api.helpers import get_table_cls_from_tablename
from app.api.table_to_extras import (
    TABLE_TO_EXTRA, get_after_quest, get_dropped_by, get_drops, get_needed_for,
    get_produced_by, get_quest_scrolls, get_quests, get_quests_by_item,
    get_quests_by_scroll, get_random_boxes, get_upgrade_data, get_maps)
from app.constants import DATABASE_TABLENAMES
from app.extensions import cache


@cache.memoize(timeout=0)
def get_response(
    tablename: str,
    code: str,
    can_see_probability: bool,
) -> dict:
    table_cls = get_table_cls_from_tablename(tablename)

    response = {}

    # Base item
    obj = table_cls.query.get_or_404(code)
    if tablename == "random_box":
        response["obj"] = obj.to_dict(can_see_probability=can_see_probability)
    else:
        response["obj"] = obj.to_dict()

    # Extra data that is included
    extras = TABLE_TO_EXTRA[tablename]
    for extra in extras:
        if extra == "drops":
            response[extra] = get_drops(obj.code)

        elif extra == "maps":
            response[extra] = get_maps(obj.code)

        elif extra == "quests":
            response[extra] = get_quests(obj.code)

        elif extra == "dropped_by":
            response[extra] = get_dropped_by(obj.code)

        elif extra == "upgrade_data":
            response[extra] = get_upgrade_data(obj.upgrade_code)

        elif extra == "quests_by_item":
            response[extra] = get_quests_by_item(obj.code)

        elif extra == "quests_by_scroll":
            response[extra] = get_quests_by_scroll(obj.quest_code)

        elif extra == "random_boxes":
            response[extra] = get_random_boxes(obj.code)

        elif extra == "needed_for":
            response[extra] = get_needed_for(obj.code)

        elif extra == "produced_by":
            response[extra] = get_produced_by(obj.code)

        elif extra == "after_quest":
            response[extra] = get_after_quest(obj.code)

        elif extra == "quest_scrolls":
            response[extra] = get_quest_scrolls(obj.code)

    return response


@api_bp.route("/database/<string:tablename>/<string:code>")
@jwt_optional
def detailed_view(tablename: str, code: str):
    assert tablename in DATABASE_TABLENAMES, abort(404)

    user = get_jwt_identity()
    can_see_probability = (True if (user is not None and
                                    user["can_see_probability"])
                           else False)

    response = get_response(
        tablename=tablename,
        code=code,
        can_see_probability=can_see_probability,
    )

    return jsonify(response), 200
