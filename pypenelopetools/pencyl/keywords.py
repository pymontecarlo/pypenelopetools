""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.penelope.keyword import \
    TypeKeyword, KeywordGroup, KeywordSequence, material_type
import pypenelopetools.penelope.keywords as penelope_keywords

# Globals and constants variables.

class GeometryGroup(KeywordGroup):
    """
    This block of lines defines the geometrical structure. The
    only allowed keywords in the geometry definition list are
    'GSTART', 'LAYER_', 'CENTRE', 'CYLIND' and 'GEND__' (notice
    the blanks). The definition list must begin with the
    'GSTART' line and terminate with the 'GEND__' line. The
    second line must be a 'LAYER_' line, which initiates the
    definition of the layer structure. Each 'LAYER_' line is
    followed by a 'CENTRE' line (optional) and by one or several
    'CYLIND' lines, which define the various concentric rings in
    the layer; a layer may be void. No blank lines are allowed
    in the geometry definition list.
    
    Layers must be defined in increasing order of heights, from
    bottom to top of the structure. If the 'CENTRE' line is not
    entered, cylinders are assumed to be centred on the Z-axis
    (XCEN=YCEN=0.0). Cylinders have to be defined in increasing
    radial order, from the centre to the periphery. The two
    lengths in each 'LAYER_' and 'CYLIND' line must be entered
    in increasing order. All numerical data are read in free
    format.
    """

    def __init__(self):
        self.LAYER = TypeKeyword('LAYER', (float, float),
                                 comment='Z_lower and Z_higher')
        self.CENTER = TypeKeyword('CENTER', (float, float),
                                  comment='X_centre and Y_centre')

        keyword = TypeKeyword('CYLIND', (material_type, float, float),
                              comment='Material, R_inner and R_outer')
        self.CYLIND = KeywordSequence(keyword)

    def get_keywords(self):
        return (self.LAYER, self.CENTER, self.CYLIND)

    def set(self, zlow, zhigh, material, rin, rout, xcen=None, ycen=None):
        self.LAYER.set(zlow, zhigh)
        self.CENTER.set(xcen, ycen)
        self.CYLIND.set(material, rin, rout)

class Geometry(KeywordSequence):

    def __init__(self):
        keyword = GeometryGroup()
        super().__init__(keyword)

    def set(self, zlow, zhigh, material, rin, rout, xcen=None, ycen=None):
        return super().set(zlow, zhigh, material, rin, rout, xcen, ycen)

    def add(self, zlow, zhigh, material, rin, rout, xcen=None, ycen=None):
        return super().add(zlow, zhigh, material, rin, rout, xcen, ycen)

class SEXTND(KeywordSequence):
    """
    For internal extended sources, this line defines an active
    body KL,KC (the cylinder KC in layer KL) and its relative
    activity density, RELAC.
      DEFAULT: none.
    
    NOTE: The labels KL,KC that identify each body are defined
    by the ordering in the input geometry list. These labels
    are written in the output geometry report.
    """

    def __init__(self):
        keyword = TypeKeyword('SEXTND', (int, int, float),
                              comment='Extended source in KL,KC, rel. activity dens.')
        super().__init__(keyword)

    def set(self, kl, kc, relac):
        super().set(kl, kc, relac)

    def add(self, kl, kc, relac):
        super().add(kl, kc, relac)

class STHICK(TypeKeyword):
    """
    For an external source, thickness (height) of the
    active volume of the source (cylinder or ring).
    DEFAULT: STHICK=0.0
    """

    def __init__(self):
        super().__init__('STHICK', (float,), comment='Source height')

class SRADII(TypeKeyword):
    """
    For an external source, inner and outer radii of the active
    volume (cylinder or ring).
      DEFAULTS: SRIN=0.0, SROUT=0.0
    """

    def __init__(self):
        super().__init__('SRADII', (float, float),
                         comment='Source inner and outer radii')

class IWOODC(TypeKeyword):
    """
    Photons are transported freely across the system using an
    inverse mean free path, SUP, that is larger than the actual
    inverse mean free path, IMFP. The event at the end of each
    free flight may be either a real interaction (ICOL=1 to 4)
    or a delta interaction (ICOL=7). The latter occur with
    probability 1 - IMFP/SUP, so that the simulation remains
    unbiased.
    The method is very effective for the calculation of dose,
    preferably combined with interaction forcing.
      DEFAULT: off
    """

    def __init__(self):
        super().__init__('IWOODC', (bool,),
                         comment='Delta scattering is turned on')

    def set(self, on):
        super().set(on)

    def write(self, index_table):
        value = self.get()[0]
        if not value:
            return []

        return [self._create_line(self.name, [], self.comment)]

class NBZ(TypeKeyword):
    """
    Number of bins for the Z-coordinate; .LE. 200.
        DEFAULT: NBZ=100
    """

    def __init__(self):
        super().__init__('NBZ', (int,),
                         comment='No. of bins for the Z-coordinate')

    def set(self, nbz):
        super().set(nbz)

class NBR(TypeKeyword):
    """
    Number of bins for the radial variable, R=SQRT(X*X+Y*Y); .LE. 200.
        DEFAULT: NBR=100
    """

    def __init__(self):
        super().__init__('NBR', (int,), comment='No. of radial bins')

    def set(self, nbr):
        super().set(nbr)

class NBTL(TypeKeyword):
    """
    Limits of the interval where track-length distributions of
    primary particles are tallied. Number of track-length bins;
    .LE. 200.
      DEFAULT: TLMIN=0, TLMAX=5*RANGE(EPMAX,KPARP,1), NBTL=200
    """

    def __init__(self):
        super().__init__('NBTL', (float, float, int),
                         comment='Track-length interval and no. of TL-bins')

    def set(self, tlmin, tlmax, nbtl):
        super().set(tlmin, tlmax, nbtl)

class EMERGP(TypeKeyword):
    """
    The program can generate the PDFs of the coordinates (X,Y) of points
    where trajectories of emerging particles intersect the upper and
    lower planes of the geometry definition (upbound and downbound
    particles, respectively), and the PDF of the radial distance of the
    intersections, R=SQRT(X*X+Y*Y).
    
    Activates the generation of the distributions of trajectory
    crossings with the upper and lower planes. RADM is the
    radius of the scoring region, and NBRE is the number of
    bins of the radial distributions. The (X,Y) distributions
    are tallied on a square of side 2*RADM, with (2*NBRE)**2
    bins.
      DEFAULT: None
    """

    def __init__(self):
        super().__init__('EMERGP', (float, int),
                         comment='Radius of the scoring region, no. of bins')

    def set(self, radm, nbre):
        super().set(radm, nbre)

class EnergyDepositionDetectorGroup(KeywordGroup):
    """
    Each energy-deposition detector consists of a set of active bodies,
    which must have been defined as parts of the geometry. The output
    spectrum is the distribution of absorbed energy (per primary shower)
    in the active bodies.
    
             *** WARNING: The energy-deposition spectrum may be strongly
             biased when interaction forcing is applied, even outside the
             detector bodies.
    """

    def __init__(self):
        self.ENDETC = penelope_keywords.ENDETC()
        self.EDSPC = penelope_keywords.EDSPC()

        keyword = TypeKeyword('EDBODY', (int, int), comment='Active cylinder')
        self.EDBODY = KeywordSequence(keyword)

    def get_keywords(self):
        return (self.ENDETC, self.EDSPC, self.EDBODY)

    def set(self, el, eu, nbe, spectrum_filename=None, cylinders=None):
        self.ENDETC.set(el, eu, nbe)
        self.EDSPC.set(spectrum_filename)

        if not hasattr(cylinders, '__iter__'):
            cylinders = [cylinders]
        self.EDBODY.clear()
        for kl, kc in cylinders:
            self.EDBODY.add(kl, kc)

class EnergyDepositionDetectors(KeywordSequence):

    def __init__(self):
        keyword = EnergyDepositionDetectorGroup()
        super().__init__(keyword)

    def set(self, el, eu, nbe, spectrum_filename=None, cylinders=None):
        return super().set(el, eu, nbe, spectrum_filename, cylinders)

    def add(self, el, eu, nbe, spectrum_filename=None, cylinders=None):
        return super().add(el, eu, nbe, spectrum_filename, cylinders)

class DOSE2D(KeywordSequence):
    """
    The program will tally 2D, depth-radius, dose and deposited
    charge distributions in the body KL,KC (i.e. the cylinder
    KC of layer KL). The numbers NZ and NR of Z- and R-bins have
    to be specified by the user, they must be in the interval
    from 1 to 200. Up to ten different bodies can be selected,
    a separate line for each body.
      DEFAULT: off
    """

    def __init__(self):
        keyword = TypeKeyword('DOSE2D', (int, int, int, int),
                              comment='Tally distributions in KL,KC with NZ,NR bins')
        super().__init__(keyword)

    def set(self, kl, kc, nz, nr):
        super().set(kl, kc, nz, nr)

    def add(self, kl, kc, nz, nr):
        super().add(kl, kc, nz, nr)







