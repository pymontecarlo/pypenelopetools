""""""

# Standard library modules.
import abc
import logging
logger = logging.getLogger(__name__)

# Third party modules.

# Local modules.
from pypenelopetools.penelope.iterator import LineIterator

# Globals and constants variables.

class PenelopeInput(metaclass=abc.ABCMeta):

    def read(self, fileobj):
        line_iterator = LineIterator(fileobj)

        for keyword in self.get_keywords():
            keyword.read(line_iterator)

    def write(self, fileobj, index_table):
        lines = []
        for keyword in self.get_keywords():
            lines += keyword.write(index_table)

        fileobj.write('\n'.join(lines))

    @abc.abstractmethod
    def get_keywords(self):
        return []
