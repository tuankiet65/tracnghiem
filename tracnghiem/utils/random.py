import random
import string


def generate_random_string(length: int = 50) -> string:
    rand = random.SystemRandom()
    letters = string.ascii_letters + string.digits
    return ''.join(rand.choice(letters) for _ in range(length))


def generate_random_int() -> int:
    rand = random.SystemRandom()
    return rand.randint(0, (1 << 31))
