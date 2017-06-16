""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.input import PenelopeInput
import pypenelopetools.penelope.keywords as penelope_keywords
import pypenelopetools.penelope.separators as penelope_separators
import pypenelopetools.penepma.keywords as penepma_keywords
import pypenelopetools.penepma.separators as penepma_separators

# Globals and constants variables.

class PenepmaInput(PenelopeInput):

    def __init__(self, filename):
        super().__init__(filename)

        self.TITLE = penelope_keywords.TITLE()

        # Source definition
        self.SKPAR = penelope_keywords.SKPAR()
        self.SENERG = penelope_keywords.SENERG()
        self.SPOSIT = penelope_keywords.SPOSIT()
        self.SRADI = penepma_keywords.SRADI()
        self.SDIREC = penepma_keywords.SDIREC()
        self.SAPERT = penepma_keywords.SAPERT()

        # Material data and simulation parameters
        self.materials = penelope_keywords.Materials()

        # Geometry and local simulation parameters
        self.GEOMFN = penelope_keywords.GEOMFN()
        self.DSMAX = penelope_keywords.DSMAX()

        # Interaction forcing
        self.IFORCE = penelope_keywords.IFORCE()

        # Bremsstrahlung splitting
        self.IBRSPL = penelope_keywords.IBRSPL()

        # X-ray splitting
        self.IXRSPL = penelope_keywords.IXRSPL()

        # Emerging particles
        self.NBE = penelope_keywords.NBE()
        self.NBANGL = penelope_keywords.NBANGL()

        # Photon detectors
        self.photon_detectors = penepma_keywords.PhotonDetectors()

        # Spatial distribution
        self.GRIDX = penelope_keywords.GRIDX()
        self.GRIDY = penelope_keywords.GRIDY()
        self.GRIDZ = penelope_keywords.GRIDZ()
        self.XRAYE = penepma_keywords.XRAYE()
        self.XRLINE = penepma_keywords.XRLINE()

        # Job properties
        self.RESUME = penelope_keywords.RESUME()
        self.DUMPTO = penelope_keywords.DUMPTO()
        self.DUMPP = penelope_keywords.DUMPP()
        self.RSEED = penelope_keywords.RSEED()
        self.REFLIN = penepma_keywords.REFLIN()
        self.NSIMSH = penelope_keywords.NSIMSH()
        self.TIME = penelope_keywords.TIME()

    def get_keywords(self):
        return [self.TITLE,

                penelope_separators.DOT,
                penelope_separators.SOURCE_DEFINITION,
                self.SKPAR, self.SENERG, self.SPOSIT, self.SRADI, self.SDIREC, self.SAPERT,

                penelope_separators.DOT,
                penelope_separators.MATERIAL,
                self.materials,

                penelope_separators.DOT,
                penepma_separators.GEOMETRY,
                self.GEOMFN, self.DSMAX,

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
                penepma_separators.PHOTON_DETECTORS,
                self.photon_detectors,

                penelope_separators.DOT,
                penepma_separators.SPATIAL_DISTRIBUTION,
                self.GRIDX, self.GRIDY, self.GRIDZ, self.XRAYE, self.XRLINE,

                penelope_separators.DOT,
                penelope_separators.JOB_PROPERTIES,
                self.RESUME, self.DUMPTO, self.DUMPP,

                penelope_separators.DOT,
                self.RSEED, self.REFLIN, self.NSIMSH, self.TIME]
