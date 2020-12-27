from flask import request
from flask_jwt_extended import create_access_token
from flask_restx import Resource, abort
from webapp.models import User


class LoginView(Resource):
    def post(self):
        content: dict = request.json

        username = content.get("username", None)
        password = content.get("password", None)

        if not username:
            abort(400, "Username field is missing or empty.")
        elif not password:
            abort(400, "Password field is missing or empty.")

        # Check if user exists
        user: User = User.query.filter(User.username == username).first()
        if user is None:
            abort(404, "User does not exists.")

        # Check password
        if not user.check_password(password):
            abort(401, "Password does not match.")

        # Create JWT token
        access_token = create_access_token(
            identity=user.get_jwt_content(),
            # Prevents JWT tokens from expiring
            expires_delta=False)

        return {"access_token": access_token}, 200
