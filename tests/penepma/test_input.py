""" """

# Standard library modules.
import io

# Third party modules.
import pyxray
import pytest

# Local modules.
from pypenelopetools.penelope.enums import KPAR, ICOL
from pypenelopetools.penepma.input import PenepmaInput
from pypenelopetools.material import Material
from pypenelopetools.pengeom.surface import xplane, zplane, cylinder
from pypenelopetools.pengeom.module import Module, SidePointer
from pypenelopetools.pengeom.geometry import Geometry
from pypenelopetools.penepma.utils import convert_xrayline_to_izs1s200

# Globals and constants variables.

MATERIAL_CU = Material("Cu", {29: 1.0}, 8.9)
MATERIAL_FE = Material("Fe", {26: 1.0}, 7.874)
XRAYLINE_CU_KA2 = pyxray.xray_line(29, "Ka2")
XRAYLINE_FE_KA2 = pyxray.xray_line(26, "Ka2")


def create_epma1():
    # Create geometry
    module = Module(MATERIAL_CU, "Sample")
    module.add_surface(zplane(0.0), SidePointer.NEGATIVE)
    module.add_surface(zplane(-0.1), SidePointer.POSITIVE)
    module.add_surface(cylinder(1.0), SidePointer.NEGATIVE)

    geometry = Geometry("Cylindrical homogeneous foil")
    geometry.add_module(module)

    index_lookup = geometry.indexify()

    # Create input
    input = PenepmaInput()

    input.TITLE.set("A Cu slab")
    input.SENERG.set(15e3)
    input.SPOSIT.set(0.0, 0.0, 1.0)
    input.SDIREC.set(180, 0.0)
    input.SAPERT.set(0.0)

    input.materials.add(
        index_lookup[MATERIAL_CU],
        MATERIAL_CU.filename,
        1e3,
        1e3,
        1e3,
        0.2,
        0.2,
        1e3,
        1e3,
    )

    input.GEOMFN.set("epma1.geo")
    input.DSMAX.add(index_lookup[module], 1e-4)

    input.IFORCE.add(
        index_lookup[module],
        KPAR.ELECTRON,
        ICOL.HARD_BREMSSTRAHLUNG_EMISSION,
        -5,
        0.9,
        1.0,
    )
    input.IFORCE.add(
        index_lookup[module],
        KPAR.ELECTRON,
        ICOL.INNER_SHELL_IMPACT_IONISATION,
        -250,
        0.9,
        1.0,
    )
    input.IFORCE.add(
        index_lookup[module], KPAR.PHOTON, ICOL.INCOHERENT_SCATTERING, 10, 1e-3, 1.0
    )
    input.IFORCE.add(
        index_lookup[module], KPAR.PHOTON, ICOL.PHOTOELECTRIC_ABSORPTION, 10, 1e-3, 1.0
    )
    input.IBRSPL.add(index_lookup[module], 2)
    input.IXRSPL.add(index_lookup[module], 2)

    input.NBE.set(0, 0, 300)
    input.NBANGL.set(45, 30)

    input.photon_detectors.add(0, 90, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(5, 15, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(15, 25, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(25, 35, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(35, 45, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(45, 55, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(55, 65, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(65, 75, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(75, 85, 0, 360, 0, 0.0, 0.0, 1000)

    input.GRIDX.set(-4e-5, 4e-5, 60)
    input.GRIDY.set(-4e-5, 4e-5, 60)
    input.GRIDZ.set(-6e-5, 0.0, 60)
    input.XRLINE.add(convert_xrayline_to_izs1s200(XRAYLINE_CU_KA2))

    input.RESUME.set("dump1.dat")
    input.DUMPTO.set("dump1.dat")
    input.DUMPP.set(60)

    input.RSEED.set(-10, 1)
    input.REFLIN.set(convert_xrayline_to_izs1s200(XRAYLINE_CU_KA2), 1, 1.25e-3)
    input.NSIMSH.set(2e9)
    input.TIME.set(2e9)

    return input


def create_epma2():
    # Create geometry
    surface_top = zplane(0.0)
    surface_bottom = zplane(-0.1)
    surface_cylinder = cylinder(1.0)
    surface_divider = xplane(0.0)

    module_right = Module(MATERIAL_CU, "Right half of the sample")
    module_right.add_surface(surface_top, SidePointer.NEGATIVE)
    module_right.add_surface(surface_bottom, SidePointer.POSITIVE)
    module_right.add_surface(surface_cylinder, SidePointer.NEGATIVE)
    module_right.add_surface(surface_divider, SidePointer.POSITIVE)

    module_left = Module(MATERIAL_FE, "Left half of the sample")
    module_left.add_surface(surface_top, SidePointer.NEGATIVE)
    module_left.add_surface(surface_bottom, SidePointer.POSITIVE)
    module_left.add_surface(surface_cylinder, SidePointer.NEGATIVE)
    module_left.add_module(module_right)

    geometry = Geometry("Cylindrical homogeneous foil")
    geometry.add_module(module_right)
    geometry.add_module(module_left)

    index_lookup = geometry.indexify()
    index_lookup[MATERIAL_CU] = 1
    index_lookup[MATERIAL_FE] = 2

    # Create input
    input = PenepmaInput()

    input.TITLE.set("A CU-Fe couple")
    input.SENERG.set(15e3)
    input.SPOSIT.set(2e-5, 0.0, 1.0)
    input.SDIREC.set(180, 0.0)
    input.SAPERT.set(0.0)

    input.materials.add(
        index_lookup[MATERIAL_FE],
        MATERIAL_FE.filename,
        1e3,
        1e3,
        1e3,
        0.2,
        0.2,
        1e3,
        1e3,
    )  # Note inversion
    input.materials.add(
        index_lookup[MATERIAL_CU],
        MATERIAL_CU.filename,
        1e3,
        1e3,
        1e3,
        0.2,
        0.2,
        1e3,
        1e3,
    )

    input.GEOMFN.set("epma2.geo")
    input.DSMAX.add(index_lookup[module_right], 1e-4)
    input.DSMAX.add(index_lookup[module_left], 1e-4)

    input.IFORCE.add(
        index_lookup[module_right],
        KPAR.ELECTRON,
        ICOL.HARD_BREMSSTRAHLUNG_EMISSION,
        -5,
        0.9,
        1.0,
    )
    input.IFORCE.add(
        index_lookup[module_right],
        KPAR.ELECTRON,
        ICOL.INNER_SHELL_IMPACT_IONISATION,
        -250,
        0.9,
        1.0,
    )
    input.IFORCE.add(
        index_lookup[module_right],
        KPAR.PHOTON,
        ICOL.INCOHERENT_SCATTERING,
        10,
        1e-3,
        1.0,
    )
    input.IFORCE.add(
        index_lookup[module_right],
        KPAR.PHOTON,
        ICOL.PHOTOELECTRIC_ABSORPTION,
        10,
        1e-3,
        1.0,
    )
    input.IFORCE.add(
        index_lookup[module_left],
        KPAR.ELECTRON,
        ICOL.HARD_BREMSSTRAHLUNG_EMISSION,
        -5,
        0.9,
        1.0,
    )
    input.IFORCE.add(
        index_lookup[module_left],
        KPAR.ELECTRON,
        ICOL.INNER_SHELL_IMPACT_IONISATION,
        -7,
        0.9,
        1.0,
    )
    input.IFORCE.add(
        index_lookup[module_left],
        KPAR.PHOTON,
        ICOL.INCOHERENT_SCATTERING,
        10,
        1e-3,
        1.0,
    )
    input.IFORCE.add(
        index_lookup[module_left],
        KPAR.PHOTON,
        ICOL.PHOTOELECTRIC_ABSORPTION,
        10,
        1e-3,
        1.0,
    )

    input.IBRSPL.add(index_lookup[module_right], 2)
    input.IBRSPL.add(index_lookup[module_left], 2)

    input.IXRSPL.add(index_lookup[module_right], 2)
    input.IXRSPL.add(index_lookup[module_left], 2)

    input.NBE.set(0, 0, 300)
    input.NBANGL.set(45, 30)

    input.photon_detectors.add(0, 90, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(5, 15, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(15, 25, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(25, 35, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(35, 45, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(45, 55, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(55, 65, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(65, 75, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(75, 85, 0, 360, 0, 0.0, 0.0, 1000)

    input.GRIDX.set(-1e-5, 5e-5, 60)
    input.GRIDY.set(-3e-5, 3e-5, 60)
    input.GRIDZ.set(-6e-5, 0.0, 60)
    input.XRLINE.add(convert_xrayline_to_izs1s200(XRAYLINE_FE_KA2))
    input.XRLINE.add(convert_xrayline_to_izs1s200(XRAYLINE_CU_KA2))

    input.RESUME.set("dump2.dat")
    input.DUMPTO.set("dump2.dat")
    input.DUMPP.set(60)

    input.RSEED.set(-10, 1)
    input.REFLIN.set(convert_xrayline_to_izs1s200(XRAYLINE_FE_KA2), 1, 1.5e-3)
    input.NSIMSH.set(2e9)
    input.TIME.set(2e9)

    return input


def _write_read_input(input):
    fileobj = io.StringIO()

    try:
        input.write(fileobj)

        fileobj.seek(0)
        outinput = PenepmaInput()
        outinput.read(fileobj)
    finally:
        fileobj.close()

    return outinput


def _test_epma1(input):
    (se0,) = input.SENERG.get()
    assert se0 == pytest.approx(15e3, abs=1e-5)

    sx0, sy0, sz0 = input.SPOSIT.get()
    assert sx0 == pytest.approx(0.0, abs=1e-5)
    assert sy0 == pytest.approx(0.0, abs=1e-5)
    assert sz0 == pytest.approx(1.0, abs=1e-5)

    theta, phi = input.SDIREC.get()
    assert theta == pytest.approx(180.0, abs=1e-5)
    assert phi == pytest.approx(0.0, abs=1e-5)

    (alpha,) = input.SAPERT.get()
    assert alpha == pytest.approx(0.0, abs=1e-5)

    (materials,) = input.materials.get()
    assert len(materials) == 1

    filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[0]
    assert filename == "Cu.mat"
    assert eabs1 == pytest.approx(1e3, abs=1e-5)
    assert eabs2 == pytest.approx(1e3, abs=1e-5)
    assert eabs3 == pytest.approx(1e3, abs=1e-5)
    assert c1 == pytest.approx(0.2, abs=1e-5)
    assert c2 == pytest.approx(0.2, abs=1e-5)
    assert wcc == pytest.approx(1e3, abs=1e-5)
    assert wcr == pytest.approx(1e3, abs=1e-5)

    assert input.GEOMFN.get()[0] == "epma1.geo"

    (dsmaxs,) = input.DSMAX.get()
    assert len(dsmaxs) == 1

    kb, dsmax = dsmaxs[0]
    assert kb == 1
    assert dsmax == pytest.approx(1e-4, abs=1e-5)

    (iforces,) = input.IFORCE.get()
    assert len(iforces) == 4

    kb, kpar, icol, forcer, wlow, whig = iforces[0]
    assert kb == 1
    assert kpar == 1
    assert icol == 4
    assert forcer == pytest.approx(-5, abs=1e-5)
    assert wlow == pytest.approx(0.9, abs=1e-5)
    assert whig == pytest.approx(1.0, abs=1e-5)

    kb, kpar, icol, forcer, wlow, whig = iforces[1]
    assert kb == 1
    assert kpar == 1
    assert icol == 5
    assert forcer == pytest.approx(-250, abs=1e-5)
    assert wlow == pytest.approx(0.9, abs=1e-5)
    assert whig == pytest.approx(1.0, abs=1e-5)

    kb, kpar, icol, forcer, wlow, whig = iforces[2]
    assert kb == 1
    assert kpar == 2
    assert icol == 2
    assert forcer == pytest.approx(10, abs=1e-5)
    assert wlow == pytest.approx(1e-3, abs=1e-5)
    assert whig == pytest.approx(1.0, abs=1e-5)

    kb, kpar, icol, forcer, wlow, whig = iforces[3]
    assert kb == 1
    assert kpar == 2
    assert icol == 3
    assert forcer == pytest.approx(10, abs=1e-5)
    assert wlow == pytest.approx(1e-3, abs=1e-5)
    assert whig == pytest.approx(1.0, abs=1e-5)

    (ibrspls,) = input.IBRSPL.get()
    assert len(ibrspls) == 1

    kb, factor = ibrspls[0]
    assert kb == 1
    assert factor == pytest.approx(2.0, abs=1e-5)

    (ixrspls,) = input.IXRSPL.get()
    assert len(ixrspls) == 1

    kb, factor = ixrspls[0]
    assert kb == 1
    assert factor == pytest.approx(2.0, abs=1e-5)

    el, eu, nbe = input.NBE.get()
    assert el == pytest.approx(0.0, abs=1e-5)
    assert eu == pytest.approx(0.0, abs=1e-5)
    assert nbe == 300

    nbth, nbph = input.NBANGL.get()
    assert nbth == 45
    assert nbph == 30

    (photon_detectors,) = input.photon_detectors.get()
    assert len(photon_detectors) == 9

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[0]
    assert theta1 == pytest.approx(0.0, abs=1e-5)
    assert theta2 == pytest.approx(90.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[1]
    assert theta1 == pytest.approx(5.0, abs=1e-5)
    assert theta2 == pytest.approx(15.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[2]
    assert theta1 == pytest.approx(15.0, abs=1e-5)
    assert theta2 == pytest.approx(25.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[3]
    assert theta1 == pytest.approx(25.0, abs=1e-5)
    assert theta2 == pytest.approx(35.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[4]
    assert theta1 == pytest.approx(35.0, abs=1e-5)
    assert theta2 == pytest.approx(45.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[5]
    assert theta1 == pytest.approx(45.0, abs=1e-5)
    assert theta2 == pytest.approx(55.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[6]
    assert theta1 == pytest.approx(55.0, abs=1e-5)
    assert theta2 == pytest.approx(65.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[7]
    assert theta1 == pytest.approx(65.0, abs=1e-5)
    assert theta2 == pytest.approx(75.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[8]
    assert theta1 == pytest.approx(75.0, abs=1e-5)
    assert theta2 == pytest.approx(85.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    xl, xu, ndbx = input.GRIDX.get()
    assert xl == pytest.approx(-4e-5, abs=1e-5)
    assert xu == pytest.approx(4e-5, abs=1e-5)
    assert ndbx == 60

    yl, yu, ndby = input.GRIDY.get()
    assert yl == pytest.approx(-4e-5, abs=1e-5)
    assert yu == pytest.approx(4e-5, abs=1e-5)
    assert ndby == 60

    zl, zu, ndbz = input.GRIDZ.get()
    assert zl == pytest.approx(-6e-5, abs=1e-5)
    assert zu == pytest.approx(0.0, abs=1e-5)
    assert ndbz == 60

    (xrlines,) = input.XRLINE.get()
    assert len(xrlines) == 1

    (izs1s200,) = xrlines[0]
    assert izs1s200 == 29010300

    (filename,) = input.RESUME.get()
    assert filename == "dump1.dat"

    (filename,) = input.DUMPTO.get()
    assert filename == "dump1.dat"

    (dumpp,) = input.DUMPP.get()
    assert dumpp == pytest.approx(60.0, abs=1e-5)

    seed1, seed2 = input.RSEED.get()
    assert seed1 == -10
    assert seed2 == 1

    izs1s200, idet, tol = input.REFLIN.get()
    assert izs1s200 == 29010300
    assert idet == 1
    assert tol == pytest.approx(1.25e-3, abs=1e-5)

    (dshn,) = input.NSIMSH.get()
    assert dshn == pytest.approx(2e9, abs=1e-5)

    (timea,) = input.TIME.get()
    assert timea == pytest.approx(2e9, abs=1e-5)


def _test_epma2(input):
    (se0,) = input.SENERG.get()
    assert se0 == pytest.approx(15e3, abs=1e-5)

    sx0, sy0, sz0 = input.SPOSIT.get()
    assert sx0 == pytest.approx(2e-5, abs=1e-8)
    assert sy0 == pytest.approx(0.0, abs=1e-5)
    assert sz0 == pytest.approx(1.0, abs=1e-5)

    theta, phi = input.SDIREC.get()
    assert theta == pytest.approx(180.0, abs=1e-5)
    assert phi == pytest.approx(0.0, abs=1e-5)

    (alpha,) = input.SAPERT.get()
    assert alpha == pytest.approx(0.0, abs=1e-5)

    (materials,) = input.materials.get()
    assert len(materials) == 2

    filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[0]
    assert filename == "Cu.mat"
    assert eabs1 == pytest.approx(1e3, abs=1e-5)
    assert eabs2 == pytest.approx(1e3, abs=1e-5)
    assert eabs3 == pytest.approx(1e3, abs=1e-5)
    assert c1 == pytest.approx(0.2, abs=1e-5)
    assert c2 == pytest.approx(0.2, abs=1e-5)
    assert wcc == pytest.approx(1e3, abs=1e-5)
    assert wcr == pytest.approx(1e3, abs=1e-5)

    filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[1]
    assert filename == "Fe.mat"
    assert eabs1 == pytest.approx(1e3, abs=1e-5)
    assert eabs2 == pytest.approx(1e3, abs=1e-5)
    assert eabs3 == pytest.approx(1e3, abs=1e-5)
    assert c1 == pytest.approx(0.2, abs=1e-5)
    assert c2 == pytest.approx(0.2, abs=1e-5)
    assert wcc == pytest.approx(1e3, abs=1e-5)
    assert wcr == pytest.approx(1e3, abs=1e-5)

    assert input.GEOMFN.get()[0] == "epma2.geo"

    (dsmaxs,) = input.DSMAX.get()
    assert len(dsmaxs) == 2

    kb, dsmax = dsmaxs[0]
    assert kb == 1
    assert dsmax == pytest.approx(1e-4, abs=1e-5)

    kb, dsmax = dsmaxs[1]
    assert kb == 2
    assert dsmax == pytest.approx(1e-4, abs=1e-5)

    (iforces,) = input.IFORCE.get()
    assert len(iforces) == 8

    kb, kpar, icol, forcer, wlow, whig = iforces[0]
    assert kb == 1
    assert kpar == 1
    assert icol == 4
    assert forcer == pytest.approx(-5, abs=1e-5)
    assert wlow == pytest.approx(0.9, abs=1e-5)
    assert whig == pytest.approx(1.0, abs=1e-5)

    kb, kpar, icol, forcer, wlow, whig = iforces[1]
    assert kb == 1
    assert kpar == 1
    assert icol == 5
    assert forcer == pytest.approx(-250, abs=1e-5)
    assert wlow == pytest.approx(0.9, abs=1e-5)
    assert whig == pytest.approx(1.0, abs=1e-5)

    kb, kpar, icol, forcer, wlow, whig = iforces[2]
    assert kb == 1
    assert kpar == 2
    assert icol == 2
    assert forcer == pytest.approx(10, abs=1e-5)
    assert wlow == pytest.approx(1e-3, abs=1e-5)
    assert whig == pytest.approx(1.0, abs=1e-5)

    kb, kpar, icol, forcer, wlow, whig = iforces[3]
    assert kb == 1
    assert kpar == 2
    assert icol == 3
    assert forcer == pytest.approx(10, abs=1e-5)
    assert wlow == pytest.approx(1e-3, abs=1e-5)
    assert whig == pytest.approx(1.0, abs=1e-5)

    kb, kpar, icol, forcer, wlow, whig = iforces[4]
    assert kb == 2
    assert kpar == 1
    assert icol == 4
    assert forcer == pytest.approx(-5, abs=1e-5)
    assert wlow == pytest.approx(0.9, abs=1e-5)
    assert whig == pytest.approx(1.0, abs=1e-5)

    kb, kpar, icol, forcer, wlow, whig = iforces[5]
    assert kb == 2
    assert kpar == 1
    assert icol == 5
    assert forcer == pytest.approx(-7, abs=1e-5)
    assert wlow == pytest.approx(0.9, abs=1e-5)
    assert whig == pytest.approx(1.0, abs=1e-5)

    kb, kpar, icol, forcer, wlow, whig = iforces[6]
    assert kb == 2
    assert kpar == 2
    assert icol == 2
    assert forcer == pytest.approx(10, abs=1e-5)
    assert wlow == pytest.approx(1e-3, abs=1e-5)
    assert whig == pytest.approx(1.0, abs=1e-5)

    kb, kpar, icol, forcer, wlow, whig = iforces[7]
    assert kb == 2
    assert kpar == 2
    assert icol == 3
    assert forcer == pytest.approx(10, abs=1e-5)
    assert wlow == pytest.approx(1e-3, abs=1e-5)
    assert whig == pytest.approx(1.0, abs=1e-5)

    (ibrspls,) = input.IBRSPL.get()
    assert len(ibrspls) == 2

    kb, factor = ibrspls[0]
    assert kb == 1
    assert factor == pytest.approx(2.0, abs=1e-5)

    kb, factor = ibrspls[1]
    assert kb == 2
    assert factor == pytest.approx(2.0, abs=1e-5)

    (ixrspls,) = input.IXRSPL.get()
    assert len(ixrspls) == 2

    kb, factor = ixrspls[0]
    assert kb == 1
    assert factor == pytest.approx(2.0, abs=1e-5)

    kb, factor = ixrspls[1]
    assert kb == 2
    assert factor == pytest.approx(2.0, abs=1e-5)

    el, eu, nbe = input.NBE.get()
    assert el == pytest.approx(0.0, abs=1e-5)
    assert eu == pytest.approx(0.0, abs=1e-5)
    assert nbe == 300

    nbth, nbph = input.NBANGL.get()
    assert nbth == 45
    assert nbph == 30

    (photon_detectors,) = input.photon_detectors.get()
    assert len(photon_detectors) == 9

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[0]
    assert theta1 == pytest.approx(0.0, abs=1e-5)
    assert theta2 == pytest.approx(90.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[1]
    assert theta1 == pytest.approx(5.0, abs=1e-5)
    assert theta2 == pytest.approx(15.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[2]
    assert theta1 == pytest.approx(15.0, abs=1e-5)
    assert theta2 == pytest.approx(25.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[3]
    assert theta1 == pytest.approx(25.0, abs=1e-5)
    assert theta2 == pytest.approx(35.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[4]
    assert theta1 == pytest.approx(35.0, abs=1e-5)
    assert theta2 == pytest.approx(45.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[5]
    assert theta1 == pytest.approx(45.0, abs=1e-5)
    assert theta2 == pytest.approx(55.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[6]
    assert theta1 == pytest.approx(55.0, abs=1e-5)
    assert theta2 == pytest.approx(65.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[7]
    assert theta1 == pytest.approx(65.0, abs=1e-5)
    assert theta2 == pytest.approx(75.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    (
        theta1,
        theta2,
        phi1,
        phi2,
        ipsf,
        edel,
        edeu,
        nche,
        emission_filename,
    ) = photon_detectors[8]
    assert theta1 == pytest.approx(75.0, abs=1e-5)
    assert theta2 == pytest.approx(85.0, abs=1e-5)
    assert phi1 == pytest.approx(0.0, abs=1e-5)
    assert phi2 == pytest.approx(360.0, abs=1e-5)
    assert ipsf == 0
    assert edel == pytest.approx(0.0, abs=1e-5)
    assert edeu == pytest.approx(0.0, abs=1e-5)
    assert nche == 1000
    assert emission_filename is None

    xl, xu, ndbx = input.GRIDX.get()
    assert xl == pytest.approx(-1e-5, abs=1e-5)
    assert xu == pytest.approx(5e-5, abs=1e-5)
    assert ndbx == 60

    yl, yu, ndby = input.GRIDY.get()
    assert yl == pytest.approx(-3e-5, abs=1e-5)
    assert yu == pytest.approx(3e-5, abs=1e-5)
    assert ndby == 60

    zl, zu, ndbz = input.GRIDZ.get()
    assert zl == pytest.approx(-6e-5, abs=1e-5)
    assert zu == pytest.approx(0.0, abs=1e-5)
    assert ndbz == 60

    (xrlines,) = input.XRLINE.get()
    assert len(xrlines) == 2

    (izs1s200,) = xrlines[0]
    assert izs1s200 == 26010300

    (izs1s200,) = xrlines[1]
    assert izs1s200 == 29010300

    (filename,) = input.RESUME.get()
    assert filename == "dump2.dat"

    (filename,) = input.DUMPTO.get()
    assert filename == "dump2.dat"

    (dumpp,) = input.DUMPP.get()
    assert dumpp == pytest.approx(60.0, abs=1e-5)

    seed1, seed2 = input.RSEED.get()
    assert seed1 == -10
    assert seed2 == 1

    izs1s200, idet, tol = input.REFLIN.get()
    assert izs1s200 == 26010300
    assert idet == 1
    assert tol == pytest.approx(1.5e-3, abs=1e-5)

    (dshn,) = input.NSIMSH.get()
    assert dshn == pytest.approx(2e9, abs=1e-5)

    (timea,) = input.TIME.get()
    assert timea == pytest.approx(2e9, abs=1e-5)


def test_epma1_skeleton():
    input = create_epma1()
    _test_epma1(input)


def test_epma1_write():
    input = create_epma1()
    input = _write_read_input(input)
    _test_epma1(input)


def test_epma1_read(testdatadir):
    filepath = testdatadir.joinpath("penepma", "epma1.in")
    input = PenepmaInput()
    with open(filepath, "r") as fp:
        input.read(fp)
    _test_epma1(input)


def test_epma2_skeleton():
    input = create_epma2()
    _test_epma2(input)


def test_epma2_write():
    input = create_epma2()
    input = _write_read_input(input)
    _test_epma2(input)


def test_epma2_read(testdatadir):
    filepath = testdatadir.joinpath("penepma", "epma2.in")
    input = PenepmaInput()
    with open(filepath, "r") as fp:
        input.read(fp)
    _test_epma2(input)
