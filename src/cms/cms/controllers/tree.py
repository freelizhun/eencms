import logging

from pylons import session, tmpl_context as c, url, config
from pylons.controllers.util import redirect

from cms.lib.base import BaseController, render
from cms.lib.decorators import get, access_cmsuser

log = logging.getLogger(__name__)


class TreeController(BaseController):
    @get
    @access_cmsuser
    def index(self):
        if not session.get('cmsuser') and \
                config.get('debug', 'false') == 'false':
            redirect(url(controller='mgmt', action='login'))

        return render('/pages/tree/index.html')

    @get
    @access_cmsuser
    def test(self):
        cmsnode = c.tree.find_node(iname='cms')
        log.debug(cmsnode)
        for child in c.tree.get_nodes(cmsnode.id):
            log.debug(child)
        return 'See terminal'
