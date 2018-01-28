""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.input import PenelopeInputBase
import pypenelopetools.penelope.keywords as penelope_keywords
import pypenelopetools.penelope.separators as penelope_separators
import pypenelopetools.pencyl.keywords as pencyl_keywords
import pypenelopetools.pencyl.separators as pencyl_separators

# Globals and constants variables.

class PencylInput(PenelopeInputBase):

    def __init__(self):
        self.TITLE = penelope_keywords.TITLE()

        # Geometry definition list
        self.geometry_definitions = pencyl_keywords.GeometryDefinitions()

        # Source definition
        self.SKPAR = penelope_keywords.SKPAR()
        self.SENERG = penelope_keywords.SENERG()
        self.SPECTR = penelope_keywords.SPECTR()
        self.SGPOL = penelope_keywords.SGPOL()
        self.SEXTND = pencyl_keywords.SEXTND()
        self.STHICK = pencyl_keywords.STHICK()
        self.SRADII = pencyl_keywords.SRADII()
        self.SPOSIT = penelope_keywords.SPOSIT()
        self.SCONE = penelope_keywords.SCONE()
        self.SRECTA = penelope_keywords.SRECTA()

        # Material data and simulation parameters
        self.materials = penelope_keywords.Materials()

        # Geometry and local simulation parameters
        self.DSMAX = pencyl_keywords.DSMAX()
        self.EABSB = pencyl_keywords.EABSB()

        # Interaction forcing
        self.IFORCE = pencyl_keywords.IFORCE()

        # Bremsstrahlung splitting
        self.IBRSPL = pencyl_keywords.IBRSPL()

        # X-ray splitting
        self.IXRSPL = pencyl_keywords.IXRSPL()

        # Woodcock's delta-scattering method for photons.
        self.IWOODC = pencyl_keywords.IWOODC()

        # Emerging particles
        self.NBE = penelope_keywords.NBE()
        self.NBANGL = penelope_keywords.NBANGL()
        self.NBZ = pencyl_keywords.NBZ()
        self.NBR = pencyl_keywords.NBR()
        self.NBTL = pencyl_keywords.NBTL()

        # Particle positions at the lower and upper planes
        self.EMERGP = pencyl_keywords.EMERGP()

        # Energy-deposition detectors
        self.energy_deposition_detectors = pencyl_keywords.EnergyDepositionDetectors()

        # Dose and charge distributions
        self.DOSE2D = pencyl_keywords.DOSE2D()

        # Job properties
        self.RESUME = penelope_keywords.RESUME()
        self.DUMPTO = penelope_keywords.DUMPTO()
        self.DUMPP = penelope_keywords.DUMPP()
        self.RSEED = penelope_keywords.RSEED()
        self.NSIMSH = penelope_keywords.NSIMSH()
        self.TIME = penelope_keywords.TIME()

    def get_keywords(self):
        return [self.TITLE,

                penelope_separators.DOT,
                pencyl_separators.GEOMETRY_LIST_START,
                self.geometry_definitions,
                pencyl_separators.GEOMETRY_LIST_END,

                penelope_separators.DOT,
                penelope_separators.SOURCE_DEFINITION,
                self.SKPAR, self.SENERG, self.SPECTR, self.SGPOL,
                self.SEXTND, self.STHICK, self.SRADII,
                self.SPOSIT, self.SCONE, self.SRECTA,

                penelope_separators.DOT,
                penelope_separators.MATERIAL,
                self.materials,

                penelope_separators.DOT,
                pencyl_separators.DSMAX_EABSB,
                self.DSMAX, self.EABSB,

                penelope_separators.DOT,
                penelope_separators.INTERACTION_FORCING,
                self.IFORCE,

                penelope_separators.DOT,
                penelope_separators.BREMSSTRAHLUNG_SPLITTING,
                self.IBRSPL,

                penelope_separators.DOT,
                penelope_separators.XRAY_SPLITTING,
                self.IXRSPL,

                penelope_separators.DOT,
                pencyl_separators.WOODCOCK,
                self.IWOODC,

                penelope_separators.DOT,
                pencyl_separators.COUNTER_ARRAY,
                self.NBE, self.NBANGL, self.NBZ, self.NBR, self.NBTL,

                penelope_separators.DOT,
                pencyl_separators.PARTICLE_POSITIONS,
                self.EMERGP,

                penelope_separators.DOT,
                penelope_separators.ENERGY_DEPOSITON_DETECTORS,
                self.energy_deposition_detectors,

                penelope_separators.DOT,
                pencyl_separators.DOSE_CHARGE_DISTRIBUTION,
                self.DOSE2D,

                penelope_separators.DOT,
                penelope_separators.JOB_PROPERTIES,
                self.RESUME, self.DUMPTO, self.DUMPP,

                penelope_separators.DOT,
                self.RSEED, self.NSIMSH, self.TIME,

                penelope_separators.END]
