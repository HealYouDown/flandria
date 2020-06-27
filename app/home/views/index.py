import os

from flask import current_app, render_template

from app.extensions import cache
from app.home.blueprint import home_bp
from app.api.helpers import get_table_cls_from_tablename
from app.constants import DATABASE_TABLENAMES
from typing import Tuple


@cache.memoize(timeout=0)
def get_icon_and_name(path: str) -> Tuple[str, str]:
    # Preview for links
    icon = "/static/assets/favicon.png"
    name = "Flandria"

    path_splitted = path.split("/")
    if "database" in path_splitted and len(path_splitted) == 3:
        # ["database", "tablename", "code"] = 3
        tablename, code = path_splitted[1:]
        if tablename in DATABASE_TABLENAMES:
            table_cls = get_table_cls_from_tablename(tablename)
            obj = table_cls.query.get(code)

            if obj is not None:
                if tablename == "production":
                    obj = obj.result_item

                name = obj.name

                if tablename == "quest":
                    pass
                elif tablename == "monster":
                    icon = "/static/assets/monster_icons/" + obj.icon
                else:
                    icon = "/static/assets/item_icons/" + obj.icon

    return icon, name


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

    # link preview
    icon, name = get_icon_and_name(path)

    return render_template("index.html",
                           bundle_fname="bundles/" + bundle_fname,
                           icon=icon,
                           name=name)
