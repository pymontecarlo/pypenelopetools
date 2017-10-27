#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import os

# Third party modules.

# Local modules.
from pypenelopetools.penepma.results import PenepmaResult

# Globals and constants variables.

class TestPenepmaResult(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.testdatadir = os.path.join(os.path.dirname(__file__), '..', 'testdata')
        self.result = PenepmaResult()

    def _test_result(self, result):
        self.assertAlmostEqual(1.949920e2, result.simulation_time_s.n, 8)
        self.assertAlmostEqual(0.0, result.simulation_time_s.s * 3, 8)

        self.assertAlmostEqual(2.291479e2, result.simulation_speed_1_per_s.n, 8)
        self.assertAlmostEqual(0.0, result.simulation_speed_1_per_s.s * 3, 8)

        self.assertAlmostEqual(4.468200e4, result.simulated_primary_showers.n, 8)
        self.assertAlmostEqual(0.0, result.simulated_primary_showers.s * 3, 8)

        self.assertAlmostEqual(1.349200e4, result.upbound_primary_particles.n, 8)
        self.assertAlmostEqual(0.0, result.upbound_primary_particles.s * 3, 8)

        self.assertAlmostEqual(0.0, result.downbound_primary_particles.n, 8)
        self.assertAlmostEqual(0.0, result.downbound_primary_particles.s * 3, 8)

        self.assertAlmostEqual(3.119000e4, result.absorbed_primary_particles.n, 8)
        self.assertAlmostEqual(0.0, result.absorbed_primary_particles.s * 3, 8)

        self.assertAlmostEqual(3.117275e-1, result.upbound_fraction.n, 8)
        self.assertAlmostEqual(7.9e-3, result.upbound_fraction.s * 3, 8)

        self.assertAlmostEqual(0.0, result.downbound_fraction.n, 8)
        self.assertAlmostEqual(0.0, result.downbound_fraction.s * 3, 8)

        self.assertAlmostEqual(6.980440e-1, result.absorbed_fraction.n, 8)
        self.assertAlmostEqual(6.5e-3, result.absorbed_fraction.s * 3, 8)

        self.assertAlmostEqual(9.771483e-3, result.upbound_secondary_electron_generation_probabilities.n, 8)
        self.assertAlmostEqual(1.3e-3, result.upbound_secondary_electron_generation_probabilities.s * 3, 8)

        self.assertAlmostEqual(0.0, result.downbound_secondary_electron_generation_probabilities.n, 8)
        self.assertAlmostEqual(0.0, result.downbound_secondary_electron_generation_probabilities.s * 3, 8)

        self.assertAlmostEqual(1.070119e0, result.absorbed_secondary_electron_generation_probabilities.n, 8)
        self.assertAlmostEqual(1.4e-2, result.absorbed_secondary_electron_generation_probabilities.s * 3, 8)

        self.assertAlmostEqual(8.416581e-4, result.upbound_secondary_photon_generation_probabilities.n, 8)
        self.assertAlmostEqual(9.1e-6, result.upbound_secondary_photon_generation_probabilities.s * 3, 8)

        self.assertAlmostEqual(0.0, result.downbound_secondary_photon_generation_probabilities.n, 8)
        self.assertAlmostEqual(0.0, result.downbound_secondary_photon_generation_probabilities.s * 3, 8)

        self.assertAlmostEqual(1.975118e-3, result.absorbed_secondary_photon_generation_probabilities.n, 8)
        self.assertAlmostEqual(1.8e-5, result.absorbed_secondary_photon_generation_probabilities.s * 3, 8)

        self.assertAlmostEqual(0.0, result.upbound_secondary_positron_generation_probabilities.n, 8)
        self.assertAlmostEqual(0.0, result.upbound_secondary_positron_generation_probabilities.s * 3, 8)

        self.assertAlmostEqual(0.0, result.downbound_secondary_positron_generation_probabilities.n, 8)
        self.assertAlmostEqual(0.0, result.downbound_secondary_positron_generation_probabilities.s * 3, 8)

        self.assertAlmostEqual(0.0, result.absorbed_secondary_positron_generation_probabilities.n, 8)
        self.assertAlmostEqual(0.0, result.absorbed_secondary_positron_generation_probabilities.s * 3, 8)

        self.assertEqual(1, len(result.average_deposited_energy_eV))
        self.assertIn(2, result.average_deposited_energy_eV)
        self.assertAlmostEqual(1.174728e4, result.average_deposited_energy_eV[2].n, 8)
        self.assertAlmostEqual(7.4e1, result.average_deposited_energy_eV[2].s * 3, 8)

        self.assertEqual(9, len(result.average_photon_energy_eV))
        self.assertIn(1, result.average_photon_energy_eV)
        self.assertAlmostEqual(4.673420e0, result.average_photon_energy_eV[1].n, 8)
        self.assertAlmostEqual(5.7e-2, result.average_photon_energy_eV[1].s * 3, 8)

        self.assertIn(2, result.average_photon_energy_eV)
        self.assertAlmostEqual(1.466286e-1, result.average_photon_energy_eV[2].n, 8)
        self.assertAlmostEqual(7.4e-3, result.average_photon_energy_eV[2].s * 3, 8)

        self.assertIn(3, result.average_photon_energy_eV)
        self.assertAlmostEqual(2.899320e-1, result.average_photon_energy_eV[3].n, 8)
        self.assertAlmostEqual(1.1e-2, result.average_photon_energy_eV[3].s * 3, 8)

        self.assertIn(4, result.average_photon_energy_eV)
        self.assertAlmostEqual(4.227645e-1, result.average_photon_energy_eV[4].n, 8)
        self.assertAlmostEqual(1.3e-2, result.average_photon_energy_eV[4].s * 3, 8)

        self.assertIn(5, result.average_photon_energy_eV)
        self.assertAlmostEqual(5.488068e-1, result.average_photon_energy_eV[5].n, 8)
        self.assertAlmostEqual(1.5e-2, result.average_photon_energy_eV[5].s * 3, 8)

        self.assertIn(6, result.average_photon_energy_eV)
        self.assertAlmostEqual(6.711430e-1, result.average_photon_energy_eV[6].n, 8)
        self.assertAlmostEqual(1.7e-2, result.average_photon_energy_eV[6].s * 3, 8)

        self.assertIn(7, result.average_photon_energy_eV)
        self.assertAlmostEqual(7.438198e-1, result.average_photon_energy_eV[7].n, 8)
        self.assertAlmostEqual(1.8e-2, result.average_photon_energy_eV[7].s * 3, 8)

        self.assertIn(8, result.average_photon_energy_eV)
        self.assertAlmostEqual(7.975043e-1, result.average_photon_energy_eV[8].n, 8)
        self.assertAlmostEqual(1.9e-2, result.average_photon_energy_eV[8].s * 3, 8)

        self.assertIn(9, result.average_photon_energy_eV)
        self.assertAlmostEqual(7.671009e-1, result.average_photon_energy_eV[9].n, 8)
        self.assertAlmostEqual(1.9e-2, result.average_photon_energy_eV[9].s * 3, 8)

        self.assertAlmostEqual(616846078, result.last_random_seed1.n, 8)
        self.assertAlmostEqual(0.0, result.last_random_seed1.s * 3, 8)

        self.assertAlmostEqual(938690756, result.last_random_seed2.n, 8)
        self.assertAlmostEqual(0.0, result.last_random_seed2.s * 3, 8)

        self.assertAlmostEqual(3.559e-2, result.reference_line_uncertainty.n, 8)
        self.assertAlmostEqual(0.0, result.reference_line_uncertainty.s * 3, 8)

    def testread(self):
        filepath = os.path.join(self.testdatadir, 'penepma', 'penepma-res.dat')
        with open(filepath, 'r') as fp:
            self.result.read(fp)
        self._test_result(self.result)

    def testread_directory(self):
        dirpath = os.path.join(self.testdatadir, 'penepma')
        self.result.read_directory(dirpath)
        self._test_result(self.result)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
