from flask import Flask

from app.api.blueprint import api_bp
from app.auth.blueprint import auth_bp
from app.config import DevelopmentConfig, ProductionConfig
from app.converters import RegexConverter
from app.extensions import cache, db, jwt
from app.home.blueprint import home_bp
from app.models import User
from app.update_server import update_server


@jwt.user_loader_callback_loader
def user_loader(jwt_identity: dict):
    return User.query.filter(User.username == jwt_identity["username"]).first()


def create_app(development: False) -> Flask:
    app = Flask(__name__.split('.')[0])

    # Config
    if development:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    # Url converters
    app.url_map.converters['regex'] = RegexConverter

    # Extensions
    db.init_app(app)
    db.reflect(bind="unstatic_data", app=app)
    cache.init_app(app)
    jwt.init_app(app)

    # Update Server rule
    app.add_url_rule(
        "/update-server",
        "update_server",
        view_func=update_server,
        methods=["POST"]
    )

    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)

    # Clear cache on startup
    with app.app_context():
        cache.clear()
        """
        db.create_all()

        import json
        from app.models import User
        import datetime
        with open("user.json", "r") as f:
            userd = json.load(f)

        for user in userd:
            user = User(username=user["username"], password=user["password"],
                        email=user["email"],
                        register_date=datetime.datetime.strptime(
                            user["register_date"],
                            "%Y-%m-%d %H:%M:%S.%f"),
                        can_edit_drops=bool(int(user["_can_edit_drops"])))
            db.session.add(user)
        db.session.commit()
        """
    return app
