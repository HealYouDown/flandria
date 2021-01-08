import logging

from flask import current_app
from flask.cli import AppGroup

tasks_cli = AppGroup("tasks")


@tasks_cli.command("update-ranking")
def update_ranking_cli():
    from webapp.tasks.update_ranking import update_ranking

    current_app.logger.setLevel(logging.INFO)
    update_ranking()
