import logging

from pylons import session, config

from cms.model.meta import Session, Base  # noqa
from cms.model import meta  # noqa
from cms.model.cmsuser import CMSUser
from cms.model.document import Document
from cms.model.image import Image
from cms.model.news import News
from cms.model.content import Content  # noqa
from cms.model.page import Page  # noqa
from cms.model.rsscache import RSSCache  # noqa

log = logging.getLogger(__name__)


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)


def reattach(obj):
    Session.add(obj)


def commit():
    """
    This method is a replacement for the meta.Session.commit() method. This
    commits both sessions and removes the need to act with Session's or
    metadata in logic.
    """
    Session.commit()


def delete(obj):
    Session.delete(obj)


def save(obj):
    Session.add(obj)


def _getOffset(page):
    return (int(page) - 1) * int(config['items_per_page'])


def listCMSUsers():
    q = Session.query(CMSUser).order_by(CMSUser.fullname)
    return q.count(), q


def listDocuments():
    q = Session.query(Document).order_by(Document.filename)
    return q.count(), q


def listImages():
    q = Session.query(Image).order_by(Image.filename)
    return q.count(), q


def list_news(**kargs):
    q = Session.query(News)
    if not session.get('cmsuser'):
        q = q.filter(News.active == True)  # noqa
    q = q.order_by(News.created.desc())
    num = q.count()
    if 'limit' not in kargs:
        q = q.limit(int(config['items_per_page']))
    else:
        if kargs.get('limit'):
            q = q.limit(kargs.get('limit'))
    if kargs.get('page'):
        q = q.offset(_getOffset(kargs.get('page')))
    return num, q


def findImage(id):
    return Session.query(Image).get(id)


def findDocument(id):
    return Session.query(Document).get(id)


def findNews(id):
    return Session.query(News).get(id)


def find_cms_user(id=None, username=None):
    if id:
        return Session.query(CMSUser).get(id)
    elif username:
        return Session.query(CMSUser).filter(CMSUser.username == username)\
            .one()
    else:
        raise Exception("No id or username supplied. Go away.")


def get_news_for_home():
    q = meta.Session.query(News)
    q = q.filter(News.active == True)  # NOQA
    q = q.order_by(News.created.desc())
    return q
