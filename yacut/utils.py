import random
import string


def get_unique_short_id():
    required_length = 6
    possible_symbols = string.ascii_letters + string.digits
    id = random.choices(possible_symbols, k=required_length)
    return ''.join(id)
