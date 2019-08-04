from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian
from flask_restful import Api
from flask import Blueprint

db = SQLAlchemy()

guard = Praetorian()

api_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api = Api(api_bp)
