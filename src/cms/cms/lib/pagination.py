from operator import attrgetter
import logging
import math

from pylons import config, request

log = logging.getLogger(__name__)


class Page:
    PREV = 2
    NEXT = 1
    NORMAL = 0
    SEPARATOR = 3

    def __init__(self, label, active=False, tp=None):
        self.label = label
        self.type = self.NORMAL
        if tp:
            self.type = tp
        self.active = active


def getNumPages(numItems):
    return int(math.ceil(float(numItems) / float(config['items_per_page'])))


def getCurrentPage():
    return int(request.params.get('page', 1))


def getPageList(numitems):
    maxpages = getNumPages(numitems)
    curpage = int(request.params.get('page', 1))

    pages = []

    # First 3
    for i in range(1, 4):
        if i > maxpages:
            continue
        active = (i == curpage)
        pages.append(Page(i, active))

    # Last 3
    for i in range(maxpages - 2, maxpages + 1):
        if i < 1:
            continue
        active = (i == curpage)
        pages.append(Page(i, active))

    # Surrounding 2 for current
    for i in range(curpage - 2, curpage + 3):
        if i < 1 or i > maxpages:
            continue
        active = (i == curpage)
        pages.append(Page(i, active))

    pages = sorted(list(pages), key=attrgetter('label'))
    _pages = []
    done = []
    for page in pages:
        if page.label not in done:
            _pages.append(page)
            done.append(page.label)
    pages = _pages

    inserts = []
    for idx, p in enumerate(pages):
        if idx < 2:
            continue
        if int(pages[idx - 1].label) != int(p.label) - 1:
            inserts.append(idx)

    inserts.reverse()

    for i in inserts:
        pages.insert(i, Page('...', Page.SEPARATOR))

    if curpage > 1:
        pages.insert(0, Page('&lt; vorig', tp=Page.PREV))
    if curpage < maxpages:
        pages.append(Page('volgend &gt;', tp=Page.NEXT))

    return pages


def require_pagination(numitems):
    log.debug("Determining pagination requirement: %d, %d",
              numitems,
              int(config['items_per_page']))
    return (numitems > int(config['items_per_page']))
