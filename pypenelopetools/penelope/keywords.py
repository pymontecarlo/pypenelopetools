"""
Keywords used across different PENELOPE main programs.
"""

# Standard library modules.
from operator import attrgetter

# Third party modules.

# Local modules.
from pypenelopetools.penelope.keyword import \
    TypeKeyword, KeywordSequence, KeywordGroupBase
from pypenelopetools.penelope.enums import KPAR, ICOL

# Globals and constants variables.

class TITLE(TypeKeyword):
    """Title of the job.
    
    The TITLE string is used to mark dump files. To prevent the
    improper use of wrong resuming files, change the title each
    time you modify basic parameters of your problem. The code
    will then be able to identify the inconsistency and to print
    an error message before stopping.
    """

    def __init__(self):
        super().__init__('TITLE', (str,))

    def _parse_line(self, line):
        name, values, comment = super()._parse_line(line)
        return name, (' '.join(values),), comment

    def set(self, title):
        """
        Sets value.
        
        Args:
            title (str): Title of the job (up to 65 characters).
        """
        super().set(title)

    def validate(self, title):
        if len(title) > 65:
            raise ValueError('Title is too long. Maximum 65 characters')
        return super().validate(title)

class SKPAR(TypeKeyword):
    """Type of primary particle KPARP (1=electrons, 2=photons or 3=positrons).
    
    If KPARP=0, the initial states of primary particles are
    set by subroutine SOURCE, to be provided by the user. An
    example of that subroutine, corresponding to a 60-Co source
    (two gamma rays in each nuclear deexcitation), is included
    in the PENMAIN package (file 'source.f').
    """

    def __init__(self):
        super().__init__('SKPAR', (KPAR,),
                         comment="Primary particles: 1=electron, 2=photon, 3=positron")

    def set(self, kparp):
        """
        Sets value.
        
        Args:
            kparp (:class:`KPAR`): Type of primary particles
        """
        super().set(kparp)

    def validate(self, kparp):
        if kparp not in KPAR:
            raise ValueError('Invalid particle')
        return super().validate(kparp)

class SENERG(TypeKeyword):
    """For a monoenergetic source, initial energy SE0 of primary particles."""

    def __init__(self):
        super().__init__('SENERG', (float,),
                         comment="Initial energy (monoenergetic sources only)")

    def set(self, se0):
        """
        Sets value.
        
        Args:
            se0 (float): Initial energy of primary particles in eV
        """
        super().set(se0)

    def validate(self, se0):
        if se0 <= 0.0:
            raise ValueError('SE0 must be greater than 0')
        return super().validate(se0)

class SPECTR(KeywordSequence):
    """Define a source with continuous (stepwise constant) spectrum.
    
    For a source with continuous (stepwise constant) spectrum,
    each 'SPECTR' line gives the lower end-point of an energy
    bin of the source spectrum (Ei) and the associated relative
    probability (Pi), integrated over the bin. Up to NSEM=1000
    lines, in arbitrary order. The upper end of the spectrum is
    defined by entering a line with Ei equal to the upper energy
    end point and with a negative Pi value.
    """

    def __init__(self, maxlength=1000):
        keyword = TypeKeyword('SPECTR', (float, float),
                              comment='E bin: lower-end and total probability')
        super().__init__(keyword, maxlength)

    def add(self, ei, pi):
        """
        Adds a step in the spectrum.
        
        Args:
            ei (float): Lower end-point of an energy bin of the source spectrum in eV
            pi (float): Associated relative probability
        """
        return super().add(ei, pi)

class SGPOL(TypeKeyword):
    """Activates the simulation of polarisation effects in the scattering of photons.
    
    This line activates the simulation of polarisation effects
    in the scattering of photons (electrons and positrons are
    assumed to be unpolarised). SP1, SP2, SP3 are the Stokes
    parameters of primary photons, which define the degrees of
    linear polarisation at 45 deg azimuth, of circular
    polarisation, and of linear polarisation at zero azimuth,
    respectively. It is assumed that secondary photons are
    emitted with null polarisation (SP1=SP2=SP3=0).
    """

    def __init__(self):
        super().__init__('SGPOL', (float, float, float),
                         comment="Stokes parameters for polarized photons")

    def set(self, sp1, sp2, sp3):
        """
        Sets Stokes polarisation parameters.
        
        Args:
            sp1 (float): Degrees of linear polarisation at 45 deg azimuth
            sp2 (float): Degrees of circular polarisation
            sp3 (float): Degrees of linear polarisation at 0 deg azimuth
        """
        super().set(sp1, sp2, sp3)

class SPOSIT(TypeKeyword):
    """Coordinates of the source centre."""

    def __init__(self):
        super().__init__("SPOSIT", (float, float, float),
                         comment="Coordinates of the source")

    def set(self, sx0, sy0, sz0):
        """
        Sets coordinates.
        
        Args:
            sx0 (float): x-coordinate in cm.
            sy0 (float): y-coordinate in cm.
            sz0 (float): z-coordinate in cm.
        """
        super().set(sx0, sy0, sz0)

class SCONE(TypeKeyword):
    """Initial direction of primary particles is sampled uniformly within a conical beam.
    
    Conical source beam. Polar and azimuthal angles of the
    beam axis direction, THETA and PHI, and angular aperture,
    ALPHA, in deg.
    
    The case ALPHA=0 defines a monodirectional source, and ALPHA
    =180 deg corresponds to an isotropic source.
    """

    def __init__(self):
        super().__init__("SCONE", (float, float, float),
                         comment="Conical beam; angles in deg")

    def set(self, theta, phi, alpha):
        """
        Sets angles.
        
        Args:
            theta (float): Polar angle of the beam axis direction in deg.
            phi (float): Azimuthal angle of the beam axis direction in deg.
            alpha (float): Angular aperture in deg.
        """
        super().set(theta, phi, alpha)

class SRECTA(TypeKeyword):
    """Initial direction of primary particles is sampled uniformly within a rectangular beam.
    
    Rectangular source beam. Limiting polar and azimuthal angles
    of the source beam window, (THETAL,THETAU)x(PHIL,PHIU), in deg.
    
    The case THETAL=THETAU, PHIL=PHIU defines a monodirectional
    source. To define an isotropic source, set THETAL=0, THETAU=
    180, PHIL=0 and PHIU=360.
    """

    def __init__(self):
        super().__init__("SRECTA", (float, float, float, float),
                         comment="Rectangular beam; angles in deg")

    def set(self, thetal, thetau, phil, phiu):
        """
        Sets angles.
        
        Args:
            thetal (float): Lower limit polar angle in deg.
            thetau (float): Upper limit polar angle in deg.
            phil (float): Lower limit azimuthal angle in deg.
            phiu (float): Upper limit azimuthal angle in deg.
        """
        super().set(thetal, thetau, phil, phiu)

class MFNAME(TypeKeyword):
    """Name of a PENELOPE input material data file.
    
    This file must be generated in advance by running the program MATERIAL.
    """

    def __init__(self):
        super().__init__("MFNAME", (str,),
                         comment="Material file, up to 20 chars")

    def set(self, filename):
        """
        Sets filename.
        
        Args:
            filename (str): File name of material file (up to 20 characters).
        """
        super().set(filename)

class MSIMPA(TypeKeyword):
    """Set of simulation parameters for this material
    
    * absorption energies, EABS(1:3,M), 
    * elastic scattering parameters, C1(M) and C2(M), and 
    * cutoff energy losses for inelastic collisions and Bremsstrahlung emission, 
      WCC(M) and WCR(M).
    """

    def __init__(self):
        super().__init__("MSIMPA", (float, float, float, float, float, float, float),
                         comment="EABS(1:3),C1,C2,WCC,WCR")

    def set(self, eabs1, eabs2, eabs3, c1, c2, wcc, wcr):
        """
        Sets parameters.
        
        Args:
            eabs1 (float): Absorption energy of electrons in eV.
            eabs2 (float): Absorption energy of photons in eV.
            eabs3 (float): Absorption energy of positrons in eV.
            c1 (float): Elastic scattering coefficient.
            c2 (float): Elastic scattering coefficient.
            wcc (float): Cutoff energy losses for inelastic collisions in eV.
            wcr (float): Cutoff energy losses for Bremsstrahlung emission in eV.
        """
        super().set(eabs1, eabs2, eabs3, c1, c2, wcc, wcr)

class MaterialGroup(KeywordGroupBase):
    """Group to define both material file name and its simulation parameters."""

    def __init__(self):
        super().__init__()
        self.MFNAME = MFNAME()
        self.MSIMPA = MSIMPA()
        self.index = None

    def set(self, filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr, index=None):
        """
        Sets material file name and simulation parameters.
        
        Args:
            filename (str): File name of material file (up to 20 characters).
            eabs1 (float): Absorption energy of electrons in eV.
            eabs2 (float): Absorption energy of photons in eV.
            eabs3 (float): Absorption energy of positrons in eV.
            c1 (float): Elastic scattering coefficient.
            c2 (float): Elastic scattering coefficient.
            wcc (float): Cutoff energy losses for inelastic collisions in eV.
            wcr (float): Cutoff energy losses for Bremsstrahlung emission in eV.
            index (int, optional): Index of this material in the geometry
        """
        self.MFNAME.set(filename)
        self.MSIMPA.set(eabs1, eabs2, eabs3, c1, c2, wcc, wcr)
        self.index = index

    def get_keywords(self):
        return (self.MFNAME, self.MSIMPA)

class Materials(KeywordSequence):
    """Definition of materials."""

    def __init__(self, maxlength=10):
        keyword = MaterialGroup()
        super().__init__(keyword, maxlength)

    def add(self, index, filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr):
        """
        Adds a new material.
        
        Args:
            index (int): Index of this material in the geometry
            filename (str): File name of material file (up to 20 characters).
            eabs1 (float): Absorption energy of electrons in eV.
            eabs2 (float): Absorption energy of photons in eV.
            eabs3 (float): Absorption energy of positrons in eV.
            c1 (float): Elastic scattering coefficient.
            c2 (float): Elastic scattering coefficient.
            wcc (float): Cutoff energy losses for inelastic collisions in eV.
            wcr (float): Cutoff energy losses for Bremsstrahlung emission in eV.
        """
        return super().add(filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr, index)

    def _add_keyword(self, keyword):
        super()._add_keyword(keyword)
        if keyword.index is None:
            keyword.index = len(self._keywords)

    def get(self):
        values = []
        for keyword in sorted(self._keywords, key=attrgetter('index')):
            values.append(keyword.get())
        return (tuple(values),)

    def write(self, fileobj):
        for keyword in sorted(self._keywords, key=attrgetter('index')):
            keyword.write(fileobj)

class GEOMFN(TypeKeyword):
    """Name of geometry definition file.
    
    The bodies in the material structure are normally identified
    by the sequential labels assigned by PENGEOM. For complex
    geometries, however, it may be more practical to employ user
    labels, i.e., the four-character strings that identify the
    body in the geometry definition file. In PENMAIN (and only
    in the parts of the code that follow the definition of the
    geometry), a body can be specified by giving either its
    PENGEOM numerical label or its user label enclosed in a
    pair of apostrophes (e.g., 'BOD1'). However, bodies that
    result from the cloning of modules (as well as those defined
    in an INCLUDEd geometry file) do not have a user label and
    only the PENGEOM numerical label is acceptable.
    """

    def __init__(self):
        super().__init__("GEOMFN", (str,),
                         comment='Geometry file, up to 20 chars')

    def set(self, filename):
        """
        Sets filename.
        
        Args:
            filename (str): File name of material file (up to 20 characters).
        """
        super().set(filename)

class DSMAX(KeywordSequence):
    """Maximum step length of electrons and positrons in body. 
    
    .. note::
       This parameter is important only for thin bodies; it should be given a 
       value of the order of one tenth of the body thickness or less.
    """

    def __init__(self, maxlength=5000):
        keyword = TypeKeyword("DSMAX", (int, float),
                              comment="KB, maximum step length in body KB")
        super().__init__(keyword, maxlength)

    def add(self, kb, dsmax):
        """
        Sets maximum step length.
        
        Args:
            kb (int): Index of body.
            dsmax: Maximum step length in cm.
        """
        return super().add(kb, dsmax)

class EABSB(KeywordSequence):
    """Local absorption energies EABSB(KPAR,KB) of particles of type KPAR in body KB. 
    
    These values must be larger than EABS(KPAR,M), where M is the material of body KB. When the
    particle is moving within body KB, the absorption energy
    EABS(KPAR,M) is temporarily set equal to EABSB(KPAR,KB).
    Thus, the simulation of the particle history is discontinued
    when the energy becomes less than EABSB(KPAR,KB). This
    feature can be used, e.g., to reduce the simulation work in
    regions of lesser interest.
    """

    def __init__(self, maxlength=5000):
        keyword = TypeKeyword("EABSB", (int, float, float, float),
                              comment="KB, local absorption energies, EABSB(1:3)")
        super().__init__(keyword, maxlength)

    def add(self, kb, eabs1, eabs2, eabs3):
        """
        Sets local absorption energies.
        
        Args:
            kb (int): Index of body.
            eabs1 (float): Absorption energy of electrons in eV.
            eabs2 (float): Absorption energy of photons in eV.
            eabs3 (float): Absorption energy of positrons in eV.
        """
        return super().add(kb, eabs1, eabs2, eabs3)

class InteractionForcings(KeywordSequence):
    """Forcing of interactions. 
    
    FORCER is the forcing factor, which must
    be larger than unity. WLOW and WHIG are the lower and upper
    limits of the pweight window where interaction forcing is
    applied. When several interaction mechanisms are forced in
    the same body, the effective weight window is set equal to
    the intersection of the windows for these mechanisms.
    
    If the mean free path for real interactions of type ICOL is
    MFP, the program will simulate interactions of this type
    (real or forced) with an effective mean free path equal to
    MFP/FORCER.
    
    .. hint::
       A negative input value of FORCER, -FN, is assumed to mean that a particle 
       with energy E=EPMAX should interact, on average, +FN times in the course 
       of its slowing down to rest, for electrons and positrons, or along a mean
       free path, for photons. This is very useful, e.g., to generate x-ray 
       spectra from bulk samples.
    """

    def __init__(self, maxlength=120000):
        keyword = TypeKeyword("IFORCE", (int, KPAR, ICOL, float, float, float),
                              comment="KB,KPAR,ICOL,FORCER,WLOW,WHIG")
        super().__init__(keyword, maxlength)

    def add(self, kb, kpar, icol, forcer, wlow, whig):
        """
        Adds forcing for an interaction.
        
        Args:
            kb (int): Index of body.
            kparp (:class:`KPAR`): Type of primary particles
        """
        return super().add(kb, kpar, icol, forcer, wlow, whig)

class IBRSPL(KeywordSequence):
    """Bremsstrahlung splitting for electrons and positrons.
    
    .. note:: 
       Note that bremsstrahlung splitting is applied in combination
       with interaction forcing and, consequently, it is activated
       only in those bodies where interaction forcing is active.
    """

    def __init__(self, maxlength=5000):
        keyword = TypeKeyword("IBRSPL", (int, float),
                              comment="KB,splitting factor")
        super().__init__(keyword, maxlength)

    def add(self, kb, ibrspl):
        """
        Add Bremsstrahlung splitting.
        
        Args:
            kb (int): Index of body.
            ibrspl (int): Splitting factor.
        """
        return super().add(kb, ibrspl)

class IXRSPL(KeywordSequence):
    """Splitting of characteristic x rays emitted. 
    
    Each unsplit x ray with ILB(2)=2 (i.e., of the second generation) when 
    extracted from the secondary stack is split into IXRSPL quanta. 
    The new, lighter, quanta are assigned random directions distributed 
    isotropically.
    """

    def __init__(self, maxlength=5000):
        keyword = TypeKeyword("IXRSPL", (int, float),
                              comment="KB,splitting factor")
        super().__init__(keyword, maxlength)

    def add(self, kb, ixrspl):
        """
        Add characteristic x rays splitting.
        
        Args:
            kb (int): Index of body.
            ixrspl (int): Splitting factor.
        """
        return super().add(kb, ixrspl)

class NBE(TypeKeyword):
    """Definition of energy distributions of emerging particles."""

    def __init__(self):
        super().__init__("NBE", (float, float, int),
                         comment="Energy window and no. of bins")

    def set(self, el, eu, nbe):
        """
        Sets energy distributions.
        
        Args:
            el (float): Lower limit in eV.
            eu (float): Upper limit in eV.
            nbe (int): Number of bins in the output energy distribution.
                Should be less than 1000. 
                If NBE is positive, energy bins have uniform width, 
                DE=(EU-EL)/NBE. 
                When NBE is negative, the bin width increases geometrically 
                with the energy, i.e., the energy bins have uniform width on a 
                logarithmic scale.
        """
        super().set(el, eu, nbe)

class NBANGL(TypeKeyword):
    """Definition of angular distributions of emerging particles.
    
    .. note::
       In the output files, the terms 'upbound' and 'downbound' are used to 
       denote particles that leave the material system moving upwards (W>0) and 
       downwards (W<0), respectively.
    """

    def __init__(self):
        super().__init__("NBANGL", (int, int),
                         comment="No. of bins for the angles THETA and PHI")

    def set(self, nbth, nbph):
        """
        Sets angular distributions.
        
        Args:
            nbth (int): Numbers of bins for the polar angle THETA. 
                Should be less than 3600.
                If NBTH is positive, angular bins have uniform width,
                DTH=180./NBTHE. 
                When NBTH is negative, the bin width increases geometrically 
                with THETA, i.e., the bins have uniform width on a logarithmic 
                scale.
            nbph (int): Number of bins for the azimuthal angle PHI
                Should be less than 180.
        """
        super().set(nbth, nbph)

#TODO: Fix ENDETC, EDSPC. It should be a KeywordSequence
class ENDETC(TypeKeyword):
    """Definition of an energy-deposition detector."""

    def __init__(self):
        super().__init__('ENDETC', (float, float, int),
                         comment='Energy window and no. of bins')

    def set(self, el, eu, nbe):
        """
        Sets energy limits.
        
        Args:
            el (float): Lower limit in eV.
            eu (float): Upper limit in eV.
            nbe (int): Number of bins in the output energy distribution.
                Should be less than 1000. 
                If NBE is positive, energy bins have uniform width, 
                DE=(EU-EL)/NBE. 
                When NBE is negative, the bin width increases geometrically 
                with the energy, i.e., the energy bins have uniform width on a 
                logarithmic scale.
        """
        super().set(el, eu, nbe)

class EDSPC(TypeKeyword):
    """Name of the output spectrum file."""

    def __init__(self):
        super().__init__('EDSPC', (str,),
                         comment='Output spectrum file name, 20 chars')

    def set(self, filename):
        """
        Sets filename.
        
        Args:
            filename (str): File name of output spectrum file (up to 20 characters).
        """
        super().set(filename)

class GRIDX(TypeKeyword):
    """Definition of x-coordinates of the vertices of the dose box."""

    def __init__(self):
        super().__init__('GRIDX', (float, float, int),
                         comment='X coords of the box vertices, no. of bins')

    def set(self, xl, xu, ndbx):
        """
        Sets dimensions.
        
        Args:
            xl (float): Lower limit of the dose box along the x-axis in cm.
            xu (float): Upper limit of the dose box along the x-axis in cm.
            ndbx (int): Number of bins (i.e. voxels) along the x-axis.
        """
        super().set(xl, xu, ndbx)

class GRIDY(TypeKeyword):
    """Definition of y-coordinates of the vertices of the dose box."""

    def __init__(self):
        super().__init__('GRIDY', (float, float, int),
                         comment='Y coords of the box vertices, no. of bins')

    def set(self, yl, yu, ndby):
        """
        Sets dimensions.
        
        Args:
            yl (float): Lower limit of the dose box along the y-axis in cm.
            yu (float): Upper limit of the dose box along the y-axis in cm.
            ndby (int): Number of bins (i.e. voxels) along the y-axis.
        """
        super().set(yl, yu, ndby)

class GRIDZ(TypeKeyword):
    """Definition of z-coordinates of the vertices of the dose box."""

    def __init__(self):
        super().__init__('GRIDZ', (float, float, int),
                         comment='Z coords of the box vertices, no. of bins')

    def set(self, zl, zu, ndbz):
        """
        Sets dimensions.
        
        Args:
            zl (float): Lower limit of the dose box along the z-axis in cm.
            zu (float): Upper limit of the dose box along the z-axis in cm.
            ndbz (int): Number of bins (i.e. voxels) along the z-axis.
        """
        super().set(zl, zu, ndbz)

class RESUME(TypeKeyword):
    """Name of the resume file.
    
    The program will read the dump file named ``dump1.dmp`` and resume the 
    simulation from the point where it was left. 
    
    .. warning::
       Use this option very, **VERY** carefully.
       Make sure that the input data file is fully consistent with the one used 
       to generate the dump file.
    """

    def __init__(self):
        super().__init__('RESUME', (str,),
                         comment='Resume from this dump file, 20 chars')

    def set(self, filename):
        """
        Sets filename.
        
        Args:
            filename (str): File name of resume file (up to 20 characters).
        """
        super().set(filename)

class DUMPTO(TypeKeyword):
    """Name of dump file.
    
    Generate a dump file named 'dump2.dmp' after completing the simulation run. 
    This allows the simulation to be resumed later on to improve statistics.
    
    .. note:: 
       If the file 'dump2.dmp' already exists, it is overwritten.
    """

    def __init__(self):
        super().__init__('DUMPTO', (str,),
                         comment='Generate this dump file, 20 chars')

    def set(self, filename):
        """
        Sets filename.
        
        Args:
            filename (str): File name of dump file (up to 20 characters).
        """
        super().set(filename)

class DUMPP(TypeKeyword):
    """Dump interval.
    
    When the DUMPTO option is activated, simulation results are written in the 
    output files every DUMPP seconds. 
    This option is useful to check the progress of long simulations. 
    It also allows the program to be run with a long execution time and to be 
    stopped when the required statistical uncertainty has been reached.
    """

    def __init__(self):
        super().__init__('DUMPP', (float,), comment='Dumping period, in sec')

    def set(self, dumpp):
        """
        Sets interval.
        
        Args:
            dumpp (int): Dump interval in seconds.
        """
        super().set(dumpp)

class RSEED(TypeKeyword):
    """Seeds of the random-number generator."""

    def __init__(self):
        super().__init__('RSEED', (int, int),
                         comment='Seeds of the random-number generator')

    def set(self, iseed1, iseed2):
        """
        Sets seeds.
        
        Args:
            iseed1 (int): First seed.
                When ISEED1 is equal to a negative integer, -N, the seeds are 
                set by calling subroutine RAND0(N) with the input argument 
                equal to N.
                This ensures that sequences of random numbers used in different
                runs of the program (with different values of N) are truly
                independent.
            iseed2 (int): Second seed.
        """
        super().set(iseed1, iseed2)

class NSIMSH(TypeKeyword):
    """Desired number of simulated showers."""

    def __init__(self):
        super().__init__('NSIMSH', (float,),
                         comment='Desired number of simulated showers')

    def set(self, dshn):
        """
        Sets showers.
        
        Args:
            dshn (int): Number of simulated showers.
        """
        super().set(dshn)

class TIME(TypeKeyword):
    """Allotted simulation time."""

    def __init__(self):
        super().__init__('TIME', (float,),
                         comment='Allotted simulation time, in sec')

    def set(self, timea):
        """
        Sets simulation time.
        
        Args:
            timea (int): Allotted simulation time in seconds.
        """
        super().set(timea)

