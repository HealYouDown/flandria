from flask import jsonify, request
from sqlalchemy import or_

from app.api.blueprint import api_bp
from app.models import ItemList


@api_bp.route("/search")
def search_database():
    search_string = request.args.get("s")

    query = (ItemList.query
             .filter(or_(ItemList.name.contains(search_string),
                         ItemList.code.contains(search_string)),
                     ItemList.code.notin_([]))
             .limit(30))

    return jsonify([obj.to_dict() for obj in query.all()])
