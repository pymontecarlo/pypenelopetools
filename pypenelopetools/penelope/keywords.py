""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.keyword import TypeKeyword, KeywordSequence, Separator

# Globals and constants variables.

DOT_SEPARATOR = Separator('.')
SOURCE_DEFINITION_SEPARATOR = Separator('>>>>>>>> Source definition.')

class TITLE(TypeKeyword):

    def __init__(self):
        super().__init__('TITLE', (str,), required=True)
        self.set('Untitled')

    def _extract_name_values_comment(self, line):
        name, values, comment = super()._extract_name_values_comment(line)
        return name, (' '.join(values),), comment

    def set(self, title):
        super().set(title)

    def validate(self, title):
        if len(title) > 65:
            raise ValueError('Title is too long. Maximum 65 characters')
        return super().validate(title)

class SKPAR(TypeKeyword):

    def __init__(self):
        super().__init__('SKPAR', (int,),
                         comment="Primary particles: 1=electron, 2=photon, 3=positron")
        self.set(1)

    def set(self, kparp):
        super().set(kparp)

    def validate(self, kparp):
        if kparp not in [0, 1, 2, 3]:
            raise ValueError('Invalid particle')
        return super().validate(kparp)

class SENERG(TypeKeyword):

    def __init__(self):
        super().__init__('SENERG', (float,),
                         comment="Initial energy (monoenergetic sources only)")
        self.set(1e6)

    def set(self, se0):
        super().set(se0)

    def validate(self, se0):
        if se0 <= 0.0:
            raise ValueError('SE0 must be greater than 0')
        return super().validate(se0)

class SPECTR(KeywordSequence):

    def __init__(self):
        keyword = TypeKeyword('SPECTR', (float, float),
                              comment='E bin: lower-end and total probability')
        super().__init__(keyword)

class SGPOL(TypeKeyword):

    def __init__(self):
        super().__init__('SGPOL', (float, float, float),
                         comment="Stokes parameters for polarized photons")

    def set(self, sp1, sp2, sp3):
        super().set(sp1, sp2, sp3)

