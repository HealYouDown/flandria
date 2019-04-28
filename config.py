import os

basedir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.abspath(os.path.join(basedir, os.pardir))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", default="secret_key")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", default="secret_password_salt")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    LANGUAGES = {
        "de": "Deutsch",
        "en": "English",
    }


class DevelopmentConfig(Config):
    SQLALCHEMY_BINDS = {
        "user_data": "sqlite:///" + os.path.join(basedir, "users.db"),
        "static_florensia_data": "sqlite:///" + os.path.join(basedir, "static_florensia_data.db"),
        "unstatic_florensia_data": "sqlite:///" + os.path.join(basedir, "unstatic_florensia_data.db"),
        "logs_data": "sqlite:///" + os.path.join(basedir, "logs.db"),
    }

    DEBUG = True
    FLASK_DEBUG = True
    ENV = "development"

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    SQLALCHEMY_BINDS = {
        "user_data": "sqlite:///" + os.path.join(parentdir, "users.db"),
        "static_florensia_data": "sqlite:///" + os.path.join(parentdir, "static_florensia_data.db"),
        "unstatic_florensia_data": "sqlite:///" + os.path.join(parentdir, "unstatic_florensia_data.db"),
        "logs_data": "sqlite:///" + os.path.join(parentdir, "logs.db"),
    }
