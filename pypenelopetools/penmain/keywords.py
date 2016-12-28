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
        super().set(ei, pi)

    def add(self, ei, pi):
        super().add(ei, pi)

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

class SBOX(TypeKeyword):
    """
    Extended source box. The source has uniform activity within
    the volume of a right prism centred at the point (SX0,SY0,
    SZ0) and whose sides have lengths SSX, SSY and SSZ.
      DEFAULT: SSX=SSY=SSZ=0.0
    """

    def __init__(self):
        super().__init__("SPOSIT", (float, float, float),
                         comment="Source box dimensions")

    def set(self, ssx, ssy, ssz):
        super().set(ssx, ssy, ssz)

class SBODY(KeywordSequence):
    """
    In the case of a extended source, the active volume can be restricted
    to that of a body or a set of bodies, which must be defined as parts
    of the geometry. The activity of the source is assumed to be uniform
    within the volume of the intersection of the active bodies and the
    source box. Note that the initial coordinates of primary particles
    are sampled by the rejection method; the sampling efficiency is equal
    to the fraction of the source box volume that is occupied by active
    bodies.
    
    To define each active source body, add the following keyword.
    
    Active source body (PENGEOM sequential body label). 
    One line for each body.
    DEFAULT: None
    
    The program stops if the source box has not been defined previously.
    """

    def __init__(self):
        keyword = TypeKeyword("SBODY", (module_type,),
                              comment='Active source body; one line for each body')
        super().__init__(keyword)

    def set(self, kb):
        """
        :arg kb: index of the body or a 
            :class:`Module <pypenelopetools.pengeom.module.Module>` object from 
            a :class:`Geometry <penelopetools.pengeom.geometry.Geometry>` object
        """
        super().set(kb)

    def add(self, kb):
        """
        :arg kb: index of the body or a 
            :class:`Module <pypenelopetools.pengeom.module.Module>` object from 
            a :class:`Geometry <penelopetools.pengeom.geometry.Geometry>` object
        """
        super().add(kb)

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

class IPSFN(KeywordSequence):
    """
    The initial state variables of primary particles can be read directly
    from a set of pre-calculated phase-space files (psf). When this
    option is active, previous definitions about the source are ignored.
    Photons from the psf's are assumed to be unpolarised.
    
    Name of an input psf (up to 20 characters).
        DEFAULT: none
    Up to 100 psf's may be declared. They are read sequentially.
    
    The input psf is in ASCII format. Each line defines the initial state
    of a particle; it contains the following quantities in free format
    (and in the order they are listed here):
    -- KPAR, type of particle (1, electron; 2, photon; 3, positron).
    -- E, energy.
    -- X,Y,Z, position coordinates.
    -- U,V,W, direction cosines.
    -- WGHT, weight.
    -- ILB(1),ILB(2),ILB(3),ILB(4), a set of indices that provide
           information on how the particle was generated (see the file
           'manual.txt').
    -- NSHI, incremental shower number (difference between the shower
           numbers of the present particle and the one preceding it
           in the psf).
    Phase-space files can be generated by running PENMAIN using an impact
    detector with the flag IPSF=1 (see below).
    """

    def __init__(self):
        keyword = TypeKeyword("IPSFN", (filename_type,),
                              comment="Input psf name, up to 20 characters")
        super().__init__(keyword)

    def set(self, filename):
        super().set(filename)

    def add(self, filename):
        super().add(filename)

class IPSPLI(TypeKeyword):
    """
    Because of the limited size of the psf's, the results of analogue
    simulations tend to be 'too noisy'. This can be partially corrected
    by splitting the particles from the psf.
    
    Splitting number. Each particle in the psf's will be split
    into NSPLIT equivalent particles, with weights equal to
    WGHT/NSPLIT.
      DEFAULT: NSPLIT=1 (no splitting)
    """

    def __init__(self):
        super().__init__("IPSPLI", (int,),
                         comment="Splitting number")

    def set(self, nsplit):
        super().set(nsplit)

class WGTWIN(TypeKeyword):
    """
    Weight window, (WGMIN,WGMAX). Particles in the phase-space
    file that have initial weights WGHT less than WGMIN will be
    subjected to Russian roulette, and those with WGHT larger
    than WGMAX will be split. Note that the weight window has
    preference over the splitting option, i.e., a particle will
    be split into NSPLIT or less particles only if the latter
    have weights larger than WGMIN.
      DEFAULTS: WGMIN=1.0E-35, WGMAX=1.0E35  (no action)
    """

    def __init__(self):
        super().__init__("WGTWIN", (float, float),
                         comment="Weight window, RR & spl of psf particles")

    def set(self, wgmin, wgmax):
        super().set(wgmin, wgmax)

class EPMAX(TypeKeyword):
    """
    Maximum energy (in eV) of particles in the psf's.
    EPMAX is the upper limit of the energy interval covered by
    the simulation lookup tables. To minimize interpolation
    errors, EPMAX should not be much larger than the maximum
    energy actually occurring during the simulation.
    
    When the initial state variables of particles are read from
    a psf, this parameter is required to initialise PENELOPE and
    is critical; the code crashes if it finds a particle that
    has energy larger than EPMAX.
      DEFAULT: EPMAX=1.0E9 (interpolation is not optimal)
    """

    def __init__(self):
        super().__init__("EPMAX", (float,),
                         comment="Maximum energy of particles in the psf")

    def set(self, epmax):
        super().set(epmax)

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
        super().set(material_or_filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr)

    def add(self, material_or_filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr):
        super().add(material_or_filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr)

class GEOMFN(TypeKeyword):
    """
    PENGEOM geometry definition file name (a string of up to
    20 characters).
      DEFAULT: none.
    
    --> The geometry definition file can be debugged/visualised
    with the viewers GVIEW2D and GVIEW3D (operable only under
    Windows).
    
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
        super().__init__("GEOMFN", (filename_type,),
                         comment='Geometry file, up to 20 chars')

class PARINP(KeywordSequence):
    """
    The values of certain parameters of the geometry definition
    may be defined from the main program by means of the array
    PARINP (an input argument of the GEOMIN subroutine). The
    entered PARINP(IP) value replaces the parameter values that
    are marked with the index IP in the geometry definition
    file.
      DEFAULT:  none
    """

    def __init__(self):
        keyword = TypeKeyword("PARINP", (int, float),
                              comment="Replacement parameter")
        super().__init__(keyword)

    def set(self, ip, parinp):
        super().set(ip, parinp)

    def add(self, ip, parinp):
        super().add(ip, parinp)

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
        super().set(kb, dsmax)

    def add(self, kb, dsmax):
        super().add(kb, dsmax)

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
        super().set(kb, eabs1, eabs2, eabs3)

    def add(self, kb, eabs1, eabs2, eabs3):
        super().add(kb, eabs1, eabs2, eabs3)

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
        super().set(kb, kpar, icol, forcer, wlow, whig)

    def add(self, kb, kpar, icol, forcer, wlow, whig):
        super().add(kb, kpar, icol, forcer, wlow, whig)

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
        super().set(kb, ibrspl)

    def add(self, kb, ibrspl):
        super().add(kb, ibrspl)

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
        super().set(kb, ixrspl)

    def add(self, kb, ixrspl):
        super().add(kb, ixrspl)

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

class ImpactDetectorGroup(KeywordGroup):
    """
    Each impact detector consists of a set of active bodies, which must
    have been defined as parts of the geometry. The output spectrum is
    the energy distribution of particles that entered any of the active
    bodies coming from a body that is not active (i.e. that is not part
    of the detector). Notice that a detected particle can re-enter the
    detector volume and, consequently, be 'counted' several times (except
    when the flag IDCUT is set equal to 0, see below).
    
    Active bodies cannot be void, because the geometry routines would not
    stop particles at their limiting surfaces. In case you need to define
    detectors outside the material system, fill them with an arbitrary
    material of very small density to avoid perturbing the transport
    process.
    
    To define each impact detector, insert the following block of lines;
    
    IMPDET : Starts the definition of a new detector. Up to 25 different
             detectors can be considered.
             EL and EU are the lower and upper limits of the energy
               window covered by the impact detector.
             NBE is the number of bins in the output energy spectrum of
               the detector (.LE. 1000). If NBE is positive, energy bins
               have uniform width, DE=(EU-EL)/NBE. When NBE is negative,
               the bin width increases geometrically with the energy,
               i.e., the energy bins have uniform width on a logarithmic
               scale.
    
             The integer flag IPSF serves to activate the creation of a
             phase-space file (psf), which contains the state variables
             of all particles that enter the detector. Use this option
             with care, because psf's may grow very fast.
             IPSF=0; no psf is created.
             IPSF=1; the psf is created. Only one PSF can be created in
               each simulation run.
    
             The integer flag IDCUT allows discontinuing the tracking of
             particles that enter the detector.
             IDCUT=0; the simulation of a particle is discontinued when
               it enters the detector (useful to stop the simulation of
               particles recorded in a psf).
             IDCUT=1; the presence of the detector does not affect the
               tracking of particles.
             IDCUT=2; the presence of the detector does not affect the
               tracking of particles. The distribution of particle
               fluence with respect to energy (integrated over the volume
               of the detector) is tallied. The calculated distribution
               has dimensions of length/energy.
    
               DEFAULTS: None
    
    IDPSF_ : Name of the output phase-space file (up to 20 characters).
               DEFAULT: 'psf-impdet-##.dat'
    
    IDSPC_ : Name of the output energy spectrum file (up to 20
             characters).
               DEFAULT: 'spc-impdet-##.dat'
    
    IDFLNC : Name of the output file with the energy distribution of
             particle fluence (20 characters). This file is generated
             only when IDCUT=2.
               DEFAULT: 'fln-impdet-##.dat'
    
    IDAGEL : Activates the evaluation of the age of particles, defined as
             the time elapsed since the start of the primary particle
             that originated the shower. The program generates the age
             distribution of detected particles, i.e., particles of the
             types declared in lines IDKPAR (see below) that enter the
             detector with energy in the window (EL,EU). The distribution
             is tallied for ages in the interval between AGEL and AGEU
             (both in seconds), which is partitioned into NAGE bins. If
             NAGE is positive, the age bins have uniform width. When
             NAGE is negative, the width of age bins is uniform on a
             logarithmic scale.
    
               DEFAULTS: NAGE=100, AGEL=0.0, AGEU must always be
                         specified
    
    IDAGEF : Name of the output age distribution file (up to 20
             characters)
               DEFAULT: 'age-impdet-##.dat'
    
    IDBODY : Active body of the detector. One line for each active body.
               DEFAULT: None
             --> Notice that a body cannot be part of more than one
             impact detector.
    
    IDKPAR : Type of particle that is detected (1=electrons, 2=photons or
             3=positrons). One line for each type.
    
             The detector has no effect for particles that are not
             detected. This feature can be used, e.g., to make a body or
             a set of bodies opaque to particles of a certain type.
    
               DEFAULT: All particles are detected
   """

    def __init__(self):
        self.IMPDET = TypeKeyword('IMPDET', (float, float, int, int, int),
                                  comment='E-window, no. of bins, IPSF, IDCUT')
        self.IDSPC = TypeKeyword('IDSPC', (filename_type,),
                                 comment='Spectrum file name, 20 chars')
        self.IDPSF = TypeKeyword('IDPSF', (filename_type,),
                                 comment='Phase-space file name, 20 chars')
        self.IDFLNC = TypeKeyword('IDFLNC', (filename_type,),
                                  comment='Fluence spectrum file name, 20 chars')
        self.IDAGEL = TypeKeyword('IDAGEL', (float, float, int),
                                  comment='Age interval and no. of bins')
        self.IDAGEF = TypeKeyword('IDAGEF', (filename_type,),
                                  comment='Age-distribution file name, 20 chars')

        keyword = TypeKeyword('IDBODY', (module_type,), comment='Active body')
        self.IDBODY = KeywordSequence(keyword)

        keyword = TypeKeyword('IDKPAR', (int,), comment='Kind of detected particles')
        self.IDKPAR = KeywordSequence(keyword)

    def get_keywords(self):
        return (self.IMPDET, self.IDSPC, self.IDPSF, self.IDFLNC,
                self.IDAGEL, self.IDAGEF, self.IDBODY, self.IDKPAR)

    def set(self, el, eu, nbe, ipsf, idcut,
            spectrum_filename=None, psf_filename=None, fln_filename=None,
            agel=None, ageu=None, nage=None, age_filename=None,
            kb=None, kpar=None):
        self.IMPDET.set(el, eu, nbe, ipsf, idcut)
        self.IDSPC.set(spectrum_filename)
        self.IDPSF.set(psf_filename)
        self.IDFLNC.set(fln_filename)
        self.IDAGEL.set(agel, ageu, nage)
        self.IDAGEF.set(age_filename)

        if not hasattr(kb, '__iter__'):
            kb = [kb]
        self.IDBODY.clear()
        for item in kb:
            self.IDBODY.add(item)

        if not hasattr(kpar, '__iter__'):
            kpar = [kpar]
        self.IDKPAR.clear()
        for item in kpar:
            self.IDKPAR.add(item)

class ImpactDetectors(KeywordSequence):

    def __init__(self):
        keyword = ImpactDetectorGroup()
        super().__init__(keyword)

    def set(self, el, eu, nbe, ipsf, idcut,
            spectrum_filename=None, psf_filename=None, fln_filename=None,
            agel=None, ageu=None, nage=None, age_filename=None,
            kb=None, kpar=None):
        super().set(el, eu, nbe, ipsf, idcut,
                    spectrum_filename, psf_filename, fln_filename,
                    agel, ageu, nage, age_filename,
                    kb, kpar)

    def add(self, el, eu, nbe, ipsf, idcut,
            spectrum_filename=None, psf_filename=None, fln_filename=None,
            agel=None, ageu=None, nage=None, age_filename=None,
            kb=None, kpar=None):
        super().add(el, eu, nbe, ipsf, idcut,
                    spectrum_filename, psf_filename, fln_filename,
                    agel, ageu, nage, age_filename,
                    kb, kpar)

class EnergyDepositionDetectorGroup(KeywordGroup):
    """
    Each energy-deposition detector consists of a set of active bodies,
    which must have been defined as parts of the geometry. The output
    spectrum is the distribution of absorbed energy (per primary shower)
    in the active bodies.
    
             *** WARNING: The energy-deposition spectrum may be strongly
             biased when interaction forcing is applied, even outside the
             detector bodies.
    
    To define each energy-deposition detector insert the following block
    of lines;
    
    ENDETC : Starts the definition of a new energy-deposition detector.
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
    
    EDSPC_ : Name of the output spectrum file (up to 20 characters).
               DEFAULT: 'spc-enddet-##.dat'
    
    EDBODY : Active body KB of the detector. One line for each active
             body.
               DEFAULT: None
             --> Notice that a body cannot be part of more than one
             energy-deposition detector.
    """

    def __init__(self):
        self.ENDETC = TypeKeyword('ENDETC', (float, float, int),
                                  comment='Energy window and no. of bins')
        self.EDSPC = TypeKeyword('EDSPC', (filename_type,),
                                 comment='Output spectrum file name, 20 chars')

        keyword = TypeKeyword('EDBODY', (module_type,), comment='Active body')
        self.EDBODY = KeywordSequence(keyword)

    def get_keywords(self):
        return (self.ENDETC, self.EDSPC, self.EDBODY)

    def set(self, el, eu, nbe, spectrum_filename=None, kb=None):
        self.ENDETC.set(el, eu, nbe)
        self.EDSPC.set(spectrum_filename)

        if not hasattr(kb, '__iter__'):
            kb = [kb]
        self.EDBODY.clear()
        for item in kb:
            self.EDBODY.add(item)

class EnergyDepositionDetectors(KeywordSequence):

    def __init__(self):
        keyword = EnergyDepositionDetectorGroup()
        super().__init__(keyword)

    def set(self, el, eu, nbe, spectrum_filename=None, kb=None):
        super().set(el, eu, nbe, spectrum_filename, kb)

    def add(self, el, eu, nbe, spectrum_filename=None, kb=None):
        super().add(el, eu, nbe, spectrum_filename, kb)

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

class GRIDR(TypeKeyword):
    """
    The efficiency of the dose map calculation can be increased by taking
    advantage of possible symmetries of the system (source and geometry).
    In problems with axial symmetry about the Z axis, it is advantageous
    to tally the dose distribution in the volume of a cylinder of radius
    RU, about the Z axis, limited by the planes Z=ZL and Z=ZU. For
    systems with spherical symmetry about the origin of coordinates, it
    is most convenient to consider the radial dose distribution in a
    sphere of radius RU. The generation of these symmetric dose maps is
    activated by entering the line
    
    GRIDR_ : Radius RU of the dose zone and number of radial bins.
               DEFAULT: None
    
    Specifically, when the input file contains only the lines GRIDZ_ and
    GRIDR_, the program assumes that the dose distribution is axially
    symmetric and generates a cylindrical map. When the input file has
    only the line GRIDR_, spherical symmetry is assumed and the radial
    distribution of absorbed dose is tallied.
    
    The different types of dose maps are mutually exclusive. Notice that
    when the assumed symmetry does not hold, the program may not be able
    to evaluate the masses of voxels correctly.
    """

    def __init__(self):
        super().__init__('GRIDR', (float, int),
                         comment='Radius of the dose volume, no. of bins')

    def set(self, ru, ndbr):
        super().set(ru, ndbr)

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


