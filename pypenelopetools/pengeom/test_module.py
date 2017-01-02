#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.module import Module
from pypenelopetools.pengeom.surface import SurfaceImplicit
from pypenelopetools.material.material import Material, VACUUM

# Globals and constants variables.

class TestModule(unittest.TestCase):

    GEO1 = ['MODULE  (   1) Test',
            'MATERIAL(   1)',
            'SURFACE (   1), SIDE POINTER=(-1)',
            'SURFACE (   2), SIDE POINTER=( 1)',
            'MODULE  (   2)',
            '1111111111111111111111111111111111111111111111111111111111111111',
            '  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
            '  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
            '    PHI=(+1.800000000000000E+02,   0) DEG          (DEFAULT=0.0)',
            'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
            'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
            'Z-SHIFT=(-1.000000000000000E+05,   0)              (DEFAULT=0.0)']
    GEO2 = ['MODULE  (   2) ',
            'MATERIAL(   0)',
            '1111111111111111111111111111111111111111111111111111111111111111',
            '  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
            '  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
            '    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
            'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
            'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
            'Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)']

    def setUp(self):
        unittest.TestCase.setUp(self)

        mat1 = Material('copper', {29: 1.0}, 8.9)
        mat2 = VACUUM

        surface1 = SurfaceImplicit()
        surface2 = SurfaceImplicit()

        self.module2 = Module(mat2)

        self.module1 = Module(mat1, 'Test')
        self.module1.add_surface(surface1, -1)
        self.module1.add_surface(surface2, 1)
        self.module1.add_module(self.module2)
        self.module1.rotation.phi_deg = 180
        self.module1.shift.z_cm = -1e5

        self.index_lookup = {VACUUM: 0, mat1: 1,
                             surface1: 1, surface2: 2,
                             self.module1: 1, self.module2: 2}

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        # Module 1
        self.assertEqual('copper', self.module1.material.name)
        self.assertEqual('Test', self.module1.description)
        self.assertAlmostEqual(180, self.module1.rotation.phi_deg, 4)
        self.assertAlmostEqual(-1e5, self.module1.shift.z_cm, 4)
        self.assertEqual(2, len(self.module1.get_surfaces()))
        self.assertEqual(1, len(self.module1.get_modules()))

        # Module 2
        self.assertEqual(str(VACUUM), str(self.module2.material))
        self.assertEqual(0, len(self.module2.get_surfaces()))
        self.assertEqual(0, len(self.module2.get_modules()))

    def testto_geo(self):
        # Module 1
        lines = self.module1.to_geo(self.index_lookup)
        self.assertEqual(12, len(lines))
        self.assertEqual(self.GEO1, lines)

        # Module 2
        lines = self.module2.to_geo(self.index_lookup)
        self.assertEqual(9, len(lines))
        self.assertEqual(self.GEO2, lines)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
