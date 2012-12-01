import logging

from pylons import session, tmpl_context as c, url, config
from pylons.controllers.util import redirect

from cms.lib.base import BaseController, render

log = logging.getLogger(__name__)


class TreeController(BaseController):

    def index(self):
        if not session.get('cmsuser') and \
                config.get('debug', 'false') == 'false':
            redirect(url(controller='mgmt', action='login'))

        return render('/pages/tree/index.html')

    def test(self):
        cmsnode = c.tree.findNode(iname='cms')
        log.debug(cmsnode)
        for child in c.tree.get_nodes(cmsnode.id):
            log.debug(child)
        return 'See terminal'
