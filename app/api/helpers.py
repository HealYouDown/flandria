from typing import List

from flask import abort

import app.models as models
from app.extensions import cache, db
from app.models import HiddenItem


def tablename_to_classname(tablename: str) -> str:
    """
    Capitalizes a given tablename.
    E.g. quest_scroll -> QuestScroll
    """
    parts = [part.title() for part in tablename.split("_")]
    return "".join(part for part in parts)


def get_table_cls_from_tablename(tablename: str):
    # Get table class based on tablename
    table_cls_name = tablename_to_classname(tablename)
    try:
        return getattr(models, table_cls_name)
    except AttributeError:  # table not found
        abort(404)


@cache.memoize(timeout=900)
def get_hidden_item_codes() -> List[str]:
    return [item.code for item in db.session.query(HiddenItem.code).all()]
