from __future__ import division
import datetime
import logging
import mimetypes
import os
import Image

from pylons import config

log = logging.getLogger(__name__)


def findFile(dir, id):
    start = datetime.datetime.now()
    retval = None
    path = os.path.join(config[dir], str(id))
    for tp in getFileTypes():
        np = '%s%s' % (path, tp)
        if os.path.exists(np):
            retval = np
            break
    diff = datetime.datetime.now() - start
    if retval:
        log.debug("Finding file (%s/%s) took %.6fs seconds",
                  dir,
                  os.path.split(retval)[1],
                  (diff.seconds + (diff.microseconds / 1000000.0)))
    else:
        log.debug("Not finding file (%s/%s.*) took %.6fs seconds",
                  dir,
                  id,
                  (diff.seconds + (diff.microseconds / 1000000.0)))
    return retval


def getFileTypes():
    return ['.png', '.gif', '.jpg', '.jpeg']

    # Enable this for support for _all_ imagetypes. But since we don't really
    # need to (internet, remember), don't. It will slow things down by a factor
    # of 5 to 10.
    return [x for x, mt in mimetypes.types_map.items() if mt[:5] == 'image']


def getDimensions(path):
    i = Image.open(path)
    x, y = i.size
    return (x, y)


def resizeDimensions(x, y, maxx, maxy):
    newx, newy = x, y
    if x > maxx or y > maxy:
        newx = maxx
        newy = (maxx / x) * y
        if newy > maxy:
            newy = maxy
            newx = (maxy / y) * x
    return int(newx), int(newy)


def get_path_for_id(id):
    return os.path.join(config['pictures_dir'], '%d.dat' % (int(id),))
