from sqlalchemy import Column
from sqlalchemy.types import Integer, String

from pylons import config

from cms.lib import security
from cms.model.meta import Base


class CMSUser(Base):
    __tablename__ = "cmsuser"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), index=True)
    password = Column(String(64))
    fullname = Column(String(255))

    def __repr__(self):
        return "<CMSUser id={0};username={1}>".format(self.id, self.username)

    def passwdMatch(self, passwd):
        return security.check_password(passwd, self.password)
