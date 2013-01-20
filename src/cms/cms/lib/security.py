import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt(12))


def check_password(password, stored_password):
    return bcrypt.hashpw(password, stored_password) == stored_password
