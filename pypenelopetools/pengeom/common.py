"""
Common classes to PENGEOM
"""

# Standard library modules.
import abc
import math

# Third party modules.

# Local modules.

# Globals and constants variables.
LINE_SIZE = 64
LINE_KEYWORDS_SIZE = 8

LINE_START = 'X' * LINE_SIZE
LINE_SEPARATOR = '0' * LINE_SIZE
LINE_EXTRA = '1' * LINE_SIZE
LINE_END = 'END      0000000000000000000000000000000000000000000000000000000'

class Keyword(object):

    def __init__(self, name, termination=""):
        self._name = name
        self._termination = termination

    @property
    def name(self):
        return self._name

    @property
    def termination(self):
        return self._termination

    def _toexponent(self, number):
        """
        Formats exponent to PENELOPE format (E22.15)

        :arg number: number to format
        :type number: :class:`float`

        :rtype: :class:`str`
        """
        if number == 0.0:
            exponent = 0.0
        else:
            exponent = math.log10(abs(number))

        if exponent >= 0 :
            exponentStr = '+%2i' % abs(exponent)
        else:
            exponentStr = '-%2i' % abs(exponent)

        exponentStr = exponentStr.replace(' ', '0') #Replace white space in the exponent

        coefficient = float(abs(number)) / 10 ** int(exponent)

        if number >= 0:
            numberStr = '+%17.15fE%s' % (coefficient, exponentStr)
        else:
            numberStr = '-%17.15fE%s' % (coefficient, exponentStr)

        # The number should not be longer than 22 characters
        assert len(numberStr) == 22

        return numberStr

    def create_expline(self, value):
        """
        Creates a exponent line.
        This type of line is characterised by a keyword, a value express as an
        exponent (see :meth:`._toexponent`) and a termination string.
        The keyword and the total length of the line is checked not to exceed
        their respective maximum size.

        :arg keyword: 8-character keyword
        :arg value: value of the keyword
        :type value: :class:`float`
        :arg termination: termination of the line
        """
        keyword = self.name.rjust(LINE_KEYWORDS_SIZE)

        assert len(keyword) == LINE_KEYWORDS_SIZE

        line = '%s(%s,%4i)%s' % (keyword, self._toexponent(value), 0, self.termination)

        assert len(line) <= LINE_SIZE

        return line

    def create_line(self, text, override_comment=None):
        """
        Creates an input line from the specified keyword, text and comment.
        The white space between the items is automatically adjusted to fit the
        line size.
        The keyword and the total length of the line is checked not to exceed
        their respective maximum size.

        :arg keyword: 8-character keyword
        :arg text: value of the keyword
        :arg comment: comment associated with the line
        """
        keyword = self.name.ljust(LINE_KEYWORDS_SIZE)

        assert len(keyword) == LINE_KEYWORDS_SIZE

        if override_comment is None:
            line = '%s(%s)%s' % (keyword, text, self.termination)
        else:
            line = '%s(%s)%s' % (keyword, text, override_comment)

        assert len(line) <= LINE_SIZE

        return line

class PengeomComponent(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def to_geo(self, index_lookup): #pragma: no cover
        raise NotImplementedError

class DescriptionMixin(object):

    @property
    def description(self):
        """
        Description of the surface.
        """
        return self._description

    @description.setter
    def description(self, desc):
        self._description = desc

class ModuleMixin(object):

    def add_module(self, module):
        if module == self:
            raise ValueError("Cannot add this module to this module.")
        self._modules.add(module)

    def pop_module(self, module):
        self._modules.discard(module)

    def clear_modules(self):
        self._modules.clear()

    def get_modules(self):
        return list(self._modules)
