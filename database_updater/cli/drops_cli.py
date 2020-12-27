import logging

import click
from flask import current_app
from flask.cli import AppGroup

# Command group
drops_cli = AppGroup("drops")

# TODO: Set the logging level outside for the whole group,
# not in each function seperately.


@drops_cli.command("add")
@click.argument("monster_code", type=str)
@click.argument("item_code", type=str)
@click.argument("quantity", type=int)
def drops_add_cli(monster_code: str, item_code: str, quantity: int) -> None:
    current_app.logger.setLevel(logging.INFO)

    from webapp.models import Drop
    from webapp.extensions import db
    db.session.add(Drop(monster_code=monster_code,
                        item_code=item_code,
                        quantity=quantity))
    db.session.commit()
