"""
Definition of base separator classes.
"""

# Standard library modules.
import os

# Third party modules.

# Local modules.
from pypenelopetools.penelope.base import InputLineBase

# Globals and constants variables.

class Separator(InputLineBase):
    """
    Base of all PENELOPE separators.
    
    Args:
        text (str): Comment of the separator
        name (str, optional): name of separator keyword (e.g. END)
        
    Attributes:
        text (str): Comment of the separator
        name (str, optional): name of separator keyword (e.g. END)
    """

    def __init__(self, text, name=''):
        self.text = text
        self.name = name

    def __str__(self):
        if self.name:
            return '{0} {1}'.format(self.name, self.text)
        else:
            return self.text

    def read(self, fileobj):
        if not self.name:
            return

        line = self._peek_next_line(fileobj)
        name = line[:6].strip()

        if name != self.name:
            return

        self._read_next_line(fileobj)

    def write(self, fileobj):
        line = self._create_line(self.name, (self.text,))
        fileobj.write(line + os.linesep)

