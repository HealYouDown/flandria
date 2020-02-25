import os

filedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.abspath(os.path.join(filedir, os.pardir))
parentdir = os.path.abspath(os.path.join(basedir, os.pardir))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get("SECRET_KEY", default="secret_key")
    GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", default="")

    JWT_SECRET_KEY = os.environ.get("SECRET_KEY", default="jwt-secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = False  # Token do not expire


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True

    CACHE_TYPE = "null"

    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_BINDS = {
        "static_data": "sqlite:///{fp}".format(
            fp=os.path.join(basedir, "database.db")),
        "unstatic_data": "sqlite:///{fp}".format(
            fp=os.path.join(basedir, "unstatic_data.db")),
        "user_data": "sqlite:///{fp}".format(
            fp=os.path.join(basedir, "user_data.db")),
    }


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False

    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 900

    SQLALCHEMY_BINDS = {
        "static_data": "sqlite:///{fp}".format(
            fp=os.path.join(parentdir, "database.db")),
        "unstatic_data": "sqlite:///{fp}".format(
            fp=os.path.join(parentdir, "unstatic_data.db")),
        "user_data": "sqlite:///{fp}".format(
            fp=os.path.join(parentdir, "user_data.db")),
    }
