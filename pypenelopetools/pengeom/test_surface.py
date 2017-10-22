#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import io

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.surface import SurfaceImplicit, SurfaceReduced

# Globals and constants variables.

class TestSurfaceImplicit(unittest.TestCase):

    LINES = ['SURFACE (   1) surface',
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
               'Z-SHIFT=(-1.000000000000000E+05,   0)              (DEFAULT=0.0)',
               '0000000000000000000000000000000000000000000000000000000000000000']

    def setUp(self):
        super().setUp()

        coefficients = (1e3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1e9, 0.0, 0.0)
        self.surface = SurfaceImplicit(coefficients, description='surface')
        self.surface.rotation.phi_deg = 180
        self.surface.shift.z_cm = -1e5

    def _test_surface(self, surface):
        self.assertEqual('surface', surface.description)
        self.assertAlmostEqual(180, surface.rotation.phi_deg, 4)
        self.assertAlmostEqual(-1e5, surface.shift.z_cm, 4)
        self.assertAlmostEqual(1e3, surface.coefficients['xx'], 4)
        self.assertAlmostEqual(0.0, surface.coefficients['xy'], 4)
        self.assertAlmostEqual(0.0, surface.coefficients['xz'], 4)
        self.assertAlmostEqual(0.0, surface.coefficients['yy'], 4)
        self.assertAlmostEqual(0.0, surface.coefficients['yz'], 4)
        self.assertAlmostEqual(0.0, surface.coefficients['zz'], 4)
        self.assertAlmostEqual(0.0, surface.coefficients['x'], 4)
        self.assertAlmostEqual(1e9, surface.coefficients['y'], 4)
        self.assertAlmostEqual(0.0, surface.coefficients['z'], 4)
        self.assertAlmostEqual(0.0, surface.coefficients['0'], 4)

    def testskeleton(self):
        self._test_surface(self.surface)

    def test_write_read(self):
        fileobj = io.StringIO()

        try:
            self.surface._write(fileobj, {self.surface: 1})

            lines = fileobj.getvalue().splitlines()
            self.assertListEqual(self.LINES, lines)

            fileobj.seek(0)
            surface = SurfaceImplicit()
            surface._read(fileobj, {}, {}, {})
            self._test_surface(surface)
        finally:
            fileobj.close()

class TestSurfaceReduced(unittest.TestCase):

    LINES = ['SURFACE (   1) surface',
               'INDICES=( 1, 1, 1, 0,-1)',
               'X-SCALE=(+3.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Y-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Z-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               '  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               '    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
               'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '0000000000000000000000000000000000000000000000000000000000000000']

    def setUp(self):
        super().setUp()

        self.surface = SurfaceReduced((1, 1, 1, 0, -1), 'surface')
        self.surface.scale.x = 3.0

    def _test_surface(self, surface):
        self.assertEqual((1, 1, 1, 0, -1), surface.indices)
        self.assertEqual('surface', surface.description)
        self.assertAlmostEqual(3.0, surface.scale.x, 4)

    def testskeleton(self):
        self._test_surface(self.surface)

    def test_write_read(self):
        fileobj = io.StringIO()

        try:
            self.surface._write(fileobj, {self.surface: 1})

            lines = fileobj.getvalue().splitlines()
            self.assertListEqual(self.LINES, lines)

            fileobj.seek(0)
            surface = SurfaceReduced()
            surface._read(fileobj, {}, {}, {})
            self._test_surface(surface)
        finally:
            fileobj.close()

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
