from __future__ import division
import datetime
import logging
import os

from paste.deploy import appconfig
from paste.script.command import Command

from cms.config.environment import load_environment
from cms import model

log = logging.getLogger(__name__)


class LoadStructure(Command):
    max_args = 1
    min_args = 1

    usage = 'CONFIGFILE'
    group_name = 'cms'
    summary = 'Loads the database with a basic website structure'
    parser = Command.standard_parser()

    def command(self):
        print "TODO: Actually load basic website structure into the database"
