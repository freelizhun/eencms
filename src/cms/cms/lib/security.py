import bcrypt
import hashlib
import random


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt(12))


def check_password(password, stored_password):
    return bcrypt.hashpw(password, stored_password) == stored_password


def generate_token():
    return hashlib.sha256(str(random.getrandbits(64))).hexdigest()


def check_token(request, session):
    if request.method == 'POST' and \
       ('token' not in request.POST or
        request.POST.get('token') != session.get('token')):
        raise Exception('Token invalid or missing')
    return True
