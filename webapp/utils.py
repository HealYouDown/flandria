import pytz
import datetime
from webapp import babel
from flask import request, current_app

def get_current_time(*args):
    utc = pytz.timezone('UTC')
    now = utc.localize(datetime.datetime.utcnow())
    tz = pytz.timezone('Europe/Berlin')
    time = now.astimezone(tz)
    if args: # logging gives us two unnecessary args, that's why we know when to return tuple and when datetime obj
        return time.timetuple()
    return time

@babel.localeselector
def get_locale():
    cookie = request.cookies.get('flandria-language')
    if cookie and cookie in current_app.config["LANGUAGES"]:
        return cookie

    return "en"

@babel.timezoneselector
def get_timezone():
    return None