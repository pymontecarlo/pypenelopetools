""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.separator import Separator

# Globals and constants variables.

GEOMETRY_LIST_START = Separator('>>>>>>>> Geometry definition list.', 'GSTART')
GEOMETRY_LIST_END = Separator('<<<<<<<< End of the geometry definition list.', 'GEND')
DSMAX_EABSB = Separator('>>>>>>>> Local maximum step lengths and absorption energies.')
WOODCOCK = Separator(">>>>>>>> Woodcock's delta-scattering method for photons.")
COUNTER_ARRAY = Separator('>>>>>>>> Counter array dimensions and PDF ranges.')
PARTICLE_POSITIONS = Separator('>>>>>>>> Particle positions at the lower and upper planes.')
DOSE_CHARGE_DISTRIBUTION = Separator('>>>>>>>> Dose and charge distributions.')
