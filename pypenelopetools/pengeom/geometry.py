"""
Geometry definition for PENGEOM.
"""

# Standard library modules.
import os
from itertools import chain
from operator import methodcaller, attrgetter

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.mixin import ModuleMixin
from pypenelopetools.pengeom.module import Module
from pypenelopetools.pengeom.surface import SurfaceImplicit, SurfaceReduced
from pypenelopetools.pengeom.base import GeometryBase, LINE_SIZE, LINE_START, LINE_SEPARATOR, LINE_END
from pypenelopetools.material import VACUUM

# Globals and constants variables.

def _topological_sort(d, k):
    """
    Togological sort.
    http://stackoverflow.com/questions/108586/topological-sort-recursive-using-generators
    """
    for ii in d.get(k, []):
        yield from _topological_sort(d, ii)
    yield k

class Geometry(ModuleMixin, GeometryBase):
    """
    Creates a new PENELOPE geometry.
    
    Args:
        title (str, optional): 
            Title of the geometry.
        tilt_deg (float, optional): 
            Specimen tilt in degrees along the x-axis.
        rotation_deg (float, optional): 
            Specimen rotation in degrees along the z-axis
    """

    def __init__(self, title="Untitled", tilt_deg=0.0, rotation_deg=0.0):
        self.title = title
        self.tilt_deg = tilt_deg
        self.rotation_deg = rotation_deg
        self._modules = set()

    def _read(self, fileobj, material_lookup, surface_lookup, module_lookup):
        line = self._read_next_line(fileobj)
        if line != LINE_START:
            raise IOError('Expected start line')

        line = self._read_next_line(fileobj)
        self.title = ''
        while line != LINE_SEPARATOR:
            line = line.lstrip('C').strip()
            self.title += line
            line = self._read_next_line(fileobj)

        line = self._peek_next_line(fileobj)
        while line != LINE_END:
            # Parse section name
            section_name, index, _ = self._parse_line(line)
            index = int(index)

            # Parse surface or module
            if section_name == 'SURFACE':
                # Read 2 lines down the INDICES line
                offset = fileobj.tell()
                self._read_next_line(fileobj)
                indices_line = self._read_next_line(fileobj)
                _, indices, _ = self._parse_line(indices_line)
                indices = map(int, indices.split(','))
                fileobj.seek(offset)

                if sum(indices) == 0:
                    surface = SurfaceImplicit()
                else:
                    surface = SurfaceReduced()

                surface._read(fileobj, material_lookup, surface_lookup, module_lookup)
                surface_lookup[index] = surface

            elif section_name == 'MODULE':
                module = Module()
                module._read(fileobj, material_lookup, surface_lookup, module_lookup)
                self.add_module(module)
                module_lookup[index] = module

            else:
                raise IOError('Cannot read {} section'.format(section_name))

            # Next line
            line = self._peek_next_line(fileobj).rstrip()

    def read(self, fileobj, material_lookup):
        """
        Reads a geometry file (``.geo``).
        
        Args:
            fileobj (file object): 
                File object opened with read access.
            material_lookup (dict(int, :class:`Material <pypenelopetools.material.Material>`)): 
                A lookup table for the materials used in the geometry. 
                Dictionary where the keys are material indexes in the geometry 
                file and the values, 
                :class:`Material <pypenelopetools.material.Material>` instances.
        """
        surface_lookup = {}
        module_lookup = {}
        material_lookup.setdefault(0, VACUUM)

        self._read(fileobj, material_lookup, surface_lookup, module_lookup)

    def _write(self, fileobj, index_lookup):
        fileobj.write(LINE_START + os.linesep)
        fileobj.write('       ' + self.title + os.linesep)
        fileobj.write(LINE_SEPARATOR + os.linesep)

        # Surfaces
        surfaces = sorted((index_lookup[surface], surface)
                          for surface in self.get_surfaces())

        for _index, surface in surfaces:
            surface._write(fileobj, index_lookup)

        # Modules
        modules = sorted((index_lookup[module], module)
                          for module in self.get_modules())

        for _index, module in modules:
            module._write(fileobj, index_lookup)

        # Extra module for tilt and rotation
        if self.tilt_deg != 0.0 or self.rotation_deg != 0.0:
            extra = self._create_extra_module()

            index_lookup[extra] = len(self.get_modules()) + 1
            extra._write(fileobj, index_lookup)

        # End of line
        fileobj.write(LINE_END + os.linesep)

    def write(self, fileobj, index_lookup=None):
        """
        Writes the geometry file (``.geo``) to create this geometry.
        
        Args:
            fileobj (file object): 
                File object opened with write access.
            index_lookup (dict(:obj:`GeometryBase <pypenelopetools.pengeom.base.GeometryBase>`, int), optional): 
                A lookup table for the surfaces, modules and materials of this 
                geometry. 
                If ``None``, the index lookup is generated by the method 
                :meth:`indexify <pypenelopetools.pengeom.geometry.Geometry.indexify>`.
            
        Returns:
            dict(:obj:`GeometryBase <pypenelopetools.pengeom.base.GeometryBase>`, int): lookup table
        """
        if not index_lookup:
            index_lookup = self.indexify()
        self._write(fileobj, index_lookup)
        return index_lookup

    def get_materials(self):
        """
        Returns all materials in this geometry.
        """
        materials = set(map(attrgetter('material'), self.get_modules()))
        materials.discard(VACUUM)
        return materials

    def get_surfaces(self):
        """
        Returns all surfaces in this geometry.
        """
        return set(chain(*map(methodcaller('get_surfaces'), self.get_modules())))

    def indexify(self):
        """
        Returns a lookup table which associates the surfaces, modules and 
        materials of this geometry to their index used in the geometry file. 
        The lookup table is a dictionary where the keys are surfaces, modules 
        and materials instances, and the values, an integer index.
        """
        index_lookup = {}

        # Materials
        index_lookup[VACUUM] = 0
        for i, material in enumerate(self.get_materials(), 1):
            index_lookup[material] = i

        # Surfaces
        for i, surface in enumerate(self.get_surfaces(), 1):
            index_lookup[surface] = i

        # Modules
        modules_dep = {} # module dependencies
        for module in self.get_modules():
            modules_dep.setdefault(module, [])
            for submodule in module.get_modules():
                modules_dep[module].append(submodule)

        modules_order = []
        for module in modules_dep:
            for dep_module in _topological_sort(modules_dep, module):
                if dep_module not in modules_order:
                    modules_order.append(dep_module)

        for i, module in enumerate(modules_order, 1):
            index_lookup[module] = i

        return index_lookup

    def _create_extra_module(self):
        extra = Module(VACUUM, description='Extra module for rotation and tilt')

        ## Find all unlinked modules
        all_modules = set(self.get_modules())
        linked_modules = set(chain(*map(methodcaller('get_modules'), all_modules)))
        unlinked_modules = all_modules - linked_modules
        for module in unlinked_modules:
            extra.add_module(module)

        ## Change of Euler angles convention from ZXZ to ZYZ
        extra.rotation.omega_deg = (self.rotation_deg - 90.0) % 360.0
        extra.rotation.theta_deg = self.tilt_deg
        extra.rotation.phi_deg = 90.0

        return extra

    @property
    def title(self):
        """
        Title of the geometry.
        The title must have less than 61 characters.
        """
        return self._title

    @title.setter
    def title(self, title):
        if len(title) > LINE_SIZE - 3:
            raise ValueError("The length of the title ({0:d}) must be less than {1:d}."
                             .format(len(title), LINE_SIZE - 3))
        self._title = title

    @property
    def tilt_deg(self):
        """
        Specimen tilt in degrees along the x-axis
        """
        return self._tilt_deg

    @tilt_deg.setter
    def tilt_deg(self, angle_deg):
        while angle_deg < 0:
            angle_deg += 360.0
        self._tilt_deg = angle_deg

    @property
    def rotation_deg(self):
        """
        Specimen rotation in degrees along the z-axis
        """
        return self._rotation_deg

    @rotation_deg.setter
    def rotation_deg(self, angle_deg):
        self._rotation_deg = angle_deg
