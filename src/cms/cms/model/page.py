import re
import datetime
import cPickle

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Boolean, Text, DateTime
from sqlalchemy.orm import relation, backref

from pylons import url

from cms.model.meta import Base


class Page(Base):
    __tablename__ = "page"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, index=True)
    order_id = Column(Integer, index=True)
    created = Column(DateTime)
    lastchange = Column(DateTime)
    title = Column(String(200))
    menutitle = Column(String(50))
    type = Column(String(24))
    content_id = Column(Integer, ForeignKey("content.id"))
    iname = Column(String(64))
    immutable = Column(Boolean)
    extradata = Column(Text)

    content = relation('Content', backref=backref('page'))

    def __repr__(self):
        return "<Page id=%d;menutitle=%s>" % (self.id, self.menutitle)

    def get_url(self):
        """This method returns a valid URL for the node.
        It's preferred to use this method, since it knows best where to point,
        for instance, if there are shortcuts or similar thingamadoods.
        """
        if self.type == 'content':
            return url(controller='page', action='view', id=self.id,
                       title=self.getUrlTitle())
        elif self.type == 'shortcut':
            target = cPickle.loads(str(self.extradata))['target']
            return url(**target)
        elif self.type == 'cms':
            return url(controller=self.iname[3:], action='list')

        return '/'

    def getExtra(self, field, default=None):
        if not self.extradata:
            return default
        dat = cPickle.loads(self.extradata)
        return dat.get(field, default)

    def getUrlTitle(self):
        return re.sub('([^\w\d]+)', '_', self.menutitle).strip('_')

    def eq(self, node):
        if node.id == self.id:
            return True
        return False

    def getContent(self):
        if self.content:
            return self.content.content
        else:
            return ''

    def getSidebarContent(self):
        if self.content:
            return self.content.sidebar
        else:
            return ''

    def __setattr__(self, name, val):
        Base.__setattr__(self, name, val)
        self.__dict__[name] = val
        if name[:1] != '_':
            self.__dict__['lastchange'] = datetime.datetime.now()
