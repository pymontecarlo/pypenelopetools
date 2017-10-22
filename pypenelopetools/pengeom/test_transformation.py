#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import os
import io

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.transformation import Rotation, Shift, Scale
from pypenelopetools.pengeom.base import LINE_SEPARATOR

# Globals and constants variables.

class TestRotation(unittest.TestCase):

    LINES = ['  OMEGA=(+1.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
             '  THETA=(+2.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
             '    PHI=(+3.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
             '0000000000000000000000000000000000000000000000000000000000000000']

    def setUp(self):
        super().setUp()

        self.rotation = Rotation(1.0, 2.0, 3.0)

    def _test_rotation(self, rotation):
        self.assertAlmostEqual(1.0, rotation.omega_deg, 4)
        self.assertAlmostEqual(2.0, rotation.theta_deg, 4)
        self.assertAlmostEqual(3.0, rotation.phi_deg, 4)

    def testskeleton(self):
        self._test_rotation(self.rotation)

    def test_write_read(self):
        fileobj = io.StringIO()

        try:
            self.rotation._write(fileobj, {})
            fileobj.write(LINE_SEPARATOR + os.linesep)

            lines = fileobj.getvalue().splitlines()
            self.assertListEqual(self.LINES, lines)

            fileobj.seek(0)
            rotation = Rotation()
            rotation._read(fileobj, {}, {}, {})
            self._test_rotation(rotation)
        finally:
            fileobj.close()

class TestShift(unittest.TestCase):

    LINES = ['X-SHIFT=(+1.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Y-SHIFT=(+2.000000000000000E+00,   0)              (DEFAULT=0.0)',
               'Z-SHIFT=(+3.000000000000000E+00,   0)              (DEFAULT=0.0)',
               '0000000000000000000000000000000000000000000000000000000000000000']

    def setUp(self):
        super().setUp()

        self.shift = Shift(1.0, 2.0, 3.0)

    def _test_shift(self, shift):
        self.assertAlmostEqual(1.0, shift.x_cm, 4)
        self.assertAlmostEqual(2.0, shift.y_cm, 4)
        self.assertAlmostEqual(3.0, shift.z_cm, 4)

    def testskeleton(self):
        self._test_shift(self.shift)

    def test_write_read(self):
        fileobj = io.StringIO()

        try:
            self.shift._write(fileobj, {})
            fileobj.write(LINE_SEPARATOR + os.linesep)

            lines = fileobj.getvalue().splitlines()
            self.assertListEqual(self.LINES, lines)

            fileobj.seek(0)
            shift = Shift()
            shift._read(fileobj, {}, {}, {})
            self._test_shift(shift)
        finally:
            fileobj.close()

class TestScale(unittest.TestCase):

    LINES = ['X-SCALE=(+1.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Y-SCALE=(+2.000000000000000E+00,   0)              (DEFAULT=1.0)',
               'Z-SCALE=(+3.000000000000000E+00,   0)              (DEFAULT=1.0)',
               '0000000000000000000000000000000000000000000000000000000000000000']

    def setUp(self):
        super().setUp()

        self.scale = Scale(1.0, 2.0, 3.0)

    def _test_scale(self, scale):
        self.assertAlmostEqual(1.0, scale.x, 4)
        self.assertAlmostEqual(2.0, scale.y, 4)
        self.assertAlmostEqual(3.0, scale.z, 4)

    def testskeleton(self):
        self._test_scale(self.scale)

    def test_write_read(self):
        fileobj = io.StringIO()

        try:
            self.scale._write(fileobj, {})
            fileobj.write(LINE_SEPARATOR + os.linesep)

            lines = fileobj.getvalue().splitlines()
            self.assertListEqual(self.LINES, lines)

            fileobj.seek(0)
            scale = Scale()
            scale._read(fileobj, {}, {}, {})
            self._test_scale(scale)
        finally:
            fileobj.close()

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
