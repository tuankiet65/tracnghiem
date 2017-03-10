import random
import string
import datetime


def generate_random_string(length: int = 50) -> string:
    rand = random.SystemRandom()
    letters = string.ascii_letters + string.digits
    return ''.join(rand.choice(letters) for _ in range(50))


def get_current_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

def datetime_from_utc_timestamp(timestamp: int) -> datetime.datetime:
    dt = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
    return dt

def generate_random_int() -> int:
    rand = random.SystemRandom()
    return rand.randint(0, (1 << 31))