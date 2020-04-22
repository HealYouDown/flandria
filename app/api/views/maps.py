from flask import jsonify, request, abort

from app.api.blueprint import api_bp
from app.extensions import db, cache

from app.models import Map, MapPoint
from itertools import groupby
from flask_jwt_extended import get_current_user, jwt_required


@api_bp.route("/map/<code>")
@cache.memoize(timeout=0)
def map_points(code):
    map_ = Map.query.filter(Map.code == code).first()
    points = MapPoint.query.filter(MapPoint.map_code == code).order_by(MapPoint.monster_code.asc()).all()

    values = {}
    for monster_code, grouped_points in groupby(points, key=lambda p: p.monster_code):
        points_as_list = list(grouped_points)

        values[monster_code] = {
            "monster": points_as_list[0].monster.to_dict(),
            "points": [p.to_dict() for p in points_as_list]
        }

    data = {
        "map": map_.to_dict(),
        "values": values,
    }

    return jsonify(data), 200


@api_bp.route("/map/<code>", methods=["POST"])
@jwt_required
def add_point(code):
    user = get_current_user()
    if not user.is_admin:
        return abort(401)

    json = request.json

    point = MapPoint(
        x=json["x"],
        y=json["y"],
        z=json["z"],
        monster_code=json["monster_code"],
        map_code=code,
    )

    db.session.add(point)
    db.session.commit()

    return jsonify({"msg": "Point added"}), 201
