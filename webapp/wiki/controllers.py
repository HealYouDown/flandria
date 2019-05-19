from flask import Blueprint, render_template

wiki = Blueprint("wiki", __name__, url_prefix="/wiki")

@wiki.route("/")
def index():
    return render_template("wiki/index.html", title="Wiki")