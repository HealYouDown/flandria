import os

from flask import current_app, render_template

from app.extensions import cache
from app.home.blueprint import home_bp


@cache.memoize(timeout=0)
def get_bundle_filename():
    bundles_path = os.path.join(current_app.static_folder, "bundles")

    bundle_fname = filter(lambda f: f.endswith("bundle.js"),
                          os.listdir(bundles_path))

    return next(bundle_fname)


@home_bp.route('/', defaults={'path': ''})
@home_bp.route('/<path:path>')
def index(path):
    if current_app.config.get("ENV") == "development":
        bundle_fname = "bundle.js"
    else:
        bundle_fname = get_bundle_filename()

    return render_template("index.html",
                           bundle_fname="bundles/" + bundle_fname)
