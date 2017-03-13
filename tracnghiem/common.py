import random
import string
import datetime
from . import app


def generate_random_string(length: int = 50) -> string:
    rand = random.SystemRandom()
    letters = string.ascii_letters + string.digits
    return ''.join(rand.choice(letters) for _ in range(50))


def get_current_time() -> datetime.datetime:
    return datetime.datetime.now(app.config['TIMEZONE'])


def local_datetime_from_timestamp(timestamp: int) -> datetime.datetime:
    dt = datetime.datetime.fromtimestamp(timestamp, app.config['TIMEZONE'])
    return dt


def generate_random_int() -> int:
    rand = random.SystemRandom()
    return rand.randint(0, (1 << 31))


def to_local_timezone(dt):
    if type(dt) is datetime.date:
        dt = datetime.datetime(dt.year, dt.month, dt.day)
    return dt.replace(tzinfo = app.config['TIMEZONE'])
