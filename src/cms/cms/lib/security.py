import bcrypt
import hashlib
import random


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt(12))


def check_password(password, stored_password):
    return bcrypt.hashpw(password, stored_password) == stored_password


def allowed_action(action, method, user):
    return all([allowed_user(action, user),
                allowed_method(action, method)])


def allowed_user(action, user):
    userlevels = getattr(action, 'userlevels', {})
    if userlevels.get('all', False):
        return True
    if userlevels.get('cmsuser', False) and user:
        return True
    print 'no matching userlevel found'
    return False


def allowed_method(action, method):
    if method.lower() in getattr(action, 'required_methods', {}):
        return True
    return False


def generate_token():
    return hashlib.sha256(str(random.getrandbits(64))).hexdigest()


def check_token(request, session):
    if request.method == 'POST' and \
       ('token' not in request.POST or
        request.POST.get('token') != session.get('token')):
        raise Exception('Token invalid or missing')
    return True
