""""""

# Standard library modules.
import abc
import logging
logger = logging.getLogger(__name__)

# Third party modules.

# Local modules.

# Globals and constants variables.

class _PenelopeInputBase(metaclass=abc.ABCMeta):

    def read(self, fileobj):
        for keyword in self.get_keywords():
            keyword.read(fileobj)

    def write(self, fileobj):
        for keyword in self.get_keywords():
            keyword.write(fileobj)

    @abc.abstractmethod
    def get_keywords(self):
        return []
