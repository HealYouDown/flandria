from flask import jsonify, request

from app.api.blueprint import api_bp
from app.extensions import db, cache

from app.models import Map, MapPoint
from itertools import groupby


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
