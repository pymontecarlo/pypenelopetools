""""""

# Standard library modules.
from pathlib import Path

# Third party modules.
import pytest

# Local modules.

# Globals and constants variables.


@pytest.fixture
def testdatadir():
    return Path(__file__).parent.joinpath("testdata").resolve()
