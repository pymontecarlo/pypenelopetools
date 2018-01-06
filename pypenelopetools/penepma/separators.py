"""
Separators used specifically for PENEPMA.
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.separator import Separator

# Globals and constants variables.

GEOMETRY = Separator('>>>>>>>> Geometry of the sample.')
"""Section for geometry."""

PHOTON_DETECTORS = Separator('>>>>>>>> Photon detectors (up to 25 different detectors).')
"""Section for photon detector(s)."""

SPATIAL_DISTRIBUTION = Separator('>>>>>>>> Spatial distribution of events in a box.')
"""Section for spatial distribution."""
