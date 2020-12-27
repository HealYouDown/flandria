import os
import time

import git
from flask import (Blueprint, current_app, render_template, request,
                   send_from_directory)
from webapp.api.database.constants import ALLOWED_DATABASE_TABLES
from webapp.api.database.utils import get_model_from_tablename
from webapp.main.check_git_signature import is_valid_signature
from webapp.models import ItemList, Monster, Npc, Quest

main_bp = Blueprint("main", __name__)


@main_bp.route("/", defaults={"path": ""})
@main_bp.route("/<path:path>")
def index(path: str):
    # To have a link preview, query based on given path
    icon = "favicon.png"
    name = "Flandria"

    splitted = path.split("/")
    if "database" in splitted and len(splitted) == 3:
        # database table code
        tablename = splitted[1]
        code = splitted[2]

        if tablename in ALLOWED_DATABASE_TABLES:
            model = get_model_from_tablename(tablename)
            obj = model.query.get(code)

            if tablename == "production":
                obj = obj.result_item

            if tablename == "monster":
                name = obj.name
                icon = f"monster_icons/{obj.icon}"
            elif tablename == "quest":
                name = obj.title
            elif tablename == "npc":
                name = obj.name
                icon = f"npc_icons/{obj.icon}"
            else:
                name = obj.name
                icon = f"item_icons/{obj.icon}"

    return render_template(
        "index.html",
        icon=f"/static/assets/{icon}",
        name=name,
    )


@main_bp.route("/static/js/<filename>")
def js_file(filename: str):
    """Sends the gzipped js file if it is supported by the browser."""
    accept_encoding = request.headers.get('Accept-Encoding', '')
    gzip_supported = "gzip" in accept_encoding

    if gzip_supported:
        filename += ".gz"

    resp = send_from_directory(
        directory=os.path.join(
            current_app.static_folder,
            "js",
        ),
        filename=filename,
        mimetype="text/javascript")

    # Increase cache timeout (365 days)
    # (we use cache busting, so it does not matter)
    resp.cache_control.max_age = 31536000

    if gzip_supported:
        # Set the new content type
        resp.headers.set("Content-Encoding", "gzip")

    return resp


@main_bp.route("/sitemap.txt")
def sitemap():
    base_url = "https://www.flandria.info"

    urls = [
        f"{base_url}",
        f"{base_url}/database",
        f"{base_url}/auth/login",
        f"{base_url}/auth/register",
        f"{base_url}/planner/mercenary",
        f"{base_url}/planner/saint",
        f"{base_url}/planner/noble",
        f"{base_url}/planner/explorer",
        f"{base_url}/planner/ship",
        f"{base_url}/about",
        f"{base_url}/privacy-policy",
        f"{base_url}/legal-notice",
    ]

    for tablename in ALLOWED_DATABASE_TABLES:
        urls.append(f"{base_url}/database/{tablename}")

    for monster in Monster.query.all():
        urls.append(f"{base_url}/database/monster/{monster.code}")

    for quest in Quest.query.all():
        urls.append(f"{base_url}/database/quest/{quest.code}")

    for item in ItemList.query.all():
        urls.append(f"{base_url}/database/{item.table}/{item.code}")

    for npc in Npc.query.all():
        urls.append(f"{base_url}/database/npc/{npc.code}")

    result = "\n".join(urls)

    return result


@main_bp.route("/update-server", methods=["POST"])
def update_server():
    """Runs by github workflow to update server."""
    x_hub_signature = request.headers.get("X-Hub-Signature", None)
    if x_hub_signature is None:
        return "Missing signature", 401

    github_webhook_secret = current_app.config["GITHUB_WEBHOOK_SECRET"]

    if not is_valid_signature(x_hub_signature,
                              request.data,
                              github_webhook_secret):
        return "Invalid", 401

    # Local path on server to the repo
    repo = git.Repo("flandria")
    origin = repo.remotes.origin

    _ = origin.pull()

    # touch wsgi file to reload server
    os.utime(r"/var/www/www_flandria_info_wsgi.p",
             (time.time(), time.time()))

    return "Updated server", 200
