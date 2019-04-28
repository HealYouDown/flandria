from functools import wraps
from flask import flash, abort
from flask_login import current_user

def check_can_edit_drops(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.can_edit_drops:
            abort(403)
        return func(*args, **kwargs)

    return decorated_function
