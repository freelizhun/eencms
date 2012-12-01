import logging
import crypt

from pylons import request, session, tmpl_context as c, url
from pylons.controllers.util import redirect

from cms.lib.base import BaseController, render, model

log = logging.getLogger(__name__)


class MgmtController(BaseController):
    def index(self):
        if not session.get('cmsuser'):
            return self.login()

        return render('/pages/cms/index.html')

    def login(self, error=None):
        c.error = error
        return render('/pages/cms/login.html')

    def submit(self):
        login = str(request.params.get('username'))
        passwd = str(request.params.get('passwd'))

        try:
            usr = model.findCMSUser(username=login)
            if not usr or crypt.crypt(passwd, usr.password) != usr.password:
                raise Exception('Wrong')
            session['cmsuser'] = usr.id
            session.save()
            log.info('CMS-user %r logged in', usr)
        except Exception, e:
            log.info("Failed login attempt for login %s: %s", login, str(e))
            return self.login('Gebruikersnaam onbekend of wachtwoord fout.')

        return redirect(url(controller='cms', action='index'))

    def logout(self):
        try:
            del session['cmsuser']
        except:
            pass
        finally:
            session.save()

        return redirect(url(controller='home', action='index'))
