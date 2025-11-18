import os

import click

from src.core.constants import (
    DROPS_DATA_PATH,
    MAPS_DATA_PATH,
    OUTPUT_ASSETS_FOLDER,
)
from src.database.base import Base
from src.database.engine import engine
from src.updater.load_availble_3d_models import load_available_3d_models
from src.updater.load_drops import load_drops
from src.updater.load_maps import load_maps
from src.updater.updater import (
    download_updater_files,
    fix_fk_violations,
    update_tables,
)


@click.group(name="database", chain=True)
def database_cli():
    pass


@database_cli.command("init")
def init_cli():
    from src.database import models  # noqa: F401

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@database_cli.command("download")
@click.option(
    "--skip-existing/--keep-existing",
    default=False,
    help="Skips files that are already present",
)
def download_cli(skip_existing: bool):
    """Downloads the required files to update the database."""
    download_updater_files(skip_existing)


@database_cli.command("update")
@click.argument("tablenames", nargs=-1)
def update_cli(tablenames: list[str]):
    """Updates the database."""
    update_tables(tablenames)


@database_cli.command("drops")
@click.option(
    "--path",
    type=click.Path(exists=True, readable=True),
    default=DROPS_DATA_PATH,
)
def load_drops_cli(path: str):
    """Loads drop files into the database."""
    load_drops(path)


@database_cli.command("maps")
@click.option(
    "--path",
    type=click.Path(exists=True, readable=True),
    default=MAPS_DATA_PATH,
)
def load_maps_cli(path):
    """Loads map files (monsters and respawn timers) into the database."""
    load_maps(path)


@database_cli.command("models")
@click.option(
    "--path",
    type=click.Path(exists=True, readable=True),
    default=os.path.join(OUTPUT_ASSETS_FOLDER, "models"),
)
def load_available_3d_models_cli(path):
    """Loads 3d models from assets into the database."""
    load_available_3d_models(path)


@database_cli.command("prune")
def prune():
    """Removes all FK violations from the database. It is recommended
    to run this after you update the database."""
    fix_fk_violations()
