"""
Definition of surfaces
"""

__all__ = ['SurfaceImplicit', 'SurfaceReduced',
           'xplane', 'yplane', 'zplane', 'cylinder', 'sphere',
           'AXIS_X', 'AXIS_Y', 'AXIS_Z']

# Standard library modules.
import math

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.common import \
    Keyword, PengeomComponent, DescriptionMixin, LINE_EXTRA
from pypenelopetools.pengeom.transformation import Rotation, Shift, Scale

# Globals and constants variables.
AXIS_X = 'x'
AXIS_Y = 'y'
AXIS_Z = 'z'

class _Surface(DescriptionMixin, PengeomComponent):

    _KEYWORD_SURFACE = Keyword("SURFACE")
    _KEYWORD_INDICES = Keyword('INDICES=')

    def __init__(self, description=''):
        self.description = description

        self._rotation = Rotation()
        self._shift = Shift()

    def to_geo(self, index_lookup):
        lines = []

        index = index_lookup[self]
        text = "%4i" % (index + 1,)
        comment = " %s" % self.description
        line = self._KEYWORD_SURFACE.create_line(text, comment)
        lines.append(line)

        lines.extend(self.rotation.to_geo(index_lookup))
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

class SurfaceImplicit(_Surface):

    _KEYWORD_AXX = Keyword('AXX=', '              (DEFAULT=0.0)')
    _KEYWORD_AXY = Keyword('AXY=', '              (DEFAULT=0.0)')
    _KEYWORD_AXZ = Keyword('AXZ=', '              (DEFAULT=0.0)')
    _KEYWORD_AYY = Keyword('AYY=', '              (DEFAULT=0.0)')
    _KEYWORD_AYZ = Keyword('AYZ=', '              (DEFAULT=0.0)')
    _KEYWORD_AZZ = Keyword('AZZ=', '              (DEFAULT=0.0)')
    _KEYWORD_AX = Keyword('AX=', '              (DEFAULT=0.0)')
    _KEYWORD_AY = Keyword('AY=', '              (DEFAULT=0.0)')
    _KEYWORD_AZ = Keyword('AZ=', '              (DEFAULT=0.0)')
    _KEYWORD_A0 = Keyword('A0=', '              (DEFAULT=0.0)')

    def __init__(self, coefficients=[0.0] * 10, description=''):
        super().__init__(description)

        self.coefficients = coefficients

    def __repr__(self):
        coeffs = ['%s=%s' % (key, value) for key, value in self.coefficients.iteritems()]
        return '<Surface(description=%s, %s, rotation=%s, shift=%s)>' % \
            (self.description, ', '.join(coeffs), str(self.rotation), str(self.shift))

    def to_geo(self, index_lookup):
        def create_coefficient_line(key):
            value = self.coefficients[key]
            keyword = getattr(self, "_KEYWORD_A" + key.upper())
            return keyword.create_expline(value)

        lines = super().to_geo(index_lookup)

        # Indices
        text = "%2i,%2i,%2i,%2i,%2i" % (0, 0, 0, 0, 0)
        line = self._KEYWORD_INDICES.create_line(text)
        lines.insert(1, line)

        # Coefficients
        lines.insert(2, create_coefficient_line('xx'))
        lines.insert(3, create_coefficient_line('xy'))
        lines.insert(4, create_coefficient_line('xz'))
        lines.insert(5, create_coefficient_line('yy'))
        lines.insert(6, create_coefficient_line('yz'))
        lines.insert(7, create_coefficient_line('zz'))
        lines.insert(8, create_coefficient_line('x'))
        lines.insert(9, create_coefficient_line('y'))
        lines.insert(10, create_coefficient_line('z'))
        lines.insert(11, create_coefficient_line('0'))
        lines.insert(12, LINE_EXTRA)

        return lines

    @property
    def coefficients(self):
        """
        Coefficients for the implicit form of the quadratic equation.
        The coefficients are defined by a dictionary, a list or a tuple.
        See examples below.

        **Examples**::

          >>> s = Surface()
          >>> s.coefficients = {'xx': 0.0, 'xy': 0.0, 'xz': 0.0, 'yy': 0.0, 'yz': 0.0, 'zz': 0.0, 'x': 0.0, 'y': 0.0, 'z': 0.0, '0': 0.0}
          >>> s.coefficients = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
          >>> s.coefficients = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
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

class SurfaceReduced(_Surface):

    def __init__(self, indices, description=''):
        super().__init__(description)

        self.indices = indices
        self._scale = Scale()

    def __repr__(self):
        return '<Surface(description=%s, indices=%s, scale=%s, rotation=%s, shift=%s)>' % \
            (self.description, str(self.indices), str(self.scale),
             str(self.rotation), str(self.shift))

    def to_geo(self, index_lookup):
        lines = super().to_geo(index_lookup)

        # Indices
        text = "%2i,%2i,%2i,%2i,%2i" % self.indices
        line = self._KEYWORD_INDICES.create_line(text)
        lines.insert(1, line)

        for i, line in enumerate(self.scale.to_geo(index_lookup)):
            lines.insert(2 + i, line)

        return lines

    @property
    def indices(self):
        """
        Indices for the explicit form of the quadratic equation.
        The indices are defined by a :class:`tuple` containing 5 indices (-1, 0 or 1).
        If the attribute is deleted, all the indices are set to 0.
        """
        return self._indices

    @indices.setter
    def indices(self, indices):
        if len(indices) != 5:
            raise ValueError("Five indices must be defined.")

        for indice in indices:
            if not indice in [-1, 0, 1]:
                raise ValueError("Index (%s) must be either -1, 0 or 1." % indice)

        self._indices = tuple(indices)

    @property
    def scale(self):
        """
        Scaling of the surface.
        The scaling is defined by a :class:`.Scale`.
        """
        return self._scale

def xplane(x_m):
    """
    Returns a surface for a plane X=x

    :arg z_m: intercept on the x-axis (in m)

    :rtype: :class:`.Surface`
    """
    s = SurfaceReduced((0, 0, 0, 1, 0), 'Plane X=%4.2f m' % x_m)
    s.shift.x_m = x_m
    s.rotation.theta_rad = math.pi / 2.0
    return s

def yplane(y_m):
    """
    Returns a surface for a plane Y=y

    :arg y_m: intercept on the y-axis (in m)

    :rtype: :class:`.Surface`
    """
    s = SurfaceReduced((0, 0, 0, 1, 0), 'Plane Y=%4.2f m' % y_m)
    s.shift.y_m = y_m
    s.rotation.theta_rad = math.pi / 2.0
    s.rotation.phi_rad = math.pi / 2.0
    return s

def zplane(z_m):
    """
    Returns a surface for a plane Z=z

    :arg z_m: intercept on the z-axis (in m)

    :rtype: :class:`.Surface`
    """
    s = SurfaceReduced((0, 0, 0, 1, 0), 'Plane Z=%4.2f m' % z_m)
    s.shift.z_m = z_m
    return s

def cylinder(radius_m, axis=AXIS_Z):
    """
    Returns a surface for a cylinder along *axis* with *radius*

    :arg radius_m: radius of the cylinder (in m)
    :arg axis: axis of the cylinder (:const:`AXIS_X`, :const:`AXIS_Y` or :const:`AXIS_Z`)

    :rtype: :class:`.Surface`
    """
    axis = axis.lower()
    description = 'Cylinder of radius %4.2f m along %s-axis' % (radius_m, axis)
    s = SurfaceReduced((1, 1, 0, 0, -1), description)

    s.scale.x = radius_m * 100
    s.scale.y = radius_m * 100

    if axis == 'z':
        pass
    elif axis == 'x':
        s.rotation.theta_rad = math.pi / 2.0
    elif axis == 'y':
        s.rotation.theta_rad = math.pi / 2.0
        s.rotation.phi_rad = math.pi / 2.0

    return s

def sphere(radius_m):
    """
    Returns a surface for a sphere or *radius*

    :arg radius_m: radius of the cylinder (in m)

    :rtype: :class:`.Surface`
    """
    description = 'Sphere of radius %4.2f m' % radius_m
    s = SurfaceReduced((1, 1, 1, 0, -1), description)

    s.scale.x = radius_m * 100
    s.scale.y = radius_m * 100
    s.scale.z = radius_m * 100

    return s
