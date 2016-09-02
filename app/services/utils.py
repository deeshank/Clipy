import random
import string
import json, ast


def generate_uname():
    # return ''.join(choice(ascii_uppercase) for i in range(8))
    key = ''
    for i in range(8):
        key += random.choice(string.lowercase + string.uppercase + string.digits)
    return key


def cleanup(data):
    return ast.literal_eval(json.dumps(data))
