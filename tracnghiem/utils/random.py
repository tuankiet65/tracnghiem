import secrets
import string


def generate_random_string(length: int = 50) -> string:
    rand = secrets.SystemRandom()
    letters = string.ascii_letters + string.digits
    return ''.join(rand.choice(letters) for _ in range(length))


def generate_random_int() -> int:
    rand = secrets.SystemRandom()
    return rand.randint(0, (2 ** 31))
