"""
Keywords used specifically for PENEPMA.
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.keyword import \
    TypeKeyword, KeywordGroupBase, KeywordSequence

# Globals and constants variables.

class SRADI(TypeKeyword):
    """Initial position of the particle is sampled randomly within a circle.
    
    The circle is centered at (SX0,SY0,SZ0) and perpendicular to the beam 
    axis direction.
    """

    def __init__(self):
        super().__init__('SRADI', (float,),
                         comment='Radius of the beam, in cm')

    def set(self, sradius):
        """
        Sets circle.
        
        Args:
            sradius (float): Radius of the circle in cm.
        """
        super().set(sradius)

class SDIREC(TypeKeyword):
    """Polar and azimuthal angles of the electron beam axis direction."""

    def __init__(self):
        super().__init__('SDIREC', (float, float),
                         comment='Direction angles of the beam axis, in deg')

    def set(self, stheta, sphi):
        """
        Sets angles.
        
        Args:
            stheta (float): Polar angle in deg.
            sphi (float): Azimuthal angle in deg.
        """
        super().set(stheta, sphi)

class SAPERT(TypeKeyword):
    """Angular aperture of the electron beam."""

    def __init__(self):
        super().__init__('SAPERT', (float,), comment='Beam aperture, in deg')

    def set(self, salpha):
        """
        Sets angle.
        
        Args:
            salpha (float): Angular aperture in deg.
        """
        super().set(salpha)

class PhotonDetectorGroup(KeywordGroupBase):
    """Definition of photon detector.
    
    Each detector collects photons that leave the sample with directions within 
    a *rectangle( on the unit sphere, limited by the *parallels* THETA1 and 
    THETA2 and the *meridians* PHI1 and PHI2. 
    The output spectrum is the energy distribution of photons that emerge within 
    the acceptance solid angle of the detector with energies in the interval 
    from EDEL to EDEU, recorded using NCHE channels. 
    Notice that the spectrum is given in absolute units (per incident electron, 
    per eV and per unit solid angle).
    """

    def __init__(self):
        super().__init__()
        self.PDANGL = TypeKeyword('PDANGL', (float, float, float, float, int),
                                  comment='Angular window, in deg, IPSF')
        self.PDENER = TypeKeyword('PDENER', (float, float, int),
                                  comment='Energy window, no. of channels')
        self.XRORIG = TypeKeyword('XRORIG', (str,),
                                  comment='Map of emission sites of detected x rays')

    def set(self, theta1, theta2, phi1, phi2, ipsf, edel, edeu, nche, emission_filename=None):
        """
        Sets parameters of detector.
        
        .. note::
           ``phi1`` and ``phi2`` must be both either in the interval (0,360) or 
           in the interval (-180,180).
        
        Args:
            theta1 (float): Lower limit polar angle in deg.
            theta2 (float): Upper limit polar angle in deg.
            phi1 (float): Lower limit azimuthal angle in deg.
            phi2 (float): Upper limit azimuthal angle in deg.
            ipsf (int): Flag to activate the creation of a phase-space file
                (psf), which contains the state variables and weights of 
                particles that enter the detector. 
                Use this option with care, because psf's may grow very fast.
                
                * ``ipsf=0``: the psf is not created.
                * ``ipsf=1``: a psf is created.
                * ``ipsf>1``: a psf is created, but contains only state
                  variables of detected photons that have ILB(4)=IPSF 
                  (used for studying angular distributions of x rays).
                
                Generating the psf is useful for tuning interaction forcing,
                which requires knowing the weights of detected particles.
            edel (float): Lower limits of the energy window covered by the 
                detector in eV.
            edeu (float): Upper limits of the energy window covered by the 
                detector in eV.
            nche (int): Number of energy channels in the output spectrum.
                Should be less than 1000.
            emission_filename (str, optional): File name of the generation file.
                Specifying a file name activates the generation of a file with 
                the position coordinates of the emission sites of the photons 
                that reach the detector. 
                Notice that the file may grow very fast, so use this option 
                only in short runs. 
                The output file is overwritten when a simulation is resumed.
        """
        self.PDANGL.set(theta1, theta2, phi1, phi2, ipsf)
        self.PDENER.set(edel, edeu, nche)
        self.XRORIG.set(emission_filename)

    def get_keywords(self):
        return (self.PDANGL, self.PDENER, self.XRORIG)

class PhotonDetectors(KeywordSequence):
    """Definition of the photon detectors.
    
    Up to 25 different detectors can be defined.
    """

    def __init__(self, maxlength=25):
        keyword = PhotonDetectorGroup()
        super().__init__(keyword, maxlength)

    def add(self, theta1, theta2, phi1, phi2, ipsf, edel, edeu, nche, emission_filename=None):
        """
        Add a new photon detector.
        
        .. note::
           ``phi1`` and ``phi2`` must be both either in the interval (0,360) or 
           in the interval (-180,180).
           
        .. important::
           The theta angles are defined as angles from the positive z-axis.
           This is different than the take-off angle usually used in 
           microanalysis.
           For a take-off angle of 30deg, theta would be 60deg.
        
        Args:
            theta1 (float): Lower limit polar angle in deg.
            theta2 (float): Upper limit polar angle in deg.
            phi1 (float): Lower limit azimuthal angle in deg.
            phi2 (float): Upper limit azimuthal angle in deg.
            ipsf (int): Flag to activate the creation of a phase-space file
                (psf), which contains the state variables and weights of 
                particles that enter the detector. 
                Use this option with care, because psf's may grow very fast.
                
                * ``ipsf=0``: the psf is not created.
                * ``ipsf=1``: a psf is created.
                * ``ipsf>1``: a psf is created, but contains only state
                  variables of detected photons that have ILB(4)=IPSF 
                  (used for studying angular distributions of x rays).
                
                Generating the psf is useful for tuning interaction forcing,
                which requires knowing the weights of detected particles.
            edel (float): Lower limits of the energy window covered by the 
                detector in eV.
            edeu (float): Upper limits of the energy window covered by the 
                detector in eV.
            nche (int): Number of energy channels in the output spectrum.
                Should be less than 1000.
            emission_filename (str, optional): File name of the generation file.
                Specifying a file name activates the generation of a file with 
                the position coordinates of the emission sites of the photons 
                that reach the detector. 
                Notice that the file may grow very fast, so use this option 
                only in short runs. 
                The output file is overwritten when a simulation is resumed.
        """
        super().add(theta1, theta2, phi1, phi2, ipsf, edel, edeu, nche, emission_filename)

class XRAYE(KeywordSequence):
    """Space distribution of emission sites of x rays within an energy interval."""

    def __init__(self, maxlength=10):
        keyword = TypeKeyword('XRAYE', (float, float),
                              comment='Energy interval where x rays are mapped')
        super().__init__(keyword, maxlength)

    def add(self, emin, emax):
        """
        Add an energy interval.
        
        Args:
            emin (float): Lower limit in eV.
            emax (float): Upper limit in eV.
        """
        super().add(emin, emax)

class XRLINE(KeywordSequence):
    """Space distribution of emission sites of x rays."""

    def __init__(self, maxlength=10):
        keyword = TypeKeyword('XRLINE', (int,),
                              comment='X-ray line, IZ*1e6+S1*1e4+S2*1e2')
        super().__init__(keyword, maxlength)

    def add(self, izs1s200):
        """
        Adds a characteristic x ray.
        
        .. hint::
           Use :func:`convert_xrayline_to_izs1s200 <pypenelopetools.penepma.utils.convert_xrayline_to_izs1s200>`
           to convert :class:`XrayLine` to ILB(4) notation.
        
        Args:
            izs1s200 (int): x ray identification.
                ILB(4) notation, note the final double zero (IZ*1e6+S1*1e4+S2*1e2).
        """
        super().add(izs1s200)

class REFLIN(TypeKeyword):
    """Termination of simulation based on relative statistical uncertainty of the intensity of line."""

    def __init__(self):
        super().__init__('REFLIN', (int, int, float),
                         comment='IZ*1e6+S1*1e4+S2*1e2,detector,tolerance')

    def set(self, izs1s200, idet, tol):
        """
        Sets termination.
        
        .. hint::
           Use :func:`convert_xrayline_to_izs1s200 <pypenelopetools.penepma.utils.convert_xrayline_to_izs1s200>`
           to convert :class:`XrayLine` to ILB(4) notation.
        
        Args:
            izs1s200: x ray identification.
                ILB(4) notation, note the final double zero (IZ*1e6+S1*1e4+S2*1e2).
            idet (int): Index of detector.
            tol (float): Relative statistical uncertainty (3*sigma) of the intensity of line
        """
        super().set(izs1s200, idet, tol)



