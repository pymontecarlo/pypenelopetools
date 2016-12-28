"""
Common classes to PENGEOM
"""

# Standard library modules.
import abc

# Third party modules.

# Local modules.

# Globals and constants variables.

class GeoBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def to_geo(self, index_lookup): #pragma: no cover
        raise NotImplementedError

