from flask import abort, jsonify, request
from flask_jwt_extended import get_current_user, jwt_required

from app.api.blueprint import api_bp
from app.extensions import db, cache
from app.models import Drop, Monster, ItemList
from app.webhook import (send_add_drop_webhook, send_delete_drop_webhook,
                         send_edit_drop_webhook)
from .detailed_view import get_response


@api_bp.route("/drops/add", methods=["POST"])
@jwt_required
def add_drop():
    user = get_current_user()
    if not user.is_able_to_edit_drops:
        return abort(401)

    json = request.json

    item_code = json.get("item_code", None)
    monster_code = json.get("monster_code", None)

    if item_code is None:
        return jsonify({"msg": "item_code is missing"}), 422

    if monster_code is None:
        return jsonify({"msg": "monster_code is missing"}), 422

    # Check if drop exists
    if Drop.query.filter(Drop.monster_code == monster_code,
                  Drop.item_code == item_code).count() != 0:
        return jsonify({"msg": "Drop already exists"}), 422

    # webhook
    monster = Monster.query.get(monster_code)
    item = ItemList.query.get(item_code)
    try:
        send_add_drop_webhook(monster, item, user)
    except:  # noqa E722
        pass

    drop = Drop(monster_code=monster_code, item_code=item_code, quantity=1)
    db.session.add(drop)
    db.session.commit()

    # Clear cache
    cache.delete_memoized(get_response)

    return jsonify({
        "msg": "Drop was added successfully",
        "drop": drop.to_dict(exclude_monster=True)
    }), 201


@api_bp.route("/drops/edit", methods=["PATCH"])
@jwt_required
def edit_drop():
    user = get_current_user()
    if not user.is_able_to_edit_drops:
        return abort(401)

    json = request.json

    drop_id = json.get("drop_id", None)
    new_quantity = json.get("new_quantity", None)

    if drop_id is None:
        return jsonify({"msg": "drop_id is missing"}), 422

    if new_quantity is None:
        return jsonify({"msg": "new_quantity is missing"}), 422

    drop = Drop.query.filter(Drop.index == drop_id).first()

    if drop is None:
        return jsonify({"msg": "Drop id does not exist"}), 404

    if new_quantity < 1:
        new_quantity = 1

    drop.quantity = new_quantity

    db.session.commit()

    # Clear cache
    cache.delete_memoized(get_response)

    # webhook
    monster = Monster.query.get(drop.monster_code)
    item = ItemList.query.get(drop.item_code)
    try:
        send_edit_drop_webhook(monster, item, new_quantity, user)
    except:  # noqa E722
        pass

    return jsonify({"msg": "Drop was updated successfully"}), 200


@api_bp.route("/drops/delete", methods=["DELETE"])
@jwt_required
def delete_drop():
    user = get_current_user()
    if not user.is_able_to_edit_drops:
        return abort(401)

    json = request.json

    drop_id = json.get("drop_id", None)

    if drop_id is None:
        return jsonify({"msg": "drop_id is missing"}), 422

    drop = Drop.query.filter(Drop.index == drop_id).first()

    if drop is None:
        return jsonify({"msg": "Drop id does not exist"}), 404

    db.session.delete(drop)
    db.session.commit()

    # Clear cache
    cache.delete_memoized(get_response)

    # webhook
    monster = Monster.query.get(drop.monster_code)
    item = ItemList.query.get(drop.item_code)
    try:
        send_delete_drop_webhook(monster, item, user)
    except: # noqa E722
        pass

    return jsonify({"msg": "Drop was deleted successfully"}), 200
