from operator import attrgetter
import logging
import datetime
import cPickle

from pylons import url

import cms.model as model
from exceptions import NodeException, NotFoundException

log = logging.getLogger(__name__)


class Tree:
    def __init__(self, session):
        self.session = session
        self.nodes = {}
        self.rootNodes = {}
        self.child_nodes = {}
        self.inames = {}

    def load(self):
        all_nodes = self.session.query(model.Page)
        all_nodes.order_by(model.Page.parent_id)
        all_nodes.order_by(model.Page.order_id)
        for node in all_nodes:
            self.nodes[node.id] = node
            if node.iname and node.iname not in self.inames:
                self.inames[node.iname] = node
            if node.parent_id != 0:
                if not node.parent_id in self.child_nodes:
                    self.child_nodes[node.parent_id] = []
                self.child_nodes[node.parent_id].append(node)
            else:
                self.rootNodes[node.id] = node
        log.debug("Loaded %d nodes", len(self.nodes))

    def get_nodes(self, parent_id=None):
        if not parent_id is None and parent_id == 0:
            nodes = self.rootNodes.values()
        elif not parent_id is None:
            if parent_id in self.child_nodes:
                nodes = self.child_nodes.get(parent_id)
            else:
                nodes = []
        else:
            nodes = self.nodes.values()

        return sorted(nodes, key=attrgetter('order_id'))

    def find_node(self, id=None, iname=None):
        if not id and not iname:
            raise Exception("findNode requires id or iname to locate nodes.")

        retval = None

        if id:
            retval = self.nodes.get(id)
        elif iname:
            if iname in self.inames:
                return self.inames[iname]

        if not retval:
            raise NotFoundException("Node not found")

        return retval

    def find_matching_shortcut(self, controller, action):
        retval = None
        for page in self.nodes.values():
            if not page.extradata:
                continue
            dat = cPickle.loads(str(page.extradata))
            tgt = dat.get('target')
            if not tgt:
                continue

            if tgt['controller'] == controller and tgt['action'] == action:
                retval = page
                break

        if not retval:
            raise NotFoundException("Somehow, I couldn't find the page")

        return retval

    def get_parent(self, node):
        if not node.parent_id:
            raise NodeException("node %s has no parent" % (repr(node),))

        return self.nodes[node.parent_id]

    def get_children(self, node):
        return self.get_nodes(node.id)

    def get_path(self, node):
        path = [node]
        curnode = node
        while curnode.parent_id > 0:
            curnode = self.findNode(id=curnode.parent_id)
            path.insert(0, curnode)
        return path

    def add_child(self, parent, after=None):
        nodeset = self.get_nodes(parent)

        newnode = model.Page()
        newnode.title = "Nieuwe Pagina"
        newnode.menutitle = "Nieuwe Pagina"
        newnode.type = 'content'
        newnode.parent_id = parent
        newnode.created = datetime.datetime.now()

        if not after:
            order = max(x.order_id for x in nodeset) if len(nodeset) else 1
            newnode.order_id = order
            nodeset.append(newnode)
        else:
            curorder = 1
            for node in nodeset:
                node.order_id = curorder
                curorder += 1
                if node.id == after:
                    newnode.order_id = curorder
                    curorder += 1

        self.session.save(newnode)
        self.save()

        return newnode.id

    def move_node(self, node, direction):
        parent_id = self.findNode(node).parent_id
        nodeset = self.get_nodes(parent_id)

        prev, childn, next = None, None, None
        for child in nodeset:
            if child.id == node:
                childindex = nodeset.index(child)
                if childindex > 0:
                    prev = nodeset[childindex - 1]
                if childindex < len(nodeset) - 1:
                    next = nodeset[childindex + 1]
                childn = child

        if direction == 'up':
            if prev is not None:
                prev.order_id, childn.order_id = childn.order_id, prev.order_id
        else:
            if next is not None:
                next.order_id, childn.order_id = childn.order_id, next.order_id

        self.save()
        return parent_id

    def del_child(self, childid):
        children = self.get_nodes(childid)
        for child in children:
            self.delChild(child.id)

        child = self.findNode(id=childid)
        parentset = self.get_nodes(child.parent_id)
        curorder = 1
        for node in parentset:
            if node.id == child.id:
                continue

            node.order_id = curorder
            curorder += 1

        self.session.delete(child)
        self.save()
        return True

    def save(self):
        self.session.commit()

    def get_menu_options(self):
        options = {}
        for node in self.get_nodes():
            opt = []
            if not node.immutable:
                opt.append(dict(label='Pagina bewerken',
                                url=url(controller='page',
                                action='edit',
                                id=node.id)))
            opt.append(dict(label='Pagina toevoegen (onder)',
                            url=url(controller='page',
                                    action='addbelow',
                                    id=node.id),
                            separate=True))
            opt.append(dict(label='Pagina omhoog',
                            url=url(controller='page',
                                    action='moveup',
                                    id=node.id),
                            valid='valid_display(1)'))
            opt.append(dict(label='Pagina omlaag',
                            url=url(controller='page',
                                    action='movedown',
                                    id=node.id),
                            valid='valid_display(1)'))
            if not node.immutable:
                opt.append(dict(label='Pagina verwijderen',
                                url=url(controller='page',
                                        action='delete',
                                        id=node.id),
                                separate=True,
                                confirm="confirm('weet je het zeker?');"))
            options[node.id] = opt
        return options
