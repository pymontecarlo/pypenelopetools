#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import os
import io

# Third party modules.

# Local modules.
from pypenelopetools.penelope.enums import KPAR, ICOL
from pypenelopetools.pencyl.input import PencylInput
from pypenelopetools.material import Material

# Globals and constants variables.

def create_example1_disc():
    # Create materials
    material_cu = Material('Cu', {29: 1.0}, 8.9)

    # Create input
    input = PencylInput()

    input.TITLE.set('Point source and a homogeneous cylinder.')

    definition = input.geometry_definitions.add(0.0, 0.005)
    definition.CYLIND.add(1, 0, 0.01)

    input.SKPAR.set(1)
    input.SENERG.set(40e3)
    input.SPOSIT.set(0, 0, -0.0001)
    input.SCONE.set(0, 0, 5)

    input.materials.add(1, material_cu.filename, 1e3, 1e3, 1e3, 0.05, 0.05, 1e3, 1e3)

    input.DSMAX.add(1, 1, 1e-4)

    input.IFORCE.add(1, 1, KPAR.ELECTRON, ICOL.HARD_BREMSSTRAHLUNG_EMISSION, 2000, 0.1, 2.0)
    input.IFORCE.add(1, 1, KPAR.ELECTRON, ICOL.INNER_SHELL_IMPACT_IONISATION, 200, 0.1, 2.0)

    input.IBRSPL.add(1, 1, 2)

    input.IXRSPL.add(1, 1, 2)

    input.NBE.set(0, 0, 100)
    input.NBANGL.set(45, 18)

    input.EMERGP.set(0.005, 100)

    detector = input.energy_deposition_detectors.add(0, 0, 100)
    detector.EDBODY.add(1, 1)

    input.DOSE2D.add(1, 1, 100, 50)

    input.RESUME.set('dump.dat')
    input.DUMPTO.set('dump.dat')
    input.DUMPP.set(60)

    input.RSEED.set(1, 1)
    input.NSIMSH.set(1e9)
    input.TIME.set(600)

    return input

def create_example3_detector():
    # Create materials
    material_nai = Material('NaI', {11: 0.1534, 53: 0.8466}, 3.667)
    material_al2o3 = Material('Al2O3', {8: 0.4707, 13: 0.5293}, 3.97)
    material_al = Material('Al', {13: 1.0}, 2.7)
    materials = (material_nai, material_al2o3, material_al)

    # Create input
    input = PencylInput()

    input.TITLE.set('NaI detector with Al cover and Al2O3 reflecting foil')

    layer1 = input.geometry_definitions.add(-0.24, -0.16, 0.0, 0.0)
    layer1.CYLIND.add(3, 0.00, 4.05)

    layer2 = input.geometry_definitions.add(-0.16, 0.00)
    layer2.CYLIND.add(2, 0.00, 3.97)
    layer2.CYLIND.add(3, 3.97, 4.05)

    layer3 = input.geometry_definitions.add(0.00, 7.72)
    layer3.CYLIND.add(1, 0.00, 3.81)
    layer3.CYLIND.add(2, 3.81, 3.97)
    layer3.CYLIND.add(3, 3.97, 4.05)

    layer4 = input.geometry_definitions.add(7.72, 9.72)
    layer4.CYLIND.add(3, 0.00, 4.05)

    input.SKPAR.set(2)
    input.SENERG.set(9.5e6)
    input.SPOSIT.set(0, 0, -10.0)
    input.SCONE.set(0, 0, 0)

    input.materials.add(1, material_nai.filename, 5.0e4, 5.0e3, 5.0e4, 0.1, 0.1, 2e3, 2e3)
    input.materials.add(2, material_al2o3.filename, 5.0e4, 5.0e3, 5.0e4, 0.1, 0.1, 2e3, 2e3)
    input.materials.add(3, material_al.filename, 5.0e4, 5.0e3, 5.0e4, 0.1, 0.1, 2e3, 2e3)

    detector = input.energy_deposition_detectors.add(0, 1e7, 1000)
    detector.EDBODY.add(3, 1)

    input.DOSE2D.add(3, 1, 50, 50)

    input.RESUME.set('dump.dat')
    input.DUMPTO.set('dump.dat')
    input.DUMPP.set(60)

    input.NSIMSH.set(1e8)
    input.TIME.set(2e9)

    return input, materials

class TestPencylInput(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.testdatadir = os.path.join(os.path.dirname(__file__),
                                        '..', 'testdata', 'pencyl')

    def _write_read_input(self, input):
        fileobj = io.StringIO()

        try:
            input.write(fileobj)

            fileobj.seek(0)
            outinput = PencylInput()
            outinput.read(fileobj)
        finally:
            fileobj.close()

        return outinput

    def _test_example1_disc(self, input):
        geometry_definitions, = input.geometry_definitions.get()
        self.assertEqual(1, len(geometry_definitions))

        zlow, zhigh, xcen, ycen, cylinders = geometry_definitions[0]
        self.assertAlmostEqual(0.0, zlow, 5)
        self.assertAlmostEqual(0.005, zhigh, 5)
        self.assertIsNone(xcen)
        self.assertIsNone(ycen)
        self.assertEqual(1, len(cylinders))

        material, rin, rout = cylinders[0]
        self.assertEqual(1, material)
        self.assertAlmostEqual(0.0, rin, 5)
        self.assertAlmostEqual(0.01, rout, 5)

        kparp, = input.SKPAR.get()
        self.assertEqual(1, kparp)

        se0, = input.SENERG.get()
        self.assertAlmostEqual(40e3, se0, 5)

        sx0, sy0, sz0 = input.SPOSIT.get()
        self.assertAlmostEqual(0.0, sx0, 5)
        self.assertAlmostEqual(0.0, sy0, 5)
        self.assertAlmostEqual(-0.0001, sz0, 5)

        theta, phi, alpha = input.SCONE.get()
        self.assertAlmostEqual(0.0, theta, 5)
        self.assertAlmostEqual(0.0, phi, 5)
        self.assertAlmostEqual(5.0, alpha, 5)

        materials, = input.materials.get()
        self.assertEqual(1, len(materials))

        filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[0]
        self.assertEqual('Cu.mat', filename)
        self.assertAlmostEqual(1e3, eabs1, 5)
        self.assertAlmostEqual(1e3, eabs2, 5)
        self.assertAlmostEqual(1e3, eabs3, 5)
        self.assertAlmostEqual(0.05, c1, 5)
        self.assertAlmostEqual(0.05, c2, 5)
        self.assertAlmostEqual(1e3, wcc, 5)
        self.assertAlmostEqual(1e3, wcr, 5)

        dsmaxs, = input.DSMAX.get()
        self.assertEqual(1, len(dsmaxs))

        kl, kc, dsmax = dsmaxs[0]
        self.assertEqual(1, kl)
        self.assertEqual(1, kc)
        self.assertAlmostEqual(1e-4, dsmax, 5)

        iforces, = input.IFORCE.get()
        self.assertEqual(2, len(iforces))

        kl, kc, kpar, icol, forcer, wlow, whig = iforces[0]
        self.assertEqual(1, kl)
        self.assertEqual(1, kc)
        self.assertEqual(1, kpar)
        self.assertEqual(4, icol)
        self.assertAlmostEqual(2000, forcer, 5)
        self.assertAlmostEqual(0.1, wlow, 5)
        self.assertAlmostEqual(2.0, whig, 5)

        kl, kc, kpar, icol, forcer, wlow, whig = iforces[1]
        self.assertEqual(1, kl)
        self.assertEqual(1, kc)
        self.assertEqual(1, kpar)
        self.assertEqual(5, icol)
        self.assertAlmostEqual(200, forcer, 5)
        self.assertAlmostEqual(0.1, wlow, 5)
        self.assertAlmostEqual(2.0, whig, 5)

        ibrspls, = input.IBRSPL.get()
        self.assertEqual(1, len(ibrspls))

        kl, kc, factor = ibrspls[0]
        self.assertEqual(1, kl)
        self.assertEqual(1, kc)
        self.assertAlmostEqual(2.0, factor, 5)

        ixrspls, = input.IXRSPL.get()
        self.assertEqual(1, len(ixrspls))

        kl, kc, factor = ibrspls[0]
        self.assertEqual(1, kl)
        self.assertEqual(1, kc)
        self.assertAlmostEqual(2.0, factor, 5)

        el, eu, nbe = input.NBE.get()
        self.assertAlmostEqual(0.0, el, 5)
        self.assertAlmostEqual(0.0, eu, 5)
        self.assertEqual(100, nbe)

        nbth, nbph = input.NBANGL.get()
        self.assertEqual(45, nbth)
        self.assertEqual(18, nbph)

        radm, nbre = input.EMERGP.get()
        self.assertAlmostEqual(0.005, radm, 5)
        self.assertEqual(100, nbre)

        energy_deposition_detectors, = input.energy_deposition_detectors.get()
        self.assertEqual(1, len(energy_deposition_detectors))

        el, eu, nbe, spectrum_filename, cylinders = energy_deposition_detectors[0]
        self.assertAlmostEqual(0.0, el, 5)
        self.assertAlmostEqual(0.0, eu, 5)
        self.assertEqual(100, nbe)
        self.assertIsNone(spectrum_filename)
        self.assertEqual(1, len(cylinders))

        kl, kc = cylinders[0]
        self.assertEqual(1, kl)
        self.assertEqual(1, kc)

        dose2d, = input.DOSE2D.get()
        self.assertEqual(1, len(dose2d))

        kl, kc, nz, nr = dose2d[0]
        self.assertEqual(1, kl)
        self.assertEqual(1, kc)
        self.assertEqual(nz, 100)
        self.assertEqual(nr, 50)

        filename, = input.RESUME.get()
        self.assertEqual('dump.dat', filename)

        filename, = input.DUMPTO.get()
        self.assertEqual('dump.dat', filename)

        dumpp, = input.DUMPP.get()
        self.assertAlmostEqual(60.0, dumpp, 5)

        seed1, seed2 = input.RSEED.get()
        self.assertEqual(1, seed1)
        self.assertEqual(1, seed2)

        dshn, = input.NSIMSH.get()
        self.assertAlmostEqual(1e9, dshn, 5)

        timea, = input.TIME.get()
        self.assertAlmostEqual(600.0, timea, 5)

    def test_example1_disc_write(self):
        input = create_example1_disc()
        input = self._write_read_input(input)
        self._test_example1_disc(input)

    def test_example1_disc_read(self):
        filepath = os.path.join(self.testdatadir, '1-disc', 'disc.in')
        input = PencylInput()
        with open(filepath, 'r') as fp:
            input.read(fp)
        self._test_example1_disc(input)

    def _test_example3_detector(self, input):
        geometry_definitions, = input.geometry_definitions.get()
        self.assertEqual(4, len(geometry_definitions))

        zlow, zhigh, xcen, ycen, cylinders = geometry_definitions[0]
        self.assertAlmostEqual(-0.24, zlow, 5)
        self.assertAlmostEqual(-0.16, zhigh, 5)
        self.assertAlmostEqual(0.0, xcen, 5)
        self.assertAlmostEqual(0.0, ycen, 5)
        self.assertEqual(1, len(cylinders))

        material, rin, rout = cylinders[0]
        self.assertEqual(3, material)
        self.assertAlmostEqual(0.0, rin, 5)
        self.assertAlmostEqual(4.05, rout, 5)

        zlow, zhigh, xcen, ycen, cylinders = geometry_definitions[1]
        self.assertAlmostEqual(-0.16, zlow, 5)
        self.assertAlmostEqual(0.0, zhigh, 5)
        self.assertIsNone(xcen)
        self.assertIsNone(ycen)
        self.assertEqual(2, len(cylinders))

        material, rin, rout = cylinders[0]
        self.assertEqual(2, material)
        self.assertAlmostEqual(0.0, rin, 5)
        self.assertAlmostEqual(3.97, rout, 5)

        material, rin, rout = cylinders[1]
        self.assertEqual(3, material)
        self.assertAlmostEqual(3.97, rin, 5)
        self.assertAlmostEqual(4.05, rout, 5)

        zlow, zhigh, xcen, ycen, cylinders = geometry_definitions[2]
        self.assertAlmostEqual(0.0, zlow, 5)
        self.assertAlmostEqual(7.72, zhigh, 5)
        self.assertIsNone(xcen)
        self.assertIsNone(ycen)
        self.assertEqual(3, len(cylinders))

        material, rin, rout = cylinders[0]
        self.assertEqual(1, material)
        self.assertAlmostEqual(0.0, rin, 5)
        self.assertAlmostEqual(3.81, rout, 5)

        material, rin, rout = cylinders[1]
        self.assertEqual(2, material)
        self.assertAlmostEqual(3.81, rin, 5)
        self.assertAlmostEqual(3.97, rout, 5)

        material, rin, rout = cylinders[2]
        self.assertEqual(3, material)
        self.assertAlmostEqual(3.97, rin, 5)
        self.assertAlmostEqual(4.05, rout, 5)

        zlow, zhigh, xcen, ycen, cylinders = geometry_definitions[3]
        self.assertAlmostEqual(7.72, zlow, 5)
        self.assertAlmostEqual(9.72, zhigh, 5)
        self.assertIsNone(xcen)
        self.assertIsNone(ycen)
        self.assertEqual(1, len(cylinders))

        material, rin, rout = cylinders[0]
        self.assertEqual(3, material)
        self.assertAlmostEqual(0.0, rin, 5)
        self.assertAlmostEqual(4.05, rout, 5)

        kparp, = input.SKPAR.get()
        self.assertEqual(2, kparp)

        se0, = input.SENERG.get()
        self.assertAlmostEqual(9.5e6, se0, 5)

        sx0, sy0, sz0 = input.SPOSIT.get()
        self.assertAlmostEqual(0.0, sx0, 5)
        self.assertAlmostEqual(0.0, sy0, 5)
        self.assertAlmostEqual(-10.0, sz0, 5)

        theta, phi, alpha = input.SCONE.get()
        self.assertAlmostEqual(0.0, theta, 5)
        self.assertAlmostEqual(0.0, phi, 5)
        self.assertAlmostEqual(0.0, alpha, 5)
#
        materials, = input.materials.get()
        self.assertEqual(3, len(materials))

        filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[0]
        self.assertEqual('NaI.mat', filename)
        self.assertAlmostEqual(5e4, eabs1, 5)
        self.assertAlmostEqual(5e3, eabs2, 5)
        self.assertAlmostEqual(5e4, eabs3, 5)
        self.assertAlmostEqual(0.1, c1, 5)
        self.assertAlmostEqual(0.1, c2, 5)
        self.assertAlmostEqual(2e3, wcc, 5)
        self.assertAlmostEqual(2e3, wcr, 5)

        filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[1]
        self.assertEqual('Al2O3.mat', filename)
        self.assertAlmostEqual(5e4, eabs1, 5)
        self.assertAlmostEqual(5e3, eabs2, 5)
        self.assertAlmostEqual(5e4, eabs3, 5)
        self.assertAlmostEqual(0.1, c1, 5)
        self.assertAlmostEqual(0.1, c2, 5)
        self.assertAlmostEqual(2e3, wcc, 5)
        self.assertAlmostEqual(2e3, wcr, 5)

        filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[2]
        self.assertEqual('Al.mat', filename)
        self.assertAlmostEqual(5e4, eabs1, 5)
        self.assertAlmostEqual(5e3, eabs2, 5)
        self.assertAlmostEqual(5e4, eabs3, 5)
        self.assertAlmostEqual(0.1, c1, 5)
        self.assertAlmostEqual(0.1, c2, 5)
        self.assertAlmostEqual(2e3, wcc, 5)
        self.assertAlmostEqual(2e3, wcr, 5)
#
        energy_deposition_detectors, = input.energy_deposition_detectors.get()
        self.assertEqual(1, len(energy_deposition_detectors))

        el, eu, nbe, spectrum_filename, cylinders = energy_deposition_detectors[0]
        self.assertAlmostEqual(0.0, el, 5)
        self.assertAlmostEqual(1e7, eu, 5)
        self.assertEqual(1000, nbe)
        self.assertIsNone(spectrum_filename)
        self.assertEqual(1, len(cylinders))

        kl, kc = cylinders[0]
        self.assertEqual(3, kl)
        self.assertEqual(1, kc)

        dose2d, = input.DOSE2D.get()
        self.assertEqual(1, len(dose2d))

        kl, kc, nz, nr = dose2d[0]
        self.assertEqual(3, kl)
        self.assertEqual(1, kc)
        self.assertEqual(nz, 50)
        self.assertEqual(nr, 50)

        filename, = input.RESUME.get()
        self.assertEqual('dump.dat', filename)

        filename, = input.DUMPTO.get()
        self.assertEqual('dump.dat', filename)

        dumpp, = input.DUMPP.get()
        self.assertAlmostEqual(60.0, dumpp, 5)

        dshn, = input.NSIMSH.get()
        self.assertAlmostEqual(1e8, dshn, 5)

        timea, = input.TIME.get()
        self.assertAlmostEqual(2e9, timea, 5)

    def test_example3_detector_write(self):
        input, _materials = create_example3_detector()
        input = self._write_read_input(input)
        self._test_example3_detector(input)

    def test_example3_detector_read(self):
        filepath = os.path.join(self.testdatadir, '3-detector', 'cyld.in')
        input = PencylInput()
        with open(filepath, 'r') as fp:
            input.read(fp)
        self._test_example3_detector(input)

if __name__ == '__main__': #pragma: no cover
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
