"""
Definition of base keyword classes
"""

# Standard library modules.
import abc
import os

# Third party modules.

# Local modules.
from pypenelopetools.penelope.base import _InputLineBase

# Globals and constants variables.

#--- Abstract classes

class _KeywordBase(_InputLineBase):

    def __str__(self):
        return self.name

    @abc.abstractmethod
    def get(self):
        raise NotImplementedError

    @abc.abstractmethod
    def copy(self):
        raise NotImplementedError

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError

#--- Core classes

class TypeKeyword(_KeywordBase):

    def __init__(self, name, types, comment=""):
        self._name = name
        self._types = tuple(types)
        self._values = tuple([None] * len(types))
        self._comment = comment

    def set(self, *args):
        if len(args) < len(self._types): # Less than to account for additional, not parsed values
            raise ValueError("Keyword {0} requires {1} values, {2} given"
                             .format(self.name, len(self._types), len(args)))

        values = []
        for type_, value in zip(self._types, args):
            if value is not None:
                try:
                    value = type_(value)
                except ValueError:
                    raise TypeError("Value {0} must be of type {1}"
                                    .format(value, type_))
            values.append(value)

        self._values = tuple(values)

    def get(self):
        return self._values

    def copy(self):
        return self.__class__(self.name, self._types, self.comment)

    def read(self, fileobj):
        line = self._peek_next_line(fileobj)
        name, values, _comment = self._parse_line(line)

        # If it is not the expected line, do nothing
        if name != self.name:
            return

        # Set values
        self.set(*values)

        # Jump to next line
        self._read_next_line(fileobj)

    def write(self, fileobj):
        values = list(self.get())

        # Skip if no values are defined
        if None in values:
            return

        # Write to file
        line = self._create_line(self.name, values, self.comment)
        fileobj.write(line + os.linesep)

    @property
    def name(self):
        return self._name

    @property
    def comment(self):
        return self._comment

class KeywordGroup(_KeywordBase):

    @abc.abstractmethod
    def get_keywords(self):
        raise NotImplementedError

    def get(self):
        values = []

        for keyword in self.get_keywords():
            values.extend(keyword.get())

        return tuple(values)

    def copy(self):
        return self.__class__()

    def read(self, fileobj):
        for keyword in self.get_keywords():
            keyword.read(fileobj)

    def write(self, fileobj):
        for keyword in self.get_keywords():
            keyword.write(fileobj)

    def _set_keyword_sequence(self, keyword, values):
        keyword.clear()
        if values is None:
            return

        if not isinstance(values, (list, tuple)):
            values = [values]

        for args in values:
            keyword.add(*args)

    @property
    def name(self):
        return self.get_keywords()[0].name

class KeywordSequence(_KeywordBase):

    def __init__(self, keyword):
        self._base_keyword = keyword
        self._keywords = []

    def _create_keyword(self):
        return self._base_keyword.copy()

    def _add_keyword(self, keyword):
        self._keywords.append(keyword)

    def add(self, *args):
        keyword = self._create_keyword()
        keyword.set(*args)
        self._add_keyword(keyword)
        return keyword

    def pop(self, index):
        self._keywords.pop(index)

    def clear(self):
        self._keywords.clear()

    def get(self):
        values = []
        for keyword in self._keywords:
            values.append(keyword.get())
        return (tuple(values),)

    def copy(self):
        return self.__class__(self._base_keyword.copy())

    def read(self, fileobj):
        line = self._peek_next_line(fileobj)
        name, _values, _comment = self._parse_line(line)

        while name == self._base_keyword.name:
            # Read keyword
            keyword = self._create_keyword()
            keyword.read(fileobj)
            self._add_keyword(keyword)

            # Try to read line
            line = self._peek_next_line(fileobj)
            name, _values, _comment = self._parse_line(line)

    def write(self, fileobj):
        for keyword in self._keywords:
            keyword.write(fileobj)

    @property
    def name(self):
        return self._base_keyword.name

