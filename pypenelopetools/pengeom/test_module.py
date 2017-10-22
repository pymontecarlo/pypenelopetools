#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import io

# Third party modules.

# Local modules.
from pypenelopetools.pengeom.module import Module
from pypenelopetools.pengeom.surface import SurfaceImplicit
from pypenelopetools.material import Material, VACUUM

# Globals and constants variables.

class TestModule(unittest.TestCase):

    LINES1 = ['MODULE  (   1) Test',
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
            'Z-SHIFT=(-1.000000000000000E+05,   0)              (DEFAULT=0.0)',
            '0000000000000000000000000000000000000000000000000000000000000000']
    LINES2 = ['MODULE  (   2) ',
            'MATERIAL(   0)',
            '1111111111111111111111111111111111111111111111111111111111111111',
            '  OMEGA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
            '  THETA=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
            '    PHI=(+0.000000000000000E+00,   0) DEG          (DEFAULT=0.0)',
            'X-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
            'Y-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
            'Z-SHIFT=(+0.000000000000000E+00,   0)              (DEFAULT=0.0)',
            '0000000000000000000000000000000000000000000000000000000000000000']

    def setUp(self):
        super().setUp()

        self.mat1 = Material('copper', {29: 1.0}, 8.9)

        self.surface1 = SurfaceImplicit()
        self.surface2 = SurfaceImplicit()

        self.module2 = Module(VACUUM)

        self.module1 = Module(self.mat1, 'Test')
        self.module1.add_surface(self.surface1, -1)
        self.module1.add_surface(self.surface2, 1)
        self.module1.add_module(self.module2)
        self.module1.rotation.phi_deg = 180
        self.module1.shift.z_cm = -1e5

    def _test_module1(self, module1):
        self.assertEqual('copper', module1.material.name)
        self.assertEqual('Test', module1.description)
        self.assertAlmostEqual(180, module1.rotation.phi_deg, 4)
        self.assertAlmostEqual(-1e5, module1.shift.z_cm, 4)
        self.assertEqual(2, len(module1.get_surfaces()))
        self.assertEqual(1, len(module1.get_modules()))

    def _test_module2(self, module2):
        self.assertEqual(str(VACUUM), str(module2.material))
        self.assertEqual(0, len(module2.get_surfaces()))
        self.assertEqual(0, len(module2.get_modules()))

    def testskeleton(self):
        self._test_module1(self.module1)
        self._test_module2(self.module2)

    def test_write_read(self):
        material_lookup = {0: VACUUM, 1: self.mat1}
        surface_lookup = {1: self.surface1, 2: self.surface2}
        module_lookup = {2: self.module2}
        index_lookup = {VACUUM: 0, self.mat1: 1,
                        self.surface1: 1, self.surface2: 2,
                        self.module1: 1, self.module2: 2}

        # Module 1
        fileobj = io.StringIO()

        try:
            self.module1._write(fileobj, index_lookup)

            lines = fileobj.getvalue().splitlines()
            self.assertListEqual(self.LINES1, lines)

            fileobj.seek(0)
            module = Module()
            module._read(fileobj, material_lookup, surface_lookup, module_lookup)
            self._test_module1(module)
        finally:
            fileobj.close()

        # Module 2
        fileobj = io.StringIO()

        try:
            self.module2._write(fileobj, index_lookup)

            lines = fileobj.getvalue().splitlines()
            self.assertListEqual(self.LINES2, lines)

            fileobj.seek(0)
            module = Module()
            module._read(fileobj, material_lookup, surface_lookup, module_lookup)
            self._test_module2(module)
        finally:
            fileobj.close()

#    def test_create_lines(self):
#        # Module 1
#        lines = self.module1._create_lines(self.index_lookup)
#        self.assertEqual(12, len(lines))
#        self.assertEqual(self.LINES1, lines)
#
#        # Module 2
#        lines = self.module2._create_lines(self.index_lookup)
#        self.assertEqual(9, len(lines))
#        self.assertEqual(self.LINES2, lines)
#
#    def test_parse_lines(self):

#
#        module1 = Module._parse_lines(self.LINES1, material_lookup, surface_lookup, module_lookup)
#        self._test_module1(module1)
#
#        module2 = Module._parse_lines(self.LINES2, material_lookup, surface_lookup, module_lookup)
#        self._test_module2(module2)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
