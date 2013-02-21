def method(fn, method):
    if not 'required_methods' in fn.__dict__:
        fn.required_methods = {}
    fn.required_methods[method] = True
    return fn


def userlevel(fn, level):
    if not 'userlevels' in fn.__dict__:
        fn.userlevels = {}
    fn.userlevels[level] = True
    return fn


def post(fn):
    return method(fn, 'post')


def get(fn):
    return method(fn, 'get')


def access_cmsuser(fn):
    return userlevel(fn, 'cmsuser')


def access_all(fn):
    return userlevel(fn, 'all')
