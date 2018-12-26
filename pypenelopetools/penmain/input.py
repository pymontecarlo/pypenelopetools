""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.input import PenelopeInputBase
import pypenelopetools.penelope.keywords as penelope_keywords
import pypenelopetools.penmain.keywords as penmain_keywords
import pypenelopetools.penelope.separators as penelope_separators
import pypenelopetools.penmain.separators as penmain_separators

# Globals and constants variables.

class PenmainInput(PenelopeInputBase):

    def __init__(self):
        self.TITLE = penelope_keywords.TITLE()

        # Source definition
        self.SKPAR = penelope_keywords.SKPAR()
        self.SENERG = penelope_keywords.SENERG()
        self.SPECTR = penelope_keywords.SPECTR()
        self.SGPOL = penelope_keywords.SGPOL()
        self.SPOSIT = penelope_keywords.SPOSIT()
        self.SBOX = penmain_keywords.SBOX()
        self.SBODY = penmain_keywords.SBODY()
        self.SCONE = penelope_keywords.SCONE()
        self.SRECTA = penelope_keywords.SRECTA()

        # Input phase-space file
        self.IPSFN = penmain_keywords.IPSFN()
        self.IPSPLI = penmain_keywords.IPSPLI()
        self.WGTWIN = penmain_keywords.WGTWIN()
        self.EPMAX = penmain_keywords.EPMAX()

        # Material data and simulation parameters
        self.materials = penelope_keywords.Materials()

        # Geometry and local simulation parameters
        self.GEOMFN = penelope_keywords.GEOMFN()
        self.PARINP = penmain_keywords.PARINP()
        self.DSMAX = penelope_keywords.DSMAX()
        self.EABSB = penelope_keywords.EABSB()

        # Interaction forcing
        self.IFORCE = penelope_keywords.InteractionForcings()

        # Bremsstrahlung splitting
        self.IBRSPL = penelope_keywords.IBRSPL()

        # X-ray splitting
        self.IXRSPL = penelope_keywords.IXRSPL()

        # Emerging particles
        self.NBE = penelope_keywords.NBE()
        self.NBANGL = penelope_keywords.NBANGL()

        # Impact detectors
        self.impact_detectors = penmain_keywords.ImpactDetectors()

        # Energy-deposition detectors
        self.energy_deposition_detectors = penmain_keywords.EnergyDepositionDetectors()

        # Absorbed dose distribution
        self.GRIDX = penelope_keywords.GRIDX()
        self.GRIDY = penelope_keywords.GRIDY()
        self.GRIDZ = penelope_keywords.GRIDZ()
        self.GRIDR = penmain_keywords.GRIDR()

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
                penelope_separators.SOURCE_DEFINITION,
                self.SKPAR, self.SENERG, self.SPECTR, self.SGPOL,
                self.SPOSIT, self.SBOX, self.SBODY, self.SCONE, self.SRECTA,

                penelope_separators.DOT,
                penmain_separators.INPUT_PHASE_SPACE_FILE,
                self.IPSFN, self.IPSPLI, self.WGTWIN, self.EPMAX,

                penelope_separators.DOT,
                penelope_separators.MATERIAL,
                self.materials,

                penelope_separators.DOT,
                penmain_separators.GEOMETRY,
                self.GEOMFN, self.PARINP, self.DSMAX, self.EABSB,

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
                penelope_separators.EMERGING_PARTICLES,
                self.NBE, self.NBANGL,

                penelope_separators.DOT,
                penmain_separators.IMPACT_DETECTORS,
                self.impact_detectors,

                penelope_separators.DOT,
                penelope_separators.ENERGY_DEPOSITON_DETECTORS,
                self.energy_deposition_detectors,

                penelope_separators.DOT,
                penmain_separators.ABSORBED_DOSE_DISTRIBUTION,
                self.GRIDX, self.GRIDY, self.GRIDZ, self.GRIDR,

                penelope_separators.DOT,
                penelope_separators.JOB_PROPERTIES,
                self.RESUME, self.DUMPTO, self.DUMPP,

                penelope_separators.DOT,
                self.RSEED, self.NSIMSH, self.TIME,

                penelope_separators.END]
