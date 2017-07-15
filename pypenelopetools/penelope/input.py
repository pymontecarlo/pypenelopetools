""""""

# Standard library modules.
import os
import abc
import logging
logger = logging.getLogger(__name__)

# Third party modules.

# Local modules.
from pypenelopetools.penelope.iterator import LineIterator
from pypenelopetools.penelope.mixin import FilenameMixin

# Globals and constants variables.

class PenelopeInput(FilenameMixin, metaclass=abc.ABCMeta):

    def __init__(self, filename):
        self.filename = filename

    def read(self, fileobj):
        line_iterator = LineIterator(fileobj)

        for keyword in self.get_keywords():
            keyword.read(line_iterator)

    def write(self, fileobj, index_table):
        lines = []
        for keyword in self.get_keywords():
            lines += keyword.write(index_table)

        fileobj.write(os.linesep.join(lines))

    @abc.abstractmethod
    def get_keywords(self):
        return []
