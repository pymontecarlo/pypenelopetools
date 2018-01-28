"""
Definition of surfaces.
"""

__all__ = ['SurfaceImplicit', 'SurfaceReduced',
           'xplane', 'yplane', 'zplane', 'cylinder', 'sphere']

# Standard library modules.
import os

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.transformation import Rotation, Shift, Scale
from pypenelopetools.pengeom.base import GeometryBase, LINE_EXTRA, LINE_SEPARATOR
from pypenelopetools.pengeom.mixin import DescriptionMixin

# Globals and constants variables.

class SurfaceBase(DescriptionMixin, GeometryBase):
    """
    Base class for surface definition.
    
    Args:
        description (str): Description of the surface
    """

    def __init__(self, description=''):
        self.description = description

        self._rotation = Rotation()
        self._shift = Shift()

    def _write(self, fileobj, index_lookup):
        index = index_lookup[self]
        text = "{:4d}".format(index)
        comment = " " + self.description
        line = self._create_line("SURFACE", text, comment)
        fileobj.write(line + os.linesep)

    @property
    def rotation(self):
        """:obj:`Rotation <pypenelopetools.pengeom.transformation.Rotation>`: Rotation of the surface."""
        return self._rotation

    @property
    def shift(self):
        """:obj:`Shift <pypenelopetools.pengeom.transformation.Shift>`: Shift/translation of the surface."""
        return self._shift

class SurfaceImplicit(SurfaceBase):
    """
    Definition of an implicit surface.
    
    Args:
        coefficients (dict(str, float) or list(float)):
            Coefficients for the implicit form of the quadratic equation.
            If the argument is a :obj:`dict`, the keys are the names of 
            coefficient (e.g. ``xx``) and the values the coefficient values.
            If the argument is a :obj:`list`, the list must contain 10 values,
            one for each coefficient.
        description (str): Description of the surface
    """

    def __init__(self, coefficients=None, description=''):
        super().__init__(description)

        if coefficients is None:
            coefficients = [0.0] * 10
        self.coefficients = coefficients

    def __repr__(self):
        coeffs = ['{0}={1}'.format(key, value)
                  for key, value in self.coefficients.items()]
        return '<Surface(description={0}, {1}, rotation={2}, shift={3})>' \
            .format(self.description, ', '.join(coeffs), str(self.rotation), str(self.shift))

    def _read(self, fileobj, material_lookup, surface_lookup, module_lookup):
        line = self._read_next_line(fileobj)
        _, _, self.description = self._parse_line(line)

        line = self._read_next_line(fileobj)
        if line != 'INDICES=( 0, 0, 0, 0, 0)':
            raise IOError('Expected line "INDICES=( 0, 0, 0, 0, 0)" instead of "{0}"'
                          .format(line))

        line = self._read_next_line(fileobj)
        while line != LINE_EXTRA and line != LINE_SEPARATOR:
            keyword, value, _ = self._parse_expline(line)
            key = keyword[1:-1].lower()
            self.coefficients[key] = value
            line = self._read_next_line(fileobj)

        if line == LINE_EXTRA:
            extra_offset = fileobj.tell()
            self.rotation._read(fileobj, material_lookup, surface_lookup, module_lookup)

            fileobj.seek(extra_offset)
            self.shift._read(fileobj, material_lookup, surface_lookup, module_lookup)

    def _create_coefficient_line(self, key):
        value = self.coefficients[key]
        return self._create_expline('A{}='.format(key.upper()), value, '              (DEFAULT=0.0)')

    def _write(self, fileobj, index_lookup):
        super()._write(fileobj, index_lookup)

        # Indices
        text = "{0:2d},{1:2d},{2:2d},{3:2d},{4:2d}".format(0, 0, 0, 0, 0)
        line = self._create_line('INDICES=', text)
        fileobj.write(line + os.linesep)

        # Coefficients
        fileobj.write(self._create_coefficient_line('xx') + os.linesep)
        fileobj.write(self._create_coefficient_line('xy') + os.linesep)
        fileobj.write(self._create_coefficient_line('xz') + os.linesep)
        fileobj.write(self._create_coefficient_line('yy') + os.linesep)
        fileobj.write(self._create_coefficient_line('yz') + os.linesep)
        fileobj.write(self._create_coefficient_line('zz') + os.linesep)
        fileobj.write(self._create_coefficient_line('x') + os.linesep)
        fileobj.write(self._create_coefficient_line('y') + os.linesep)
        fileobj.write(self._create_coefficient_line('z') + os.linesep)
        fileobj.write(self._create_coefficient_line('0') + os.linesep)
        fileobj.write(LINE_EXTRA + os.linesep)

        self.rotation._write(fileobj, index_lookup)
        self.shift._write(fileobj, index_lookup)

        fileobj.write(LINE_SEPARATOR + os.linesep)

    @property
    def coefficients(self):
        """(dict(str, float) or list(float)): Coefficients for the implicit form of the quadratic equation.
        If the value is a :obj:`dict`, the keys are the names of 
        coefficient (e.g. ``xx``) and the values the coefficient values.
        If the argument is a :obj:`list`, the list must contain 10 values,
        one for each coefficient.
        
        Examples:

          >>> s = Surface()
          >>> s.coefficients = {'xx': 0.0, 'xy': 0.0, 'xz': 0.0, 'yy': 0.0, 'yz': 0.0, 'zz': 0.0, 'x': 0.0, 'y': 0.0, 'z': 0.0, '0': 0.0}
          >>> s.coefficients = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
          >>> s.coefficients = {'xx': 1.0, 'xy': 1.0}
        """
        return self._coefficients

    @coefficients.setter
    def coefficients(self, coefficients):
        if isinstance(coefficients, dict):
            self._coefficients = {'xx': 0.0, 'xy': 0.0, 'xz': 0.0,
                                  'yy': 0.0, 'yz': 0.0,
                                  'zz': 0.0,
                                  'x': 0.0, 'y': 0.0, 'z': 0.0, '0': 0.0}

            for key in coefficients:
                key = key.lower()
                assert key in self._coefficients
                self._coefficients[key] = coefficients[key]
        else:
            assert len(coefficients) == 10

            self._coefficients = \
                {'xx': coefficients[0], 'xy': coefficients[1], 'xz': coefficients[2],
                 'yy': coefficients[3], 'yz': coefficients[4],
                 'zz': coefficients[5],
                 'x': coefficients[6], 'y': coefficients[7], 'z': coefficients[8],
                 '0': coefficients[9]}

class SurfaceReduced(SurfaceBase):
    """
    Definition of a reduced/explicit surface.
    
    Args:
        indices (tuple(int)):
            Indices for the explicit form of the quadratic equation.
            Indices are 5 integers (-1, 0 or 1) defining the surface.
        description (str): Description of the surface
    """

    def __init__(self, indices=None, description=''):
        super().__init__(description)

        if indices is None:
            indices = (0, 0, 0, 0, 0)
        self.indices = indices
        self._scale = Scale()

    def __repr__(self):
        return '<Surface(description={0}, indices={1}, scale={2}, rotation={3}, shift={4})>' \
            .format(self.description, str(self.indices), str(self.scale),
                    str(self.rotation), str(self.shift))

    def _read(self, fileobj, material_lookup, surface_lookup, module_lookup):
        line = self._read_next_line(fileobj)
        _, _, self.description = self._parse_line(line)

        line = self._read_next_line(fileobj)
        keyword, text, _termination = self._parse_line(line)
        if keyword != 'INDICES=':
            raise IOError('Expected keyword "INDICES=" instead of "{0}"'.format(keyword))
        self.indices = tuple(map(int, text.split(',')))

        extra_offset = fileobj.tell()
        self.rotation._read(fileobj, material_lookup, surface_lookup, module_lookup)

        fileobj.seek(extra_offset)
        self.shift._read(fileobj, material_lookup, surface_lookup, module_lookup)

        fileobj.seek(extra_offset)
        self.scale._read(fileobj, material_lookup, surface_lookup, module_lookup)

    def _write(self, fileobj, index_lookup):
        super()._write(fileobj, index_lookup)

        # Indices
        text = "{0:2d},{1:2d},{2:2d},{3:2d},{4:2d}".format(*self.indices)
        line = self._create_line('INDICES=', text)
        fileobj.write(line + os.linesep)

        self.scale._write(fileobj, index_lookup)
        self.rotation._write(fileobj, index_lookup)
        self.shift._write(fileobj, index_lookup)

        fileobj.write(LINE_SEPARATOR + os.linesep)

    @property
    def indices(self):
        """(tuple(int)):Indices for the explicit form of the quadratic equation.
        Indices are 5 integers (-1, 0 or 1) defining the surface.
        """
        return self._indices

    @indices.setter
    def indices(self, indices):
        if len(indices) != 5:
            raise ValueError("Five indices must be defined.")

        for indice in indices:
            if not indice in [-1, 0, 1]:
                raise ValueError("Index ({:d}) must be either -1, 0 or 1.".format(indice))

        self._indices = tuple(indices)

    @property
    def scale(self):
        """:obj:`Scale <pypenelopetools.pengeom.transformation.Scale>`: Scaling of the surface."""
        return self._scale

def xplane(x_cm):
    """
    Returns a surface for a plane X=x.
    
    Args:
        x_cm (float): Intercept on the x-axis (in cm).
    
    Returns:
        :obj:`SurfaceReduced`
    """
    s = SurfaceReduced((0, 0, 0, 1, 0), 'Plane X={:4.2f} cm'.format(x_cm))
    s.shift.x_cm = x_cm
    s.rotation.theta_deg = 90.0
    return s

def yplane(y_cm):
    """
    Returns a surface for a plane Y=y.
    
    Args:
        y_cm (float): Intercept on the y-axis (in cm).

    Returns:
        :obj:`SurfaceReduced`
    """
    s = SurfaceReduced((0, 0, 0, 1, 0), 'Plane Y={:4.2f} cm'.format(y_cm))
    s.shift.y_cm = y_cm
    s.rotation.theta_deg = 90.0
    s.rotation.phi_deg = 90.0
    return s

def zplane(z_cm):
    """
    Returns a surface for a plane Z=z.
    
    Args:
        z_cm (float): Intercept on the z-axis (in cm).

    Returns:
        :obj:`SurfaceReduced`
    """
    s = SurfaceReduced((0, 0, 0, 1, 0), 'Plane Z={:4.2f} cm'.format(z_cm))
    s.shift.z_cm = z_cm
    return s

def cylinder(radius_cm, axis='x'):
    """
    Returns a surface for a cylinder along *axis* with *radius*.

    Args:
        radius_cm (float): Radius of the cylinder (in cm).
        axis (str): Axis of the cylinder, either ``x``, ``y`` or ``z``.
    
    Returns:
        :obj:`SurfaceReduced`
    """
    axis = axis.lower()
    description = 'Cylinder of radius {0:4.2f} cm along {1}-axis'.format(radius_cm, axis)
    s = SurfaceReduced((1, 1, 0, 0, -1), description)

    s.scale.x = radius_cm
    s.scale.y = radius_cm

    if axis == 'z':
        pass
    elif axis == 'x':
        s.rotation.theta_deg = 90.0
    elif axis == 'y':
        s.rotation.theta_deg = 90.0
        s.rotation.phi_deg = 90.0

    return s

def sphere(radius_cm):
    """
    Returns a surface for a sphere or *radius*.
    
    Args:
        radius_cm (float): Radius of the sphere (in cm).

    Returns:
        :obj:`SurfaceReduced`
    """
    description = 'Sphere of radius {:4.2f} cm'.format(radius_cm)
    s = SurfaceReduced((1, 1, 1, 0, -1), description)

    s.scale.x = radius_cm
    s.scale.y = radius_cm
    s.scale.z = radius_cm

    return s
