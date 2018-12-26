"""
Definition of base classes.
"""

# Standard library modules.
import abc
import re
import enum

# Third party modules.

# Local modules.

# Globals and constants variables.
LINE_KEYWORDS_SIZE = 6
LINE_SIZE = 80
SKIP_LINE = "       ."

PATTERN_LINE = re.compile(r'([A-Z0-9 ]{6})([\w\.\-\+ ]*)(\[.*\])?')

class InputLineBase(metaclass=abc.ABCMeta):
    """
    Base class to parse and read PENELOPE text files.
    """

    def _parse_line(self, line):
        """
        Extracts the keyword, the values and the comment of an input line.
        The values are returned as a list.
        
        Args:
            line (str): Input line.

        Returns:
            tuple(str, tuple(str), str): Keyword, values, comment.
        """
        if line.startswith(' ' * 6):
            return None, None, line.strip()

        match = re.match(PATTERN_LINE, line)
        if not match:
            return None, None, None

        keyword, values, comment = match.groups()

        keyword = keyword.strip()
        values = tuple(values.split())
        if comment:
            comment = comment[1:-1]

        return keyword, values, comment

    def _create_line(self, name, values, comment=''):
        """
        Creates an input line of this keyword from the specified text.
        The white space between the items is automatically adjusted to fit the
        line size.
        The keyword and the total length of the line is checked not to exceed 
        their respective maximum size.
        
        Args:
            name (str): 6-character keyword.
            values (tuple or list): Values.
            comment (str, optional): Comment associated with the line.
            
        Returns:
            str: Formatted line.
        """
        # Keyword
        name = name.ljust(LINE_KEYWORDS_SIZE)
        assert len(name) == LINE_KEYWORDS_SIZE
        line = '{0} '.format(name.upper())

        # Values
        strvalues = []
        for value in values:
            if isinstance(value, float):
                strvalues.append('{0:g}'.format(value))
            elif isinstance(value, enum.IntEnum):
                strvalues.append(str(value.value))
            else:
                strvalues.append(str(value))

        line += ' '.join(strvalues)

        # Comment
        if len(comment) > 0 and len(line) + len(comment) + 2 <= LINE_SIZE:
            line = line.ljust(LINE_SIZE - (len(comment) + 2))
            line += '[{0}]'.format(comment)

        if len(line) > LINE_SIZE:
            raise ValueError('Line of keyword {0} is too long, {1} > {2} characters'
                             .format(name, len(line), LINE_SIZE))

        return line

    def _peek_next_line(self, fileobj):
        """
        Returns the next line without advancing the current position.
        
        Args:
            fileobj (file object): File object opened with read access.
            
        Returns:
            str: Next line, stripped of all trailing white spaces.
        """
        # Remember the current position
        offset = fileobj.tell()

        # Read line
        line = self._read_next_line(fileobj)

        # Roll back to previous position
        fileobj.seek(offset)

        return line

    def _read_next_line(self, fileobj):
        """
        Returns the next line and advances the current position.
        Comment line (line starting with 7 spaces) are automatically skipped.
        
        Args:
            fileobj (file object): File object opened with read access.
            
        Returns:
            str: Next line, stripped of all trailing white spaces.
        """
        line = fileobj.readline().rstrip()

        # If line starts with 7 spaces, read next
        if line.startswith(' ' * 7):
            return self._read_next_line(fileobj)

        return line

    @abc.abstractmethod
    def read(self, fileobj):
        """
        Reads a PENELOPE-type file.
        
        Args:
            fileobj (file object): File object opened with read access.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, fileobj):
        """
        Writes to a PENELOPE-type file.
        
        Args:
            fileobj (file object): File object opened with write access.
        """
        raise NotImplementedError
