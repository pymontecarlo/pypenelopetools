"""
Definition of module
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.transformation import Rotation, Shift
from pypenelopetools.pengeom.common import \
    Keyword, PengeomComponent, DescriptionMixin, ModuleMixin

# Globals and constants variables.
from pypenelopetools.pengeom.common import LINE_EXTRA

SIDEPOINTER_POSITIVE = 1
SIDEPOINTER_NEGATIVE = -1

class Module(DescriptionMixin, ModuleMixin, PengeomComponent):

    _KEYWORD_MODULE = Keyword("MODULE")
    _KEYWORD_MATERIAL = Keyword('MATERIAL')
    _KEYWORD_SURFACE = Keyword("SURFACE")
    _KEYWORD_SIDEPOINTER = ', SIDE POINTER='
    _KEYWORD_MODULE = Keyword('MODULE')

    def __init__(self, material, description=''):
        self.material = material
        self.description = description

        self._surfaces = {}
        self._modules = set()

        self._rotation = Rotation()
        self._shift = Shift()

    def __repr__(self):
        return '<Module(description=%s, material=%s, surfaces_count=%i, modules_count=%i, rotation=%s, shift=%s)>' % \
            (self.description, self.material, len(self._surfaces),
             len(self._modules), str(self.rotation), str(self.shift))

    def add_surface(self, surface, pointer):
        if pointer not in [SIDEPOINTER_NEGATIVE, SIDEPOINTER_POSITIVE]:
            raise ValueError("Pointer (%s) must be either -1 or 1." % pointer)
        if surface in self._surfaces:
            raise ValueError("Module already contains this surface.")
        self._surfaces[surface] = pointer

    def pop_surface(self, surface):
        self._surfaces.pop(surface)

    def clear_surfaces(self):
        self._surfaces.clear()

    def get_surface_pointer(self, surface):
        """
        Returns the surface pointer for the specified surface.
        """
        return self._surfaces[surface]

    def get_surfaces(self):
        return self._surfaces.keys()

    def to_geo(self, index_lookup):
        """
        Returns the lines of this class to create a GEO file.
        """
        lines = []

        index = index_lookup[self]
        text = "%4i" % (index + 1,)
        comment = " %s" % self.description
        line = self._KEYWORD_MODULE.create_line(text, comment)
        lines.append(line)

        # Material index
        index = index_lookup[self.material]
        text = "%4i" % index
        line = self._KEYWORD_MATERIAL.create_line(text)
        lines.append(line)

        # Surface pointers
        surfaces = sorted((index_lookup[surface], surface, pointer)
                          for surface, pointer in self._surfaces.items())

        for index, surface, pointer in surfaces:
            text = "%4i" % (index + 1,)
            comment = "%s(%2i)" % (self._KEYWORD_SIDEPOINTER, pointer)
            line = self._KEYWORD_SURFACE.create_line(text, comment)
            lines.append(line)

        # Module indexes
        modules = sorted((index_lookup[module], module)
                          for module in self.get_modules())

        for index, module in modules:
            text = "%4i" % (index + 1,)
            line = self._KEYWORD_MODULE.create_line(text)
            lines.append(line)

        # Separator
        lines.append(LINE_EXTRA)

        # Rotation
        lines.extend(self.rotation.to_geo(index_lookup))

        # Shift
        lines.extend(self.shift.to_geo(index_lookup))

        return lines

    @property
    def rotation(self):
        """
        Rotation of the surface.
        The rotation is defined by a :class:`.Rotation`.
        """
        return self._rotation

    @property
    def shift(self):
        """
        Shift/translation of the surface.
        The shift is defined by a :class:`.Shift`.
        """
        return self._shift
