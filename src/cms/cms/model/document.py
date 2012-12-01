from sqlalchemy import Column
from sqlalchemy.types import Integer, String

from cms.model.meta import Base


class Document(Base):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255))
    filesize = Column(Integer)
    filelocation = Column(String(255))
    filetype = Column(String(255))

    def __repr__(self):
        return "<Document id=%r;title=%s)>" % (self.id, self.filename)
