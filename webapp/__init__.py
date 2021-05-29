from webapp.api.planner.planner_build import PlannerBuildView, PlannerStarView
from database_updater.cli import drops_cli, updater_cli
from flask import Flask

from webapp.api.auth import LoginView, RegisterView
from webapp.api.database import DetailedTableView, MapView, Search, TableView
from webapp.api.planner import PlannerView
from webapp.api.ranking import (GuildDetailedView, GuildOverviewView,
                                RankingStatisticsView, PlayerDetailedView,
                                PlayerOverviewView)
from webapp.config import DevelopmentConfig, ProductionConfig, TestingConfig
from webapp.extensions import api_, cache, db, jwt, migrate
from webapp.main import main_bp
from webapp.tasks import tasks_cli
from webapp.utils import gzip_response, set_cors_header  # noqa: F401
from webapp.loaders import user_lookup_loader


def create_app(
    debug: bool = False,
    testing: bool = False
) -> Flask:
    """Creates and configures a flask application object.

    Args:
        debug (bool, optional): Whether the app should be run with the debug
            config. Defaults to False.
        testing (bool, optional): Whether the app should be run with the
            testing config. Defaults to False.

    Returns:
        Flask: The application object.
    """
    app = Flask(__name__)

    # Config
    if testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig if debug
                               else ProductionConfig)

    # Extensions
    register_extensions(app)

    # Register blueprints
    register_blueprints(app)

    # Register api endpoints
    register_api_endpoints()

    # Commands
    register_commands(app)

    # Register functions for extensions
    jwt.user_lookup_loader(user_lookup_loader)

    # Register teardown functions
    # app.after_request(gzip_response)
    if debug:
        app.after_request(set_cors_header)

    # Clear cache on startup
    with app.app_context():
        cache.clear()

    return app


def register_blueprints(app: Flask) -> None:
    """Registers all blueprints to the given app object.

    Args:
        app (Flask): The flask application object.
    """
    app.register_blueprint(main_bp)


def register_extensions(app: Flask) -> None:
    """Registers flask extensions to the application object.

    Args:
        app (Flask): The flask application object.
    """
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    api_.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)


def register_commands(app: Flask) -> None:
    """Registers custom commands to the flask db utilities.

    Args:
        app (Flask): The flask application object.
    """
    app.cli.add_command(updater_cli)
    app.cli.add_command(drops_cli)
    app.cli.add_command(tasks_cli)


def register_api_endpoints() -> None:

    # Database API
    database_ns = api_.namespace("/database")
    database_ns.add_resource(TableView, "/<table>")
    database_ns.add_resource(DetailedTableView, "/<table>/<code>")
    database_ns.add_resource(Search, "/search")
    database_ns.add_resource(MapView, "/map/<code>")

    # Auth API
    auth_ns = api_.namespace("/auth")
    auth_ns.add_resource(RegisterView, "/register")
    auth_ns.add_resource(LoginView, "/login")

    # Planner API
    planner_ns = api_.namespace("/planner")
    planner_ns.add_resource(PlannerView, "/<classname>")
    planner_ns.add_resource(PlannerBuildView,
                            "/<string:classname>/builds",
                            "/builds/<int:id>/delete",
                            "/builds/add")
    planner_ns.add_resource(PlannerStarView,
                            "/builds/<int:build_id>/star/add",
                            "/builds/<int:build_id>/star/delete")

    # Ranking API
    ranking_ns = api_.namespace("/ranking")
    ranking_ns.add_resource(RankingStatisticsView, "/statistics")
    ranking_ns.add_resource(GuildOverviewView, "/guilds")
    ranking_ns.add_resource(GuildDetailedView, "/guilds/<path:name>")
    ranking_ns.add_resource(PlayerOverviewView, "/players/<server>")
    ranking_ns.add_resource(PlayerOverviewView, "/players")
    ranking_ns.add_resource(PlayerDetailedView, "/players/<server>/<name>")
