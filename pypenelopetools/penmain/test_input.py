#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import io

# Third party modules.

# Local modules.
from pypenelopetools.penmain.input import PenmainInput

# Globals and constants variables.

class TestPenmainInput(unittest.TestCase):

    IN = ['TITLE  Point source and a homogeneous cylinder.',
          '       Note that interaction forcing distorts the detector output.',
          '       .',
          '       >>>>>>>> Source definition.',
          'SKPAR  1        [Primary particles: 1=electron, 2=photon, 3=positron]',
          'SENERG 40e3             [Initial energy (monoenergetic sources only)]',
          'SPECTR 1.17e6  0.5e0         [E bin: lower-end and total probability]',
          'SPECTR 1.17e6  1.0e-35       [E bin: lower-end and total probability]',
          'SPOSIT 0 0 -1                             [Coordinates of the source]',
          'SCONE  0 0 10                           [Conical beam; angles in deg]',
          '       .',
          '       >>>>>>>> Material data and simulation parameters.',
          'MFNAME Cu.mat                         [Material file, up to 20 chars]',
          'MSIMPA 1e    3 1e3 1e3 0.05 0.05 1e3 1e3        [EABS(1:3),C1,C2,WCC,WCR]',
          '       .',
          '       >>>>>>>> Geometry and local simulation parameters.',
          'GEOMFN disc.geo                       [Geometry file, up to 20 chars]',
          'PARINP   1  0.005            thickness [Optional geometry parameters]',
          'PARINP   2  1.000               radius [Optional geometry parameters]',
          'DSMAX  1 1 1e-4                  [Mmaximum step length in body KL,KC]',
          '       .',
          '       >>>>>>>> Interaction forcing.',
          'IFORCE 1 1 4 2000 .1  2                         [Interaction forcing]',
          'IFORCE 1 1 5 200  .1  2                         [Interaction forcing]',
          '       .',
          '       >>>>>>>> Bremsstrahlung splitting.',
          'IBRSPL 1 2                                      [KB,splitting factor]',
          '       .',
          '       >>>>>>>> X-ray splitting.',
          'IXRSPL 1 2                       [KB,splitting factor, weight window]',
          '       .',
          '       >>>>>>>> Emerging particles. Energy and angular distributions.',
          'NBE    0  0    100                    [Energy window and no. of bins]',
          'NBANGL 45 18               [No. of bins for the angles THETA and PHI]',
          '       .',
          '       >>>>>>>> Energy-deposition detectors (up to 25).',
          'ENDETC 0 0 100                     [Energy window and number of bins]',
          'EDBODY 1                        [Active body; one line for each body]',
          '       .',
          '       >>>>>>>> Job properties',
          'RESUME dump.dat                [Resume from this dump file, 20 chars]',
          'DUMPTO dump.dat                   [Generate this dump file, 20 chars]',
          'DUMPP  60                                    [Dumping period, in sec]',
          '       .',
          'NSIMSH 2e9                      [Desired number of simulated showers]',
          'TIME   600                         [Allotted simulation time, in sec]',
          '       .',
          'END                                  [Ends the reading of input data]']

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.input = PenmainInput()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testread(self):
        fileobj = io.StringIO('\n'.join(self.IN))
        self.input.read(fileobj)

        print(self.input.SPECTR.get())

    def testwrite(self):
        self.input.TITLE.set('Point source and a homogeneous cylinder.')
        self.input.SKPAR.set(1)
        self.input.SENERG.set(40e3)
        self.input.SPECTR.add(1.17e6, 0.5)
        self.input.SPECTR.add(1.17e6, 1e-35)

        fileobj = io.StringIO()
        self.input.write(fileobj, {})

        print(fileobj.getvalue())

if __name__ == '__main__': #pragma: no cover
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
