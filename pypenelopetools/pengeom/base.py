"""
Definition of base PENGEOM classes.
"""

# Standard library modules.
import abc
import math
import re

# Third party modules.

# Local modules.
LINE_SIZE = 64
LINE_KEYWORDS_SIZE = 8
LINE_EXTRA = '1' * LINE_SIZE
LINE_START = 'X' * LINE_SIZE
LINE_SEPARATOR = '0' * LINE_SIZE
LINE_END = 'END      0000000000000000000000000000000000000000000000000000000'

PATTERN_LINE = re.compile(r'([A-Z= ]{8})\(([0-9\-\+\, ]*)\)(.*)')
PATTERN_EXPLINE = re.compile(r'([A-Z0-9\-= ]{8})\(([0-9\+\-\.Ee ]*)\,([0-9 ]{4})\)(.*)')

# Globals and constants variables.

def _toexponent(number):
    """
    Formats exponent to PENELOPE format (E22.15)

    Args:
        number (Float): Number to format
    
    Returns:
        str: number to PENELOPE format (E22.15)
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

class GeometryBase(metaclass=abc.ABCMeta):
    """
    Base class for geometry objects.
    """

    @abc.abstractmethod
    def _read(self, fileobj, material_lookup, surface_lookup, module_lookup): #@NoSelf
        """
        Reads file object.
        
        Args:
            fileobj (file object): 
                File object opened with read access.
            material_lookup (dict(int, :class:`Material <pypenelopetools.material.Material>`)): 
                A lookup table for the materials used in the geometry. 
                Dictionary where the keys are material indexes in the geometry 
                file and the values, 
                :class:`Material <pypenelopetools.material.Material>` instances.
            surface_lookup (dict(int, :class:`Surface <pypeneloptools.pengeom.surface._SurfaceBase>`)): 
                A lookup table for surfaces used in the geometry. 
                Dictionary where the keys are surface indexes in the geometry 
                file and the values, 
                :class:`Surface <pypenelopetools.pengeom.surface._SurfaceBase>` 
                instances.
            module_lookup (dict(int, :class:`Module <pypenelopetools.pengeom.module.Module>`)): 
                A lookup table for modules used in the geometry. 
                Dictionary where the keys are module indexes in the geometry 
                file and the values, 
                :class:`Module <pypenelopetools.pengeom.module.Module>` instances.
        """
        raise NotImplementedError

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
        
        Args:
            fileobj (file object): File object opened with read access.
            
        Returns:
            str: Next line, stripped of all trailing white spaces.
        """
        return fileobj.readline().rstrip()

    def _parse_line(self, line):
        match = PATTERN_LINE.match(line)
        if not match:
            raise IOError('Cannot parse line: "{0}"'.format(line))

        keyword, text, termination = match.groups()
        keyword = keyword.strip()
        text = text.strip()
        termination = termination.strip()

        return keyword, text, termination

    def _parse_expline(self, line):
        match = PATTERN_EXPLINE.match(line)
        if not match:
            raise IOError('Cannot parse line: "{0}"'.format(line))

        keyword, value, index, termination = match.groups()
        keyword = keyword.strip()
        value = float(value)
        index = int(index)
        termination = termination.strip()

        if index != 0:
            raise RuntimeError('Index different than zero is not supported: ' + line)

        return keyword, value, termination

    @abc.abstractmethod
    def _write(self, fileobj, index_lookup): #pragma: no cover
        """
        Writes to file object.
        
        Args:
            fileobj (file object): 
                File object opened with write access.
            index_lookup (dict(:obj:`GeometryBase <pypenelopetools.pengeom.base.GeometryBase>`, int)): 
                A lookup table for the surfaces, modules and materials of the 
                associated geometry. 
                Each component is assigned an index by the method 
                :meth:`indexify <pypenelopetools.pengeom.geometry.Geometry.indexify>`.
                Dictionary where the keys are surfaces, modules and materials 
                instances, and the values, an integer index.
        """
        raise NotImplementedError

    def _create_line(self, keyword, text, termination=''):
        """
        Creates an input line from the specified keyword, text and comment.
        The white space between the items is automatically adjusted to fit the
        line size.
        The keyword and the total length of the line is checked not to exceed
        their respective maximum size.

        Args:
            keyword (str): 8-character keyword.
            text (str): value of the keyword.
            termination (str, optional): comment associated with the line.
        """
        keyword = keyword.ljust(LINE_KEYWORDS_SIZE)

        assert len(keyword) == LINE_KEYWORDS_SIZE

        line = '{0}({1}){2}'.format(keyword, text, termination)

        assert len(line) <= LINE_SIZE

        return line

    def _create_expline(self, keyword, value, termination=''):
        """
        Creates a exponent line.
        This type of line is characterised by a keyword, a value express as an
        exponent (see :func:`_toexponent`) and a termination string.
        The keyword and the total length of the line is checked not to exceed
        their respective maximum size.
        
        Args:
            keyword (str): 8-character keyword.
            value (float): value of the keyword.
            termination (str, optional): comment associated with the line.
        """
        keyword = keyword.rjust(LINE_KEYWORDS_SIZE)

        assert len(keyword) == LINE_KEYWORDS_SIZE

        line = '{0}({1},{2:4d}){3}'.format(keyword, _toexponent(value),
                                           0, termination)

        assert len(line) <= LINE_SIZE

        return line
