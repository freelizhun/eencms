import re
import logging
import datetime

from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean, Text, DateTime

from cms.model.meta import Base

log = logging.getLogger(__name__)


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    active = Column(Boolean, index=True)
    created = Column(DateTime, index=True)
    title = Column(String(200))
    teaser = Column(Text)
    content = Column(Text)
    lastchange = Column(DateTime)

    def getURLTitle(self):
        return re.sub('[^\w\d-]+', '_', self.title)

    def __repr__(self):
        return "<News('%s')>" % self.id

    def __setattr__(self, name, val):
        Base.__setattr__(self, name, val)
        self.__dict__[name] = val
        if name[:1] != '_':
            if hasattr(self, name):
                log.debug("Changing {0} ({1}) to {2}".format(
                    name,
                    getattr(self, name),
                    val))
            else:
                log.debug("New property %s: %r" % (name, val))
            self.__dict__['lastchange'] = datetime.datetime.now()
