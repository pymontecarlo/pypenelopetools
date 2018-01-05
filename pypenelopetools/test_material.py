""""""

# Standard library modules.
import unittest
import logging
import os
import io

# Third party modules.

# Local modules.
from pypenelopetools.material import Material

# Globals and constants variables.

class TestMaterial(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.mat = Material('mat1', {29: 0.4, 30: 0.6}, 8.9, 326.787, 2.686, 13.496)

        self.testdatadir = os.path.join(os.path.dirname(__file__), 'testdata')

    def _test_material(self, mat):
        self.assertEqual('mat1', mat.name)
        self.assertAlmostEqual(0.4, mat.composition[29], 4)
        self.assertAlmostEqual(0.6, mat.composition[30], 4)
        self.assertAlmostEqual(8.9, mat.density_g_per_cm3, 4)
        self.assertAlmostEqual(326.787, mat.mean_excitation_energy_eV, 4)
        self.assertAlmostEqual(2.686, mat.oscillator_strength_fcb, 4)
        self.assertAlmostEqual(13.496, mat.plasmon_energy_wcb_eV, 4)

    def test__init__(self):
        self._test_material(self.mat)

    def testwriteread_input(self):
        fileobj = io.StringIO()

        try:
            self.mat.write_input(fileobj)

            fileobj.seek(0)
            mat = Material.read_input(fileobj)

            self._test_material(mat)
        finally:
            fileobj.close()

    def testread_material(self):
        filepath = os.path.join(self.testdatadir, 'material', 'mat1.mat')
        with open(filepath, 'r') as fp:
            mat = Material.read_material(fp)

        self._test_material(mat)

if __name__ == '__main__': #pragma: no cover
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
