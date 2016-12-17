#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
from math import radians

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.surface import SurfaceImplicit, SurfaceReduced

# Globals and constants variables.

class TestSurfaceImplicit(unittest.TestCase):

    GEOFILE = ['SURFACE (   1) surface',
               'INDICES=( 0, 0, 0, 0, 0)',
               '    AXX=(+1.000000000000000E+03,   0)              (DEFAULT=0.0)',
               '    AXY=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '    AXZ=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '    AYY=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '    AYZ=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '    AZZ=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '     AX=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '     AY=(+1.000000000000000E+09,   0)              (DEFAULT=0.0)',
               '     AZ=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '     A0=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '1111111111111111111111111111111111111111111111111111111111111111',
               '  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '    PHI=(+1.800000000000000E+02,   0) DEG          (DEFAULT=0.0)',
               'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Z-SHIFT=(-1.000000000000000E+05,   0)              (DEFAULT=0.0)']

    def setUp(self):
        unittest.TestCase.setUp(self)

        coefficients = (1e3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1e9, 0.0, 0.0)
        self.surface = SurfaceImplicit(coefficients, description='surface')
        self.surface.rotation.phi_rad = radians(180)
        self.surface.shift.z_m = -1e3

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual('surface', self.surface.description)
        self.assertAlmostEqual(radians(180), self.surface.rotation.phi_rad, 4)
        self.assertAlmostEqual(-1e3, self.surface.shift.z_m, 4)
        self.assertAlmostEqual(1e3, self.surface.coefficients['xx'], 4)
        self.assertAlmostEqual(0.0, self.surface.coefficients['xy'], 4)
        self.assertAlmostEqual(0.0, self.surface.coefficients['xz'], 4)
        self.assertAlmostEqual(0.0, self.surface.coefficients['yy'], 4)
        self.assertAlmostEqual(0.0, self.surface.coefficients['yz'], 4)
        self.assertAlmostEqual(0.0, self.surface.coefficients['zz'], 4)
        self.assertAlmostEqual(0.0, self.surface.coefficients['x'], 4)
        self.assertAlmostEqual(1e9, self.surface.coefficients['y'], 4)
        self.assertAlmostEqual(0.0, self.surface.coefficients['z'], 4)
        self.assertAlmostEqual(0.0, self.surface.coefficients['0'], 4)

    def testto_geo(self):
        lines = self.surface.to_geo({self.surface: 0})
        self.assertEqual(19, len(lines))
        self.assertEqual(self.GEOFILE, lines)

class TestSurfaceReduced(unittest.TestCase):

    GEOFILE = ['SURFACE (   1) surface',
               'INDICES=( 1, 1, 1, 0,-1)',
               'X-SCALE=(+3.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Y-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Z-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               '  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)']

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.surface = SurfaceReduced((1, 1, 1, 0, -1), 'surface')
        self.surface.scale.x = 3.0

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual((1, 1, 1, 0, -1), self.surface.indices)
        self.assertEqual('surface', self.surface.description)
        self.assertAlmostEqual(3.0, self.surface.scale.x, 4)

    def testto_geo(self):
        lines = self.surface.to_geo({self.surface: 0})
        self.assertEqual(11, len(lines))
        self.assertEqual(self.GEOFILE, lines)
if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
