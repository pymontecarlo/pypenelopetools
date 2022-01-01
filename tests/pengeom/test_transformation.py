""" """

# Standard library modules.
import io

# Third party modules.
import pytest

# Local modules.
from pypenelopetools.pengeom.transformation import Rotation, Shift, Scale
from pypenelopetools.pengeom.base import LINE_SEPARATOR

# Globals and constants variables.


LINES_ROTATION = [
    "  OMEGA=(+1.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "  THETA=(+2.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "    PHI=(+3.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
]
LINES_SHIFT = [
    "X-SHIFT=(+1.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Y-SHIFT=(+2.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Z-SHIFT=(+3.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
]
LINES_SCALE = [
    "X-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "Y-SCALE=(+2.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "Z-SCALE=(+3.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
]


@pytest.fixture
def rotation():
    return Rotation(1.0, 2.0, 3.0)


@pytest.fixture
def shift():
    return Shift(1.0, 2.0, 3.0)


@pytest.fixture
def scale():
    return Scale(1.0, 2.0, 3.0)


def _test_rotation(rotation):
    assert rotation.omega_deg == pytest.approx(1.0, abs=1e-4)
    assert rotation.theta_deg == pytest.approx(2.0, abs=1e-4)
    assert rotation.phi_deg == pytest.approx(3.0, abs=1e-4)


def _test_shift(shift):
    assert shift.x_cm == pytest.approx(1.0, abs=1e-4)
    assert shift.y_cm == pytest.approx(2.0, abs=1e-4)
    assert shift.z_cm == pytest.approx(3.0, abs=1e-4)


def _test_scale(scale):
    assert scale.x == pytest.approx(1.0, abs=1e-4)
    assert scale.y == pytest.approx(2.0, abs=1e-4)
    assert scale.z == pytest.approx(3.0, abs=1e-4)


def testrotation(rotation):
    _test_rotation(rotation)


def testrotation_write_read(rotation):
    fileobj = io.StringIO()

    try:
        rotation._write(fileobj, {})
        fileobj.write(LINE_SEPARATOR + "\n")

        lines = fileobj.getvalue().splitlines()
        assert lines == LINES_ROTATION

        fileobj.seek(0)
        rotation = Rotation()
        rotation._read(fileobj, {}, {}, {})
        _test_rotation(rotation)
    finally:
        fileobj.close()


def testshift(shift):
    _test_shift(shift)


def testshift_write_read(shift):
    fileobj = io.StringIO()

    try:
        shift._write(fileobj, {})
        fileobj.write(LINE_SEPARATOR + "\n")

        lines = fileobj.getvalue().splitlines()
        assert lines == LINES_SHIFT

        fileobj.seek(0)
        shift = Shift()
        shift._read(fileobj, {}, {}, {})
        _test_shift(shift)
    finally:
        fileobj.close()


def testscale(scale):
    _test_scale(scale)


def testscale_write_read(scale):
    fileobj = io.StringIO()

    try:
        scale._write(fileobj, {})
        fileobj.write(LINE_SEPARATOR + "\n")

        lines = fileobj.getvalue().splitlines()
        assert lines == LINES_SCALE

        fileobj.seek(0)
        scale = Scale()
        scale._read(fileobj, {}, {}, {})
        _test_scale(scale)
    finally:
        fileobj.close()
