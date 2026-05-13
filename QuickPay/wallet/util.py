
import random
import string


def generate_wallet_number():
    return "44" + str(random.randrange(00000000, 99999999))


def generate_reference():
    # characters = string.ascii_letters + string.digits
    # return ''.join(random.choices(characters, k=12))
    return ''.join(random.choices(string.ascii_lowercase, k=5) + random.choices(string.digits, k=9))


