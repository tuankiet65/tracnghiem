import datetime
import random
import string

from . import app
from .database import School


def generate_random_string(length: int = 50) -> string:
    rand = random.SystemRandom()
    letters = string.ascii_letters + string.digits
    return ''.join(rand.choice(letters) for _ in range(length))


def get_current_local_dt() -> datetime.datetime:
    return datetime.datetime.now(app.config['TIMEZONE'])


def local_datetime_from_timestamp(timestamp: int) -> datetime.datetime:
    dt = datetime.datetime.fromtimestamp(timestamp, app.config['TIMEZONE'])
    return dt


def generate_random_int() -> int:
    rand = random.SystemRandom()
    return rand.randint(0, (1 << 31))


def dt_to_local_dt(dt: datetime.datetime):
    return dt.replace(tzinfo = app.config['TIMEZONE'])


def d_to_local_dt(d: datetime.date, min_time: bool = True):
    if min_time:
        dt = datetime.datetime.combine(d, datetime.datetime.min.time())
    else:
        dt = datetime.datetime.combine(d, datetime.datetime.max.time())
    return dt_to_local_dt(dt)


def get_minutes_delta(minutes = 0):
    return datetime.timedelta(minutes = minutes)


def get_schools():
    query = School.select()
    return [(entry.id, entry.name) for entry in query]
