from functools import wraps
from app.extensions import guard
from flask_praetorian import current_user
from flask_praetorian.exceptions import InvalidTokenHeader, MissingTokenHeader
from flask_praetorian.decorators import _verify_and_add_jwt


def auth_optional(method):
    """
    Decorator to check if a token exists and then adds an argument
    to the wrapped function called 'user'.
    User is either the database user object or None, if no token was supplied.
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            token = guard.read_token_from_header()
            _verify_and_add_jwt()
            user = current_user()
        except (InvalidTokenHeader, MissingTokenHeader):
            user = None
        return method(*args, user=user, **kwargs)
    return wrapper


def catch_errors(method):
    """
    Catches and logs all errors in the wrapped function and returns an empty list
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            # TODO: Log Exception
            return []
    return wrapper
