"""
Definition of base input classes.
"""

# Standard library modules.
import abc

# Third party modules.

# Local modules.
from pypenelopetools.penelope.base import InputLineBase

# Globals and constants variables.

class PenelopeInputBase(InputLineBase):
    """
    Base input class.
    """

    def read(self, fileobj):
        """
        Reads an input file (i.e. ``.in``).
        
        Args:
            fileobj (file object): File object opened with read access.
        """
        for keyword in self.get_keywords():
            keyword.read(fileobj)

    def write(self, fileobj):
        """
        Writes to an input file (i.e. ``.in``).
        
        Args:
            fileobj (file object): File object opened with write access.
        """
        for keyword in self.get_keywords():
            keyword.write(fileobj)

    @abc.abstractmethod
    def get_keywords(self):
        """
        Returns:
            list: Sorted list of all keywords in the input.
        """
        return []
