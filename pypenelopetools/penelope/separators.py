""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.separator import Separator

# Globals and constants variables.

DOT = Separator('.')
SOURCE_DEFINITION = Separator('>>>>>>>> Source definition.')
MATERIAL = Separator('>>>>>>>> Material data and simulation parameters.')
INTERACTION_FORCING = Separator('>>>>>>>> Interaction forcing.')
BREMSSTRAHLUNG_SPLITTING = Separator('>>>>>>>> Bremsstrahlung splitting.')
XRAY_SPLITTING = Separator('>>>>>>>> X-ray splitting.')
EMERGING_PARTICLES = Separator('>>>>>>>> Emerging particles. Energy and angular distributions.')
ENERGY_DEPOSITON_DETECTORS = Separator('>>>>>>>> Energy-deposition detectors (up to 25).')
JOB_PROPERTIES = Separator('>>>>>>>> Job properties.')
END = Separator('Ends the reading of input data', 'END')