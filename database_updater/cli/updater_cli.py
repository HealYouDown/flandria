import logging

import click
from flask import current_app
from flask.cli import AppGroup

# Command group
updater_cli = AppGroup("updater")

# TODO: Set the logging level outside for the whole group,
# not in each function seperately.


@updater_cli.command("download")
def update_download_cli() -> None:
    """CLI Implementation to download patchserver files.

    Example:
    >> flask updater download
    """
    current_app.logger.setLevel(logging.INFO)

    from database_updater.download import download
    download()


@updater_cli.command("database")
@click.argument("tables",
                type=str,
                nargs=-1)
def update_database_cli(tables: tuple) -> None:
    """CLI Implementation to update the database.

    Example:
    >> flask updater database
    """
    current_app.logger.setLevel(logging.INFO)

    from database_updater.update_database import update_database

    update_database(tables)


@updater_cli.command("icons")
def update_icons_cli() -> None:
    """CLI Implementation to update the icons.

    Example:
    >> flask updater icons
    """
    current_app.logger.setLevel(logging.INFO)

    from database_updater.update_icons import update_icons
    update_icons()
