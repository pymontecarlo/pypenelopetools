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
from pypenelopetools.penepma.test_input import create_epma1, create_epma2

# Globals and constants variables.
CONFIG = get_configuration(develop=True)

@unittest.skipUnless(CONFIG.has_program('penepma', '2014'), "no penepma program")
@unittest.skipUnless(CONFIG.has_program('material', '2014'), "no material program")
class TestPenepma2014Program(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.outdirpath = tempfile.mkdtemp()
        self.program = CONFIG.get_program('penepma', '2014')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

        shutil.rmtree(self.outdirpath, ignore_errors=True)

    def _run(self, input, geometry):
        # Create material(s)
        material_program = CONFIG.get_program('material', '2014')

        for material in geometry.get_materials():
            process = material_program.execute(material, self.outdirpath)
            process.join()

        # Write geometry
        index_table = geometry.indexify()
        geofilename, = input.GEOMFN.get()
        geofilepath = os.path.join(self.outdirpath, geofilename)

        with open(geofilepath, 'w') as fileobj:
            fileobj.write(os.linesep.join(geometry.to_geo(index_table)))

        # Change allocated time to 1 sec
        input.TIME.set(1.0)

        # Run
        process = self.program.execute(input, index_table, self.outdirpath)
        process.join()

    def _test(self, input, geometry):
        dircontent = os.listdir(self.outdirpath)

        self.assertIn('pe-geometry.rep', dircontent)
        self.assertIn('pe-material.dat', dircontent)
        self.assertIn('penepma.dat', dircontent)
        self.assertIn('penepma-res.dat', dircontent)

    def test_epma1(self):
        input, geometry = create_epma1()
        self._run(input, geometry)
        self._test(input, geometry)

    def test_epma2(self):
        input, geometry = create_epma2()
        self._run(input, geometry)
        self._test(input, geometry)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
