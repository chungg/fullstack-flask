import random
import string


ALPHABET = string.ascii_letters + string.digits


def gen_id(size=8):
    return ''.join(random.choices(ALPHABET, k=size))
