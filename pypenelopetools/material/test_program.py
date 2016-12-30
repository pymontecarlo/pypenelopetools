#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import os
import tempfile
import shutil

# Third party modules.

# Local modules.
from pypenelopetools.material.material import Material, VACUUM
from pypenelopetools.config import get_configuration

# Globals and constants variables.
CONFIG = get_configuration(develop=True)

@unittest.skipUnless(CONFIG.has_program('material', '2014'), "no material program")
class TestMaterial2014Program(unittest.TestCase):

    FIRSTLINE = " PENELOPE (v. 2014)  Material data file ..............."

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.outdirpath = tempfile.mkdtemp()
        self.program = CONFIG.get_program('material', '2014')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

        shutil.rmtree(self.outdirpath, ignore_errors=True)

    def _test_outfile(self, material):
        outfilepath = os.path.join(self.outdirpath, material.filename)
        self.assertTrue(os.path.exists(outfilepath))

        with open(outfilepath, 'r') as fp:
            firstline = fp.readline().rstrip()
        self.assertEqual(self.FIRSTLINE, firstline)

    def testsingle_element(self):
        material = Material('copper', {29: 1.0}, 8.9)

        process = self.program.execute(material, self.outdirpath)
        process.join()

        self._test_outfile(material)

    def testmulti_element(self):
        material = Material('brass', {29: 0.63, 30: 0.37}, 8.4)

        process = self.program.execute(material, self.outdirpath)
        process.join()

        self._test_outfile(material)

    def testno_element(self):
        self.assertRaises(ValueError, self.program.execute, VACUUM, self.outdirpath)

    def testexcitation_oscillator(self):
        material = Material('copper', {29: 1.0}, 8.9,
                            mean_excitation_energy_eV=300.0,
                            oscillator_strength_fcb=1.0,
                            oscillator_energy_wcb_eV=10.0)

        process = self.program.execute(material, self.outdirpath)
        process.join()

        self._test_outfile(material)


if __name__ == '__main__': #pragma: no cover
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
