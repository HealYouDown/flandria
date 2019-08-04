import app.database.models as db_models
import pytz
import datetime


def tablename_to_class_name(tablename: str):
    parts = [part.title() for part in tablename.split('_')]
    return ''.join(part for part in parts)


def get_current_time():
    utc = pytz.timezone('UTC')
    now = utc.localize(datetime.datetime.utcnow())
    tz = pytz.timezone('Europe/Berlin')
    time = now.astimezone(tz)
    return time


def get_icon_and_name(path):
    from app.database.utils import tables

    splits = path.split("/")
    len_splits = len(splits)

    icon = "/static/img/favicon.png"
    name = "Flandria"

    if len_splits == 3 and "database" in splits:
        table, code = splits[1:]
        if table in tables.keys():

            table_cls = getattr(db_models, tablename_to_class_name(table))
            item = table_cls.query.get(code)

            if item is not None:

                name = item.name

                if table == "quest":
                    pass
                elif table == "monster":
                    icon = "/static/img/monster_icons/" + item.icon
                else:
                    icon = "/static/img/item_icons/" + item.icon

    return icon, name
