""""""

# Standard library modules.
import math

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.common import Keyword, PengeomComponent

# Globals and constants variables.

class Rotation(PengeomComponent):

    _KEYWORD_OMEGA = Keyword('OMEGA=', ' DEG          (DEFAULT=0.0)')
    _KEYWORD_THETA = Keyword('THETA=', ' DEG          (DEFAULT=0.0)')
    _KEYWORD_PHI = Keyword('PHI=', ' DEG          (DEFAULT=0.0)')

    def __init__(self, omega_rad=0.0, theta_rad=0.0, phi_rad=0.0):
        """
        Represents a rotation using 3 Euler angles (YZY).

        :arg omega_rad: rotation around the z-axis (rad)
        :arg theta_rad: rotation around the y-axis (rad)
        :arg phi_rad: rotation around the new z-axis (rad)
        """
        self.omega_rad = omega_rad
        self.theta_rad = theta_rad
        self.phi_rad = phi_rad

    def __repr__(self):
        return "<Rotation(omega=%s, theta=%s, phi=%s)>" % \
                    (self.omega_rad, self.theta_rad, self.phi_rad)

    def __str__(self):
        return '(omega=%s, theta=%s, phi=%s)' % \
                    (self.omega_rad, self.theta_rad, self.phi_rad)

    def to_geo(self, index_lookup):
        """
        Returns the lines of this class to create a GEO file.
        """
        lines = []

        line = self._KEYWORD_OMEGA.create_expline(math.degrees(self.omega_rad))
        lines.append(line)

        line = self._KEYWORD_THETA.create_expline(math.degrees(self.theta_rad))
        lines.append(line)

        line = self._KEYWORD_PHI.create_expline(math.degrees(self.phi_rad))
        lines.append(line)

        return lines

    @property
    def omega_rad(self):
        """
        Rotation around the z-axis (rad).
        The value must be between 0 and 2pi.
        """
        return self._omega

    @omega_rad.setter
    def omega_rad(self, angle):
        if angle < 0 or angle > 2 * math.pi:
            raise ValueError("Angle (%s) must be between [0,pi]." % angle)
        self._omega = angle

    @property
    def theta_rad(self):
        """
        Rotation around the y-axis (rad).
        The value must be between 0 and 2pi.
        """
        return self._theta

    @theta_rad.setter
    def theta_rad(self, angle):
        if angle < 0 or angle > 2 * math.pi:
            raise ValueError("Angle (%s) must be between [0,pi]." % angle)
        self._theta = angle

    @property
    def phi_rad(self):
        """
        Rotation around the new z-axis (rad).
        The new z-axis refer to the axis after the omega and theta rotation were
        applied on the original coordinate system.
        The value must be between 0 and 2pi.
        """
        return self._phi

    @phi_rad.setter
    def phi_rad(self, angle):
        if angle < 0 or angle > 2 * math.pi:
            raise ValueError("Angle (%s) must be between [0,pi]." % angle)
        self._phi = angle

class Shift(PengeomComponent):

    _KEYWORD_X = Keyword('X-SHIFT=', '              (DEFAULT=0.0)')
    _KEYWORD_Y = Keyword('Y-SHIFT=', '              (DEFAULT=0.0)')
    _KEYWORD_Z = Keyword('Z-SHIFT=', '              (DEFAULT=0.0)')

    def __init__(self, x_m=0.0, y_m=0.0, z_m=0.0):
        """
        Represents a translation in space.

        :arg x_m: translation along the x direction (m)
        :arg y_m: translation along the y direction (m)
        :arg z_m: translation along the z direction (m)
        """
        self.x_m = x_m
        self.y_m = y_m
        self.z_m = z_m

    def __repr__(self):
        return "<Shift(x=%s, y=%s, z=%s)>" % (self.x_m, self.y_m, self.z_m)

    def __str__(self):
        return "(x=%s, y=%s, z=%s)" % (self.x_m, self.y_m, self.z_m)

    def to_geo(self, index_lookup):
        """
        Returns the lines of this class to create a GEO file.
        """
        lines = []

        line = self._KEYWORD_X.create_expline(self.x_m * 100.0)
        lines.append(line)

        line = self._KEYWORD_Y.create_expline(self.y_m * 100.0)
        lines.append(line)

        line = self._KEYWORD_Z.create_expline(self.z_m * 100.0)
        lines.append(line)

        return lines

    @property
    def x_m(self):
        """
        Translation along the x direction (m).
        """
        return self._x

    @x_m.setter
    def x_m(self, shift):
        self._x = shift

    @property
    def y_m(self):
        """
        Translation along the y direction (m).
        """
        return self._y

    @y_m.setter
    def y_m(self, shift):
        self._y = shift

    @property
    def z_m(self):
        """
        Translation along the z direction (m).
        """
        return self._z

    @z_m.setter
    def z_m(self, shift):
        self._z = shift

class Scale(PengeomComponent):

    _KEYWORD_X = Keyword('X-SCALE=', '              (DEFAULT=1.0)')
    _KEYWORD_Y = Keyword('Y-SCALE=', '              (DEFAULT=1.0)')
    _KEYWORD_Z = Keyword('Z-SCALE=', '              (DEFAULT=1.0)')

    def __init__(self, x=1.0, y=1.0, z=1.0):
        """
        Represents the scaling.

        :arg x: scaling along the x direction
        :arg y: scaling along the y direction
        :arg z: scaling along the z direction
        """
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "<Shift(x=%s, y=%s, z=%s)>" % (self.x, self.y, self.z)

    def __str__(self):
        return "(x=%s, y=%s, z=%s)" % (self.x, self.y, self.z)

    def to_geo(self, index_lookup):
        """
        Returns the lines of this class to create a GEO file.
        """
        lines = []

        line = self._KEYWORD_X.create_expline(self.x)
        lines.append(line)

        line = self._KEYWORD_Y.create_expline(self.y)
        lines.append(line)

        line = self._KEYWORD_Z.create_expline(self.z)
        lines.append(line)

        return lines

    @property
    def x(self):
        """
        Scaling along the x direction.
        The value cannot be 0.
        """
        return self._x

    @x.setter
    def x(self, scale):
        if scale == 0.0:
            raise ValueError("X scale cannot be equal to 0.")
        self._x = scale

    @property
    def y(self):
        """
        Scaling along the y direction.
        The value cannot be 0.
        """
        return self._y

    @y.setter
    def y(self, scale):
        if scale == 0.0:
            raise ValueError("Y scale cannot be equal to 0.")
        self._y = scale

    @property
    def z(self):
        """
        Scaling along the z direction.
        The value cannot be 0.
        """
        return self._z

    @z.setter
    def z(self, scale):
        if scale == 0.0:
            raise ValueError("Z scale cannot be equal to 0.")
        self._z = scale
