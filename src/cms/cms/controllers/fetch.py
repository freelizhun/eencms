import os
import logging

from pylons import response, config
from pylons.controllers.util import abort

from cms.lib.base import BaseController, model

log = logging.getLogger(__name__)


class FetchController(BaseController):
    lightWeight = True

    def image(self, id, name):
        image = model.find_image(id)
        path = self._get_image_path(image.id)
        if not os.path.exists(path):
            abort(404)
        response.headers['Content-Type'] = image.filetype
        return open(path, 'rb').read()

    def thumbnail(self, id, name):
        image = model.findImage(id)
        path = self._get_image_path(image.id)
        if not os.path.exists(path):
            abort(404)
        response.headers['Content-Type'] = image.filetype
        return open(path, 'rb').read()

    def _get_image_path(self, id):
        return os.path.join(config['pictures_dir'], '{0}.dat'.format(int(id)))
