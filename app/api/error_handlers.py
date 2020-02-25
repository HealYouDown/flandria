from flask import jsonify
from werkzeug.exceptions import HTTPException

from app.api.blueprint import api_bp


@api_bp.errorhandler(HTTPException)
def errorhandler(e):
    return jsonify({
        "msg": str(e),
    }), e.code
