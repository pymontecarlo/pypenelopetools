""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.base import _InLineBase, LINE_KEYWORDS_SIZE

# Globals and constants variables.

class Separator(_InLineBase):

    def __init__(self, text):
        self.text = text

    def read(self, line_iterator):
        pass

    def write(self, index_table):
        return [self._create_line(' ' * LINE_KEYWORDS_SIZE, (self.text,))]

    @property
    def name(self):
        return 'separator'

class EndSeparator(_InLineBase):

    def read(self, line_iterator):
        pass

    def write(self, index_table):
        return [self._create_line('END', (), 'Ends the reading of input data')]