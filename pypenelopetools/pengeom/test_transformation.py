#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.transformation import Rotation, Shift, Scale

# Globals and constants variables.

class TestRotation(unittest.TestCase):

    GEOFILE = ['  OMEGA=(+1.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '  THETA=(+2.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '    PHI=(+3.000000000000000E+00,   0) DEG          (DEFAULT=0.0)']

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.rotation = Rotation(1.0, 2.0, 3.0)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertAlmostEqual(1.0, self.rotation.omega_deg, 4)
        self.assertAlmostEqual(2.0, self.rotation.theta_deg, 4)
        self.assertAlmostEqual(3.0, self.rotation.phi_deg, 4)

    def testto_geo(self):
        lines = self.rotation.to_geo({})
        self.assertEqual(3, len(lines))
        self.assertEqual(self.GEOFILE, lines)

class TestShift(unittest.TestCase):
    GEOFILE = ['X-SHIFT=(+1.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Y-SHIFT=(+2.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Z-SHIFT=(+3.000000000000000E+00,   0)              (DEFAULT=0.0)']

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.shift = Shift(1.0, 2.0, 3.0)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertAlmostEqual(1.0, self.shift.x_cm, 4)
        self.assertAlmostEqual(2.0, self.shift.y_cm, 4)
        self.assertAlmostEqual(3.0, self.shift.z_cm, 4)

    def testto_geo(self):
        lines = self.shift.to_geo({})
        self.assertEqual(3, len(lines))
        self.assertEqual(self.GEOFILE, lines)

class TestScale(unittest.TestCase):
    GEOFILE = ['X-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Y-SCALE=(+2.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Z-SCALE=(+3.000000000000000E+00,   0)              (DEFAULT=1.0)']

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.scale = Scale(1.0, 2.0, 3.0)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertAlmostEqual(1.0, self.scale.x, 4)
        self.assertAlmostEqual(2.0, self.scale.y, 4)
        self.assertAlmostEqual(3.0, self.scale.z, 4)

    def testto_geo(self):
        lines = self.scale.to_geo({})
        self.assertEqual(3, len(lines))
        self.assertEqual(self.GEOFILE, lines)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
