"""
Geometry definition for PENGEOM
"""

# Standard library modules.
import math
from itertools import chain
from operator import methodcaller, attrgetter

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.common import \
    ModuleMixin, LINE_SIZE, LINE_START, LINE_SEPARATOR, LINE_END
from pypenelopetools.pengeom.module import Module
from pypenelopetools.material.material import VACUUM

# Globals and constants variables.

def _topological_sort(d, k):
    """
    Togological sort.
    http://stackoverflow.com/questions/108586/topological-sort-recursive-using-generators
    """
    for ii in d.get(k, []):
        yield from _topological_sort(d, ii)
    yield k

class Geometry(ModuleMixin):

    def __init__(self, title="Untitled", tilt_rad=0.0, rotation_rad=0.0):
        """
        Creates a new PENELOPE geometry.
        
        :arg tilt_rad: Specimen tilt in radians along the x-axis
        :arg rotation_rad: Specimen rotation in radians along the z-axis
        """
        self.title = title
        self.tilt_rad = tilt_rad
        self.rotation_rad = rotation_rad
        self._modules = set()

    def get_materials(self):
        return set(map(attrgetter('material'), self.get_modules()))

    def get_surfaces(self):
        return set(chain(*map(methodcaller('get_surfaces'), self.get_modules())))

    def _indexify(self):
        index_lookup = {}

        # Materials
        index_lookup[VACUUM] = 0
        for i, material in enumerate(self.get_materials(), 1):
            index_lookup[material] = i

        # Surfaces
        for i, surface in enumerate(self.get_surfaces()):
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

        for i, module in enumerate(modules_order):
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
        extra.rotation.omega_rad = (self.rotation_rad - math.pi / 2.0) % (2 * math.pi)
        extra.rotation.theta_rad = self.tilt_rad
        extra.rotation.phi_rad = math.pi / 2.0

        return extra

    def to_geo(self):
        index_lookup = self._indexify()

        lines = []

        lines.append(LINE_START)
        lines.append('       %s' % self.title)
        lines.append(LINE_SEPARATOR)

        # Surfaces
        surfaces = sorted((index_lookup[surface], surface)
                          for surface in self.get_surfaces())

        for _index, surface in surfaces:
            lines.extend(surface.to_geo(index_lookup))
            lines.append(LINE_SEPARATOR)

        # Modules
        modules = sorted((index_lookup[module], module)
                          for module in self.get_modules())

        for _index, module in modules:
            lines.extend(module.to_geo(index_lookup))
            lines.append(LINE_SEPARATOR)

        # Extra module for tilt and rotation
        extra = self._create_extra_module()

        index_lookup[extra] = len(self.get_modules())
        lines.extend(extra.to_geo(index_lookup))
        lines.append(LINE_SEPARATOR)

        # End of line
        lines.append(LINE_END)

        return lines

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
            raise ValueError("The length of the title (%i) must be less than %i." %
                             (len(title), LINE_SIZE - 3))
        self._title = title

    @property
    def tilt_rad(self):
        """
        Specimen tilt in radians along the x-axis
        """
        return self._tilt_rad

    @tilt_rad.setter
    def tilt_rad(self, angle_rad):
        while angle_rad < 0:
            angle_rad += 2.0 * math.pi
        self._tilt_rad = angle_rad

    @property
    def rotation_rad(self):
        """
        Specimen rotation in radians along the z-axis
        """
        return self._rotation_rad

    @rotation_rad.setter
    def rotation_rad(self, angle_rad):
        self._rotation_rad = angle_rad
