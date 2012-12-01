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
    local_seed = Column(String(16))
    fullname = Column(String(255))

    def __repr__(self):
        return "<CMSUser id=%d;username=%s>" % (self.id, self.username)

    def passwdMatch(self, passwd):
        return (self.password == security.hashed_passwd(passwd,
                                                        self.local_seed,
                                                        config.get('pwd_seed'))
                )
