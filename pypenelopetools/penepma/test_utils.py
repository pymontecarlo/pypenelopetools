#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.
import pyxray

# Local modules.
from pypenelopetools.penepma.utils import convert_xrayline_to_izs1s200

# Globals and constants variables.

class Testutils(unittest.TestCase):

    def testconvert_xrayline_to_izs1s200(self):
        xrayline = pyxray.xray_line(29, 'Ka2')
        izs1s200 = convert_xrayline_to_izs1s200(xrayline)
        self.assertEqual(29010300, izs1s200)

        xrayline = pyxray.xray_line(29, 'Ka')
        self.assertRaises(ValueError, convert_xrayline_to_izs1s200, xrayline)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
