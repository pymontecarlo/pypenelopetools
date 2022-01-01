""" """

# Standard library modules.

# Third party modules.
import pyxray
import pytest

# Local modules.
from pypenelopetools.penepma.utils import convert_xrayline_to_izs1s200

# Globals and constants variables.


def testconvert_xrayline_to_izs1s200():
    xrayline = pyxray.xray_line(29, "Ka2")
    izs1s200 = convert_xrayline_to_izs1s200(xrayline)
    assert izs1s200 == 29010300


def testconvert_xrayline_to_izs1s200_error():
    xrayline = pyxray.xray_line(29, "Ka")
    with pytest.raises(ValueError):
        convert_xrayline_to_izs1s200(xrayline)
