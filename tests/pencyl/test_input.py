""" """

# Standard library modules.
import io

# Third party modules.
import pytest

# Local modules.
from pypenelopetools.penelope.enums import KPAR, ICOL
from pypenelopetools.pencyl.input import PencylInput
from pypenelopetools.material import Material

# Globals and constants variables.


def create_example1_disc():
    # Create materials
    material_cu = Material("Cu", {29: 1.0}, 8.9)

    # Create input
    input = PencylInput()

    input.TITLE.set("Point source and a homogeneous cylinder.")

    definition = input.geometry_definitions.add(0.0, 0.005)
    definition.CYLIND.add(1, 0, 0.01)

    input.SKPAR.set(1)
    input.SENERG.set(40e3)
    input.SPOSIT.set(0, 0, -0.0001)
    input.SCONE.set(0, 0, 5)

    input.materials.add(1, material_cu.filename, 1e3, 1e3, 1e3, 0.05, 0.05, 1e3, 1e3)

    input.DSMAX.add(1, 1, 1e-4)

    input.IFORCE.add(
        1, 1, KPAR.ELECTRON, ICOL.HARD_BREMSSTRAHLUNG_EMISSION, 2000, 0.1, 2.0
    )
    input.IFORCE.add(
        1, 1, KPAR.ELECTRON, ICOL.INNER_SHELL_IMPACT_IONISATION, 200, 0.1, 2.0
    )

    input.IBRSPL.add(1, 1, 2)

    input.IXRSPL.add(1, 1, 2)

    input.NBE.set(0, 0, 100)
    input.NBANGL.set(45, 18)

    input.EMERGP.set(0.005, 100)

    detector = input.energy_deposition_detectors.add(0, 0, 100)
    detector.EDBODY.add(1, 1)

    input.DOSE2D.add(1, 1, 100, 50)

    input.RESUME.set("dump.dat")
    input.DUMPTO.set("dump.dat")
    input.DUMPP.set(60)

    input.RSEED.set(1, 1)
    input.NSIMSH.set(1e9)
    input.TIME.set(600)

    return input


def create_example3_detector():
    # Create materials
    material_nai = Material("NaI", {11: 0.1534, 53: 0.8466}, 3.667)
    material_al2o3 = Material("Al2O3", {8: 0.4707, 13: 0.5293}, 3.97)
    material_al = Material("Al", {13: 1.0}, 2.7)
    materials = (material_nai, material_al2o3, material_al)

    # Create input
    input = PencylInput()

    input.TITLE.set("NaI detector with Al cover and Al2O3 reflecting foil")

    layer1 = input.geometry_definitions.add(-0.24, -0.16, 0.0, 0.0)
    layer1.CYLIND.add(3, 0.00, 4.05)

    layer2 = input.geometry_definitions.add(-0.16, 0.00)
    layer2.CYLIND.add(2, 0.00, 3.97)
    layer2.CYLIND.add(3, 3.97, 4.05)

    layer3 = input.geometry_definitions.add(0.00, 7.72)
    layer3.CYLIND.add(1, 0.00, 3.81)
    layer3.CYLIND.add(2, 3.81, 3.97)
    layer3.CYLIND.add(3, 3.97, 4.05)

    layer4 = input.geometry_definitions.add(7.72, 9.72)
    layer4.CYLIND.add(3, 0.00, 4.05)

    input.SKPAR.set(2)
    input.SENERG.set(9.5e6)
    input.SPOSIT.set(0, 0, -10.0)
    input.SCONE.set(0, 0, 0)

    input.materials.add(
        1, material_nai.filename, 5.0e4, 5.0e3, 5.0e4, 0.1, 0.1, 2e3, 2e3
    )
    input.materials.add(
        2, material_al2o3.filename, 5.0e4, 5.0e3, 5.0e4, 0.1, 0.1, 2e3, 2e3
    )
    input.materials.add(
        3, material_al.filename, 5.0e4, 5.0e3, 5.0e4, 0.1, 0.1, 2e3, 2e3
    )

    detector = input.energy_deposition_detectors.add(0, 1e7, 1000)
    detector.EDBODY.add(3, 1)

    input.DOSE2D.add(3, 1, 50, 50)

    input.RESUME.set("dump.dat")
    input.DUMPTO.set("dump.dat")
    input.DUMPP.set(60)

    input.NSIMSH.set(1e8)
    input.TIME.set(2e9)

    return input, materials


def _test_example1_disc(input):
    (geometry_definitions,) = input.geometry_definitions.get()
    assert len(geometry_definitions) == 1

    zlow, zhigh, xcen, ycen, cylinders = geometry_definitions[0]
    assert zlow == pytest.approx(0.0, abs=1e-5)
    assert zhigh == pytest.approx(0.005, abs=1e-5)
    assert xcen is None
    assert ycen is None
    assert len(cylinders) == 1

    material, rin, rout = cylinders[0]
    assert material == 1
    assert rin == pytest.approx(0.0, abs=1e-5)
    assert rout == pytest.approx(0.01, abs=1e-5)

    (kparp,) = input.SKPAR.get()
    assert kparp == 1

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

    (dsmaxs,) = input.DSMAX.get()
    assert len(dsmaxs) == 1

    kl, kc, dsmax = dsmaxs[0]
    assert kl == 1
    assert kc == 1
    assert dsmax == pytest.approx(1e-4, abs=1e-5)

    (iforces,) = input.IFORCE.get()
    assert len(iforces) == 2

    kl, kc, kpar, icol, forcer, wlow, whig = iforces[0]
    assert kl == 1
    assert kc == 1
    assert kpar == 1
    assert icol == 4
    assert forcer == pytest.approx(2000, abs=1e-5)
    assert wlow == pytest.approx(0.1, abs=1e-5)
    assert whig == pytest.approx(2.0, abs=1e-5)

    kl, kc, kpar, icol, forcer, wlow, whig = iforces[1]
    assert kl == 1
    assert kc == 1
    assert kpar == 1
    assert icol == 5
    assert forcer == pytest.approx(200, abs=1e-5)
    assert wlow == pytest.approx(0.1, abs=1e-5)
    assert whig == pytest.approx(2.0, abs=1e-5)

    (ibrspls,) = input.IBRSPL.get()
    assert len(ibrspls) == 1

    kl, kc, factor = ibrspls[0]
    assert kl == 1
    assert kc == 1
    assert factor == pytest.approx(2.0, abs=1e-5)

    (ixrspls,) = input.IXRSPL.get()
    assert len(ixrspls) == 1

    kl, kc, factor = ibrspls[0]
    assert kl == 1
    assert kc == 1
    assert factor == pytest.approx(2.0, abs=1e-5)

    el, eu, nbe = input.NBE.get()
    assert el == pytest.approx(0.0, abs=1e-5)
    assert eu == pytest.approx(0.0, abs=1e-5)
    assert nbe == 100

    nbth, nbph = input.NBANGL.get()
    assert nbth == 45
    assert nbph == 18

    radm, nbre = input.EMERGP.get()
    assert radm == pytest.approx(0.005, abs=1e-5)
    assert nbre == 100

    (energy_deposition_detectors,) = input.energy_deposition_detectors.get()
    assert len(energy_deposition_detectors) == 1

    el, eu, nbe, spectrum_filename, cylinders = energy_deposition_detectors[0]
    assert el == pytest.approx(0.0, abs=1e-5)
    assert eu == pytest.approx(0.0, abs=1e-5)
    assert nbe == 100
    assert spectrum_filename is None
    assert len(cylinders) == 1

    kl, kc = cylinders[0]
    assert kl == 1
    assert kc == 1

    (dose2d,) = input.DOSE2D.get()
    assert len(dose2d) == 1

    kl, kc, nz, nr = dose2d[0]
    assert kl == 1
    assert kc == 1
    assert 100 == nz
    assert 50 == nr

    (filename,) = input.RESUME.get()
    assert filename == "dump.dat"

    (filename,) = input.DUMPTO.get()
    assert filename == "dump.dat"

    (dumpp,) = input.DUMPP.get()
    assert dumpp == pytest.approx(60.0, abs=1e-5)

    seed1, seed2 = input.RSEED.get()
    assert seed1 == 1
    assert seed2 == 1

    (dshn,) = input.NSIMSH.get()
    assert dshn == pytest.approx(1e9, abs=1e-5)

    (timea,) = input.TIME.get()
    assert timea == pytest.approx(600.0, abs=1e-5)


def _test_example3_detector(input):
    (geometry_definitions,) = input.geometry_definitions.get()
    assert len(geometry_definitions) == 4

    zlow, zhigh, xcen, ycen, cylinders = geometry_definitions[0]
    assert zlow == pytest.approx(-0.24, abs=1e-5)
    assert zhigh == pytest.approx(-0.16, abs=1e-5)
    assert xcen == pytest.approx(0.0, abs=1e-5)
    assert ycen == pytest.approx(0.0, abs=1e-5)
    assert len(cylinders) == 1

    material, rin, rout = cylinders[0]
    assert material == 3
    assert rin == pytest.approx(0.0, abs=1e-5)
    assert rout == pytest.approx(4.05, abs=1e-5)

    zlow, zhigh, xcen, ycen, cylinders = geometry_definitions[1]
    assert zlow == pytest.approx(-0.16, abs=1e-5)
    assert zhigh == pytest.approx(0.0, abs=1e-5)
    assert xcen is None
    assert ycen is None
    assert len(cylinders) == 2

    material, rin, rout = cylinders[0]
    assert material == 2
    assert rin == pytest.approx(0.0, abs=1e-5)
    assert rout == pytest.approx(3.97, abs=1e-5)

    material, rin, rout = cylinders[1]
    assert material == 3
    assert rin == pytest.approx(3.97, abs=1e-5)
    assert rout == pytest.approx(4.05, abs=1e-5)

    zlow, zhigh, xcen, ycen, cylinders = geometry_definitions[2]
    assert zlow == pytest.approx(0.0, abs=1e-5)
    assert zhigh == pytest.approx(7.72, abs=1e-5)
    assert xcen is None
    assert ycen is None
    assert len(cylinders) == 3

    material, rin, rout = cylinders[0]
    assert material == 1
    assert rin == pytest.approx(0.0, abs=1e-5)
    assert rout == pytest.approx(3.81, abs=1e-5)

    material, rin, rout = cylinders[1]
    assert material == 2
    assert rin == pytest.approx(3.81, abs=1e-5)
    assert rout == pytest.approx(3.97, abs=1e-5)

    material, rin, rout = cylinders[2]
    assert material == 3
    assert rin == pytest.approx(3.97, abs=1e-5)
    assert rout == pytest.approx(4.05, abs=1e-5)

    zlow, zhigh, xcen, ycen, cylinders = geometry_definitions[3]
    assert zlow == pytest.approx(7.72, abs=1e-5)
    assert zhigh == pytest.approx(9.72, abs=1e-5)
    assert xcen is None
    assert ycen is None
    assert len(cylinders) == 1

    material, rin, rout = cylinders[0]
    assert material == 3
    assert rin == pytest.approx(0.0, abs=1e-5)
    assert rout == pytest.approx(4.05, abs=1e-5)

    (kparp,) = input.SKPAR.get()
    assert kparp == 2

    (se0,) = input.SENERG.get()
    assert se0 == pytest.approx(9.5e6, abs=1e-5)

    sx0, sy0, sz0 = input.SPOSIT.get()
    assert sx0 == pytest.approx(0.0, abs=1e-5)
    assert sy0 == pytest.approx(0.0, abs=1e-5)
    assert sz0 == pytest.approx(-10.0, abs=1e-5)

    theta, phi, alpha = input.SCONE.get()
    assert theta == pytest.approx(0.0, abs=1e-5)
    assert phi == pytest.approx(0.0, abs=1e-5)
    assert alpha == pytest.approx(0.0, abs=1e-5)
    #
    (materials,) = input.materials.get()
    assert len(materials) == 3

    filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[0]
    assert filename == "NaI.mat"
    assert eabs1 == pytest.approx(5e4, abs=1e-5)
    assert eabs2 == pytest.approx(5e3, abs=1e-5)
    assert eabs3 == pytest.approx(5e4, abs=1e-5)
    assert c1 == pytest.approx(0.1, abs=1e-5)
    assert c2 == pytest.approx(0.1, abs=1e-5)
    assert wcc == pytest.approx(2e3, abs=1e-5)
    assert wcr == pytest.approx(2e3, abs=1e-5)

    filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[1]
    assert filename == "Al2O3.mat"
    assert eabs1 == pytest.approx(5e4, abs=1e-5)
    assert eabs2 == pytest.approx(5e3, abs=1e-5)
    assert eabs3 == pytest.approx(5e4, abs=1e-5)
    assert c1 == pytest.approx(0.1, abs=1e-5)
    assert c2 == pytest.approx(0.1, abs=1e-5)
    assert wcc == pytest.approx(2e3, abs=1e-5)
    assert wcr == pytest.approx(2e3, abs=1e-5)

    filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[2]
    assert filename == "Al.mat"
    assert eabs1 == pytest.approx(5e4, abs=1e-5)
    assert eabs2 == pytest.approx(5e3, abs=1e-5)
    assert eabs3 == pytest.approx(5e4, abs=1e-5)
    assert c1 == pytest.approx(0.1, abs=1e-5)
    assert c2 == pytest.approx(0.1, abs=1e-5)
    assert wcc == pytest.approx(2e3, abs=1e-5)
    assert wcr == pytest.approx(2e3, abs=1e-5)
    #
    (energy_deposition_detectors,) = input.energy_deposition_detectors.get()
    assert len(energy_deposition_detectors) == 1

    el, eu, nbe, spectrum_filename, cylinders = energy_deposition_detectors[0]
    assert el == pytest.approx(0.0, abs=1e-5)
    assert eu == pytest.approx(1e7, abs=1e-5)
    assert nbe == 1000
    assert spectrum_filename is None
    assert len(cylinders) == 1

    kl, kc = cylinders[0]
    assert kl == 3
    assert kc == 1

    (dose2d,) = input.DOSE2D.get()
    assert len(dose2d) == 1

    kl, kc, nz, nr = dose2d[0]
    assert kl == 3
    assert kc == 1
    assert 50 == nz
    assert 50 == nr

    (filename,) = input.RESUME.get()
    assert filename == "dump.dat"

    (filename,) = input.DUMPTO.get()
    assert filename == "dump.dat"

    (dumpp,) = input.DUMPP.get()
    assert dumpp == pytest.approx(60.0, abs=1e-5)

    (dshn,) = input.NSIMSH.get()
    assert dshn == pytest.approx(1e8, abs=1e-5)

    (timea,) = input.TIME.get()
    assert timea == pytest.approx(2e9, abs=1e-5)


def _write_read_input(input):
    fileobj = io.StringIO()

    try:
        input.write(fileobj)

        fileobj.seek(0)
        outinput = PencylInput()
        outinput.read(fileobj)
    finally:
        fileobj.close()

    return outinput


def test_example1_disc_write():
    input = create_example1_disc()
    input = _write_read_input(input)
    _test_example1_disc(input)


def test_example1_disc_read(testdatadir):
    filepath = testdatadir.joinpath("pencyl", "1-disc", "disc.in")
    input = PencylInput()
    with open(filepath, "r") as fp:
        input.read(fp)
    _test_example1_disc(input)


def test_example3_detector_write():
    input, _materials = create_example3_detector()
    input = _write_read_input(input)
    _test_example3_detector(input)


def test_example3_detector_read(testdatadir):
    filepath = testdatadir.joinpath("pencyl", "3-detector", "cyld.in")
    input = PencylInput()
    with open(filepath, "r") as fp:
        input.read(fp)
    _test_example3_detector(input)
