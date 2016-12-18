""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.input import PenelopeInput
import pypenelopetools.penelope.keywords as penelope_keywords

# Globals and constants variables.

class PenmainInput(PenelopeInput):

    def __init__(self):
        self.TITLE = penelope_keywords.TITLE()
        self.SKPAR = penelope_keywords.SKPAR()
        self.SENERG = penelope_keywords.SENERG()
        self.SPECTR = penelope_keywords.SPECTR()
        self.SGPOL = penelope_keywords.SGPOL()

    def get_keywords(self):
        return [self.TITLE,
                penelope_keywords.DOT_SEPARATOR,
                penelope_keywords.SOURCE_DEFINITION_SEPARATOR,
                self.SKPAR, self.SENERG, self.SPECTR, self.SGPOL]
