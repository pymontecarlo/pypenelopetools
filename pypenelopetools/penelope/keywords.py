""""""

# Standard library modules.
from operator import attrgetter

# Third party modules.

# Local modules.
from pypenelopetools.penelope.keyword import \
    TypeKeyword, KeywordSequence, KeywordGroup

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
            title (str): title of the job (up to 65 characters).
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
        super().__init__('SKPAR', (int,),
                         comment="Primary particles: 1=electron, 2=photon, 3=positron")

    def set(self, kparp):
        """
        Sets value.
        
        Args:
            kparp (int): Type of primary particles.
                0=user defined, 1=electrons, 2=photons or 3=positrons
        """
        super().set(kparp)

    def validate(self, kparp):
        if kparp not in [0, 1, 2, 3]:
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

    def __init__(self):
        keyword = TypeKeyword('SPECTR', (float, float),
                              comment='E bin: lower-end and total probability')
        super().__init__(keyword)

    def add(self, ei, pi):
        """
        Adds a step in the spectrum.
        
        Args:
            ei (float): lower end-point of an energy bin of the source spectrum in eV
            pi (float): associated relative probability
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
            sp1 (float): degrees of linear polarisation at 45 deg azimuth
            sp2 (float): degrees of circular polarisation
            sp3 (float): degrees of linear polarisation at 0 deg azimuth
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
            theta (float): polar angle of the beam axis direction in deg.
            phi (float): azimuthal angle of the beam axis direction in deg.
            alpha (float): angular aperture in deg.
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
            thetal (float): lower limit polar angle in deg.
            thetau (float): upper limit polar angle in deg.
            phil (float): lower limit azimuthal angle in deg.
            phiu (float): upper limit azimuthal angle in deg.
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
            filename (str): file name of material file (up to 20 characters).
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
            eabs1 (float): absorption energy of electrons.
            eabs2 (float): absorption energy of photons.
            eabs3 (float): absorption energy of positrons.
            c1 (float): elastic scattering coefficient.
            c2 (float): elastic scattering coefficient.
            wcc (float): cutoff energy losses for inelastic collisions.
            wcr (float): cutoff energy losses for Bremsstrahlung emission.
        """
        super().set(eabs1, eabs2, eabs3, c1, c2, wcc, wcr)

class MaterialGroup(KeywordGroup):
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
            filename (str): file name of material file (up to 20 characters).
            eabs1 (float): absorption energy of electrons.
            eabs2 (float): absorption energy of photons.
            eabs3 (float): absorption energy of positrons.
            c1 (float): elastic scattering coefficient.
            c2 (float): elastic scattering coefficient.
            wcc (float): cutoff energy losses for inelastic collisions.
            wcr (float): cutoff energy losses for Bremsstrahlung emission.
            index (int, optional): index of this material in the geometry
        """
        self.MFNAME.set(filename)
        self.MSIMPA.set(eabs1, eabs2, eabs3, c1, c2, wcc, wcr)
        self.index = index

    def get_keywords(self):
        return (self.MFNAME, self.MSIMPA)

class Materials(KeywordSequence):
    """All materials of a simulation."""

    def __init__(self):
        keyword = MaterialGroup()
        super().__init__(keyword)

    def add(self, index, filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr):
        """
        Adds a new material.
        
        Args:
            index (int): index of this material in the geometry
            filename (str): file name of material file (up to 20 characters).
            eabs1 (float): absorption energy of electrons.
            eabs2 (float): absorption energy of photons.
            eabs3 (float): absorption energy of positrons.
            c1 (float): elastic scattering coefficient.
            c2 (float): elastic scattering coefficient.
            wcc (float): cutoff energy losses for inelastic collisions.
            wcr (float): cutoff energy losses for Bremsstrahlung emission.
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
    """PENGEOM geometry definition file name.
    
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
            filename (str): file name of material file (up to 20 characters).
        """
        super().set(filename)

class DSMAX(KeywordSequence):
    """
    Maximum step length DSMAX(KB) of electrons and positrons in
    body KB. This parameter is important only for thin bodies;
    it should be given a value of the order of one tenth of the
    body thickness or less.
      DEFAULT: DSMAX=1.0E20 (no step length control)
    """

    def __init__(self):
        keyword = TypeKeyword("DSMAX", (int, float),
                              comment="KB, maximum step length in body KB")
        super().__init__(keyword)

    def add(self, kb, dsmax):
        return super().add(kb, dsmax)

class EABSB(KeywordSequence):
    """
    Local absorption energies EABSB(KPAR,KB) of particles of
    type KPAR in body KB. These values must be larger than
    EABS(KPAR,M), where M is the material of body KB. When the
    particle is moving within body KB, the absorption energy
    EABS(KPAR,M) is temporarily set equal to EABSB(KPAR,KB).
    Thus, the simulation of the particle history is discontinued
    when the energy becomes less than EABSB(KPAR,KB). This
    feature can be used, e.g., to reduce the simulation work in
    regions of lesser interest.
        DEFAULTS: EABSB(KPAR,KB)=EABS(KPAR,M)  (no action)
    """

    def __init__(self):
        keyword = TypeKeyword("EABSB", (int, float, float, float),
                              comment="KB, local absorption energies, EABSB(1:3)")
        super().__init__(keyword)

    def add(self, kb, eabs1, eabs2, eabs3):
        return super().add(kb, eabs1, eabs2, eabs3)

class IFORCE(KeywordSequence):
    """
    Activates forcing of interactions of type ICOL of particles
    KPAR in body KB. FORCER is the forcing factor, which must
    be larger than unity. WLOW and WHIG are the lower and upper
    limits of the weight window where interaction forcing is
    applied. When several interaction mechanisms are forced in
    the same body, the effective weight window is set equal to
    the intersection of the windows for these mechanisms.
      DEFAULT: no interaction forcing
    
    If the mean free path for real interactions of type ICOL is
    MFP, the program will simulate interactions of this type
    (real or forced) with an effective mean free path equal to
    MFP/FORCER.
    
    TRICK: a negative input value of FORCER, -FN, is assumed to
    mean that a particle with energy E=EPMAX should interact,
    on average, +FN times in the course of its slowing down to
    rest, for electrons and positrons, or along a mean free
    path, for photons. This is very useful, e.g., to generate
    x-ray spectra from bulk samples.
    """

    def __init__(self):
        keyword = TypeKeyword("IFORCE", (int, int, int, float, float, float),
                              comment="KB,KPAR,ICOL,FORCER,WLOW,WHIG")
        super().__init__(keyword)

    def add(self, kb, kpar, icol, forcer, wlow, whig):
        return super().add(kb, kpar, icol, forcer, wlow, whig)

class IBRSPL(KeywordSequence):
    """
    Activates bremsstrahlung splitting in body KB for electrons
    and positrons with weights in the window (WLOW,WHIG) where
    interaction forcing is applied. The integer IBRSPL is the
    splitting factor.
      DEFAULT: no bremsstrahlung splitting
    
    Note that bremsstrahlung splitting is applied in combination
    with interaction forcing and, consequently, it is activated
    only in those bodies where interaction forcing is active.
    """

    def __init__(self):
        keyword = TypeKeyword("IBRSPL", (int, float),
                              comment="KB,splitting factor")
        super().__init__(keyword)

    def add(self, kb, ibrspl):
        return super().add(kb, ibrspl)

class IXRSPL(KeywordSequence):
    """
    Splitting of characteristic x rays emitted in body KB, from
    any element. Each unsplit x ray with ILB(2)=2 (i.e., of the
    second generation) when extracted from the secondary stack
    is split into IXRSPL quanta. The new, lighter, quanta are
    assigned random directions distributed isotropically.
      DEFAULT: no x-ray splitting
    """

    def __init__(self):
        keyword = TypeKeyword("IXRSPL", (int, float),
                              comment="KB,splitting factor")
        super().__init__(keyword)

    def add(self, kb, ixrspl):
        return super().add(kb, ixrspl)

class NBE(TypeKeyword):
    """
    Limits EL and EU of the interval where energy distributions
    of emerging particles are tallied. Number of energy bins
    (.LE. 1000).
      DEFAULT: EL=0.0, EU=EPMAX, NBE=500
    
    NBE is the number of bins in the output energy distribution
    (.LE. 1000). If NBE is positive, energy bins have uniform
    width, DE=(EU-EL)/NBE. When NBE is negative, the bin width
    increases geometrically with the energy, i.e., the energy
    bins have uniform width on a logarithmic scale.
    """

    def __init__(self):
        super().__init__("NBE", (float, float, int),
                         comment="Energy window and no. of bins")

    def set(self, el, eu, nbe):
        super().set(el, eu, nbe)

class NBANGL(TypeKeyword):
    """
    Numbers of bins for the polar angle THETA and the azimuthal
    angle PHI, respectively, NBTH and NBPH (.LE. 3600 and 180,
    respectively).
      DEFAULT: NBTH=90, NBPH=1 (azimuthal average)
    
    If NBTH is positive, angular bins have uniform width,
    DTH=180./NBTHE. When NBTH is negative, the bin width
    increases geometrically with THETA, i.e., the bins have
    uniform width on a logarithmic scale.
    
    NOTE: In the output files, the terms 'upbound' and
    'downbound' are used to denote particles that leave the
    material system moving upwards (W>0) and downwards (W<0),
    respectively.
    """

    def __init__(self):
        super().__init__("NBANGL", (int, int),
                         comment="No. of bins for the angles THETA and PHI")

    def set(self, nbth, nbph):
        super().set(nbth, nbph)

class ENDETC(TypeKeyword):
    """
    Starts the definition of a new energy-deposition detector.
    Up to 25 different detectors can be considered.
    EL and EU are the lower and upper limits of the energy
      window covered by the detector.
    NBE is the number of bins in the output energy spectrum of
      the detector (.LE. 1000). If NBE is positive, energy bins
      have uniform width, DE=(EU-EL)/NBE. When NBE is negative,
      the bin width increases geometrically with the energy,
      i.e., the energy bins have uniform width on a logarithmic
      scale.
    
      DEFAULTS: None
    """

    def __init__(self):
        super().__init__('ENDETC', (float, float, int),
                         comment='Energy window and no. of bins')

    def set(self, el, eu, nbe):
        super().set(el, eu, nbe)

class EDSPC(TypeKeyword):
    """
    Name of the output spectrum file (up to 20 characters).
        DEFAULT: 'spc-enddet-##.dat'
    """

    def __init__(self):
        super().__init__('EDSPC', (str,),
                         comment='Output spectrum file name, 20 chars')

    def set(self, filename):
        super().set(filename)

class GRIDX(TypeKeyword):
    """
    Generally, the program can calculate the dose distribution inside a
    parallelepiped (dose box) whose edges are parallel to the axes of the
    laboratory frame. The dose box is defined by giving the coordinates
    of its vertices. The dose is tallied using a uniform orthogonal grid
    with NDBX, NDBY and NDBZ bins (= voxels) along the directions of
    the respective coordinate axes. These numbers should be odd, to make
    sure that each 'central' axis (i.e., the line that join the centres
    of two opposite faces of the box) goes through the centres of a row
    of voxels.
    
    X-coordinates of the vertices of the dose box and number of
    bins in the X direction.
      DEFAULT: None
    """

    def __init__(self):
        super().__init__('GRIDX', (float, float, int),
                         comment='X coords of the box vertices, no. of bins')

    def set(self, xl, xu, ndbx):
        super().set(xl, xu, ndbx)

class GRIDY(TypeKeyword):
    """
    Generally, the program can calculate the dose distribution inside a
    parallelepiped (dose box) whose edges are parallel to the axes of the
    laboratory frame. The dose box is defined by giving the coordinates
    of its vertices. The dose is tallied using a uniform orthogonal grid
    with NDBX, NDBY and NDBZ bins (= voxels) along the directions of
    the respective coordinate axes. These numbers should be odd, to make
    sure that each 'central' axis (i.e., the line that join the centres
    of two opposite faces of the box) goes through the centres of a row
    of voxels.
    
    Y-coordinates of the vertices of the dose box and number of
    bins in the Y direction.
      DEFAULT: None
    """

    def __init__(self):
        super().__init__('GRIDY', (float, float, int),
                         comment='Y coords of the box vertices, no. of bins')

    def set(self, yl, yu, ndby):
        super().set(yl, yu, ndby)

class GRIDZ(TypeKeyword):
    """
    Generally, the program can calculate the dose distribution inside a
    parallelepiped (dose box) whose edges are parallel to the axes of the
    laboratory frame. The dose box is defined by giving the coordinates
    of its vertices. The dose is tallied using a uniform orthogonal grid
    with NDBX, NDBY and NDBZ bins (= voxels) along the directions of
    the respective coordinate axes. These numbers should be odd, to make
    sure that each 'central' axis (i.e., the line that join the centres
    of two opposite faces of the box) goes through the centres of a row
    of voxels.
    
    Z-coordinates of the vertices of the dose box and number of
    bins in the Z direction.
      DEFAULT: None
    """

    def __init__(self):
        super().__init__('GRIDZ', (float, float, int),
                         comment='Z coords of the box vertices, no. of bins')

    def set(self, zl, zu, ndbz):
        super().set(zl, zu, ndbz)

class RESUME(TypeKeyword):
    """
    The program will read the dump file named `dump1.dmp' (up to
    20 characters) and resume the simulation from the point
    where it was left. Use this option very, _VERY_ carefully.
    Make sure that the input data file is fully consistent with
    the one used to generate the dump file.
      DEFAULT: off
    """

    def __init__(self):
        super().__init__('RESUME', (str,),
                         comment='Resume from this dump file, 20 chars')

    def set(self, filename):
        super().set(filename)

class DUMPTO(TypeKeyword):
    """
    Generate a dump file named 'dump2.dmp' (up to 20 characters)
    after completing the simulation run. This allows the
    simulation to be resumed later on to improve statistics.
      DEFAULT: off
    
    NOTE: If the file 'dump2.dmp' already exists, it is
    overwritten.
    """

    def __init__(self):
        super().__init__('DUMPTO', (str,),
                         comment='Generate this dump file, 20 chars')

    def set(self, filename):
        super().set(filename)

class DUMPP(TypeKeyword):
    """
    When the DUMPTO option is activated, simulation results are
    written in the output files every DUMPP seconds. This option
    is useful to check the progress of long simulations. It also
    allows the program to be run with a long execution time and
    to be stopped when the required statistical uncertainty has
    been reached.
      DEFAULT: DUMPP=1.0E15
    """

    def __init__(self):
        super().__init__('DUMPP', (float,), comment='Dumping period, in sec')

    def set(self, dumpp):
        super().set(dumpp)

class RSEED(TypeKeyword):
    """
    Seeds of the random-number generator. When ISEED1 is equal
    to a negative integer, -N, the seeds are set by calling
    subroutine RAND0(N) with the input argument equal to N. This
    ensures that sequences of random numbers used in different
    runs of the program (with different values of N) are truly
    independent.
      DEFAULT: ISEED1=1, ISEED2=1
    """

    def __init__(self):
        super().__init__('RSEED', (int, int),
                         comment='Seeds of the random-number generator')

    def set(self, iseed1, iseed2):
        super().set(iseed1, iseed2)

class NSIMSH(TypeKeyword):
    """
    Desired number of simulated showers.
        DEFAULT: DSHN=2.0E9
    """

    def __init__(self):
        super().__init__('NSIMSH', (float,),
                         comment='Desired number of simulated showers')

    def set(self, dshn):
        super().set(dshn)

class TIME(TypeKeyword):
    """
    Allotted simulation time, in sec.
        DEFAULT: TIMEA=2.0E9
    """

    def __init__(self):
        super().__init__('TIME', (float,),
                         comment='Allotted simulation time, in sec')

    def set(self, timea):
        super().set(timea)

