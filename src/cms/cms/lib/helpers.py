import logging
import random
import crypt
import locale
import os

from textile import textile
from pylons import config
from webhelpers.html import escape, HTML, literal, url_escape, tags  # noqa

from cms.lib import pagination  # noqa
from . import image

log = logging.getLogger(__name__)


def generate_password(readable=True, length=8):
    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou"
    characters = "!@#$%^&*()"
    sets = (consonants, vowels, characters)
    passwd = []
    for i in range(0, length):
        if readable:
            use_str = consonants if i % 2 else vowels
        else:
            use_str = random.choice(sets)
        passwd.append(random.choice(use_str))
    return ''.join(passwd)


def encodePassword(passwd):
    seed = config['passwd_seed']
    return crypt.crypt(passwd, seed)


def dutchTime(format, dt):
    oldlocale = locale.getlocale(locale.LC_TIME)
    try:
        locale.setlocale(locale.LC_TIME, config['use_locale'])
    except:
        pass
    retval = dt.strftime(format)
    locale.setlocale(locale.LC_TIME, oldlocale)
    return retval


def dictToCMSOption(option):
    retval = ''
    optionslist = []
    for key, val in option.items():
        if type(val) == bool:
            optionslist.append('%s: %s' % (key, 'true' if val else 'false'))
        else:
            optionslist.append('%s: "%s"' % (key, val))
    retval = '{%s}' % ', '.join(optionslist)
    return literal(retval)


def cut(instr, charlimit):
    words = instr.split()
    ret = ''
    wordsleft = True
    while True:
        try:
            nextword = words.pop(0)
        except:
            wordsleft = False
            break
        new_string = "{0} {1}".format(ret, nextword)
        if len(new_string) > charlimit:
            break
        ret = new_string
    if wordsleft:
        ret += '...'
    return ret


def ucwords(str):
    return ' '.join([x.capitalize() for x in str.split()])


def _create_dir(path):
    try:
        os.mkdir(path)
    except OSError, e:
        if e.errno == 17:       # 17 = "File exists"
            pass


def getThumbDimensions(imobj, config):
    path = os.path.join(config['pictures_dir'], '%d.dat' % (imobj.id))
    dim = image.getDimensions(path)
    newdim = image.resizeDimensions(dim[0], dim[1], 100, 60)
    return newdim


def sizeof_fmt(num):
    num = float(num)
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0


def pubdate(dt):
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT+2')
