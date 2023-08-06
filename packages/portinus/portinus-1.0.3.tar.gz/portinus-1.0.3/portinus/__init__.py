import logging
import os
from operator import attrgetter

from pathlib import Path
from jinja2 import Template

from .cli import task
from . import restart, monitor
from .environmentfile import EnvironmentFile
from .composesource import ComposeSource
from .service import Service

_script_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(_script_dir, 'templates')
service_dir = '/usr/local/portinus-services'


def list():
    """Print out the list of Portinus services:"""
    _ensure_service_dir()
    print("Available Portinus Services:")
    for i in sorted(Path(service_dir).iterdir()):
        if i.is_dir():
            print(i.name)


def get_instance_dir(name):
    """Return the dir where the given service resides"""
    return os.path.join(service_dir, name)


def get_template(file_name):
    """Return a template by name from the template store as a jinja2.Template object"""
    template_file = os.path.join(template_dir, file_name)
    with open(template_file) as f:
        template_contents = f.read()

    return Template(template_contents)


def _ensure_service_dir():
    """Make sure the Portinus service dir exists"""
    try:
        os.mkdir(service_dir)
    except FileExistsError:
        pass


class Application(object):
    """A collection of all Portinus objects that make up a whole application (e.g. environment file, restart timers, monitoring service, actual service, etc)"""

    log = logging.getLogger()

    def __init__(self, name, source=None, environment_file=None, restart_schedule=None):
        self.name = name
        self.environment_file = EnvironmentFile(name, environment_file)
        self.service = Service(name, source)
        self.restart_timer = restart.Timer(name, restart_schedule=restart_schedule)
        self.monitor_service = monitor.Service(name)

    def exists(self):
        return self.service.exists()

    def ensure(self):
        """Create/update the application"""
        _ensure_service_dir()
        self.environment_file.ensure()
        self.service.ensure()
        self.restart_timer.ensure()
        self.monitor_service.ensure()

    def remove(self):
        """Remove the application"""
        self.service.remove()
        self.environment_file.remove()
        self.restart_timer.remove()
        self.monitor_service.remove()
