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
from pypenelopetools.config import get_configuration
from pypenelopetools.pencyl.test_input import create_example1_disc, create_example3_detector

# Globals and constants variables.
CONFIG = get_configuration(develop=True)

@unittest.skipUnless(CONFIG.has_program('pencyl', '2014'), "no pencyl program")
@unittest.skipUnless(CONFIG.has_program('material', '2014'), "no material program")
class TestPenmain2014Program(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.outdirpath = tempfile.mkdtemp()
        self.program = CONFIG.get_program('pencyl', '2014')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

        shutil.rmtree(self.outdirpath, ignore_errors=True)

    def _run(self, input, materials):
        # Create material(s)
        material_program = CONFIG.get_program('material', '2014')

        for material in materials:
            process = material_program.execute(material, self.outdirpath)
            process.join()

        # Change allocated time to 1 sec
        input.TIME.set(1.0)

        # Run
        index_table = {}
        process = self.program.execute(input, index_table, self.outdirpath)
        process.join()

    def _test(self, input):
        dircontent = os.listdir(self.outdirpath)

        self.assertIn('material.dat', dircontent)
        self.assertIn('pencyl.dat', dircontent)
        self.assertIn('pencyl-res.dat', dircontent)

    def test_example1_disc(self):
        input, materials = create_example1_disc()
        self._run(input, materials)
        self._test(input)

    def test_example3_detector(self):
        input, materials = create_example3_detector()
        self._run(input, materials)
        self._test(input)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
