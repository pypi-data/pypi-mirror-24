from operator import attrgetter
import logging
import os
import shutil

import portinus

log = logging.getLogger(__name__)

class ComposeSource(object):
    """The source docker-compose file to build a service from"""

    def __init__(self, name, source=None):
        self.name = name
        self.source = source
        self.path = portinus.get_instance_dir(name)
        self.service_script = os.path.join(self.path, name)
        log.debug("Initialized ComposeSource for '{name}' from source: '{source}'".format(name=name, source=source))

    source = property(attrgetter('_source'))

    @source.setter
    def source(self, value):
        """The source docker-compose yaml file"""
        if value is not None:
            try:
                with open(os.path.join(value, "docker-compose.yml")):
                    pass
            except FileNotFoundError as e:
                log.error("Unable to access the specified source docker compose file in ({source})".format(source=value))
                raise(e)
        self._source = value

    def _ensure_service_script(self):
        """Create/update the script used to manage this portinus service and its environment"""
        service_script_template = os.path.join(portinus.template_dir, "service-script")
        shutil.copy(service_script_template, self.service_script)
        os.chmod(self.service_script, 0o755)

    def ensure(self):
        """Create/update the service dir with the compose file and all dependent files"""
        if not self.source:
            log.error("No valid source specified")
            raise(IOError("No valid source specified"))
        log.info("Copying source files for '{self.name}' to '{self.path}'")
        self.remove()
        shutil.copytree(self.source, self.path, symlinks=True, copy_function=shutil.copy)
        self._ensure_service_script()
        log.debug("Successfully copied source files")

    def remove(self):
        """Remove the installed service directory"""
        log.info("Removing source files for '{name}' from '{path}'".format(name=self.name, path=self.path))
        try:
            shutil.rmtree(self.path)
            log.debug("Successfully removed source files")
        except FileNotFoundError:
            log.debug("No source files found")
