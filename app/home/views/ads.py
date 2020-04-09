from flask import send_from_directory, current_app, send_file
from app.home.blueprint import home_bp
import os


@home_bp.route("/ads.txt", methods=["GET"])
def ads_txt():
    path = os.path.join(current_app.static_folder, "files")
    return send_from_directory(path, "ads.txt")
