from flask import jsonify, request

from app.auth.blueprint import auth_bp
from app.extensions import db
from app.models import User


@auth_bp.route("/register", methods=["POST"])
def register():
    json = request.json

    username = json.get("username", "")
    email = json.get("email", "")
    password = json.get("password", "")

    if not username:
        response = {"msg": "Username is required."}
        response_code = 422
        return jsonify(response), response_code

    if not password:
        response = {"msg": "Password is required."}
        response_code = 422
        return jsonify(response), response_code

    if not email:
        response = {"msg": "E-Mail is required."}
        response_code = 422
        return jsonify(response), response_code

    if User.query.filter_by(username=username).count() > 0:
        response = {"msg": "User with this username already exists."}
        response_code = 409
        return jsonify(response), response_code

    if User.query.filter_by(email=email).count() > 0:
        response = {"msg": "User with this E-Mail already exists."}
        response_code = 409
        return jsonify(response), response_code

    # Create user object
    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    response = {"msg": "User was registered successfully."}
    response_code = 201

    return jsonify(response), response_code
