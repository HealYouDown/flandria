from flask import Blueprint, render_template, send_from_directory, request, url_for, current_app, make_response, redirect

home = Blueprint("home", __name__)

@home.route("/")
def index():
    return render_template("home/index.html", title="Home")

@home.route("/language/<language_code>")
def set_language(language_code):
    url = request.args.get("url")
    if url:
        resp = make_response(redirect(url))
    else:
        resp = make_response(redirect(url_for("home.index")))
    resp.set_cookie('flandria-language', language_code, max_age=60*60*24*365*1)
    return resp

@home.route('/robots.txt')
def robots_txt():
    return send_from_directory(current_app.static_folder, request.path[1:])

@home.route('/sitemap.xml')
def sitemap_xml():
    return send_from_directory(current_app.static_folder, request.path[1:])

