"""
Definition of base result classes.
"""

# Standard library modules.
import abc
import re

# Third party modules.

# Local modules.

# Globals and constants variables.

PATTERN_NUMBER = re.compile(r'\d\.\d*E[\+\-]\d\d')

class PenelopeResultBase(metaclass=abc.ABCMeta):
    """
    Base class representing a type of result.
    """

    def _read_until_line_startswith(self, fileobj, prefix):
        """
        Reads until a line that starts with *prefix* is found.
        White spaces are ignored at the beginning of each line.
        
        Args:
            fileobj (file object): File object opened with read access.
            prefix (str): Prefix of the line to find.
            
        Returns:
            str: Found line, stripped of all leading and trailing white spaces.
        """
        line = fileobj.readline()
        if not line:
            raise EOFError('Read until EOF, no line with prefix {0}'.format(prefix))

        line = line.strip()
        if line.startswith(prefix):
            return line

        return self._read_until_line_startswith(fileobj, prefix)

    def _read_until_end_of_comments(self, fileobj):
        """
        Read until the end of the comments. 
        The next line returns by the file-object will be a non-comment line.
        
        Args:
            fileobj (file object): File object opened with read access.
        """
        offset = fileobj.tell()
        line = fileobj.readline()
        if not line:
            raise EOFError('Read until EOF')

        line = line.strip()
        if line.startswith('#'):
            return self._read_until_end_of_comments(fileobj)

        fileobj.seek(offset)

    def _read_all_values(self, line):
        """
        Parses all numbers from *line*.
        
        Returns:
            list(float): List of numbers.
        """
        return [float(v) for v in PATTERN_NUMBER.findall(line)]

    @abc.abstractmethod
    def read(self, fileobj):
        """
        Reads a result file.
        
        Args:
            fileobj (file object): File object opened with read access.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def read_directory(self, dirpath):
        """
        Read a result file from a directory.
        
        Args:
            dirpath (str): Path of a directory.
        """
        raise NotImplementedError
