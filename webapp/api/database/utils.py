import webapp.models as models
from flask_restx import abort
from flask_sqlalchemy.model import DefaultMeta


def tablename_to_classname(tablename: str) -> str:
    """Capitalizes a given tablename.

    Args:
        tablename (str): The tablename to format to classname syntax.

    Returns:
        str: the class name of the model, if correct syntax is assumed.
    """
    parts = [part.title() for part in tablename.split("_")]
    return "".join(part for part in parts)


def get_model_from_tablename(tablename: str) -> DefaultMeta:
    """Returns the model for the given tablename.

    Args:
        tablename (str): Tablename.

    Returns:
        DefaultMeta: The model.
    """
    try:
        return getattr(models, tablename_to_classname(tablename))
    except AttributeError:
        abort(404, "Table not found.")
