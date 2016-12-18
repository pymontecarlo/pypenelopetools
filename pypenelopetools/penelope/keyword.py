"""
Definition of base keyword classes
"""

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

class _KeywordBase(metaclass=abc.ABCMeta):

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

class Separator(_KeywordBase):

    def __init__(self, text):
        self.text = text

    def read(self, line_iterator):
        return False

    def write(self, index_table):
        return [self._create_line(' ' * LINE_KEYWORDS_SIZE, (self.text,))]

class Keyword(_KeywordBase):

    def __init__(self, name, comment="", required=False):
        self._name = name
        self._comment = comment
        self._required = required

    def __str__(self):
        return self.name

    @abc.abstractmethod
    def set(self, *args):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self):
        raise NotImplementedError

    @abc.abstractmethod
    def copy(self):
        raise NotImplementedError

    def read(self, line_iterator):
        line = line_iterator.peek()
        name, values, _comment = self._extract_name_values_comment(line)
        if name != self.name:
            if self.required:
                raise IOError('Expected keyword "{0}", found "{1}"'
                              .format(self.name, name))
            else:
                return False

        self.set(*values)
        next(line_iterator)

        return True

    def write(self, index_table):
        values = self.get()
        if None in values and not self.required:
            return []

        try:
            values = self.validate(*self.get())
        except Exception as e:
            if self.required:
                raise e
            return []

        return [self._create_line(self.name, values, self.comment)]

    @property
    def name(self):
        return self._name

    @property
    def comment(self):
        return self._comment

    @property
    def required(self):
        return self._required

class KeywordGroup(_KeywordBase):

    @abc.abstractmethod
    def get_keywords(self):
        raise NotImplementedError

    def read(self, line_iterator):
        for keyword, line in zip(self.get_keywords(), line_iterator):
            keyword.read(iter([line]))
        return True

    def write(self, index_table):
        lines = []
        for keyword in self.get_keywords():
            lines += keyword.write(index_table)
        return lines

class KeywordSequence(_KeywordBase):

    def __init__(self, keyword):
        self._base_keyword = keyword
        self._keywords = []

    def add(self, *args):
        keyword = self._base_keyword.copy()
        keyword.set(*args)
        self._keywords.append(keyword)

    def pop(self, index):
        self._keywords.pop(index)

    def clear(self):
        self._keywords.clear()

    def get(self):
        return tuple(keyword.get() for keyword in self._keywords)

    def read(self, line_iterator):
        line = line_iterator.peek()
        name, values, _comment = self._extract_name_values_comment(line)
        while name == self._base_keyword.name:
            self.add(*values)
            next(line_iterator)
            line = line_iterator.peek()
            name, values, _comment = self._extract_name_values_comment(line)

        return True

    def write(self, index_table):
        lines = []
        for keyword in self._keywords:
            lines += keyword.write(index_table)
        return lines

class TypeKeyword(Keyword):

    def __init__(self, name, types, comment="", required=False):
        super().__init__(name, comment, required)
        self._types = types
        self._values = tuple([None] * len(types))

    def set(self, *args):
        if len(args) != len(self._types):
            raise ValueError("Keyword requires {0} values, {1} given"
                             .format(len(self._types), len(args)))

        values = []
        for type_, value in zip(self._types, args):
            values.append(type_(value))

        values = self.validate(*values)

        self._values = tuple(values)

    def get(self):
        return self._values

    def validate(self, *args):
        return args

    def copy(self):
        return self.__class__(self.name, self._types, self.comment)
