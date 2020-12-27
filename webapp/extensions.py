from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
api_ = Api(version="1.0", title="Flandria API", prefix="/api",
           doc=False)
jwt = JWTManager()
cache = Cache()
