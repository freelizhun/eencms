import logging

from pylons import tmpl_context as c

from cms.lib.base import BaseController, render
from cms import model

log = logging.getLogger(__name__)


class HomeController(BaseController):
    def index(self):
        return self.home()

    def home(self):
        c.bodyclass = "homepage"
        c.news = model.get_news_for_home()

        return render('/pages/home/index.html')
