""""""

# Standard library modules.
import io

# Third party modules.
import pytest

# Local modules.
from pypenelopetools.material import Material

# Globals and constants variables.


@pytest.fixture
def material():
    return Material("mat1", {29: 0.4, 30: 0.6}, 8.9, 326.787, 2.686, 13.496)


def _test_material(mat):
    assert mat.name == "mat1"
    assert mat.composition[29] == pytest.approx(0.4, abs=1e-4)
    assert mat.composition[30] == pytest.approx(0.6, abs=1e-4)
    assert mat.density_g_per_cm3 == pytest.approx(8.9, abs=1e-4)
    assert mat.mean_excitation_energy_eV == pytest.approx(326.787, abs=1e-4)
    assert mat.oscillator_strength_fcb == pytest.approx(2.686, abs=1e-4)
    assert mat.plasmon_energy_wcb_eV == pytest.approx(13.496, abs=1e-4)


def testmaterial(material):
    _test_material(material)


def testwriteread_input(material):
    fileobj = io.StringIO()

    try:
        material.write_input(fileobj)

        fileobj.seek(0)
        material = Material.read_input(fileobj)

        _test_material(material)
    finally:
        fileobj.close()


def testread_material(testdatadir):
    filepath = testdatadir.joinpath("material", "mat1.mat")
    with open(filepath, "r") as fp:
        mat = Material.read_material(fp)

    _test_material(mat)
