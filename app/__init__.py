import gzip
import os
from zlib import adler32

from flask import Flask, render_template, request, send_from_directory
from werkzeug.wsgi import wrap_file

from app.auth.api import register_auth_endpoints
from app.database.api import register_database_endpoints
from app.extensions import api, api_bp, db, guard
from app.planner.api import register_planner_endpoints
from app.regex_converter import RegexConverter
from app.utils import get_icon_and_name
from config import DevelopmentConfig, ProductionConfig

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    icon, name = get_icon_and_name(path)
    bundle_filename = list(filter(lambda f: f.endswith("bundle.js"), os.listdir(app.static_folder)))[0]

    return render_template("index.html", icon=icon, name=name, bundle_filename=bundle_filename)


def bundle(bundle_filename):
    accept_encoding = request.headers.get('Accept-Encoding', '')

    if "gzip" in accept_encoding:
        bundle_filename += ".gz"

        headers = {}
        filepath = os.path.join(app.static_folder, bundle_filename)
        fsize = os.path.getsize(filepath)

        headers["Content-Length"] = fsize
        headers["Content-Encoding"] = "gzip"
        headers["Cache-Control"] = "public, max-age=43200"

        file = open(filepath, "rb")
        data = wrap_file(request.environ, file)
        rv = app.response_class(
            data, mimetype="text/javascript", headers=headers, direct_passthrough=True
        )

        rv.set_etag(
            "%s-%s-%s"
            % (
                os.path.getmtime(filepath),
                os.path.getsize(filepath),
                adler32(
                    filepath.encode("utf-8")
                    if isinstance(filepath, str)
                    else filepath
                ) & 0xFFFFFFFF,
            )
        )

    else:
        rv = send_from_directory(app.static_folder, bundle_filename, mimetype="text/javascript")

    return rv


def create_app(development=True):
    # Settings
    if development:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    # Regex Converter
    app.url_map.converters['regex'] = RegexConverter

    # Register API Endpoints
    register_database_endpoints(api)
    register_auth_endpoints(api)
    register_planner_endpoints(api)

    # Register normal endpoints
    from app.update_server import update_server
    app.add_url_rule(
        "/update-server",
        "update_server",
        view_func=update_server,
        methods=["POST"]
    )
    app.add_url_rule(
        "/static/<regex('[a-z0-9_]{20}\.bundle\.js'):bundle_filename>",
        "bundle",
        view_func=bundle,
        methods=["GET"]
    )
    # Blueprints
    app.register_blueprint(api_bp)

    # Inits Extensions
    db.init_app(app)
    from app.auth.models import User
    guard.init_app(app, User)

    # with app.app_context():
    #    db.create_all()

    return app
