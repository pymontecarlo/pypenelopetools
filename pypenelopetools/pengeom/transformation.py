"""
Definition of geometrical transformations.
"""

# Standard library modules.
import os
import math

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.base import GeometryBase, LINE_SEPARATOR

# Globals and constants variables.

class Rotation(GeometryBase):
    """
    Represents a rotation using 3 Euler angles (YZY).

    Args:
        omega_deg (float): Rotation around the z-axis (deg).
        theta_deg (float): Rotation around the y-axis (deg).
        phi_deg (float): Rotation around the new z-axis (deg).
    """

    def __init__(self, omega_deg=0.0, theta_deg=0.0, phi_deg=0.0):
        self.omega_deg = omega_deg
        self.theta_deg = theta_deg
        self.phi_deg = phi_deg

    def __repr__(self):
        return "<Rotation(omega={0:g} deg, theta={1:g} deg, phi={2:g} deg)>" \
                .format(self.omega_deg, self.theta_deg, self.phi_deg)

    def __str__(self):
        return '(omega={0:g} deg, theta={1:g} deg, phi={2:g} deg)' \
                .format(self.omega_deg, self.theta_deg, self.phi_deg)

    def _read(self, fileobj, material_lookup, surface_lookup, module_lookup):
        line = self._peek_next_line(fileobj)
        while line != LINE_SEPARATOR:
            keyword, value, termination = self._parse_expline(line)

            if termination.startswith('RAD'):
                value = math.degrees(value)

            if keyword == 'OMEGA=':
                self.omega_deg = value
            elif keyword == 'THETA=':
                self.theta_deg = value
            elif keyword == 'PHI=':
                self.phi_deg = value

            line = self._read_next_line(fileobj)

    def _write(self, fileobj, index_lookup):
        line = self._create_expline('OMEGA=', self.omega_deg, ' DEG          (DEFAULT=0.0)')
        fileobj.write(line + os.linesep)

        line = self._create_expline('THETA=', self.theta_deg, ' DEG          (DEFAULT=0.0)')
        fileobj.write(line + os.linesep)

        line = self._create_expline('PHI=', self.phi_deg, ' DEG          (DEFAULT=0.0)')
        fileobj.write(line + os.linesep)

    @property
    def omega_deg(self):
        """float: Rotation around the z-axis (deg).
        The value must be between 0 and 360.
        """
        return self._omega

    @omega_deg.setter
    def omega_deg(self, angle):
        if angle < 0 or angle > 360.0:
            raise ValueError("Angle ({0}) must be between [0,360].".format(angle))
        self._omega = angle

    @property
    def theta_deg(self):
        """float: Rotation around the y-axis (deg).
        The value must be between 0 and 360.
        """
        return self._theta

    @theta_deg.setter
    def theta_deg(self, angle):
        if angle < 0 or angle > 360:
            raise ValueError("Angle ({0}) must be between [0,360].".format(angle))
        self._theta = angle

    @property
    def phi_deg(self):
        """float: Rotation around the new z-axis (deg).
        The new z-axis refer to the axis after the omega and theta rotation were
        applied on the original coordinate system.
        The value must be between 0 and 360.
        """
        return self._phi

    @phi_deg.setter
    def phi_deg(self, angle):
        if angle < 0 or angle > 360:
            raise ValueError("Angle ({0}) must be between [0,360].".format(angle))
        self._phi = angle

class Shift(GeometryBase):
    """
    Represents a translation in space.
    
    Args:
        x_cm (float): Translation along the x direction (cm).
        y_cm (float): Translation along the y direction (cm).
        z_cm (float): Translation along the z direction (cm).
    """

    def __init__(self, x_cm=0.0, y_cm=0.0, z_cm=0.0):
        self.x_cm = x_cm
        self.y_cm = y_cm
        self.z_cm = z_cm

    def __repr__(self):
        return "<Shift(x={0:g} cm, y={1:g} cm, z={2:g} cm)>" \
            .format(self.x_cm, self.y_cm, self.z_cm)

    def __str__(self):
        return "(x={0:g} cm, y={1:g} cm, z={2:g} cm)" \
            .format(self.x_cm, self.y_cm, self.z_cm)

    def _read(self, fileobj, material_lookup, surface_lookup, module_lookup):
        line = self._peek_next_line(fileobj)
        while line != LINE_SEPARATOR:
            keyword, value, _ = self._parse_expline(line)

            if keyword == 'X-SHIFT=':
                self.x_cm = value
            elif keyword == 'Y-SHIFT=':
                self.y_cm = value
            elif keyword == 'Z-SHIFT=':
                self.z_cm = value

            line = self._read_next_line(fileobj)

    def _write(self, fileobj, index_lookup):
        line = self._create_expline('X-SHIFT=', self.x_cm, '              (DEFAULT=0.0)')
        fileobj.write(line + os.linesep)

        line = self._create_expline('Y-SHIFT=', self.y_cm, '              (DEFAULT=0.0)')
        fileobj.write(line + os.linesep)

        line = self._create_expline('Z-SHIFT=', self.z_cm, '              (DEFAULT=0.0)')
        fileobj.write(line + os.linesep)

    @property
    def x_cm(self):
        """float: Translation along the x direction (cm)."""
        return self._x

    @x_cm.setter
    def x_cm(self, shift):
        self._x = shift

    @property
    def y_cm(self):
        """float: Translation along the y direction (cm)."""
        return self._y

    @y_cm.setter
    def y_cm(self, shift):
        self._y = shift

    @property
    def z_cm(self):
        """float: Translation along the z direction (cm)."""
        return self._z

    @z_cm.setter
    def z_cm(self, shift):
        self._z = shift

class Scale(GeometryBase):
    """
    Represents scaling.
    
    Args:
        x (float): Scaling along the x direction.
        y (float): Scaling along the y direction.
        z (float): Scaling along the z direction.
    """

    def __init__(self, x=1.0, y=1.0, z=1.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "<Shift(x={0:g}, y={1:g}, z={2:g})>" \
            .format(self.x, self.y, self.z)

    def __str__(self):
        return "(x={0:g}, y={1:g}, z={2:g})".format(self.x, self.y, self.z)

    def _read(self, fileobj, material_lookup, surface_lookup, module_lookup):
        line = self._peek_next_line(fileobj)
        while line != LINE_SEPARATOR:
            keyword, value, _ = self._parse_expline(line)

            if keyword == 'X-SCALE=':
                self.x = value
            elif keyword == 'Y-SCALE=':
                self.y = value
            elif keyword == 'Z-SCALE=':
                self.z = value

            line = self._read_next_line(fileobj)

    def _write(self, fileobj, index_lookup):
        line = self._create_expline('X-SCALE=', self.x, '              (DEFAULT=1.0)')
        fileobj.write(line + os.linesep)

        line = self._create_expline('Y-SCALE=', self.y, '              (DEFAULT=1.0)')
        fileobj.write(line + os.linesep)

        line = self._create_expline('Z-SCALE=', self.z, '              (DEFAULT=1.0)')
        fileobj.write(line + os.linesep)

    @property
    def x(self):
        """float: Scaling along the x direction.
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
        """float: Scaling along the y direction.
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
        """float: Scaling along the z direction.
        The value cannot be 0.
        """
        return self._z

    @z.setter
    def z(self, scale):
        if scale == 0.0:
            raise ValueError("Z scale cannot be equal to 0.")
        self._z = scale
