import os
import shutil
import logging

from pylons import request, response, tmpl_context as c, url, config
from pylons.controllers.util import redirect

from cms.lib.base import BaseController, render, model
import cms.lib.helpers as h

log = logging.getLogger(__name__)


class PictureController(BaseController):
    def __before__(self):
        BaseController.__before__(self)
        c.bodyclass = 'cms'
        c.page = c.tree.find_node(iname='cmspicture')

    def get(self, id=None, title=None):
        doc = self._pathForImage(id)
        try:
            rec = model.findImage(int(id))
        except:
            pass
        if rec and os.path.exists(doc):
            response.headers['Content-Type'] = rec.filetype
            return open(doc).read()
        else:
            raise Exception("Image not found")

    def index(self):
        return self.list()

    def list(self):
        c.numImages, c.images = model.listImages()
        c.cmsmenuOptions['picture'] = {}
        cmsmenu_opts = c.cmsmenuOptions['picture']
        if not c.numImages:
            cmsmenu_opts[-1] = [{'label': 'Afbeelding toevoegen',
                                 'url': url(controller='picture',
                                            action='edit',
                                            id='new')}]

        for img in c.images:
            opt = []
            opt.append(dict(label='Afbeelding toevoegen',
                            url=url(controller='picture',
                            action='edit',
                            id='new')))
            opt.append(dict(label='Afbeelding bewerken',
                            url=url(controller='picture',
                            action='edit',
                            id=img.id)))
            opt.append(dict(label='Afbeelding verwijderen',
                            url=url(controller='picture',
                            action='delete',
                            id=img.id),
                       separate=True,
                       confirm="confirm('weet je het zeker?');"))
            cmsmenu_opts[img.id] = opt
        return render('/pages/picture/list.html')

    def edit(self, id=None):
        if id == 'new':
            c.image = model.Image()
            c.image.id = 'new'
        else:
            c.image = model.findImage(int(id))
        return render('/pages/picture/edit.html')

    def submit(self, id=None):
        if id == 'new':
            image = model.Image()
        else:
            image = model.find_image(int(id))

        rp = request.POST
        f = rp.get('image')
        if not os.path.exists(config['pictures_dir']):
            os.makedirs(config['pictures_dir'])

        image.filename = f.filename
        image.filetype = f.type
        image.filesize = len(f.value)
        if id == 'new':
            model.save(image)
        model.commit()

        newfile = self._pathForImage(image.id)
        nf = open(newfile, 'wb')
        shutil.copyfileobj(f.file, nf)

        return redirect(url(controller='picture', action='list'))

    def delete(self, id):
        try:
            image = model.findImage(int(id))
            model.delete(image)
            os.unlink(self._pathForImage(id))
            model.commit()
        except Exception, e:
            log.error(str(e))
        return redirect(url(controller='picture', action='list'))

    def _pathForImage(self, id):
        return os.path.join(config['pictures_dir'], '%d.dat' % (int(id),))
