import logging
import datetime

from pylons import request, response, tmpl_context as c

from cms.lib.base import BaseController, render, model

log = logging.getLogger(__name__)


class RssController(BaseController):
    def index(self):
        return self.list()

    def list(self):
        return render('/pages/rss/list.html')

    def selectNewsFeed(self):
        return render('/pages/rss/select_news.html')

    def news(self):
        self._setHeader()
        num, c.news = model.listNews(limit=35)
        c.pubdate = None
        for item in c.news:
            if not c.pubdate:
                c.pubdate = item.created
            else:
                c.pubdate = max(item.created, c.pubdate)
        return render('/pages/rss/news.xml')

    def _set_header(self):
        c.pubdate = datetime.datetime.now()
        if 'mozilla' in request.user_agent.lower():
            response.headers['Content-Type'] = 'text/xml;charset=utf-8'
        else:
            response.headers['Content-Type'] =\
                'application/rss+xml;charset=utf-8'
