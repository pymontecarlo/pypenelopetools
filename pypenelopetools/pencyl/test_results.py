#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import os

# Third party modules.
import pyxray

# Local modules.
from pypenelopetools.penelope.enums import KPAR
from pypenelopetools.pencyl.results import PencylResult

# Globals and constants variables.


class TestPencylResult(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.testdatadir = os.path.join(os.path.dirname(__file__), "..", "testdata")
        self.result = PencylResult()

    def _test_result(self, result):
        self.assertAlmostEqual(1.048234e3, result.simulation_time_s.n, 8)
        self.assertAlmostEqual(0.0, result.simulation_time_s.s * 3, 8)

        self.assertAlmostEqual(2.285416e3, result.simulation_speed_1_per_s.n, 8)
        self.assertAlmostEqual(0.0, result.simulation_speed_1_per_s.s * 3, 8)

        self.assertAlmostEqual(2.395652e6, result.simulated_primary_showers.n, 8)
        self.assertAlmostEqual(0.0, result.simulated_primary_showers.s * 3, 8)

        self.assertEqual(KPAR.ELECTRON, result.primary_particle)

        self.assertAlmostEqual(0.0, result.upbound_primary_particles.n, 8)
        self.assertAlmostEqual(0.0, result.upbound_primary_particles.s * 3, 8)

        self.assertAlmostEqual(7.273540e5, result.downbound_primary_particles.n, 8)
        self.assertAlmostEqual(0.0, result.downbound_primary_particles.s * 3, 8)

        self.assertAlmostEqual(1.668298e6, result.absorbed_primary_particles.n, 8)
        self.assertAlmostEqual(0.0, result.absorbed_primary_particles.s * 3, 8)

        self.assertAlmostEqual(0.0, result.upbound_fraction.n, 8)
        self.assertAlmostEqual(0.0, result.upbound_fraction.s * 3, 8)

        self.assertAlmostEqual(3.130722e-1, result.downbound_fraction.n, 8)
        self.assertAlmostEqual(1.1e-3, result.downbound_fraction.s * 3, 8)

        self.assertAlmostEqual(6.963858e-1, result.absorbed_fraction.n, 8)
        self.assertAlmostEqual(8.9e-4, result.absorbed_fraction.s * 3, 8)

        self.assertAlmostEqual(
            0.0, result.upbound_secondary_electron_generation_probabilities.n, 8
        )
        self.assertAlmostEqual(
            0.0, result.upbound_secondary_electron_generation_probabilities.s * 3, 8
        )

        self.assertAlmostEqual(
            9.457968e-3,
            result.downbound_secondary_electron_generation_probabilities.n,
            8,
        )
        self.assertAlmostEqual(
            1.9e-4,
            result.downbound_secondary_electron_generation_probabilities.s * 3,
            8,
        )

        self.assertAlmostEqual(
            3.509834, result.absorbed_secondary_electron_generation_probabilities.n, 8
        )
        self.assertAlmostEqual(
            4.1e-3, result.absorbed_secondary_electron_generation_probabilities.s * 3, 8
        )

        self.assertAlmostEqual(
            2.629764e-4, result.upbound_secondary_photon_generation_probabilities.n, 8
        )
        self.assertAlmostEqual(
            3.1e-5, result.upbound_secondary_photon_generation_probabilities.s * 3, 8
        )

        self.assertAlmostEqual(
            4.481035e-3, result.downbound_secondary_photon_generation_probabilities.n, 8
        )
        self.assertAlmostEqual(
            1.3e-4, result.downbound_secondary_photon_generation_probabilities.s * 3, 8
        )

        self.assertAlmostEqual(
            1.109468e-2, result.absorbed_secondary_photon_generation_probabilities.n, 8
        )
        self.assertAlmostEqual(
            2.1e-4, result.absorbed_secondary_photon_generation_probabilities.s * 3, 8
        )

        self.assertAlmostEqual(
            0.0, result.upbound_secondary_positron_generation_probabilities.n, 8
        )
        self.assertAlmostEqual(
            0.0, result.upbound_secondary_positron_generation_probabilities.s * 3, 8
        )

        self.assertAlmostEqual(
            0.0, result.downbound_secondary_positron_generation_probabilities.n, 8
        )
        self.assertAlmostEqual(
            0.0, result.downbound_secondary_positron_generation_probabilities.s * 3, 8
        )

        self.assertAlmostEqual(
            0.0, result.absorbed_secondary_positron_generation_probabilities.n, 8
        )
        self.assertAlmostEqual(
            0.0, result.absorbed_secondary_positron_generation_probabilities.s * 3, 8
        )

        self.assertEqual(1, len(result.average_body_deposited_energy_eV))
        self.assertIn(1, result.average_body_deposited_energy_eV)
        self.assertAlmostEqual(
            3.135554e4, result.average_body_deposited_energy_eV[1].n, 8
        )
        self.assertAlmostEqual(
            2.7e1, result.average_body_deposited_energy_eV[1].s * 3, 8
        )

        self.assertEqual(1, len(result.average_detector_deposited_energy_eV))
        self.assertIn(1, result.average_detector_deposited_energy_eV)
        self.assertAlmostEqual(
            3.135554e4, result.average_detector_deposited_energy_eV[1].n, 8
        )
        self.assertAlmostEqual(
            2.7e1, result.average_detector_deposited_energy_eV[1].s * 3, 8
        )

        self.assertAlmostEqual(539670842, result.last_random_seed1.n, 8)
        self.assertAlmostEqual(0.0, result.last_random_seed1.s * 3, 8)

        self.assertAlmostEqual(1065652462, result.last_random_seed2.n, 8)
        self.assertAlmostEqual(0.0, result.last_random_seed2.s * 3, 8)

    def testread(self):
        filepath = os.path.join(self.testdatadir, "pencyl", "1-disc", "pencyl-res.dat")
        with open(filepath, "r") as fp:
            self.result.read(fp)
        self._test_result(self.result)

    def testread_directory(self):
        dirpath = os.path.join(self.testdatadir, "pencyl", "1-disc")
        self.result.read_directory(dirpath)
        self._test_result(self.result)


if __name__ == "__main__":  # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
