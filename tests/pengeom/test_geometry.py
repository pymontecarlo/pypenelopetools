""" """

# Standard library modules.
import io

# Third party modules.
import pytest

# Local modules.
from pypenelopetools.pengeom.geometry import Geometry
from pypenelopetools.pengeom.surface import zplane, cylinder, xplane
from pypenelopetools.pengeom.module import Module, SidePointer
from pypenelopetools.material import Material, VACUUM

# Globals and constants variables.


@pytest.fixture
def material1():
    return Material("copper", {29: 1.0}, 8.9)


@pytest.fixture
def material2():
    return Material("zinc", {30: 1.0}, 7.14)


@pytest.fixture
def geometry(material1, material2):
    geometry = Geometry("Test Geometry")

    surface1 = zplane(1e-8)
    surface2 = zplane(-1e-1)
    surface3 = cylinder(1.0)
    surface4 = xplane(0.0)

    module1 = Module(material1)
    module1.add_surface(surface1, SidePointer.NEGATIVE)
    module1.add_surface(surface2, SidePointer.POSITIVE)
    module1.add_surface(surface3, SidePointer.NEGATIVE)
    module1.add_surface(surface4, SidePointer.POSITIVE)
    geometry.add_module(module1)

    module2 = Module(material2)
    module2.add_surface(surface1, SidePointer.NEGATIVE)
    module2.add_surface(surface2, SidePointer.POSITIVE)
    module2.add_surface(surface3, SidePointer.NEGATIVE)
    module2.add_module(module1)
    geometry.add_module(module2)

    geometry.tilt_deg = 45

    return geometry


LINES = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "       Test Geometry",
    "0000000000000000000000000000000000000000000000000000000000000000",
    "SURFACE (   1) Plane Z=0.00 m",
    "INDICES=( 0, 0, 0, 1, 0)",
    "X-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "Y-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "Z-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Z-SHIFT=(+1.000000000000000E-08,   0)              (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
    "SURFACE (   2) Cylinder of radius 0.01 m along z-axis",
    "INDICES=( 1, 1, 0, 0,-1)",
    "X-SCALE=(+1.000000000000000E-02,   0)              (DEFAULT=1.0)",
    "Y-SCALE=(+1.000000000000000E-02,   0)              (DEFAULT=1.0)",
    "Z-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
    "SURFACE (   3) Plane Z=-0.00 m",
    "INDICES=( 0, 0, 0, 1, 0)",
    "X-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "Y-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "Z-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Z-SHIFT=(-1.000000000000000E-01,   0)              (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
    "SURFACE (   4) Plane X=0.00 m",
    "INDICES=( 0, 0, 0, 1, 0)",
    "X-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "Y-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "Z-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)",
    "  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "  THETA=(+9.000000000000000E+01,   0) DEG          (DEFAULT=0.0)",
    "    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
    "MODULE  (   1) ",
    "MATERIAL(   1)",
    "SURFACE (   1), SIDE POINTER=(-1)",
    "SURFACE (   2), SIDE POINTER=(-1)",
    "SURFACE (   3), SIDE POINTER=( 1)",
    "SURFACE (   4), SIDE POINTER=( 1)",
    "1111111111111111111111111111111111111111111111111111111111111111",
    "  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
    "MODULE  (   2) ",
    "MATERIAL(   2)",
    "SURFACE (   1), SIDE POINTER=(-1)",
    "SURFACE (   2), SIDE POINTER=(-1)",
    "SURFACE (   3), SIDE POINTER=( 1)",
    "MODULE  (   1)",
    "1111111111111111111111111111111111111111111111111111111111111111",
    "  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)",
    "X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
    "MODULE  (   3) Extra module for rotation and tilt",
    "MATERIAL(   0)",
    "MODULE  (   2)",
    "1111111111111111111111111111111111111111111111111111111111111111",
    "  OMEGA=(+2.700000000000000E+02,   0) DEG          (DEFAULT=0.0)",
    "  THETA=(+4.500000000000000E+01,   0) DEG          (DEFAULT=0.0)",
    "    PHI=(+9.000000000000000E+01,   0) DEG          (DEFAULT=0.0)",
    "X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)",
    "0000000000000000000000000000000000000000000000000000000000000000",
    "END      0000000000000000000000000000000000000000000000000000000",
]


def _test_geometry(geometry):
    assert geometry.title == "Test Geometry"
    assert len(geometry.get_modules()) == 3
    assert len(geometry.get_surfaces()) == 4
    assert len(geometry.get_materials()) == 2


def testskeleton(geometry):
    assert geometry.title == "Test Geometry"
    assert len(geometry.get_modules()) == 2
    assert len(geometry.get_surfaces()) == 4
    assert len(geometry.get_materials()) == 2
    assert geometry.tilt_deg == pytest.approx(45, abs=1e-4)
    assert geometry.rotation_deg == pytest.approx(0.0, abs=1e-4)


def testindexify(geometry):
    index_lookup = geometry.indexify()

    # 4 surfaces, 2 materials, 2 modules, 1 extra module
    assert len(index_lookup) == 4 + 2 + 2 + 1

    index_lookup2 = geometry.indexify()
    assert index_lookup == index_lookup2


def testwriteread(geometry, material1, material2):
    material_lookup = {0: VACUUM, 1: material1, 2: material2}
    fileobj = io.StringIO()

    try:
        geometry.write(fileobj)

        fileobj.seek(0)
        lines = fileobj.getvalue().splitlines()
        assert lines[:3] == LINES[:3]
        assert lines[14] == LINES[14]
        assert lines[26] == LINES[26]
        assert lines[38] == LINES[38]
        assert lines[50] == LINES[50]
        assert lines[51] == LINES[51]
        assert lines[57:65] == LINES[57:65]
        assert lines[65] == LINES[65]
        assert lines[71:] == LINES[71:]

        fileobj.seek(0)
        geometry = Geometry()
        geometry.read(fileobj, material_lookup)

        _test_geometry(geometry)

        index_lookup = geometry.indexify()
        assert len(index_lookup) == 4 + 3 + 3
    finally:
        fileobj.close()


def test_epma1_read(testdatadir, material1):
    material_lookup = {1: material1}

    filepath = testdatadir.joinpath("pengeom", "epma1.geo")
    geometry = Geometry()
    with open(filepath, "r") as fp:
        geometry.read(fp, material_lookup)

    assert geometry.title == "Cylindrical homogeneous foil"
    assert len(geometry.get_surfaces()) == 3
    assert len(geometry.get_modules()) == 1
    assert len(geometry.get_materials()) == 1


def test_epma2_read(testdatadir, material1, material2):
    material_lookup = {1: material1, 2: material2}

    filepath = testdatadir.joinpath("pengeom", "epma2.geo")
    geometry = Geometry()
    with open(filepath, "r") as fp:
        geometry.read(fp, material_lookup)

    assert geometry.title == "Cylindrical foil with a material couple"
    assert len(geometry.get_surfaces()) == 4
    assert len(geometry.get_modules()) == 2
    assert len(geometry.get_materials()) == 2
