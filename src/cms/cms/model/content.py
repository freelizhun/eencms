from sqlalchemy import Column
from sqlalchemy.types import Integer, Text

from cms.model.meta import Base


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    sidebar = Column(Text)
