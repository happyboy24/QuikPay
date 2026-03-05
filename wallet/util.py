import random
import string


def generate_account_number():
    return "44" +str(random.randrange(00000000, 99999999))

def generate_reference_number():
    # upper_case = [string.ascii_uppercase]
    # lower_case = [string.ascii_lowercase]
    return "Ref_Number" + str(random.shuffle([string.ascii_letters + string.digits][: 31]))