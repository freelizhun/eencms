"""The base Controller API

Provides the BaseController class for subclassing.
"""
import logging

from pylons import session, tmpl_context as c
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render  # noqa

from cms.model.meta import Session
from cms import model
from cms.lib.tree import Tree

log = logging.getLogger(__name__)


class BaseController(WSGIController):
    lightweight = False

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

    def __before__(self):
        if self.lightweight:
            return

        c.bodyclass = None
        c.cmsuser = None

        if not session.get('cmsuser'):
            session['cmsuser'] = None
        else:
            c.cmsuser = model.find_cmsuser(session['cmsuser'])

        c.tree = Tree(Session)
        c.tree.load()
        c.menubase = c.tree.find_node(iname='pages')
        c.cmsmenuOptions = dict()
        c.cmsmenuOptions['page'] = c.tree.get_menu_options()
