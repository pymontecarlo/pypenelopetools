""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.keyword import \
    TypeKeyword, KeywordGroup, KeywordSequence, filename_type

# Globals and constants variables.

class SRADI(TypeKeyword):
    """
    The initial position of the particle is sampled randomly
    within a circle of radius SRAD, centered at (SX0,SY0,SZ0)
    and perpendicular to the beam axis direction.
        DEFAULT: SRAD=0.0
    """

    def __init__(self):
        super().__init__('SRADI', (float,),
                         comment='Radius of the beam, in cm')

    def set(self, sradius):
        super().set(sradius)

class SDIREC(TypeKeyword):
    """
    Polar and azimuthal angles of the electron beam axis direction, in deg.
        DEFAULTS: STHETA=180.0, SPHI=0.0
    """

    def __init__(self):
        super().__init__('SDIREC', (float, float),
                         comment='Direction angles of the beam axis, in deg')

    def set(self, stheta, sphi):
        super().set(stheta, sphi)

class SAPERT(TypeKeyword):
    """
    Angular aperture of the electron beam, in deg.
        DEFAULT: SALPHA=0.0
    """

    def __init__(self):
        super().__init__('SAPERT', (float,), comment='Beam aperture, in deg')

    def set(self, salpha):
        super().set(salpha)

class PhotonDetectorGroup(KeywordGroup):
    """
    Each detector collects photons that leave the sample with directions
    within a 'rectangle' on the unit sphere, limited by the 'parallels'
    THETA1 and THETA2 and the 'meridians' PHI1 and PHI2. The output
    spectrum is the energy distribution of photons that emerge within the
    acceptance solid angle of the detector with energies in the interval
    from EDEL to EDEU, recorded using NCHE channels. Notice that the
    spectrum is given in absolute units (per incident electron, per eV
    and per unit solid angle).
    
    PDANGL : Starts the definition of a new detector. Up to 25 different
             detectors can be defined. THETA1,THETA2 and PHI1,PHI2 are
             the limits of the angular intervals covered by the detector,
             in degrees.
    
             The integer flag IPSF serves to activate the creation of a
             phase-space file (psf), which contains the state variables
             and weigths of particles that enter the detector. Use this
             option with care, because psf's may grow very fast.
             IPSF=0, the psf is not created.
             IPSF=1, a psf is created.
             IPSF>1, a psf is created, but contains only state variables
                     of detected photons that have ILB(4)=IPSF (used for
                     studying angular distributions of x rays).
             Generating the psf is useful for tuning interaction forcing,
             which requires knowing the weights of detected particles.
    
               DEFAULTS: THETA1=35, THETA2=45, PHI1=0, PHI2=360, IPSF=0
    
             NOTE: PHI1 and PHI2 must be both either in the interval
             (0,360) or in the interval (-180,180).
    
    PDENER : EDEL and EDEU are the lower and upper limits of the energy
             window covered by the detector.
             NCHE is the number of energy channels in the output spectrum
             (.LE. 1000).
               DEFAULT: EDEL=0.0, EDU=E0, NCHE=1000
    
    XRORIG : This line in the input file activates the generation of a
             file with the position coordinates of the emission sites of
             the photons that reach the detector. The file name must be
             explicitly defined. Notice that the file may grow very fast,
             so use this option only in short runs. The output file is
             overwritten when a simulation is resumed.
               DEFAULT: NONE
    """

    def __init__(self):
        super().__init__()
        self.PDANGL = TypeKeyword('PDANGL', (float, float, float, float, int),
                                  comment='Angular window, in deg, IPSF')
        self.PDENER = TypeKeyword('PDENER', (float, float, int),
                                  comment='Energy window, no. of channels')
        self.XRORIG = TypeKeyword('XRORIG', (filename_type,),
                                  comment='Map of emission sites of detected x rays')

    def set(self, theta1, theta2, phi1, phi2, ipsf, edel, edeu, nche, emission_filename=None):
        self.PDANGL.set(theta1, theta2, phi1, phi2, ipsf)
        self.PDENER.set(edel, edeu, nche)
        self.XRORIG.set(emission_filename)

    def get_keywords(self):
        return (self.PDANGL, self.PDENER, self.XRORIG)

class PhotonDetectors(KeywordSequence):

    def __init__(self):
        keyword = PhotonDetectorGroup()
        super().__init__(keyword)

    def set(self, theta1, theta2, phi1, phi2, ipsf, edel, edeu, nche, emission_filename=None):
        super().set(theta1, theta2, phi1, phi2, ipsf, edel, edeu, nche, emission_filename)

    def add(self, theta1, theta2, phi1, phi2, ipsf, edel, edeu, nche, emission_filename=None):
        super().add(theta1, theta2, phi1, phi2, ipsf, edel, edeu, nche, emission_filename)

class XRAYE(KeywordSequence):
    """
    This line activates the generation of the space distribution
    of emission sites of x rays with energies in the interval
    from EMIN to EMAX, limited to the scoring box.
      DEFAULTS: none
    """

    def __init__(self):
        keyword = TypeKeyword('XRAYE', (float, float),
                              comment='Energy interval where x rays are mapped')
        super().__init__(keyword)

    def set(self, emin, emax):
        super().set(emin, emax)

    def add(self, emin, emax):
        super().add(emin, emax)

class XRLINE(KeywordSequence):
    """
    The space distribution of emission sites of x rays IZS1S200
    [ILB(4) notation, note the final double zero] will be mapped.
      DEFAULTS: none
    """

    def __init__(self):
        keyword = TypeKeyword('XRLINE', (int,),
                              comment='X-ray line, IZ*1e6+S1*1e4+S2*1e2')
        super().__init__(keyword)

    def set(self, izs1s200):
        super().set(izs1s200)

    def add(self, izs1s200):
        super().add(izs1s200)

class REFLIN(TypeKeyword):
    """
    The simulation will be discontinued when the relative
    statistical uncertainty (3*sigma) of the intensity of line
    IZS1S200 [note the final double zero] in detector IDET is
    less than the tolerance TOL.
      DEFAULTS: none
    """

    def __init__(self):
        super().__init__('REFLIN', (int, int, float),
                         comment='IZ*1e6+S1*1e4+S2*1e2,detector,tolerance')

    def set(self, izs1s200, idet, tol):
        super().set(izs1s200, idet, tol)



