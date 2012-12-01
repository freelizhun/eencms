from sqlalchemy import Column
from sqlalchemy.types import Integer, String

from cms.model.meta import Base


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255))
    filesize = Column(Integer)
    filelocation = Column(String(255))
    filetype = Column(String(255))

    def __repr__(self):
        return "<Image id=%r;filename=%s>" % (self.id, self.filename)
