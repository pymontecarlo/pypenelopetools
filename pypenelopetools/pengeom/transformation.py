""""""

# Standard library modules.
import math

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.keyword import Keyword
from pypenelopetools.pengeom.base import GeoBase

# Globals and constants variables.

class Rotation(GeoBase):

    _KEYWORD_OMEGA = Keyword('OMEGA=', ' DEG          (DEFAULT=0.0)')
    _KEYWORD_THETA = Keyword('THETA=', ' DEG          (DEFAULT=0.0)')
    _KEYWORD_PHI = Keyword('PHI=', ' DEG          (DEFAULT=0.0)')

    def __init__(self, omega_deg=0.0, theta_deg=0.0, phi_deg=0.0):
        """
        Represents a rotation using 3 Euler angles (YZY).

        :arg omega_deg: rotation around the z-axis (deg)
        :arg theta_deg: rotation around the y-axis (deg)
        :arg phi_deg: rotation around the new z-axis (deg)
        """
        self.omega_deg = omega_deg
        self.theta_deg = theta_deg
        self.phi_deg = phi_deg

    def __repr__(self):
        return "<Rotation(omega=%s, theta=%s, phi=%s)>" % \
                    (self.omega_deg, self.theta_deg, self.phi_deg)

    def __str__(self):
        return '(omega=%s, theta=%s, phi=%s)' % \
                    (self.omega_deg, self.theta_deg, self.phi_deg)

    def to_geo(self, index_lookup):
        """
        Returns the lines of this class to create a GEO file.
        """
        lines = []

        line = self._KEYWORD_OMEGA.create_expline(self.omega_deg)
        lines.append(line)

        line = self._KEYWORD_THETA.create_expline(self.theta_deg)
        lines.append(line)

        line = self._KEYWORD_PHI.create_expline(self.phi_deg)
        lines.append(line)

        return lines

    @property
    def omega_deg(self):
        """
        Rotation around the z-axis (deg).
        The value must be between 0 and 360.
        """
        return self._omega

    @omega_deg.setter
    def omega_deg(self, angle):
        if angle < 0 or angle > 360.0:
            raise ValueError("Angle (%s) must be between [0,360]." % angle)
        self._omega = angle

    @property
    def theta_deg(self):
        """
        Rotation around the y-axis (deg).
        The value must be between 0 and 360.
        """
        return self._theta

    @theta_deg.setter
    def theta_deg(self, angle):
        if angle < 0 or angle > 360:
            raise ValueError("Angle (%s) must be between [0,360]." % angle)
        self._theta = angle

    @property
    def phi_deg(self):
        """
        Rotation around the new z-axis (deg).
        The new z-axis refer to the axis after the omega and theta rotation were
        applied on the original coordinate system.
        The value must be between 0 and 360.
        """
        return self._phi

    @phi_deg.setter
    def phi_deg(self, angle):
        if angle < 0 or angle > 360:
            raise ValueError("Angle (%s) must be between [0,360]." % angle)
        self._phi = angle

class Shift(GeoBase):

    _KEYWORD_X = Keyword('X-SHIFT=', '              (DEFAULT=0.0)')
    _KEYWORD_Y = Keyword('Y-SHIFT=', '              (DEFAULT=0.0)')
    _KEYWORD_Z = Keyword('Z-SHIFT=', '              (DEFAULT=0.0)')

    def __init__(self, x_cm=0.0, y_cm=0.0, z_cm=0.0):
        """
        Represents a translation in space.

        :arg x_cm: translation along the x direction (cm)
        :arg y_cm: translation along the y direction (cm)
        :arg z_cm: translation along the z direction (cm)
        """
        self.x_cm = x_cm
        self.y_cm = y_cm
        self.z_cm = z_cm

    def __repr__(self):
        return "<Shift(x=%s, y=%s, z=%s)>" % (self.x_cm, self.y_cm, self.z_cm)

    def __str__(self):
        return "(x=%s, y=%s, z=%s)" % (self.x_cm, self.y_cm, self.z_cm)

    def to_geo(self, index_lookup):
        """
        Returns the lines of this class to create a GEO file.
        """
        lines = []

        line = self._KEYWORD_X.create_expline(self.x_cm)
        lines.append(line)

        line = self._KEYWORD_Y.create_expline(self.y_cm)
        lines.append(line)

        line = self._KEYWORD_Z.create_expline(self.z_cm)
        lines.append(line)

        return lines

    @property
    def x_cm(self):
        """
        Translation along the x direction (cm).
        """
        return self._x

    @x_cm.setter
    def x_cm(self, shift):
        self._x = shift

    @property
    def y_cm(self):
        """
        Translation along the y direction (cm).
        """
        return self._y

    @y_cm.setter
    def y_cm(self, shift):
        self._y = shift

    @property
    def z_cm(self):
        """
        Translation along the z direction (cm).
        """
        return self._z

    @z_cm.setter
    def z_cm(self, shift):
        self._z = shift

class Scale(GeoBase):

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
