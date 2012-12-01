import logging

from pylons import request, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from cms.lib.exceptions import NotFoundException
from cms.lib.cms import verify
from cms.lib.base import BaseController, render, Session
import cms.model as model

log = logging.getLogger(__name__)


class PageController(BaseController):
    def index(self):
        return render('/pages/reference/index.html')

    def reference(self):
        return render('/components/reference/reference.html')

    def view(self, id=None, title=None):
        try:
            c.page = c.tree.findNode(id=int(id))
        except NotFoundException:
            abort(404)
        except:
            raise
        if not c.page.type == 'content':
            abort(404)

        return render('/pages/page/view.html')

    def edit(self, id=None):
        verify()
        if id == 'new':
            c.page = model.Page()
            c.page.id = 'new'
        else:
            c.page = c.tree.findNode(int(id))
        return render('/pages/page/edit.html')

    def submit(self, id=None):
        verify()
        rp = request.params
        c.page = c.tree.findNode(id=int(id))
        try:
            content = Session.query(model.Content).get(c.page.content_id)
        except:
            content = model.Content()

        c.page.title = rp.get('title')
        content.content = rp.get('content')
        content.sidebar = rp.get('sidebar')
        c.page.menutitle = rp.get('menutitle')
        if not content.id:
            Session.add(content)
        Session.commit()
        c.page.type = 'content'
        c.page.content_id = content.id
        Session.commit()

        return redirect(url(controller='page',
                            action='view',
                            id=c.page.id,
                            title=c.page.getUrlTitle()))

    def addbelow(self, id=None):
        verify()
        sibling = c.tree.findNode(int(id))
        newid = c.tree.addChild(sibling.parent_id, sibling.id)
        return redirect(url(controller='page', action='edit', id=newid))

    def moveup(self, id=None):
        verify()
        c.tree.moveNode(int(id), 'up')
        node = c.tree.findNode(int(id))
        return redirect(node.getUrl())

    def movedown(self, id=None):
        verify()
        c.tree.moveNode(int(id), 'down')
        node = c.tree.findNode(int(id))
        return redirect(node.getUrl())

    def delete(self, id=None):
        verify()
        node = c.tree.findNode(int(id))
        parent_id = node.parent_id
        try:
            if node.type == 'content':
                content = Session.query(model.Content).get(node.content_id)
                Session.delete(content)
        except:
            pass
        c.tree.delChild(node.id)

        childnodes = c.tree.getNodes(parent_id)
        if len(childnodes) < 1:
            return redirect(url(controller='home', action='index'))
        else:
            firstsub = childnodes[0]
            return redirect(firstsub.getUrl())
