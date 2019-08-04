import gzip
from datetime import datetime

from flask import (Blueprint, Flask, after_this_request, render_template,
                   request, send_from_directory, abort)
from flask.json import JSONEncoder
import os

from app.auth.api import register_auth_endpoints
from app.database.api import register_database_endpoints
from app.extensions import api, api_bp, db, guard
from app.planner.api import register_planner_endpoints
from app.utils import get_icon_and_name
from config import DevelopmentConfig, ProductionConfig
from werkzeug import Response
from werkzeug.wsgi import wrap_file

import gzip

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    icon, name = get_icon_and_name(path)
    bundle_filename = list(filter(lambda f: f.endswith("bundle.js"), os.listdir(app.static_folder)))[0]
    hash = bundle_filename.split(".")[0]

    return render_template("index.html", icon=icon, name=name, hash=hash)


@app.route("/static/bundle.js")
def bundle():
    accept_encoding = request.headers.get('Accept-Encoding', '')
    bundle_filename = list(filter(lambda f: f.endswith("bundle.js"), os.listdir(app.static_folder)))[0]

    if "gzip" in accept_encoding and app.config.get("ENV") == "production":
        # if browser supports, return gzipped file
        gziped_filename = bundle_filename + ".gz"

        # this shit took me 3 hours to figure out :))
        # I hate my life.
        headers = {}
        filename = os.path.join(app.static_folder, gziped_filename)
        fsize = os.path.getsize(filename)

        headers["Content-Length"] = fsize
        headers["Content-Encoding"] = "gzip"

        file = open(filename, "rb")
        data = wrap_file(request.environ, file)
        rv = app.response_class(
            data, mimetype="text/javascript", headers=headers, direct_passthrough=True
        )

        return rv
    else:
        return send_from_directory(app.static_folder, bundle_filename)


def create_app(development=True):
    if development:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    # Register API Endpoints
    register_database_endpoints(api)
    register_auth_endpoints(api)
    register_planner_endpoints(api)

    # Blueprints
    app.register_blueprint(api_bp)

    # Inits Extensions
    db.init_app(app)
    from app.auth.models import User
    guard.init_app(app, User)

    # with app.app_context():
    #    db.create_all()

    return app
