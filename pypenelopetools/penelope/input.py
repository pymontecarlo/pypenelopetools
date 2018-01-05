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
        """
        Reads an input file (i.e. ``.in``).
        
        Args:
            fileobj (file object): file object opened with read access.
        """
        for keyword in self.get_keywords():
            keyword.read(fileobj)

    def write(self, fileobj):
        """
        Writes to an input file (i.e. ``.in``)
        
        Args:
            fileobj (file object): file object opened with write access.
        """
        for keyword in self.get_keywords():
            keyword.write(fileobj)

    @abc.abstractmethod
    def get_keywords(self):
        """
        Returns a sorted list of all keywords in the input.
        """
        return []
