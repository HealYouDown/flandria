import os
import platform
import shutil

import click
from loguru import logger

from src.assets.icons.icons import download_icon_files, extract_icons
from src.assets.models import download_model_files, process_models
from src.core.constants import OUTPUT_ASSETS_FOLDER


@click.group(name="assets")
def assets_cli():
    pass


@assets_cli.group(name="icons", chain=True)
def assets_icons_cli():
    pass


@assets_cli.group(name="models", chain=True)
def assets_models_cli():
    pass


@assets_icons_cli.command("download")
@click.option(
    "--skip-existing/--keep-existing",
    default=False,
    help="Skips files that are already present",
)
def icons_download_cli(skip_existing: bool):
    """Downloads all required icons. Requires a filled database."""
    download_icon_files(skip_existing)


@assets_icons_cli.command("extract")
@click.option(
    "--path",
    type=click.Path(),
    default=os.path.join(OUTPUT_ASSETS_FOLDER, "icons"),
)
def icons_extract_cli(path: str):
    """Extracts all required icons. Requires downloaded icon files and a filled database."""

    if os.path.exists(path):
        click.confirm(
            "Output folder for icons already exists, delete?",
            default=False,
            abort=True,
        )
        shutil.rmtree(path)
    os.makedirs(path)

    extract_icons(path)


@assets_models_cli.command("download")
@click.option(
    "--skip-existing/--keep-existing",
    default=False,
    help="Skips files that are already present",
)
def models_download_cli(skip_existing: bool):
    """Downloads all model files. Requires a filled database."""
    download_model_files(skip_existing)


@assets_models_cli.command("process")
@click.argument("model_groups", nargs=-1)
def models_process_cli(model_groups: list[str] | None):
    """Processes all model files. Requires downloaded model files and a filled database.
    Possible groups are: monster, npc, weapon, armor, dress, hat
    """
    if platform.system() != "Windows":
        logger.critical(
            "Models can only be processed on Windows due to depending on Noesis."
        )
        click.Abort()

    if not model_groups:
        model_groups = None
    process_models(model_groups)
