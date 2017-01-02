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
        if not self.name:
            return
        next(line_iterator)

    def write(self, index_table):
        return [self._create_line(self.name, (self.text,))]

class EndSeparator(Separator):

    def __init__(self):
        super().__init__('Ends the reading of input data', 'END')

