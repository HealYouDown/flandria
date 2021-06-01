import os

WEBAPP_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(WEBAPP_DIR, os.pardir))


class Config:
    # Secret keys
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
    GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET",
                                           default="secret-github-key")
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY", default="jwt-secret-key")

    # Disables overhead of SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(os.path.join(
        ROOT_DIR, "database.db"))

    # RestX Configuration
    RESTX_JSON = {
        "indent": None,
    }

    ERROR_404_HELP = False

    JWT_IDENTITY_CLAIM = "identity"


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True

    CACHE_TYPE = "null"


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False

    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 900


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
    DEBUG = True
