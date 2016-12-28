""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.separator import Separator, EndSeparator

# Globals and constants variables.

DOT = Separator('.')
SOURCE_DEFINITION = Separator('>>>>>>>> Source definition.')
INPUT_PHASE_SPACE_FILE = Separator('>>>>>>>> Input phase-space file (psf).')
MATERIAL = Separator('>>>>>>>> Material data and simulation parameters.')
GEOMETRY = Separator('>>>>>>>> Geometry and local simulation parameters.')
INTERACTION_FORCING = Separator('>>>>>>>> Interaction forcing.')
BREMSSTRAHLUNG_SPLITTING = Separator('>>>>>>>> Bremsstrahlung splitting.')
XRAY_SPLITTING = Separator('>>>>>>>> X-ray splitting.')
EMERGING_PARTICLES = Separator('>>>>>>>> Emerging particles. Energy and angular distributions.')
IMPACT_DETECTORS = Separator('>>>>>>>> Impact detectors (up to 25 different detectors).')
ENERGY_DEPOSITON_DETECTORS = Separator('>>>>>>>> Energy-deposition detectors (up to 25).')
ABSORBED_DOSE_DISTRIBUTION = Separator('>>>>>>>> Absorbed dose distribution.')
JOB_PROPERTIES = Separator('>>>>>>>> Job properties.')
END = EndSeparator()