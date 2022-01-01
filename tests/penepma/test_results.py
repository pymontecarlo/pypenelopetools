""" """

# Standard library modules.

# Third party modules.
import pyxray
import pytest

# Local modules.
from pypenelopetools.penepma.results import (
    PenepmaResult,
    PenepmaEmittedIntensityResult,
    PenepmaSpectrumResult,
    PenepmaGeneratedIntensityResult,
)

# Globals and constants variables.


def _test_penepmaresult(result):
    assert result.simulation_time_s.n == pytest.approx(1.949920e2, abs=1e-8)
    assert result.simulation_time_s.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.simulation_speed_1_per_s.n == pytest.approx(2.291479e2, abs=1e-8)
    assert result.simulation_speed_1_per_s.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.simulated_primary_showers.n == pytest.approx(4.468200e4, abs=1e-8)
    assert result.simulated_primary_showers.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.upbound_primary_particles.n == pytest.approx(1.349200e4, abs=1e-8)
    assert result.upbound_primary_particles.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.downbound_primary_particles.n == pytest.approx(0.0, abs=1e-8)
    assert result.downbound_primary_particles.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.absorbed_primary_particles.n == pytest.approx(3.119000e4, abs=1e-8)
    assert result.absorbed_primary_particles.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.upbound_fraction.n == pytest.approx(3.117275e-1, abs=1e-8)
    assert result.upbound_fraction.s * 3 == pytest.approx(7.9e-3, abs=1e-8)

    assert result.downbound_fraction.n == pytest.approx(0.0, abs=1e-8)
    assert result.downbound_fraction.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.absorbed_fraction.n == pytest.approx(6.980440e-1, abs=1e-8)
    assert result.absorbed_fraction.s * 3 == pytest.approx(6.5e-3, abs=1e-8)

    assert (
        result.upbound_secondary_electron_generation_probabilities.n
        == pytest.approx(9.771483e-3, abs=1e-8)
    )
    assert (
        result.upbound_secondary_electron_generation_probabilities.s * 3
        == pytest.approx(1.3e-3, abs=1e-8)
    )

    assert (
        result.downbound_secondary_electron_generation_probabilities.n
        == pytest.approx(0.0, abs=1e-8)
    )
    assert (
        result.downbound_secondary_electron_generation_probabilities.s * 3
        == pytest.approx(0.0, abs=1e-8)
    )

    assert (
        result.absorbed_secondary_electron_generation_probabilities.n
        == pytest.approx(1.070119e0, abs=1e-8)
    )
    assert (
        result.absorbed_secondary_electron_generation_probabilities.s * 3
        == pytest.approx(1.4e-2, abs=1e-8)
    )

    assert result.upbound_secondary_photon_generation_probabilities.n == pytest.approx(
        8.416581e-4, abs=1e-8
    )
    assert (
        result.upbound_secondary_photon_generation_probabilities.s * 3
        == pytest.approx(9.1e-6, abs=1e-8)
    )

    assert (
        result.downbound_secondary_photon_generation_probabilities.n
        == pytest.approx(0.0, abs=1e-8)
    )
    assert (
        result.downbound_secondary_photon_generation_probabilities.s * 3
        == pytest.approx(0.0, abs=1e-8)
    )

    assert result.absorbed_secondary_photon_generation_probabilities.n == pytest.approx(
        1.975118e-3, abs=1e-8
    )
    assert (
        result.absorbed_secondary_photon_generation_probabilities.s * 3
        == pytest.approx(1.8e-5, abs=1e-8)
    )

    assert (
        result.upbound_secondary_positron_generation_probabilities.n
        == pytest.approx(0.0, abs=1e-8)
    )
    assert (
        result.upbound_secondary_positron_generation_probabilities.s * 3
        == pytest.approx(0.0, abs=1e-8)
    )

    assert (
        result.downbound_secondary_positron_generation_probabilities.n
        == pytest.approx(0.0, abs=1e-8)
    )
    assert (
        result.downbound_secondary_positron_generation_probabilities.s * 3
        == pytest.approx(0.0, abs=1e-8)
    )

    assert (
        result.absorbed_secondary_positron_generation_probabilities.n
        == pytest.approx(0.0, abs=1e-8)
    )
    assert (
        result.absorbed_secondary_positron_generation_probabilities.s * 3
        == pytest.approx(0.0, abs=1e-8)
    )

    assert len(result.average_deposited_energy_eV) == 1
    assert 2 in result.average_deposited_energy_eV
    assert result.average_deposited_energy_eV[2].n == pytest.approx(
        1.174728e4, abs=1e-8
    )
    assert result.average_deposited_energy_eV[2].s * 3 == pytest.approx(7.4e1, abs=1e-8)

    assert len(result.average_photon_energy_eV) == 9
    assert 1 in result.average_photon_energy_eV
    assert result.average_photon_energy_eV[1].n == pytest.approx(4.673420e0, abs=1e-8)
    assert result.average_photon_energy_eV[1].s * 3 == pytest.approx(5.7e-2, abs=1e-8)

    assert 2 in result.average_photon_energy_eV
    assert result.average_photon_energy_eV[2].n == pytest.approx(1.466286e-1, abs=1e-8)
    assert result.average_photon_energy_eV[2].s * 3 == pytest.approx(7.4e-3, abs=1e-8)

    assert 3 in result.average_photon_energy_eV
    assert result.average_photon_energy_eV[3].n == pytest.approx(2.899320e-1, abs=1e-8)
    assert result.average_photon_energy_eV[3].s * 3 == pytest.approx(1.1e-2, abs=1e-8)

    assert 4 in result.average_photon_energy_eV
    assert result.average_photon_energy_eV[4].n == pytest.approx(4.227645e-1, abs=1e-8)
    assert result.average_photon_energy_eV[4].s * 3 == pytest.approx(1.3e-2, abs=1e-8)

    assert 5 in result.average_photon_energy_eV
    assert result.average_photon_energy_eV[5].n == pytest.approx(5.488068e-1, abs=1e-8)
    assert result.average_photon_energy_eV[5].s * 3 == pytest.approx(1.5e-2, abs=1e-8)

    assert 6 in result.average_photon_energy_eV
    assert result.average_photon_energy_eV[6].n == pytest.approx(6.711430e-1, abs=1e-8)
    assert result.average_photon_energy_eV[6].s * 3 == pytest.approx(1.7e-2, abs=1e-8)

    assert 7 in result.average_photon_energy_eV
    assert result.average_photon_energy_eV[7].n == pytest.approx(7.438198e-1, abs=1e-8)
    assert result.average_photon_energy_eV[7].s * 3 == pytest.approx(1.8e-2, abs=1e-8)

    assert 8 in result.average_photon_energy_eV
    assert result.average_photon_energy_eV[8].n == pytest.approx(7.975043e-1, abs=1e-8)
    assert result.average_photon_energy_eV[8].s * 3 == pytest.approx(1.9e-2, abs=1e-8)

    assert 9 in result.average_photon_energy_eV
    assert result.average_photon_energy_eV[9].n == pytest.approx(7.671009e-1, abs=1e-8)
    assert result.average_photon_energy_eV[9].s * 3 == pytest.approx(1.9e-2, abs=1e-8)

    assert result.last_random_seed1.n == pytest.approx(616846078, abs=1e-8)
    assert result.last_random_seed1.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.last_random_seed2.n == pytest.approx(938690756, abs=1e-8)
    assert result.last_random_seed2.s * 3 == pytest.approx(0.0, abs=1e-8)

    assert result.reference_line_uncertainty.n == pytest.approx(3.559e-2, abs=1e-8)
    assert result.reference_line_uncertainty.s * 3 == pytest.approx(0.0, abs=1e-8)


def testpenepmaresult_read(testdatadir):
    filepath = testdatadir.joinpath("penepma", "penepma-res.dat")
    result = PenepmaResult()
    with open(filepath, "r") as fp:
        result.read(fp)
    _test_penepmaresult(result)


def testpenepmaresult_read_directory(testdatadir):
    dirpath = testdatadir.joinpath("penepma")
    result = PenepmaResult()
    result.read_directory(dirpath)
    _test_penepmaresult(result)


def _test_penepmaemittedintensityresult(result):
    assert result.detector_index == 1

    assert result.theta1_deg.n == pytest.approx(0.0, abs=1e-8)
    assert result.theta1_deg.s == pytest.approx(0.0, abs=1e-8)
    assert result.theta2_deg.n == pytest.approx(90.0, abs=1e-8)
    assert result.theta2_deg.s == pytest.approx(0.0, abs=1e-8)
    assert result.phi1_deg.n == pytest.approx(0.0, abs=1e-8)
    assert result.phi1_deg.s == pytest.approx(0.0, abs=1e-8)
    assert result.phi2_deg.n == pytest.approx(360.0, abs=1e-8)
    assert result.phi2_deg.s == pytest.approx(0.0, abs=1e-8)

    assert len(result.primary_intensities_1_per_sr_electron) == 10
    assert len(result.characteristic_fluorescence_intensities_1_per_sr_electron) == 10
    assert len(result.bremsstrahlung_fluorescence_intensities_1_per_sr_electron) == 10
    assert len(result.total_fluorescence_intensities_1_per_sr_electron) == 10
    assert len(result.total_intensities_1_per_sr_electron) == 10

    cu_l1_m3 = pyxray.xray_line(29, "L1-M3")

    intensity = result.primary_intensities_1_per_sr_electron[cu_l1_m3]
    assert intensity.n == pytest.approx(1.518793e-6, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(1.28e-7, abs=1e-8)

    intensity = result.characteristic_fluorescence_intensities_1_per_sr_electron[
        cu_l1_m3
    ]
    assert intensity.n == pytest.approx(0.0, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(0.0, abs=1e-8)

    intensity = result.bremsstrahlung_fluorescence_intensities_1_per_sr_electron[
        cu_l1_m3
    ]
    assert intensity.n == pytest.approx(1.683623e-9, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(3.57e-9, abs=1e-8)

    intensity = result.total_fluorescence_intensities_1_per_sr_electron[cu_l1_m3]
    assert intensity.n == pytest.approx(1.683623e-9, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(3.57e-9, abs=1e-8)

    intensity = result.total_intensities_1_per_sr_electron[cu_l1_m3]
    assert intensity.n == pytest.approx(1.520476e-6, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(1.28e-7, abs=1e-8)

    cu_k_l3 = pyxray.xray_line(29, "K-L3")

    intensity = result.primary_intensities_1_per_sr_electron[cu_k_l3]
    assert intensity.n == pytest.approx(1.995294e-5, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(5.28e-7, abs=1e-8)

    intensity = result.characteristic_fluorescence_intensities_1_per_sr_electron[
        cu_k_l3
    ]
    assert intensity.n == pytest.approx(6.031664e-8, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(2.32e-8, abs=1e-8)

    intensity = result.bremsstrahlung_fluorescence_intensities_1_per_sr_electron[
        cu_k_l3
    ]
    assert intensity.n == pytest.approx(1.133920e-6, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(9.51e-8, abs=1e-8)

    intensity = result.total_fluorescence_intensities_1_per_sr_electron[cu_k_l3]
    assert intensity.n == pytest.approx(1.194237e-6, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(1.18e-7, abs=1e-8)

    intensity = result.total_intensities_1_per_sr_electron[cu_k_l3]
    assert intensity.n == pytest.approx(2.114718e-5, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(5.40e-7, abs=1e-8)


def testpenepmaemittedintensityresult_read(testdatadir):
    filepath = testdatadir.joinpath("penepma", "pe-intens-01.dat")
    result = PenepmaEmittedIntensityResult(1)
    with open(filepath, "r") as fp:
        result.read(fp)
    _test_penepmaemittedintensityresult(result)


def testpenepmaemittedintensityresult_read_error(testdatadir):
    result = PenepmaEmittedIntensityResult(2)
    filepath = testdatadir.joinpath("penepma", "pe-intens-01.dat")
    with open(filepath, "r") as fp, pytest.raises(IOError):
        result.read(fp)


def testpenepmaemittedintensityresult_read_directory(testdatadir):
    dirpath = testdatadir.joinpath("penepma")
    result = PenepmaEmittedIntensityResult(1)
    result.read_directory(dirpath)
    _test_penepmaemittedintensityresult(result)


def _test_penepmaspectrumresult(result):
    assert result.detector_index == 1

    assert result.theta1_deg.n == pytest.approx(0.0, abs=1e-8)
    assert result.theta1_deg.s == pytest.approx(0.0, abs=1e-8)
    assert result.theta2_deg.n == pytest.approx(90.0, abs=1e-8)
    assert result.theta2_deg.s == pytest.approx(0.0, abs=1e-8)
    assert result.phi1_deg.n == pytest.approx(0.0, abs=1e-8)
    assert result.phi1_deg.s == pytest.approx(0.0, abs=1e-8)
    assert result.phi2_deg.n == pytest.approx(360.0, abs=1e-8)
    assert result.phi2_deg.s == pytest.approx(0.0, abs=1e-8)

    assert result.energy_window_start_eV.n == pytest.approx(0.0, abs=1e-8)
    assert result.energy_window_start_eV.s == pytest.approx(0.0, abs=1e-8)
    assert result.energy_window_end_eV.n == pytest.approx(15e3, abs=1e-8)
    assert result.energy_window_end_eV.s == pytest.approx(0.0, abs=1e-8)

    assert result.channel_width_eV == pytest.approx(15.0, abs=1e-8)

    assert len(result.spectrum) == 1000

    assert result.spectrum[0, 0].n == pytest.approx(7.500001, abs=1e-8)
    assert result.spectrum[0, 0].s * 3 == pytest.approx(0.0, abs=1e-8)
    assert result.energies_eV[0] == pytest.approx(7.500001, abs=1e-8)

    assert result.spectrum[0, 1].n == pytest.approx(0.0, abs=1e-8)
    assert result.spectrum[0, 1].s * 3 == pytest.approx(0.0, abs=1e-8)
    assert result.intensities_1_per_sr_electron[0] == pytest.approx(0.0, abs=1e-8)

    assert result.spectrum[500, 0].n == pytest.approx(7.507501e3, abs=1e-8)
    assert result.spectrum[500, 0].s * 3 == pytest.approx(0.0, abs=1e-8)
    assert result.energies_eV[500] == pytest.approx(7.507501e3, abs=1e-8)

    assert result.spectrum[500, 1].n == pytest.approx(6.014721e-9, abs=1e-12)
    assert result.spectrum[500, 1].s * 3 == pytest.approx(2.163525e-9, abs=1e-12)
    assert result.intensities_1_per_sr_electron[500] == pytest.approx(
        6.014721e-9, abs=1e-12
    )


def testpenepmaspectrumresult_read(testdatadir):
    filepath = testdatadir.joinpath("penepma", "pe-spect-01.dat")
    result = PenepmaSpectrumResult(1)
    with open(filepath, "r") as fp:
        result.read(fp)
    _test_penepmaspectrumresult(result)


def testpenepmaspectrumresult_read_directory(testdatadir):
    dirpath = testdatadir.joinpath("penepma")
    result = PenepmaSpectrumResult(1)
    result.read_directory(dirpath)
    _test_penepmaspectrumresult(result)


def _test_penepmageneratedintensityresult(result):
    assert len(result.primary_intensities_1_per_sr_electron) == 10
    assert len(result.characteristic_fluorescence_intensities_1_per_sr_electron) == 10
    assert len(result.bremsstrahlung_fluorescence_intensities_1_per_sr_electron) == 10
    assert len(result.total_fluorescence_intensities_1_per_sr_electron) == 10
    assert len(result.total_intensities_1_per_sr_electron) == 10

    cu_l1_m3 = pyxray.xray_line(29, "L1-M3")

    intensity = result.primary_intensities_1_per_sr_electron[cu_l1_m3]
    assert intensity.n == pytest.approx(1.039634e-5, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(3.08e-7, abs=1e-8)

    intensity = result.characteristic_fluorescence_intensities_1_per_sr_electron[
        cu_l1_m3
    ]
    assert intensity.n == pytest.approx(7.415981e-9, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(5.74e-9, abs=1e-8)

    intensity = result.bremsstrahlung_fluorescence_intensities_1_per_sr_electron[
        cu_l1_m3
    ]
    assert intensity.n == pytest.approx(3.409337e-8, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(1.14e-8, abs=1e-8)

    intensity = result.total_fluorescence_intensities_1_per_sr_electron[cu_l1_m3]
    assert intensity.n == pytest.approx(4.150935e-8, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(1.71e-8, abs=1e-8)

    intensity = result.total_intensities_1_per_sr_electron[cu_l1_m3]
    assert intensity.n == pytest.approx(1.043785e-5, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(3.08e-7, abs=1e-8)

    cu_k_l3 = pyxray.xray_line(29, "K-L3")

    intensity = result.primary_intensities_1_per_sr_electron[cu_k_l3]
    assert intensity.n == pytest.approx(2.066530e-5, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(4.47e-7, abs=1e-8)

    intensity = result.characteristic_fluorescence_intensities_1_per_sr_electron[
        cu_k_l3
    ]
    assert intensity.n == pytest.approx(0.0, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(0.0, abs=1e-8)

    intensity = result.bremsstrahlung_fluorescence_intensities_1_per_sr_electron[
        cu_k_l3
    ]
    assert intensity.n == pytest.approx(1.504317e-6, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(8.14e-8, abs=1e-8)

    intensity = result.total_fluorescence_intensities_1_per_sr_electron[cu_k_l3]
    assert intensity.n == pytest.approx(1.504317e-6, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(8.14e-8, abs=1e-8)

    intensity = result.total_intensities_1_per_sr_electron[cu_k_l3]
    assert intensity.n == pytest.approx(2.216962e-5, abs=1e-8)
    assert intensity.s * 3 == pytest.approx(4.56e-7, abs=1e-8)


def testpenepmageneratedintensityresult_read(testdatadir):
    filepath = testdatadir.joinpath("penepma", "pe-gen-ph.dat")
    result = PenepmaGeneratedIntensityResult()
    with open(filepath, "r") as fp:
        result.read(fp)
    _test_penepmageneratedintensityresult(result)


def testpenepmageneratedintensityresult_read_directory(testdatadir):
    dirpath = testdatadir.joinpath("penepma")
    result = PenepmaGeneratedIntensityResult()
    result.read_directory(dirpath)
    _test_penepmageneratedintensityresult(result)
