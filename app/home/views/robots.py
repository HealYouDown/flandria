from app.home.blueprint import home_bp


@home_bp.route("/robots.txt")
def robots_txt():
    return "Sitemap: https://www.flandria.info/sitemap.txt"
