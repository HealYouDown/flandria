import os
from datetime import datetime
from flask.json import JSONEncoder

basedir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.abspath(os.path.join(basedir, os.pardir))


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        print(obj)
        try:
            if isinstance(obj, datetime):
                return str(obj)
        except TypeError:
            pass
        return JSONEncoder.default(self, obj)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", default="secret_key")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", default="secret_password_salt")
    GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", default="")

    JWT_ACCESS_LIFESPAN = {"days": 15}
    JWT_REFRESH_LIFESPAN = {"days": 15}

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    RESTFUL_JSON = {'cls': CustomJSONEncoder}

    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 900


class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"

    SQLALCHEMY_BINDS = {
        "user_data": "sqlite:///" + os.path.join(parentdir, "users.db"),
        "static_florensia_data": "sqlite:///" + os.path.join(parentdir, "static_florensia_data.db"),
        "unstatic_florensia_data": "sqlite:///" + os.path.join(parentdir, "unstatic_florensia_data.db"),
    }


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"

    SQLALCHEMY_BINDS = {
        "user_data": "sqlite:///" + os.path.join(basedir, "users.db"),
        "static_florensia_data": "sqlite:///" + os.path.join(basedir, "static_florensia_data.db"),
        "unstatic_florensia_data": "sqlite:///" + os.path.join(basedir, "unstatic_florensia_data.db"),
    }
