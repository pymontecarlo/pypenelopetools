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
from pypenelopetools.penmain.test_input import create_example1_disc, create_example2_plane

# Globals and constants variables.
CONFIG = get_configuration(develop=True)

@unittest.skipUnless(CONFIG.has_program('penmain', '2014'), "no penmain program")
@unittest.skipUnless(CONFIG.has_program('material', '2014'), "no material program")
class TestPenmain2014Program(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.outdirpath = tempfile.mkdtemp()
        self.program = CONFIG.get_program('penmain', '2014')

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

        self.assertIn('geometry.rep', dircontent)
        self.assertIn('material.dat', dircontent)
        self.assertIn('penmain.dat', dircontent)
        self.assertIn('penmain-res.dat', dircontent)

    def test_example1_disc(self):
        input, geometry = create_example1_disc()
        self._run(input, geometry)
        self._test(input, geometry)

    def test_example2_plane(self):
        input, geometry = create_example2_plane()
        self._run(input, geometry)
        self._test(input, geometry)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
