from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, gettext
import config
import operator

app = Flask(__name__)
login_manager = LoginManager()
db = SQLAlchemy()
babel = Babel()

@app.errorhandler(404)
def error_404(error):
    return render_template("404.html"), 404

# Custom Filters
@app.template_filter()
def is_list(value):
    return isinstance(value, list)

@app.template_filter("any_item_contains")
def any_list_item_contains(list_, value):
    if any(value in item for item in list_):
        return True
    else:
        return False

@app.template_filter("has_given_star")
def has_given_star(user, star_list):
    return any(star.user_id == user.id for star in star_list)

@app.template_filter("getattr")
def getattr_filter(obj, name):
    try:
        return operator.attrgetter(name)(obj)
    except AttributeError:
        return gettext("None")

@app.template_filter("type")
def check_type(obj, type_to_check):
    print(obj, type_to_check)
    return type(obj) == type_to_check

@app.context_processor
def stat_bonus_codes():
    return { 
        "BONUSCODES" : {
            "0": gettext("Max HP"),
            "1": gettext("Max MP"),
            "2": gettext("HP recovery"),
            "3": gettext("MP recovery"),
            "4": gettext("Physical avoidance rate"),
            "5": gettext("Moving speed"),
            "6": gettext("Melee max attack"),
            "7": gettext("Melee min attack"),
            "8": gettext("Range max attack"),
            "9": gettext("Range min attack"),
            "10": gettext("Magic max attack"),
            "11": gettext("Magic min attack"),
            "12": gettext("Physical defence"),
            "13": gettext("Magic resistance"),
            "14": gettext("Melee hitting"),
            "15": gettext("Long range hitting"),
            "16": gettext("Magic hitting"),
            "17": gettext("Melee attack speed"),
            "18": gettext("Range attack speed"),
            "19": gettext("Magic attack speed"),
            "20": gettext("Melee distance"),
            "21": gettext("Range distance"),
            "22": gettext("Magic distance"),
            "23": gettext("Melee critical rate"),
            "24": gettext("Range critical rate"),
            "25": gettext("Magic critical rate"),
            "43": gettext("Total Attack"), # FIXME: Not sure
            "69": gettext("Recovery skill up"),
            "76": None, # ship cannons
            "78": None, # ship cannons
            "81": None, # ship cannons
            "95": None, # ship cannons
            "99": None, # ship cannons
            "102": None, # special weapons
            "104": None, # special weapons
            "110": None, # special weapons
            "106": None, # ship cannons
            "113": gettext("Land EXP"),
            "114": gettext("Sea EXP"),
            "117": gettext("Fishing rate"),
            "126": gettext("All state"),
            "129": gettext("All Attack"),
            "131": gettext("Attack speed"),
            "154": gettext("Fishing time decrease"),
            "155": gettext("Constitution"),
            "156": gettext("Strength"),
            "157": gettext("Intelligence"),
            "158": gettext("Dexterity"),
            "159": gettext("Wisdom"),
            "160": gettext("Will"),
        },
    }

def create_app(production=False):
    if production:
        app.config.from_object(config.ProductionConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

    login_manager.init_app(app)
    db.init_app(app)
    babel.init_app(app)

    # Extensions
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    # Blueprints
    from webapp.home.controllers import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from webapp.auth.controllers import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from webapp.database.controllers import database as database_blueprint
    app.register_blueprint(database_blueprint)

    from webapp.planner.controllers import planner as planner_blueprint
    app.register_blueprint(planner_blueprint)

    from webapp.dashboard.controllers import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)

    return app