from flask import jsonify, request

from app.api.blueprint import api_bp
from app.extensions import cache, db
from app.models import Guild, Player


@api_bp.route("/ranking/guild")
def guilds_overview() -> dict:
    # Args
    current_page = int(request.args.get("page", 1))
    order = request.args.get("order", "asc")
    sort = request.args.get("sort", "avg_rank")
    filter_ = request.args.get("filter", "all")
    search = request.args.get("search", "").strip()

    query = Guild.query

    # Order
    if order == "asc":
        query = query.order_by(getattr(Guild, sort).asc())
    elif order == "desc":
        query = query.order_by(getattr(Guild, sort).desc())

    # Filter
    if filter_.startswith("server"):
        # Filters monster tables rating type.
        server = filter_.split(":")[-1]
        query = query.filter(
            getattr(Guild, "server") == server)

    if search:
        query = query.filter(
            getattr(Guild, "name").contains(search)
        )

    items_per_page = 60
    pagination_obj = query.paginate(page=current_page, per_page=items_per_page)

    response = {
        "items": [item.to_dict(minimal=True) for item in pagination_obj.items],
        "pagination": {
            "has_next": pagination_obj.has_next,
            "has_previous": pagination_obj.has_prev,
            "labels": list(pagination_obj.iter_pages()),
        }
    }

    return jsonify(response), 200


@api_bp.route("/ranking/guild/<name_hash>")
@cache.memoize(0)
def detailed_guilds_view(name_hash: str) -> dict:
    print(name_hash)
    guild = db.session.query(Guild).filter(Guild.name_hash == name_hash).first()

    return jsonify(guild.to_dict(minimal=False)), 200
