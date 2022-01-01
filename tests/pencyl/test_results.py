""" """

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
from pypenelopetools.penelope.enums import KPAR
from pypenelopetools.pencyl.results import PencylResult

# Globals and constants variables.


def _test_result(result):
    assert result.simulation_time_s.n == pytest.approx(1.048234e3, abs=1e-8)
    assert result.simulation_time_s.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.simulation_speed_1_per_s.n == pytest.approx(2.285416e3, abs=1e-8)
    assert result.simulation_speed_1_per_s.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.simulated_primary_showers.n == pytest.approx(2.395652e6, abs=1e-8)
    assert result.simulated_primary_showers.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.primary_particle == KPAR.ELECTRON

    assert result.upbound_primary_particles.n == pytest.approx(0.0, abs=1e-8)
    assert result.upbound_primary_particles.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.downbound_primary_particles.n == pytest.approx(7.273540e5, abs=1e-8)
    assert result.downbound_primary_particles.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.absorbed_primary_particles.n == pytest.approx(1.668298e6, abs=1e-8)
    assert result.absorbed_primary_particles.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.upbound_fraction.n == pytest.approx(0.0, abs=1e-8)
    assert result.upbound_fraction.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.downbound_fraction.n == pytest.approx(3.130722e-1, abs=1e-8)
    assert result.downbound_fraction.s * 3 == pytest.approx(1.1e-3, abs=1e-8)

    assert result.absorbed_fraction.n == pytest.approx(6.963858e-1, abs=1e-8)
    assert result.absorbed_fraction.s * 3 == pytest.approx(8.9e-4, abs=1e-8)

    assert result.upbound_secondary_electron_generation_probabilities.n == pytest.approx(0.0, abs=1e-8)
    assert result.upbound_secondary_electron_generation_probabilities.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.downbound_secondary_electron_generation_probabilities.n == pytest.approx(9.457968e-3, abs=1e-8)
    assert result.downbound_secondary_electron_generation_probabilities.s * 3 == pytest.approx(1.9e-4, abs=1e-8)

    assert result.absorbed_secondary_electron_generation_probabilities.n == pytest.approx(3.509834, abs=1e-8)
    assert result.absorbed_secondary_electron_generation_probabilities.s * 3 == pytest.approx(4.1e-3, abs=1e-8)

    assert result.upbound_secondary_photon_generation_probabilities.n == pytest.approx(2.629764e-4, abs=1e-8)
    assert result.upbound_secondary_photon_generation_probabilities.s * 3 == pytest.approx(3.1e-5, abs=1e-8)

    assert result.downbound_secondary_photon_generation_probabilities.n == pytest.approx(4.481035e-3, abs=1e-8)
    assert result.downbound_secondary_photon_generation_probabilities.s * 3 == pytest.approx(1.3e-4, abs=1e-8)

    assert result.absorbed_secondary_photon_generation_probabilities.n == pytest.approx(1.109468e-2, abs=1e-8)
    assert result.absorbed_secondary_photon_generation_probabilities.s * 3 == pytest.approx(2.1e-4, abs=1e-8)

    assert result.upbound_secondary_positron_generation_probabilities.n == pytest.approx(0.0, abs=1e-8)
    assert result.upbound_secondary_positron_generation_probabilities.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.downbound_secondary_positron_generation_probabilities.n == pytest.approx(0.0, abs=1e-8)
    assert result.downbound_secondary_positron_generation_probabilities.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.absorbed_secondary_positron_generation_probabilities.n == pytest.approx(0.0, abs=1e-8)
    assert result.absorbed_secondary_positron_generation_probabilities.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert len(result.average_body_deposited_energy_eV) == 1
    assert 1 in result.average_body_deposited_energy_eV
    assert result.average_body_deposited_energy_eV[1].n == pytest.approx(3.135554e4, abs=1e-8)
    assert result.average_body_deposited_energy_eV[1].s * 3 == pytest.approx(2.7e1, abs=1e-8)

    assert len(result.average_detector_deposited_energy_eV) == 1
    assert 1 in result.average_detector_deposited_energy_eV
    assert result.average_detector_deposited_energy_eV[1].n == pytest.approx(3.135554e4, abs=1e-8)
    assert result.average_detector_deposited_energy_eV[1].s * 3 == pytest.approx(2.7e1, abs=1e-8)

    assert result.last_random_seed1.n == pytest.approx(539670842, abs=1e-8)
    assert result.last_random_seed1.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.last_random_seed2.n == pytest.approx(1065652462, abs=1e-8)
    assert result.last_random_seed2.s * 3 == pytest.approx(0.0, abs=1e-8)


def testread(testdatadir):
    filepath = testdatadir.joinpath("pencyl", "1-disc", "pencyl-res.dat")
    result = PencylResult()

    with open(filepath, "r") as fp:
        result.read(fp)
    _test_result(result)


def testread_directory(testdatadir):
    dirpath = testdatadir.joinpath("pencyl", "1-disc")
    result = PencylResult()
    result.read_directory(dirpath)
    _test_result(result)
