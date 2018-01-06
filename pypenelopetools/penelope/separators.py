"""
Separators used across different PENELOPE main programs.
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.separator import Separator

# Globals and constants variables.

DOT = Separator('.')
"""Section separator."""

SOURCE_DEFINITION = Separator('>>>>>>>> Source definition.')
"""Section for source definition."""

MATERIAL = Separator('>>>>>>>> Material data and simulation parameters.')
"""Section for material(s)."""

INTERACTION_FORCING = Separator('>>>>>>>> Interaction forcing.')
"""Section for interaction forcing(s)."""

BREMSSTRAHLUNG_SPLITTING = Separator('>>>>>>>> Bremsstrahlung splitting.')
"""Section for Bremsstralung splitting."""

XRAY_SPLITTING = Separator('>>>>>>>> X-ray splitting.')
"""Section for characteristic x ray splitting."""

EMERGING_PARTICLES = Separator('>>>>>>>> Emerging particles. Energy and angular distributions.')
"""Section for emerging particles."""

ENERGY_DEPOSITON_DETECTORS = Separator('>>>>>>>> Energy-deposition detectors (up to 25).')
"""Section for energy deposition detectors."""

JOB_PROPERTIES = Separator('>>>>>>>> Job properties.')
"""Section for job properties."""

END = Separator('Ends the reading of input data', 'END')
"""End separator"""
