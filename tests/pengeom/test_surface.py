""" """

# Standard library modules.
import io

# Third party modules.
import pytest

# Local modules.
from pypenelopetools.pengeom.surface import SurfaceImplicit, SurfaceReduced

# Globals and constants variables.


LINES_IMPLICIT = [
    "SURFACE (   1) surface",
    "INDICES=( 0, 0, 0, 0, 0)",
    "    AXX=(+1.000000000000000E+03,   0)              (DEFAULT=0.0)",
    "    AXY=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "    AXZ=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "    AYY=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "    AYZ=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "    AZZ=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "     AX=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "     AY=(+1.000000000000000E+09,   0)              (DEFAULT=0.0)",
    "     AZ=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "     A0=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "1111111111111111111111111111111111111111111111111111111111111111",
    "  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "    PHI=(+1.800000000000000E+02,   0) DEG          (DEFAULT=0.0)",
    "X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Z-SHIFT=(-1.000000000000000E+05,   0)              (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
]

LINES_REDUCED = [
    "SURFACE (   1) surface",
    "INDICES=( 1, 1, 1, 0,-1)",
    "X-SCALE=(+3.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "Y-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "Z-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
]


@pytest.fixture
def surface_implicit():
    coefficients = (1e3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1e9, 0.0, 0.0)
    surface = SurfaceImplicit(coefficients, description="surface")
    surface.rotation.phi_deg = 180
    surface.shift.z_cm = -1e5
    return surface


@pytest.fixture
def surface_reduced():
    surface = SurfaceReduced((1, 1, 1, 0, -1), "surface")
    surface.scale.x = 3.0
    return surface


def _test_surfaceimplicit(surface):
    assert surface.description == "surface"
    assert surface.rotation.phi_deg == pytest.approx(180, abs=1e-4)
    assert surface.shift.z_cm == pytest.approx(-1e5, abs=1e-4)
    assert surface.coefficients["xx"] == pytest.approx(1e3, abs=1e-4)
    assert surface.coefficients["xy"] == pytest.approx(0.0, abs=1e-4)
    assert surface.coefficients["xz"] == pytest.approx(0.0, abs=1e-4)
    assert surface.coefficients["yy"] == pytest.approx(0.0, abs=1e-4)
    assert surface.coefficients["yz"] == pytest.approx(0.0, abs=1e-4)
    assert surface.coefficients["zz"] == pytest.approx(0.0, abs=1e-4)
    assert surface.coefficients["x"] == pytest.approx(0.0, abs=1e-4)
    assert surface.coefficients["y"] == pytest.approx(1e9, abs=1e-4)
    assert surface.coefficients["z"] == pytest.approx(0.0, abs=1e-4)
    assert surface.coefficients["0"] == pytest.approx(0.0, abs=1e-4)


def _test_surfacereduced(surface):
    assert surface.indices == (1, 1, 1, 0, -1)
    assert surface.description == "surface"
    assert surface.scale.x == pytest.approx(3.0, abs=1e-4)


def testsurfaceimplicit(surface_implicit):
    _test_surfaceimplicit(surface_implicit)


def testsurfaceimplicit_write_read(surface_implicit):
    fileobj = io.StringIO()

    try:
        surface_implicit._write(fileobj, {surface_implicit: 1})

        lines = fileobj.getvalue().splitlines()
        assert lines == LINES_IMPLICIT

        fileobj.seek(0)
        surface = SurfaceImplicit()
        surface._read(fileobj, {}, {}, {})
        _test_surfaceimplicit(surface)
    finally:
        fileobj.close()


def testsurfacereduced(surface_reduced):
    _test_surfacereduced(surface_reduced)


def testsurfacereduced_write_read(surface_reduced):
    fileobj = io.StringIO()

    try:
        surface_reduced._write(fileobj, {surface_reduced: 1})

        lines = fileobj.getvalue().splitlines()
        assert lines == LINES_REDUCED

        fileobj.seek(0)
        surface = SurfaceReduced()
        surface._read(fileobj, {}, {}, {})
        _test_surfacereduced(surface)
    finally:
        fileobj.close()
