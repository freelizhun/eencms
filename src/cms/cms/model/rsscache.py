from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Text, DateTime

from cms.model.meta import Base


class RSSCache(Base):
    __tablename__ = "rsscache"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, index=True)
    channel = Column(DateTime, index=True)
    title = Column(String(200))
    link = Column(String(255))
    description = Column(Text)
    guid = Column(Integer)

    def __repr__(self):
        return "<RSSCache('{0}')>".format(self.id)
