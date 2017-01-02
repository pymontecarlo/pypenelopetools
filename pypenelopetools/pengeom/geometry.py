"""
Geometry definition for PENGEOM
"""

# Standard library modules.
from itertools import chain
from operator import methodcaller, attrgetter

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.keyword import \
    LINE_SIZE, LINE_START, LINE_SEPARATOR, LINE_END
from pypenelopetools.pengeom.mixin import ModuleMixin
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

    def __init__(self, title="Untitled", tilt_deg=0.0, rotation_deg=0.0):
        """
        Creates a new PENELOPE geometry.
        
        :arg tilt_deg: Specimen tilt in degrees along the x-axis
        :arg rotation_deg: Specimen rotation in degrees along the z-axis
        """
        self.title = title
        self.tilt_deg = tilt_deg
        self.rotation_deg = rotation_deg
        self._modules = set()

    def get_materials(self):
        return set(map(attrgetter('material'), self.get_modules()))

    def get_surfaces(self):
        return set(chain(*map(methodcaller('get_surfaces'), self.get_modules())))

    def indexify(self):
        index_table = {}

        # Materials
        index_table[VACUUM] = 0
        for i, material in enumerate(self.get_materials(), 1):
            index_table[material] = i

        # Surfaces
        for i, surface in enumerate(self.get_surfaces(), 1):
            index_table[surface] = i

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
            index_table[module] = i

        return index_table

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

    def to_geo(self, index_table):
        lines = []

        lines.append(LINE_START)
        lines.append('       ' + self.title)
        lines.append(LINE_SEPARATOR)

        # Surfaces
        surfaces = sorted((index_table[surface], surface)
                          for surface in self.get_surfaces())

        for _index, surface in surfaces:
            lines.extend(surface.to_geo(index_table))
            lines.append(LINE_SEPARATOR)

        # Modules
        modules = sorted((index_table[module], module)
                          for module in self.get_modules())

        for _index, module in modules:
            lines.extend(module.to_geo(index_table))
            lines.append(LINE_SEPARATOR)

        # Extra module for tilt and rotation
        if self.tilt_deg != 0.0 or self.rotation_deg != 0.0:
            extra = self._create_extra_module()

            index_table[extra] = len(self.get_modules()) + 1
            lines.extend(extra.to_geo(index_table))
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
