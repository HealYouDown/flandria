import sys

import click
from loguru import logger

from .api import api_cli
from .assets import assets_cli
from .database import database_cli
from .utils import utils_cli


@click.group()
@click.option("--debug/--no-debug", default=False)
def entrypoint(debug: bool):
    level = "DEBUG" if debug else "INFO"

    logger.remove()
    logger.add(sys.stderr, level=level)

    if debug:
        logger.add("debug.log", level=level, colorize=False)


entrypoint.add_command(database_cli)
entrypoint.add_command(assets_cli)
entrypoint.add_command(utils_cli)
entrypoint.add_command(api_cli)
