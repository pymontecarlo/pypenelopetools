""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.keyword import \
    TypeKeyword, KeywordSequence, KeywordGroup, filename_type, module_type
from pypenelopetools.material.material import Material

# Globals and constants variables.

class TITLE(TypeKeyword):
    """
    Title of the job (up to 65 characters).
    DEFAULT: none (the input file must start with this line)
    
    The TITLE string is used to mark dump files. To prevent the
    improper use of wrong resuming files, change the title each
    time you modify basic parameters of your problem. The code
    will then be able to identify the inconsistency and to print
    an error message before stopping.
    """

    def __init__(self):
        super().__init__('TITLE', (str,))

    def _extract_name_values_comment(self, line):
        name, values, comment = super()._extract_name_values_comment(line)
        return name, (' '.join(values),), comment

    def set(self, title):
        super().set(title)

    def validate(self, title):
        if len(title) > 65:
            raise ValueError('Title is too long. Maximum 65 characters')
        return super().validate(title)

class SKPAR(TypeKeyword):
    """
    Type of primary particle KPARP (1=electrons, 2=photons or
    3=positrons).
      DEFAULT: KPARP=1
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
        super().set(kparp)

    def validate(self, kparp):
        if kparp not in [0, 1, 2, 3]:
            raise ValueError('Invalid particle')
        return super().validate(kparp)

class SENERG(TypeKeyword):
    """
    For a monoenergetic source, initial energy SE0 of primary
    particles.
    DEFAULT: SE0=1.0E6
    """

    def __init__(self):
        super().__init__('SENERG', (float,),
                         comment="Initial energy (monoenergetic sources only)")

    def set(self, se0):
        super().set(se0)

    def validate(self, se0):
        if se0 <= 0.0:
            raise ValueError('SE0 must be greater than 0')
        return super().validate(se0)

class SPECTR(KeywordSequence):
    """
    For a source with continuous (stepwise constant) spectrum,
    each 'SPECTR' line gives the lower end-point of an energy
    bin of the source spectrum (Ei) and the associated relative
    probability (Pi), integrated over the bin. Up to NSEM=1000
    lines, in arbitrary order. The upper end of the spectrum is
    defined by entering a line with Ei equal to the upper energy
    end point and with a negative Pi value.
      DEFAULT: none
    """

    def __init__(self):
        keyword = TypeKeyword('SPECTR', (float, float),
                              comment='E bin: lower-end and total probability')
        super().__init__(keyword)

    def set(self, ei, pi):
        return super().set(ei, pi)

    def add(self, ei, pi):
        return super().add(ei, pi)

class SGPOL(TypeKeyword):
    """
    This line activates the simulation of polarisation effects
    in the scattering of photons (electrons and positrons are
    assumed to be unpolarised). SP1, SP2, SP3 are the Stokes
    parameters of primary photons, which define the degrees of
    linear polarisation at 45 deg azimuth, of circular
    polarisation, and of linear polarisation at zero azimuth,
    respectively. It is assumed that secondary photons are
    emitted with null polarisation (SP1=SP2=SP3=0).
      DEFAULT: none
    """

    def __init__(self):
        super().__init__('SGPOL', (float, float, float),
                         comment="Stokes parameters for polarized photons")

    def set(self, sp1, sp2, sp3):
        super().set(sp1, sp2, sp3)

class SPOSIT(TypeKeyword):
    """
    Coordinates of the source centre.
    """

    def __init__(self):
        super().__init__("SPOSIT", (float, float, float),
                         comment="Coordinates of the source")

    def set(self, sx0, sy0, sz0):
        super().set(sx0, sy0, sz0)

class SCONE(TypeKeyword):
    """
    The initial direction of primary particles is sampled uniformly
    within a circle on the unit sphere (conical beam), or within a
    'rectangular' window on the unit sphere (rectangular beam).
    
    Conical source beam. Polar and azimuthal angles of the
    beam axis direction, THETA and PHI, and angular aperture,
    ALPHA, in deg.
      DEFAULTS: THETA=0.0, PHI=0.0, ALPHA=0.0
    
    The case ALPHA=0 defines a monodirectional source, and ALPHA
    =180 deg corresponds to an isotropic source.
    """

    def __init__(self):
        super().__init__("SCONE", (float, float, float),
                         comment="Conical beam; angles in deg")

    def set(self, theta, phi, alpha):
        super().set(theta, phi, alpha)

class SRECTA(TypeKeyword):
    """
    The initial direction of primary particles is sampled uniformly
    within a 'rectangular' window on the unit sphere (rectangular beam).
    
    Rectangular source beam. Limiting polar and azimuthal angles
    of the source beam window, (THETAL,THETAU)x(PHIL,PHIU), in deg.
      DEFAULTS: THETAL=0.0, THETAU=0.0, PHIL=0.0, PHIU=0.0
    
    The case THETAL=THETAU, PHIL=PHIU defines a monodirectional
    source. To define an isotropic source, set THETAL=0, THETAU=
    180, PHIL=0 and PHIU=360.
    """

    def __init__(self):
        super().__init__("SRECTA", (float, float, float, float),
                         comment="Rectangular beam; angles in deg")

    def set(self, thetal, thetau, phil, phiu):
        super().set(thetal, thetau, phil, phiu)

class MaterialGroup(KeywordGroup):
    """
    Name of a PENELOPE input material data file (up to 20
    characters). This file must be generated in advance by
    running the program MATERIAL.
      DEFAULT: none
      
    Set of simulation parameters for this material; absorption
    energies, EABS(1:3,M), elastic scattering parameters, C1(M)
    and C2(M), and cutoff energy losses for inelastic collisions
    and bremsstrahlung emission, WCC(M) and WCR(M).
      DEFAULTS: EABS(1,M)=EABS(3,M)=0.01*EPMAX,
                EABS(2,M)=0.001*EPMAX
                C1(M)=C2(M)=0.1, WCC=EABS(1,M), WCR=EABS(2,M)
    EPMAX is the upper limit of the energy interval covered by
    the simulation lookup tables.
    """

    def __init__(self):
        super().__init__()
        self.MFNAME = TypeKeyword("MFNAME", (filename_type,),
                                  comment="Material file, up to 20 chars")
        self.MSIMPA = \
            TypeKeyword("MSIMPA", (float, float, float, float, float, float, float),
                        comment="EABS(1:3),C1,C2,WCC,WCR")

    def set(self, material_or_filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr):
        if isinstance(material_or_filename, Material):
            filename = material_or_filename.filename
        else:
            filename = str(material_or_filename)
        self.MFNAME.set(filename)
        self.MSIMPA.set(eabs1, eabs2, eabs3, c1, c2, wcc, wcr)

    def get_keywords(self):
        return (self.MFNAME, self.MSIMPA)

class Materials(KeywordSequence):

    def __init__(self):
        keyword = MaterialGroup()
        super().__init__(keyword)

    def set(self, material_or_filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr):
        return super().set(material_or_filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr)

    def add(self, material_or_filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr):
        return super().add(material_or_filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr)

class DSMAX(KeywordSequence):
    """
    Maximum step length DSMAX(KB) of electrons and positrons in
    body KB. This parameter is important only for thin bodies;
    it should be given a value of the order of one tenth of the
    body thickness or less.
      DEFAULT: DSMAX=1.0E20 (no step length control)
    """

    def __init__(self):
        keyword = TypeKeyword("DSMAX", (module_type, float),
                              comment="KB, maximum step length in body KB")
        super().__init__(keyword)

    def set(self, kb, dsmax):
        return super().set(kb, dsmax)

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
        keyword = TypeKeyword("EABSB", (module_type, float, float, float),
                              comment="KB, local absorption energies, EABSB(1:3)")
        super().__init__(keyword)

    def set(self, kb, eabs1, eabs2, eabs3):
        return super().set(kb, eabs1, eabs2, eabs3)

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
        keyword = TypeKeyword("IFORCE", (module_type, int, int, float, float, float),
                              comment="KB,KPAR,ICOL,FORCER,WLOW,WHIG")
        super().__init__(keyword)

    def set(self, kb, kpar, icol, forcer, wlow, whig):
        return super().set(kb, kpar, icol, forcer, wlow, whig)

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
        keyword = TypeKeyword("IBRSPL", (module_type, float),
                              comment="KB,splitting factor")
        super().__init__(keyword)

    def set(self, kb, ibrspl):
        return super().set(kb, ibrspl)

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
        keyword = TypeKeyword("IXRSPL", (module_type, float),
                              comment="KB,splitting factor")
        super().__init__(keyword)

    def set(self, kb, ixrspl):
        return super().set(kb, ixrspl)

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
        super().__init__('EDSPC', (filename_type,),
                         comment='Output spectrum file name, 20 chars')

    def set(self, filename):
        super().set(filename)

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
        super().__init__('RESUME', (filename_type,),
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
        super().__init__('DUMPTO', (filename_type,),
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

