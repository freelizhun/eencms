import logging
import crypt

from pylons import request, session, tmpl_context as c, url, config
from pylons.controllers.util import redirect

from cms.lib.base import BaseController, render, model
from cms.lib import security

log = logging.getLogger(__name__)


class CmsuserController(BaseController):
    def __before__(self):
        BaseController.__before__(self)
        c.page = c.tree.find_node(iname='cmscmsuser')

    def index(self):
        return self.list()

    def list(self):
        c.numCmsusers, c.cmsusers = model.listCMSUsers()
        c.cmsmenuOptions['cmsuser'] = {}
        for cmsuser in c.cmsusers:
            opt = []
            opt.append(dict(label='Gebruiker toevoegen',
                            url=url(controller='cmsuser',
                                    action='edit',
                                    id='new')))
            opt.append(dict(label='Gebruiker bewerken',
                            url=url(controller='cmsuser',
                                    action='edit',
                                    id=cmsuser.id)))
            if cmsuser.id != c.cmsuser.id:
                opt.append(dict(label='Gebruiker verwijderen',
                                url=url(controller='cmsuser',
                                        action='delete',
                                        id=cmsuser.id),
                                separate=True,
                                confirm="confirm('weet je het zeker?');"))
            c.cmsmenuOptions['cmsuser'][cmsuser.id] = opt
        return render('/pages/cmsuser/list.html')

    def edit(self, id=None):
        if id == 'new':
            c.usr = model.CMSUser()
            c.usr.id = 'new'
        else:
            c.usr = model.find_cmsuser(int(id))
        c.errors = session.get('errors', [])
        if c.errors:
            rp = session.get('post', {})
            for key, val in rp.items():
                setattr(c.usr, key, val)
            del session['post']
            del session['errors']
            session.save()
        return render('/pages/cmsuser/edit.html')

    def submit(self, id=None):
        if id == 'new':
            usr = model.CMSUser()
        else:
            usr = model.find_cmsuser(int(id))

        errors = []
        rp = request.POST
        usr.fullname = rp.get('fullname')
        usr.username = rp.get('username')
        if rp.get('password1') and rp.get('password1') == rp.get('password2'):
            usr.password = security.hash_password(rp.get('password1'))

        if id == 'new' and not usr.password:
            errors.append({
                'field': 'password1',
                'message': "een wachtwoord is verplicht bij nieuwe gebruikers"}
            )
        if not usr.username:
            errors.append({'field': 'username',
                           'message': "dit veld moet worden ingevuld"})

        if errors:
            session['post'] = rp
            session['errors'] = errors
            session.save()
            redirect(url.current(action='edit'))

        if id == 'new':
            model.save(usr)
        model.commit()

        return redirect(url(controller='cmsuser', action='list'))

    def delete(self, id=None):
        if c.cmsuser.id != id:
            usr = model.findCMSUser(int(id))
            model.delete(usr)
            model.commit()
        return redirect(url(controller='cmsuser', action='list'))
