import os

from flask import current_app, request, send_from_directory

from app.home.blueprint import home_bp


@home_bp.route(
    r"/static/bundles/<regex('[a-z0-9_]{20}\.bundle\.js'):bundle_fname>"
)
def bundle(bundle_fname: str):
    # returns [hash].bundle.js.gz if gzip is supported, else the normal bundle
    accept_encoding = request.headers.get('Accept-Encoding', '')
    gzip_supported = ("gzip" in accept_encoding and
                      current_app.config.get("ENV") == "production")

    gzip_supported = False
    if gzip_supported:
        bundle_fname += ".gz"

    bundles_path = os.path.join(current_app.static_folder,
                                "bundles")

    # Response object
    rv = send_from_directory(bundles_path,
                             bundle_fname,
                             mimetype="text/javascript")

    # Increase cache timeout (365 days)
    rv.cache_control.max_age = 31536000

    if gzip_supported:
        rv.headers.set("Content-Encoding", "gzip")

    return rv


@home_bp.route("/static/bundles/bundle.js")
def dev_bundle():
    bundles_path = os.path.join(current_app.static_folder,
                                "bundles")

    # Response object
    rv = send_from_directory(bundles_path,
                             "bundle.js",
                             mimetype="text/javascript")

    return rv
