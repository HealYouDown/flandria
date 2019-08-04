from flask import abort, jsonify, request
from flask_restful import Resource

from app.auth.models import User
from app.extensions import db, guard


class Login(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username or username is None:
            return abort(400, "Username is missing.")

        if not password or password is None:
            return abort(400, "Password is missing.")

        user = User.query.filter(User.username.ilike(username)).first()

        if user is None:
            return abort(404, "User not found")

        if not user.check_password(password):
            return abort(401, "Username and password do not match.")

        custom_claims = {
            "username": user.username,
            "admin": user.admin,
            "can_edit_drops": user.can_edit_drops,
            "can_see_hidden": user.can_see_hidden,
        }

        token = guard.encode_jwt_token(user, **custom_claims)

        return {"access_token": token}, 200


class Register(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        email = request.json.get("email", None)

        if not username or username is None:
            return abort(400, "Username is missing.")

        if not email or email is None:
            return abort(400, "E-Mail is missing.")

        if "@" not in email or "." not in email:
            return abort(400, "Wrong E-Mail format.")

        if not password or password is None:
            return abort(400, "Password is missing.")

        if User.query.filter(User.username.ilike(username)).first() is not None:
            return abort(409, "Username is already taken.")

        if User.query.filter(User.email.ilike(email)).first() is not None:
            return abort(409, "E-Mail is already taken.")

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


class Refresh(Resource):
    def get(self):
        old_token = guard.read_token_from_header()
        new_token = guard.refresh_jwt_token(old_token)
        return {"access_token": new_token}, 200


def register_auth_endpoints(api):
    api.add_resource(Login, "/auth/login")
    api.add_resource(Register, "/auth/register")
    api.add_resource(Refresh, "/auth/refresh")
