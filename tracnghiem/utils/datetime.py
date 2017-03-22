import datetime

from .. import app


def get_current_local_dt() -> datetime.datetime:
    return datetime.datetime.now(app.config['TIMEZONE'])


def local_dt_from_timestamp(timestamp: int) -> datetime.datetime:
    dt = datetime.datetime.fromtimestamp(timestamp, app.config['TIMEZONE'])
    return dt


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
