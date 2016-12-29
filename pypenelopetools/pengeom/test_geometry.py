#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.geometry import Geometry
from pypenelopetools.pengeom.surface import zplane, cylinder, xplane
from pypenelopetools.pengeom.module import Module, SIDEPOINTER_NEGATIVE, SIDEPOINTER_POSITIVE
from pypenelopetools.material.material import Material

# Globals and constants variables.

class TestGeometry(unittest.TestCase):

    GEOFILE = ['XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
               '       Test Geometry',
               '0000000000000000000000000000000000000000000000000000000000000000',
               'SURFACE (   1) Plane Z=0.00 m',
               'INDICES=( 0, 0, 0, 1, 0)',
               'X-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Y-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Z-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               '  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Z-SHIFT=(+1.000000000000000E-08,   0)              (DEFAULT=0.0)',
               '0000000000000000000000000000000000000000000000000000000000000000',
               'SURFACE (   2) Cylinder of radius 0.01 m along z-axis',
               'INDICES=( 1, 1, 0, 0,-1)',
               'X-SCALE=(+1.000000000000000E-02,   0)              (DEFAULT=1.0)',
               'Y-SCALE=(+1.000000000000000E-02,   0)              (DEFAULT=1.0)',
               'Z-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               '  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '0000000000000000000000000000000000000000000000000000000000000000',
               'SURFACE (   3) Plane Z=-0.00 m',
               'INDICES=( 0, 0, 0, 1, 0)',
               'X-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Y-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Z-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               '  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Z-SHIFT=(-1.000000000000000E-01,   0)              (DEFAULT=0.0)',
               '0000000000000000000000000000000000000000000000000000000000000000',
               'SURFACE (   4) Plane X=0.00 m',
               'INDICES=( 0, 0, 0, 1, 0)',
               'X-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Y-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Z-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               '  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '  THETA=(+9.000000000000000E+01,   0) DEG          (DEFAULT=0.0)',
               '    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '0000000000000000000000000000000000000000000000000000000000000000',
               'MODULE  (   1) ',
               'MATERIAL(   1)',
               'SURFACE (   1), SIDE POINTER=(-1)',
               'SURFACE (   2), SIDE POINTER=(-1)',
               'SURFACE (   3), SIDE POINTER=( 1)',
               'SURFACE (   4), SIDE POINTER=( 1)',
               '1111111111111111111111111111111111111111111111111111111111111111',
               '  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '0000000000000000000000000000000000000000000000000000000000000000',
               'MODULE  (   2) ',
               'MATERIAL(   2)',
               'SURFACE (   1), SIDE POINTER=(-1)',
               'SURFACE (   2), SIDE POINTER=(-1)',
               'SURFACE (   3), SIDE POINTER=( 1)',
               'MODULE  (   1)',
               '1111111111111111111111111111111111111111111111111111111111111111',
               '  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '0000000000000000000000000000000000000000000000000000000000000000',
               'MODULE  (   3) Extra module for rotation and tilt',
               'MATERIAL(   0)',
               'MODULE  (   2)',
               '1111111111111111111111111111111111111111111111111111111111111111',
               '  OMEGA=(+2.700000000000000E+02,   0) DEG          (DEFAULT=0.0)',
               '  THETA=(+4.500000000000000E+01,   0) DEG          (DEFAULT=0.0)',
               '    PHI=(+9.000000000000000E+01,   0) DEG          (DEFAULT=0.0)',
               'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '0000000000000000000000000000000000000000000000000000000000000000',
               'END      0000000000000000000000000000000000000000000000000000000']

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.geo = Geometry('Test Geometry')

        surface1 = zplane(1e-8)
        surface2 = zplane(-1e-1)
        surface3 = cylinder(1.0)
        surface4 = xplane(0.0)

        mat1 = Material('copper', {29: 1.0}, 8.9)
        self.module1 = Module(mat1)
        self.module1.add_surface(surface1, SIDEPOINTER_NEGATIVE)
        self.module1.add_surface(surface2, SIDEPOINTER_POSITIVE)
        self.module1.add_surface(surface3, SIDEPOINTER_NEGATIVE)
        self.module1.add_surface(surface4, SIDEPOINTER_POSITIVE)
        self.geo.add_module(self.module1)

        mat2 = Material('zinc', {30: 1.0}, 7.14)
        self.module2 = Module(mat2)
        self.module2.add_surface(surface1, SIDEPOINTER_NEGATIVE)
        self.module2.add_surface(surface2, SIDEPOINTER_POSITIVE)
        self.module2.add_surface(surface3, SIDEPOINTER_NEGATIVE)
        self.module2.add_module(self.module1)
        self.geo.add_module(self.module2)

        self.geo.tilt_deg = 45

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual('Test Geometry', self.geo.title)
        self.assertAlmostEqual(45, self.geo.tilt_deg, 4)
        self.assertAlmostEqual(0.0, self.geo.rotation_deg, 4)
        self.assertEqual(2, len(self.geo.get_modules()))
        self.assertEqual(4, len(self.geo.get_surfaces()))
        self.assertEqual(2, len(self.geo.get_materials()))

    def testto_geo(self):
        index_table = self.geo.indexify()
        lines = self.geo.to_geo(index_table)
        self.assertEqual(self.GEOFILE[:3], lines[:3])
        self.assertEqual(self.GEOFILE[14], lines[14])
        self.assertEqual(self.GEOFILE[26], lines[26])
        self.assertEqual(self.GEOFILE[38], lines[38])
        self.assertEqual(self.GEOFILE[50], lines[50])
        self.assertEqual(self.GEOFILE[51], lines[51])
        self.assertEqual(self.GEOFILE[57:65], lines[57:65])
        self.assertEqual(self.GEOFILE[65], lines[65])
        self.assertEqual(self.GEOFILE[71:], lines[71:])

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
