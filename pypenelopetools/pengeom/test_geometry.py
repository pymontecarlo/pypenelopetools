#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import os
import io

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.geometry import Geometry
from pypenelopetools.pengeom.surface import zplane, cylinder, xplane
from pypenelopetools.pengeom.module import Module, SidePointer
from pypenelopetools.material import Material, VACUUM

# Globals and constants variables.

class TestGeometry(unittest.TestCase):

    LINES = ['XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
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
        super().setUp()

        self.testdatadir = os.path.join(os.path.dirname(__file__),
                                        '..', 'testdata', 'pengeom')

        self.geo = Geometry('Test Geometry')

        surface1 = zplane(1e-8)
        surface2 = zplane(-1e-1)
        surface3 = cylinder(1.0)
        surface4 = xplane(0.0)

        self.mat1 = Material('copper', {29: 1.0}, 8.9)
        self.module1 = Module(self.mat1)
        self.module1.add_surface(surface1, SidePointer.NEGATIVE)
        self.module1.add_surface(surface2, SidePointer.POSITIVE)
        self.module1.add_surface(surface3, SidePointer.NEGATIVE)
        self.module1.add_surface(surface4, SidePointer.POSITIVE)
        self.geo.add_module(self.module1)

        self.mat2 = Material('zinc', {30: 1.0}, 7.14)
        self.module2 = Module(self.mat2)
        self.module2.add_surface(surface1, SidePointer.NEGATIVE)
        self.module2.add_surface(surface2, SidePointer.POSITIVE)
        self.module2.add_surface(surface3, SidePointer.NEGATIVE)
        self.module2.add_module(self.module1)
        self.geo.add_module(self.module2)

        self.geo.tilt_deg = 45

    def _test_geometry(self, geometry):
        self.assertEqual('Test Geometry', geometry.title)
        self.assertEqual(3, len(geometry.get_modules()))
        self.assertEqual(4, len(geometry.get_surfaces()))
        self.assertEqual(2, len(geometry.get_materials()))

    def testskeleton(self):
        self.assertEqual('Test Geometry', self.geo.title)
        self.assertEqual(2, len(self.geo.get_modules()))
        self.assertEqual(4, len(self.geo.get_surfaces()))
        self.assertEqual(2, len(self.geo.get_materials()))
        self.assertAlmostEqual(45, self.geo.tilt_deg, 4)
        self.assertAlmostEqual(0.0, self.geo.rotation_deg, 4)

    def testindexify(self):
        index_lookup = self.geo.indexify()

        # 4 surfaces, 2 materials, 2 modules, 1 extra module
        self.assertEqual(4 + 2 + 2 + 1, len(index_lookup))

        index_lookup2 = self.geo.indexify()
        self.assertDictEqual(index_lookup, index_lookup2)

    def testwriteread(self):
        material_lookup = {0: VACUUM, 1: self.mat1, 2: self.mat2}
        fileobj = io.StringIO()

        try:
            self.geo.write(fileobj)

            fileobj.seek(0)
            lines = fileobj.getvalue().splitlines()
            self.assertListEqual(self.LINES[:3], lines[:3])
            self.assertEqual(self.LINES[14], lines[14])
            self.assertEqual(self.LINES[26], lines[26])
            self.assertEqual(self.LINES[38], lines[38])
            self.assertEqual(self.LINES[50], lines[50])
            self.assertEqual(self.LINES[51], lines[51])
            self.assertListEqual(self.LINES[57:65], lines[57:65])
            self.assertEqual(self.LINES[65], lines[65])
            self.assertListEqual(self.LINES[71:], lines[71:])

            fileobj.seek(0)
            geometry = Geometry()
            geometry.read(fileobj, material_lookup)

            self._test_geometry(geometry)

            index_lookup = geometry.indexify()
            self.assertEqual(4 + 3 + 3, len(index_lookup))
        finally:
            fileobj.close()

    def test_epma1_read(self):
        material_lookup = {1: self.mat1}

        filepath = os.path.join(self.testdatadir, 'epma1.geo')
        geometry = Geometry()
        with open(filepath, 'r') as fp:
            geometry.read(fp, material_lookup)

        self.assertEqual('Cylindrical homogeneous foil', geometry.title)
        self.assertEqual(3, len(geometry.get_surfaces()))
        self.assertEqual(1, len(geometry.get_modules()))
        self.assertEqual(1, len(geometry.get_materials()))

    def test_epma2_read(self):
        material_lookup = {1: self.mat1, 2: self.mat2}

        filepath = os.path.join(self.testdatadir, 'epma2.geo')
        geometry = Geometry()
        with open(filepath, 'r') as fp:
            geometry.read(fp, material_lookup)

        self.assertEqual('Cylindrical foil with a material couple', geometry.title)
        self.assertEqual(4, len(geometry.get_surfaces()))
        self.assertEqual(2, len(geometry.get_modules()))
        self.assertEqual(2, len(geometry.get_materials()))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
