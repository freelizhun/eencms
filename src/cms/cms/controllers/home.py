import logging

from pylons import tmpl_context as c

from cms.lib.base import BaseController, render
from cms.lib.decorators import get, access_all
from cms import model

log = logging.getLogger(__name__)


class HomeController(BaseController):
    @get
    @access_all
    def index(self):
        return self.home()

    @get
    @access_all
    def home(self):
        c.bodyclass = "homepage"
        c.news = model.get_news_for_home()

        return render('/pages/home/index.html')
