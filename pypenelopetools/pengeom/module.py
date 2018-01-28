"""
Definition of module.
"""

# Standard library modules.
import os
import enum

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.transformation import Rotation, Shift
from pypenelopetools.pengeom.mixin import DescriptionMixin, ModuleMixin
from pypenelopetools.pengeom.base import GeometryBase, LINE_EXTRA, LINE_SEPARATOR
from pypenelopetools.material import VACUUM

# Globals and constants variables.

class SidePointer(enum.IntEnum):
    """
    Whether the surface is pointing in the positive or negative direction.
    """

    POSITIVE = 1
    """Positive direction."""

    NEGATIVE = -1
    """Negative direction."""

class Module(DescriptionMixin, ModuleMixin, GeometryBase):
    """
    Definition of a module.
    
    Args:
        material (:obj:`Material <pypenelopetools.material.Material>`, optional):
            Material associated with this module.
            If ``None``, the material is set to 
            :obj:`VACUUM <pypenelopetools.material.VACUUM>`.
        description (str): Description of the module
    """

    def __init__(self, material=None, description=''):
        if material is None:
            material = VACUUM
        self.material = material

        self.description = description

        self._surfaces = {}
        self._modules = set()

        self._rotation = Rotation()
        self._shift = Shift()

    def __repr__(self):
        return '<Module(description={0}, material={1}, surfaces_count={2:d}, modules_count={3:d}, rotation={4}, shift={5})>' \
            .format(self.description, self.material, len(self._surfaces),
                    len(self._modules), str(self.rotation), str(self.shift))

    def _read(self, fileobj, material_lookup, surface_lookup, module_lookup):
        line = self._read_next_line(fileobj)
        _, _, self.description = self._parse_line(line)

        line = self._read_next_line(fileobj)
        keyword, material_index, _ = self._parse_line(line)
        if keyword != 'MATERIAL':
            raise IOError('Expected keyword "MATERIAL" instead of "{0}"'.format(keyword))

        material_index = int(material_index)
        if material_index not in material_lookup:
            raise IOError('No material {0} in lookup table'.format(material_index))
        self.material = material_lookup[material_index]

        line = self._read_next_line(fileobj)
        while line != LINE_EXTRA and line != LINE_SEPARATOR:
            keyword, index, termination = self._parse_line(line)
            index = int(index)

            if keyword == 'SURFACE':
                pointer = int(termination[16:18])
                surface = surface_lookup[index]
                self.add_surface(surface, pointer)

            elif keyword == 'MODULE':
                submodule = module_lookup[index]
                self.add_module(submodule)

            else:
                raise IOError('Unknown keyword: {0}'.format(keyword))

            line = self._read_next_line(fileobj)

        if line == LINE_EXTRA:
            extra_offset = fileobj.tell()
            self.rotation._read(fileobj, material_lookup, surface_lookup, module_lookup)

            fileobj.seek(extra_offset)
            self.shift._read(fileobj, material_lookup, surface_lookup, module_lookup)

    def _write(self, fileobj, index_lookup):
        index = index_lookup[self]
        text = "{:4d}".format(index)
        termination = " " + self.description
        line = self._create_line('MODULE', text, termination)
        fileobj.write(line + os.linesep)

        # Material index
        index = index_lookup[self.material]
        text = "{:4d}".format(index)
        line = self._create_line('MATERIAL', text)
        fileobj.write(line + os.linesep)

        # Surface pointers
        surfaces = sorted((index_lookup[surface], surface, pointer)
                          for surface, pointer in self._surfaces.items())

        for index, surface, pointer in surfaces:
            text = "{:4d}".format(index)
            termination = ", SIDE POINTER=({:2d})".format(pointer)
            line = self._create_line('SURFACE', text, termination)
            fileobj.write(line + os.linesep)

        # Module indexes
        modules = sorted((index_lookup[module], module)
                          for module in self.get_modules())

        for index, module in modules:
            text = "{:4d}".format(index)
            line = self._create_line('MODULE', text)
            fileobj.write(line + os.linesep)

        # Separator
        fileobj.write(LINE_EXTRA + os.linesep)

        # Rotation
        self.rotation._write(fileobj, index_lookup)

        # Shift
        self.shift._write(fileobj, index_lookup)

        fileobj.write(LINE_SEPARATOR + os.linesep)

    def add_surface(self, surface, pointer):
        """
        Adds a surface.
        
        Args:
            surface (:obj:`SurfaceImplicit <pypenelopetools.pengeom.surface.SurfaceImplicit>` or :obj:`SurfaceReduced <pypenelopetools.pengeom.surface.SurfaceReduced>`):
                Surface to add.
            pointer (:obj:`SidePointer`): 
                Whether the surface is pointing in the positive or negative 
                direction.
        """
        if isinstance(pointer, int):
            if pointer == SidePointer.NEGATIVE:
                pointer = SidePointer.NEGATIVE
            elif pointer == SidePointer.POSITIVE:
                pointer = SidePointer.POSITIVE
        if pointer not in SidePointer:
            raise ValueError("Pointer ({0}) must be either -1 or 1.".format(pointer))
        if surface in self._surfaces:
            raise ValueError("Module already contains this surface.")
        self._surfaces[surface] = pointer

    def pop_surface(self, surface):
        """
        Removes a surface.
        
        Args:
            surface (:obj:`SurfaceImplicit <pypenelopetools.pengeom.surface.SurfaceImplicit>` or :obj:`SurfaceReduced <pypenelopetools.pengeom.surface.SurfaceReduced>`):
                Surface to remove.
        """
        self._surfaces.pop(surface)

    def clear_surfaces(self):
        """
        Clear all surfaces.
        """
        self._surfaces.clear()

    def get_surface_pointer(self, surface):
        """
        Returns the surface pointer for the specified surface.
        
        Args:
            surface (:obj:`SurfaceImplicit <pypenelopetools.pengeom.surface.SurfaceImplicit>` or :obj:`SurfaceReduced <pypenelopetools.pengeom.surface.SurfaceReduced>`):
                Surface of interest.
        
        Returns:
            :obj:`SidePointer`: Side pointer.
        """
        return self._surfaces[surface]

    def get_surfaces(self):
        """
        Returns:
            tuple: All surfaces.
        """
        return tuple(self._surfaces.keys())

    @property
    def rotation(self):
        """:obj:`Rotation <pypenelopetools.pengeom.transformation.Rotation>`: Rotation of the module."""
        return self._rotation

    @property
    def shift(self):
        """:obj:`Shift <pypenelopetools.pengeom.transformation.Shift>`: Shift/translation of the module."""
        return self._shift
