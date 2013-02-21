import logging
import crypt

from pylons import request, session, tmpl_context as c, url
from pylons.controllers.util import redirect

from cms.lib.base import BaseController, render, model
from cms.lib import security
from cms.lib.decorators import get, post, access_cmsuser, access_all

log = logging.getLogger(__name__)


class MgmtController(BaseController):
    @get
    @access_all
    def index(self):
        if not session.get('cmsuser'):
            return self.login()

        return render('/pages/cms/index.html')

    @get
    @access_all
    def login(self, error=None):
        c.error = error
        c.info = None
        if 'cmsloggedout' in session:
            c.info = 'Je bent uitgelogt!'
            del session['cmsloggedout']
            session.save()
        return render('/pages/cms/login.html')

    @post
    @access_all
    def submit(self):
        login = str(request.params.get('username'))
        passwd = str(request.params.get('passwd'))

        try:
            usr = model.find_cmsuser(username=login)
            if not usr or not security.check_password(passwd, usr.password):
                raise Exception('')
            session['cmsuser'] = usr.id
            session.save()
            log.info('CMS-user %r logged in', usr)
        except Exception, e:
            log.info("Failed login attempt for login %s: %s", login, str(e))
            return self.login('Gebruikersnaam onbekend of wachtwoord fout.')

        return redirect(url(controller='mgmt', action='index'))

    @get
    @access_cmsuser
    def logout(self):
        try:
            del session['cmsuser']
        except:
            pass
        finally:
            session['cmsloggedout'] = True
            session.save()


        return redirect(url(controller='mgmt', action='login'))
