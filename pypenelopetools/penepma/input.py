"""
Input of PENEPMA simulation.
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.input import PenelopeInputBase
import pypenelopetools.penelope.keywords as penelope_keywords
import pypenelopetools.penelope.separators as penelope_separators
import pypenelopetools.penepma.keywords as penepma_keywords
import pypenelopetools.penepma.separators as penepma_separators

# Globals and constants variables.

class PenepmaInput(PenelopeInputBase):
    """
    Creates an object representing a PENEPMA input file.
    
    Attributes:
        TITLE (:class:`TITLE <pypenelopetools.penelope.keywords.TITLE>`): 
            Title of the job (up to 65 characters).
        SKPAR (:class:`SKPAR <pypenelopetools.penelope.keywords.SKPAR>`):
            Type of primary particle KPARP (1=electrons, 2=photons or 3=positrons).
        SENERG (:class:`SENERG <pypenelopetools.penelope.keywords.SENERG>`):
            Initial energy SE0 of primary particles.
        SPOSIT (:class:`SPOSIT <pypenelopetools.penelope.keywords.SPOSIT>`):
            Coordinates of the source centre.
        SRADI (:class:`SRADI <pypenelopetools.penepma.keywords.SRADI>`):
            Initial position of the particle is sampled randomly within a circle.
        SDIREC (:class:`SDIREC <pypenelopetools.penepma.keywords.SDIREC>`):
            Polar and azimuthal angles of the electron beam axis direction.
        SAPERT (:class:`SAPERT <pypenelopetools.penepma.keywords.SAPERT>`):
            Angular aperture of the electron beam.
        materials (:class:`Materials <pypenelopetools.penelope.keywords.Materials>`):
            Definition of materials.
        GEOMFN (:class:`GEOMFN <pypenelopetools.penelope.keywords.GEOMFN>`):
            Name of geometry definition file.
        DSMAX (:class:`DSMAX <pypenelopetools.penelope.keywords.DSMAX>`):
            Maximum step length of electrons and positrons in body.
        IFORCE (:class:`IFORCE <pypenelopetools.penelope.keywords.IFORCE>`):
            Forcing of interactions.
        IBRSPL (:class:`IBRSPL <pypenelopetools.penelope.keywords.IBRSPL>`):
            Bremsstrahlung splitting for electrons and positrons.
        IXRSPL (:class:`IXRSPL <pypenelopetools.penelope.keywords.IXRSPL>`):
            Splitting of characteristic x rays emitted.
        NBE (:class:`NBE <pypenelopetools.penelope.keywords.NBE>`):
            Definition of energy distributions of emerging particles.
        NBANGL (:class:`NBANGL <pypenelopetools.penelope.keywords.NBANGL>`):
            Definition of angular distributions of emerging particles.
        photon_detectors (:class:`PhotonDetectors <pypenelopetools.penepma.keywords.PhotonDetectors>`):
            Definition of the photon detectors.
        GRIDX (:class:`GRIDX <pypenelopetools.penelope.keywords.GRIDX>`):
            Definition of x-coordinates of the vertices of the dose box.
        GRIDY (:class:`GRIDY <pypenelopetools.penelope.keywords.GRIDY>`):
            Definition of y-coordinates of the vertices of the dose box.
        GRIDZ (:class:`GRIDZ <pypenelopetools.penelope.keywords.GRIDZ>`):
            Definition of z-coordinates of the vertices of the dose box.
        XRAYE (:class:`XRAYE <pypenelopetools.penepma.keywords.XRAYE>`):
            Space distribution of emission sites of x rays within an energy interval.
        XRLINE (:class:`XRLINE <pypenelopetools.penepma.keywords.XRLINE>`):
            Space distribution of emission sites of x rays.
        RESUME (:class:`RESUME <pypenelopetools.penelope.keywords.RESUME>`):
            Name of the resume file.
        DUMPTO (:class:`DUMPTO <pypenelopetools.penelope.keywords.DUMPTO>`):
            Name of dump file.
        DUMPP (:class:`DUMPP <pypenelopetools.penelope.keywords.DUMPP>`):
            Dump interval.
        RSEED (:class:`RSEED <pypenelopetools.penelope.keywords.RSEED>`):
            Seeds of the random-number generator.
        REFLIN (:class:`REFLIN <pypenelopetools.penepma.keywords.REFLIN>`):
            Termination of simulation based on relative statistical uncertainty of the intensity of line.
        NSIMSH (:class:`NSIMSH <pypenelopetools.penelope.keywords.NSIMSH>`):
            Desired number of simulated showers.
        TIME (:class:`TIME <pypenelopetools.penelope.keywords.TIME>`):
            Allotted simulation time.
    """

    def __init__(self):
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
        self.IFORCE = penelope_keywords.InteractionForcings()

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
