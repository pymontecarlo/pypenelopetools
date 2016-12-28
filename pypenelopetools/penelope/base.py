""""""

# Standard library modules.
import abc

# Third party modules.
from pyparsing import (Word, OneOrMore, Optional, Suppress, alphanums,
                       ParseException)

# Local modules.

# Globals and constants variables.
LINE_KEYWORDS_SIZE = 6
LINE_SIZE = 80
SKIP_LINE = "       ."

class _InLineBase(metaclass=abc.ABCMeta):

    def _extract_name_values_comment(self, line):
        """
        Extracts the keyword, the values and the comment of an input line.
        The values are returned as a list.
        
        :arg line: input line
        
        :return: keyword, values, comment
        """
        if line.startswith(' ' * 6):
            return None, None, line.strip()

        keywordletters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        keyword = Word(keywordletters, max=6)('keyword')

        value = Word(alphanums + ".-+")
        values = OneOrMore(value)('vals')

        commentletters = alphanums + ",.()-="
        comment = OneOrMore(Word(commentletters))('comment')
        comment.setParseAction(lambda tokens: " ".join(tokens))

        expr = keyword + values + Optional(Suppress("[") + comment + Suppress("]"))

        try:
            result = expr.parseString(line)
        except ParseException:
            return None, None, None

        return result.keyword, result.vals.asList(), result.comment

    def _create_line(self, name, values, comment=''):
        """
        Creates an input line of this keyword from the specified text.
        The white space between the items is automatically adjusted to fit the
        line size.
        The keyword and the total length of the line is checked not to exceed 
        their respective maximum size.
        
        :arg keyword: 6-character keyword
        :arg text: value of the keyword
        :arg comment: comment associated with the line
        """
        name = name.ljust(LINE_KEYWORDS_SIZE)
        assert len(name) == LINE_KEYWORDS_SIZE

        text = ' '.join(map(str, values))
        line = "{0} {1}".format(name.upper(), text)
        if len(comment) > 0:
            line = line.ljust(LINE_SIZE - (len(comment) + 2))
            line += '[%s]' % comment

        assert len(line) <= LINE_SIZE

        return line

    @abc.abstractmethod
    def read(self, line_iterator):
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, index_table):
        raise NotImplementedError