""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.base import _InLineBase

# Globals and constants variables.

class Separator(_InLineBase):

    def __init__(self, text, name=''):
        self.text = text
        self.name = name

    def read(self, line_iterator):
        pass

    def write(self, index_table):
        return [self._create_line(self.name, (self.text,))]

class EndSeparator(_InLineBase):

    def read(self, line_iterator):
        pass

    def write(self, index_table):
        return [self._create_line('END', (), 'Ends the reading of input data')]