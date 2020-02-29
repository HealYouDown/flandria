from flask import jsonify, request
from flask_jwt_extended import create_access_token

from app.auth.blueprint import auth_bp
from app.models import User


@auth_bp.route("/login", methods=["POST"])
def login():
    json = request.json

    username = json.get("username", "")
    password = json.get("password", "")

    if not username:
        response = {"msg": "Username is required."}
        response_code = 422
        return jsonify(response), response_code

    if not password:
        response = {"msg": "Password is required."}
        response = 422
        return jsonify(response), response_code

    # Get user object
    user = User.query.filter_by(username=username).first()

    # Check if user exists
    if user is None:
        response = {"msg": "User was not found."}
        response_code = 404
        return jsonify(response), response_code

    # Check if passwords are equal
    if not user.check_password(password):
        response = {"msg": "Password does not match."}
        response_code = 401
        return jsonify(response), response_code

    # Create access token
    token = create_access_token({
        "id": user.id,
        "username": user.username,
        "admin": user.is_admin,
        "can_see_hidden": user.is_able_to_see_hidden,
        "can_edit_drops": user.is_able_to_edit_drops,
        "can_see_probability": user.is_able_to_see_probability
    })

    return jsonify({"access_token": token}), 200
