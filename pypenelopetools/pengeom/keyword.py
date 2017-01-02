""""""

# Standard library modules.
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
            exponent = 0
        else:
            exponent = int(math.log10(abs(number)))

        if exponent >= 0 :
            exponent_str = '+{:2d}'.format(abs(exponent))
        else:
            exponent_str = '-{:2d}'.format(abs(exponent))

        exponent_str = exponent_str.replace(' ', '0') #Replace white space in the exponent

        coefficient = float(abs(number)) / 10 ** exponent

        if number >= 0:
            number_str = '+{0:17.15f}E{1}'.format(coefficient, exponent_str)
        else:
            number_str = '-{0:17.15f}E{1}'.format(coefficient, exponent_str)

        # The number should not be longer than 22 characters
        assert len(number_str) == 22

        return number_str

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

        line = '{0}({1},{2:4d}){3}'.format(keyword, self._toexponent(value),
                                           0, self.termination)

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
            override_comment = self.termination

        line = '{0}({1}){2}'.format(keyword, text, override_comment)

        assert len(line) <= LINE_SIZE

        return line
