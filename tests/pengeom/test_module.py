""" """

# Standard library modules.
import io

# Third party modules.
import pytest

# Local modules.
from pypenelopetools.pengeom.module import Module
from pypenelopetools.pengeom.surface import SurfaceImplicit
from pypenelopetools.material import Material, VACUUM

# Globals and constants variables.


LINES1 = [
    "MODULE  (   1) ",
    "MATERIAL(   0)",
    "1111111111111111111111111111111111111111111111111111111111111111",
    "  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
]
LINES2 = [
    "MODULE  (   2) Test",
    "MATERIAL(   1)",
    "SURFACE (   1), SIDE POINTER=(-1)",
    "SURFACE (   2), SIDE POINTER=( 1)",
    "MODULE  (   1)",
    "1111111111111111111111111111111111111111111111111111111111111111",
    "  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "    PHI=(+1.800000000000000E+02,   0) DEG          (DEFAULT=0.0)",
    "X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Z-SHIFT=(-1.000000000000000E+05,   0)              (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
]


@pytest.fixture
def material1():
    return Material("copper", {29: 1.0}, 8.9)


@pytest.fixture
def surface1():
    return SurfaceImplicit()


@pytest.fixture
def surface2():
    return SurfaceImplicit()


@pytest.fixture
def module1():
    return Module(VACUUM)


@pytest.fixture
def module2(material1, surface1, surface2, module1):
    module = Module(material1, "Test")
    module.add_surface(surface1, -1)
    module.add_surface(surface2, 1)
    module.add_module(module1)
    module.rotation.phi_deg = 180
    module.shift.z_cm = -1e5
    return module


def _test_module1(module):
    assert str(module.material) == str(VACUUM)
    assert len(module.get_surfaces()) == 0
    assert len(module.get_modules()) == 0


def _test_module2(module):
    assert module.material.name == "copper"
    assert module.description == "Test"
    assert module.rotation.phi_deg == pytest.approx(180, abs=1e-4)
    assert module.shift.z_cm == pytest.approx(-1e5, abs=1e-4)
    assert len(module.get_surfaces()) == 2
    assert len(module.get_modules()) == 1


def testskeleton(module1, module2):
    _test_module1(module1)
    _test_module2(module2)


def test_write_read(material1, surface1, surface2, module1, module2):
    material_lookup = {0: VACUUM, 1: material1}
    surface_lookup = {1: surface1, 2: surface2}
    module_lookup = {1: module1}
    index_lookup = {
        VACUUM: 0,
        material1: 1,
        surface1: 1,
        surface2: 2,
        module1: 1,
        module2: 2,
    }

    # Module 1
    fileobj = io.StringIO()

    try:
        module1._write(fileobj, index_lookup)

        lines = fileobj.getvalue().splitlines()
        assert lines == LINES1

        fileobj.seek(0)
        module = Module()
        module._read(fileobj, material_lookup, surface_lookup, module_lookup)
        _test_module1(module)
    finally:
        fileobj.close()

    # Module 2
    fileobj = io.StringIO()

    try:
        module2._write(fileobj, index_lookup)

        lines = fileobj.getvalue().splitlines()
        assert lines == LINES2

        fileobj.seek(0)
        module = Module()
        module._read(fileobj, material_lookup, surface_lookup, module_lookup)
        _test_module2(module)
    finally:
        fileobj.close()
