""" """

# Standard library modules.
import io

# Third party modules.
import pytest

# Local modules.
from pypenelopetools.penelope.enums import KPAR, ICOL
from pypenelopetools.penmain.input import PenmainInput
from pypenelopetools.material import Material
from pypenelopetools.pengeom.surface import sphere, zplane, cylinder
from pypenelopetools.pengeom.module import Module, SidePointer
from pypenelopetools.pengeom.geometry import Geometry

# Globals and constants variables.


def create_example1_disc():
    # Create materials
    material_cu = Material("Cu", {29: 1.0}, 8.9)

    # Create geometry
    module = Module(material_cu, "Solid cylinder")
    module.add_surface(zplane(0.0), SidePointer.POSITIVE)
    module.add_surface(zplane(0.005), SidePointer.NEGATIVE)
    module.add_surface(cylinder(1.0), SidePointer.NEGATIVE)

    geometry = Geometry("A solid cylinder.")
    geometry.add_module(module)

    # Create input
    input = PenmainInput()

    input.TITLE.set("Point source and a homogeneous cylinder.")
    input.SKPAR.set(KPAR.ELECTRON)
    input.SENERG.set(40e3)
    input.SPOSIT.set(0.0, 0.0, -0.0001)
    input.SCONE.set(0.0, 0.0, 5.0)

    input.materials.add(1, material_cu.filename, 1e3, 1e3, 1e3, 0.05, 0.05, 1e3, 1e3)

    input.GEOMFN.set("disc.geo")
    input.PARINP.add(1, 0.005)
    input.PARINP.add(2, 0.01)
    input.DSMAX.add(1, 1e-4)

    input.IFORCE.add(
        1, KPAR.ELECTRON, ICOL.HARD_BREMSSTRAHLUNG_EMISSION, 2000, 0.1, 2.0
    )
    input.IFORCE.add(
        1, KPAR.ELECTRON, ICOL.INNER_SHELL_IMPACT_IONISATION, 200, 0.1, 2.0
    )
    input.IBRSPL.add(1, 2)
    input.IXRSPL.add(1, 2)

    input.NBE.set(0, 0, 100)
    input.NBANGL.set(45, 18)

    detector = input.impact_detectors.add(0.0, 0.0, 100, 0, 2)
    detector.IDBODY.add(1)

    detector = input.energy_deposition_detectors.add(0, 0, 100)
    detector.EDBODY.add(1)

    input.GRIDZ.set(0, 0.005, 100)
    input.GRIDR.set(0.01, 50)

    input.RESUME.set("dump.dat")
    input.DUMPTO.set("dump.dat")
    input.DUMPP.set(60)

    input.NSIMSH.set(2e9)
    input.TIME.set(600)

    return input


def create_example2_plane():
    # Create materials
    material_h2o = Material("H2O", {8: 0.8881, 1: 0.1119}, 1.0)

    # Create geometry
    module_detector = Module(material_h2o, "Fluence detector")
    module_detector.add_surface(sphere(2.0), SidePointer.NEGATIVE)

    module_phantom = Module(material_h2o, "Water phantom")
    module_phantom.add_surface(zplane(0.0), SidePointer.POSITIVE)
    module_phantom.add_surface(zplane(30.0), SidePointer.NEGATIVE)

    geometry = Geometry("Semi-infinite water phantom")
    geometry.add_module(module_detector)
    geometry.add_module(module_phantom)

    index_lookup = geometry.indexify()

    # Create input
    input = PenmainInput()

    input.TITLE.set("Dose in a water phantom with a spherical impact detector")
    input.SKPAR.set(KPAR.PHOTON)
    input.SENERG.set(3e7)
    input.SPOSIT.set(0.0, 0.0, -25.0)
    input.SCONE.set(0.0, 0.0, 5.0)

    input.materials.add(1, material_h2o.filename, 1e5, 1e4, 1e5, 0.05, 0.05, 5e3, 5e3)

    input.GEOMFN.set("plane.geo")

    input.NBE.set(1e5, 3e7, 100)
    input.NBANGL.set(45, 18)

    detector = input.impact_detectors.add(1e5, 0.0, 100, 0, 2)
    detector.IDBODY.add(index_lookup[module_detector])

    input.GRIDZ.set(0, 30.0, 60)
    input.GRIDR.set(30.0, 60.0)

    input.RESUME.set("dump.dat")
    input.DUMPTO.set("dump.dat")
    input.DUMPP.set(60)

    input.NSIMSH.set(1e7)
    input.TIME.set(2e9)

    return input


def _write_read_input(input):
    fileobj = io.StringIO()

    try:
        input.write(fileobj)

        fileobj.seek(0)
        outinput = PenmainInput()
        outinput.read(fileobj)
    finally:
        fileobj.close()

    return outinput


def _test_example1_disc(input):
    (kparp,) = input.SKPAR.get()
    assert kparp == KPAR.ELECTRON

    (se0,) = input.SENERG.get()
    assert se0 == pytest.approx(40e3, abs=1e-5)

    sx0, sy0, sz0 = input.SPOSIT.get()
    assert sx0 == pytest.approx(0.0, abs=1e-5)
    assert sy0 == pytest.approx(0.0, abs=1e-5)
    assert sz0 == pytest.approx(-0.0001, abs=1e-5)

    theta, phi, alpha = input.SCONE.get()
    assert theta == pytest.approx(0.0, abs=1e-5)
    assert phi == pytest.approx(0.0, abs=1e-5)
    assert alpha == pytest.approx(5.0, abs=1e-5)

    (materials,) = input.materials.get()
    assert len(materials) == 1

    filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[0]
    assert filename == "Cu.mat"
    assert eabs1 == pytest.approx(1e3, abs=1e-5)
    assert eabs2 == pytest.approx(1e3, abs=1e-5)
    assert eabs3 == pytest.approx(1e3, abs=1e-5)
    assert c1 == pytest.approx(0.05, abs=1e-5)
    assert c2 == pytest.approx(0.05, abs=1e-5)
    assert wcc == pytest.approx(1e3, abs=1e-5)
    assert wcr == pytest.approx(1e3, abs=1e-5)

    assert input.GEOMFN.get()[0] == "disc.geo"

    (parinps,) = input.PARINP.get()
    assert len(parinps) == 2

    ip, parinp = parinps[0]
    assert ip == 1
    assert parinp == pytest.approx(0.005, abs=1e-5)

    ip, parinp = parinps[1]
    assert ip == 2
    assert parinp == pytest.approx(0.01, abs=1e-5)

    (dsmaxs,) = input.DSMAX.get()
    assert len(dsmaxs) == 1

    kb, dsmax = dsmaxs[0]
    assert kb == 1
    assert dsmax == pytest.approx(1e-4, abs=1e-5)

    (iforces,) = input.IFORCE.get()
    assert len(iforces) == 2

    kb, kpar, icol, forcer, wlow, whig = iforces[0]
    assert kb == 1
    assert kpar == KPAR.ELECTRON
    assert icol == ICOL.HARD_BREMSSTRAHLUNG_EMISSION
    assert forcer == pytest.approx(2000, abs=1e-5)
    assert wlow == pytest.approx(0.1, abs=1e-5)
    assert whig == pytest.approx(2.0, abs=1e-5)

    kb, kpar, icol, forcer, wlow, whig = iforces[1]
    assert kb == 1
    assert kpar == KPAR.ELECTRON
    assert icol == ICOL.INNER_SHELL_IMPACT_IONISATION
    assert forcer == pytest.approx(200, abs=1e-5)
    assert wlow == pytest.approx(0.1, abs=1e-5)
    assert whig == pytest.approx(2.0, abs=1e-5)

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
    assert nbe == 100

    nbth, nbph = input.NBANGL.get()
    assert nbth == 45
    assert nbph == 18

    (impact_detectors,) = input.impact_detectors.get()
    assert len(impact_detectors) == 1

    (
        el,
        eu,
        nbe,
        ipsf,
        idcut,
        spectrum_filename,
        psf_filename,
        fln_filename,
        agel,
        ageu,
        nage,
        age_filename,
        kbs,
        kpars,
    ) = impact_detectors[0]
    assert el == pytest.approx(0.0, abs=1e-5)
    assert eu == pytest.approx(0.0, abs=1e-5)
    assert nbe == 100
    assert ipsf == 0
    assert idcut == 2
    assert spectrum_filename is None
    assert psf_filename is None
    assert fln_filename is None
    assert agel is None
    assert ageu is None
    assert nage is None
    assert age_filename is None
    assert len(kbs) == 1
    assert len(kpars) == 0

    (energy_deposition_detectors,) = input.energy_deposition_detectors.get()
    assert len(energy_deposition_detectors) == 1

    el, eu, nbe, spectrum_filename, kbs = energy_deposition_detectors[0]
    assert el == pytest.approx(0.0, abs=1e-5)
    assert eu == pytest.approx(0.0, abs=1e-5)
    assert nbe == 100
    assert spectrum_filename is None
    assert len(kbs) == 1

    zl, zu, ndbz = input.GRIDZ.get()
    assert zl == pytest.approx(0.0, abs=1e-5)
    assert zu == pytest.approx(0.005, abs=1e-5)
    assert ndbz == 100

    ru, ndbr = input.GRIDR.get()
    assert ru == pytest.approx(0.01, abs=1e-5)
    assert ndbr == 50

    (filename,) = input.RESUME.get()
    assert filename == "dump.dat"

    (filename,) = input.DUMPTO.get()
    assert filename == "dump.dat"

    (dumpp,) = input.DUMPP.get()
    assert dumpp == pytest.approx(60.0, abs=1e-5)

    (dshn,) = input.NSIMSH.get()
    assert dshn == pytest.approx(2e9, abs=1e-5)

    (timea,) = input.TIME.get()
    assert timea == pytest.approx(600.0, abs=1e-5)


def _test_example2_plane(input):
    (kparp,) = input.SKPAR.get()
    assert kparp == KPAR.PHOTON

    (se0,) = input.SENERG.get()
    assert se0 == pytest.approx(3e7, abs=1e-5)

    sx0, sy0, sz0 = input.SPOSIT.get()
    assert sx0 == pytest.approx(0.0, abs=1e-5)
    assert sy0 == pytest.approx(0.0, abs=1e-5)
    assert sz0 == pytest.approx(-25.0, abs=1e-5)

    theta, phi, alpha = input.SCONE.get()
    assert theta == pytest.approx(0.0, abs=1e-5)
    assert phi == pytest.approx(0.0, abs=1e-5)
    assert alpha == pytest.approx(5.0, abs=1e-5)

    (materials,) = input.materials.get()
    assert len(materials) == 1

    filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[0]
    assert filename == "H2O.mat"
    assert eabs1 == pytest.approx(1e5, abs=1e-5)
    assert eabs2 == pytest.approx(1e4, abs=1e-5)
    assert eabs3 == pytest.approx(1e5, abs=1e-5)
    assert c1 == pytest.approx(0.05, abs=1e-5)
    assert c2 == pytest.approx(0.05, abs=1e-5)
    assert wcc == pytest.approx(5e3, abs=1e-5)
    assert wcr == pytest.approx(5e3, abs=1e-5)

    assert input.GEOMFN.get()[0] == "plane.geo"

    el, eu, nbe = input.NBE.get()
    assert el == pytest.approx(1e5, abs=1e-5)
    assert eu == pytest.approx(3e7, abs=1e-5)
    assert nbe == 100

    nbth, nbph = input.NBANGL.get()
    assert nbth == 45
    assert nbph == 18

    (impact_detectors,) = input.impact_detectors.get()
    assert len(impact_detectors) == 1

    (
        el,
        eu,
        nbe,
        ipsf,
        idcut,
        spectrum_filename,
        psf_filename,
        fln_filename,
        agel,
        ageu,
        nage,
        age_filename,
        kbs,
        kpars,
    ) = impact_detectors[0]
    assert el == pytest.approx(1e5, abs=1e-5)
    assert eu == pytest.approx(0.0, abs=1e-5)
    assert nbe == 100
    assert ipsf == 0
    assert idcut == 2
    assert spectrum_filename is None
    assert psf_filename is None
    assert fln_filename is None
    assert agel is None
    assert ageu is None
    assert nage is None
    assert age_filename is None
    assert len(kbs) == 1
    assert len(kpars) == 0

    zl, zu, ndbz = input.GRIDZ.get()
    assert zl == pytest.approx(0.0, abs=1e-5)
    assert zu == pytest.approx(30.0, abs=1e-5)
    assert ndbz == 60

    ru, ndbr = input.GRIDR.get()
    assert ru == pytest.approx(30.0, abs=1e-5)
    assert ndbr == 60

    (filename,) = input.RESUME.get()
    assert filename == "dump.dat"

    (filename,) = input.DUMPTO.get()
    assert filename == "dump.dat"

    (dumpp,) = input.DUMPP.get()
    assert dumpp == pytest.approx(60.0, abs=1e-5)

    (dshn,) = input.NSIMSH.get()
    assert dshn == pytest.approx(1e7, abs=1e-5)

    (timea,) = input.TIME.get()
    assert timea == pytest.approx(2e9, abs=1e-5)


def test_example1_disc_write():
    input = create_example1_disc()
    input = _write_read_input(input)
    _test_example1_disc(input)


def test_example1_disc_read(testdatadir):
    filepath = testdatadir.joinpath("penmain", "1-disc", "disc.in")
    input = PenmainInput()
    with open(filepath, "r") as fp:
        input.read(fp)
    _test_example1_disc(input)


def test_example2_plane_write():
    input = create_example2_plane()
    input = _write_read_input(input)
    _test_example2_plane(input)


def test_example2_plane_read(testdatadir):
    filepath = testdatadir.joinpath("penmain", "2-plane", "plane.in")
    input = PenmainInput()
    with open(filepath, "r") as fp:
        input.read(fp)
    _test_example2_plane(input)
