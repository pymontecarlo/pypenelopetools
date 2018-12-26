#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import io
import os

# Third party modules.

# Local modules.
from pypenelopetools.penelope.enums import KPAR, ICOL
from pypenelopetools.penmain.input import PenmainInput
from pypenelopetools.material import Material
from pypenelopetools.pengeom.surface import sphere, zplane, cylinder
from pypenelopetools.pengeom.module import Module, SidePointer
from pypenelopetools.pengeom.geometry import Geometry

# Globals and constants variables.

def create_example1_disc():
    # Create materials
    material_cu = Material('Cu', {29: 1.0}, 8.9)

    # Create geometry
    module = Module(material_cu, 'Solid cylinder')
    module.add_surface(zplane(0.0), SidePointer.POSITIVE)
    module.add_surface(zplane(0.005), SidePointer.NEGATIVE)
    module.add_surface(cylinder(1.0), SidePointer.NEGATIVE)

    geometry = Geometry('A solid cylinder.')
    geometry.add_module(module)

    # Create input
    input = PenmainInput()

    input.TITLE.set('Point source and a homogeneous cylinder.')
    input.SKPAR.set(KPAR.ELECTRON)
    input.SENERG.set(40e3)
    input.SPOSIT.set(0.0, 0.0, -0.0001)
    input.SCONE.set(0.0, 0.0, 5.0)

    input.materials.add(1, material_cu.filename, 1e3, 1e3, 1e3, 0.05, 0.05, 1e3, 1e3)

    input.GEOMFN.set('disc.geo')
    input.PARINP.add(1, 0.005)
    input.PARINP.add(2, 0.01)
    input.DSMAX.add(1, 1e-4)

    input.IFORCE.add(1, KPAR.ELECTRON, ICOL.HARD_BREMSSTRAHLUNG_EMISSION, 2000, 0.1, 2.0)
    input.IFORCE.add(1, KPAR.ELECTRON, ICOL.INNER_SHELL_IMPACT_IONISATION, 200, 0.1, 2.0)
    input.IBRSPL.add(1, 2)
    input.IXRSPL.add(1, 2)

    input.NBE.set(0, 0, 100)
    input.NBANGL.set(45, 18)

    detector = input.impact_detectors.add(0.0, 0.0, 100, 0, 2)
    detector.IDBODY.add(1)

    detector = input.energy_deposition_detectors.add(0, 0, 100)
    detector.EDBODY.add(1)

    input.GRIDZ.set(0, 0.005, 100)
    input.GRIDR.set(0.01, 50)

    input.RESUME.set('dump.dat')
    input.DUMPTO.set('dump.dat')
    input.DUMPP.set(60)

    input.NSIMSH.set(2e9)
    input.TIME.set(600)

    return input

def create_example2_plane():
    # Create materials
    material_h2o = Material('H2O', {8: 0.8881, 1: 0.1119}, 1.0)

    # Create geometry
    module_detector = Module(material_h2o, 'Fluence detector')
    module_detector.add_surface(sphere(2.0), SidePointer.NEGATIVE)

    module_phantom = Module(material_h2o, 'Water phantom')
    module_phantom.add_surface(zplane(0.0), SidePointer.POSITIVE)
    module_phantom.add_surface(zplane(30.0), SidePointer.NEGATIVE)

    geometry = Geometry('Semi-infinite water phantom')
    geometry.add_module(module_detector)
    geometry.add_module(module_phantom)

    index_lookup = geometry.indexify()

    # Create input
    input = PenmainInput()

    input.TITLE.set('Dose in a water phantom with a spherical impact detector')
    input.SKPAR.set(KPAR.PHOTON)
    input.SENERG.set(3e7)
    input.SPOSIT.set(0.0, 0.0, -25.0)
    input.SCONE.set(0.0, 0.0, 5.0)

    input.materials.add(1, material_h2o.filename, 1e5, 1e4, 1e5, 0.05, 0.05, 5e3, 5e3)

    input.GEOMFN.set('plane.geo')

    input.NBE.set(1e5, 3e7, 100)
    input.NBANGL.set(45, 18)

    detector = input.impact_detectors.add(1e5, 0.0, 100, 0, 2)
    detector.IDBODY.add(index_lookup[module_detector])

    input.GRIDZ.set(0, 30.0, 60)
    input.GRIDR.set(30.0, 60.0)

    input.RESUME.set('dump.dat')
    input.DUMPTO.set('dump.dat')
    input.DUMPP.set(60)

    input.NSIMSH.set(1e7)
    input.TIME.set(2e9)

    return input

class TestPenmainInput(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.testdatadir = os.path.join(os.path.dirname(__file__),
                                        '..', 'testdata', 'penmain')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def _write_read_input(self, input):
        fileobj = io.StringIO()

        try:
            input.write(fileobj)

            fileobj.seek(0)
            outinput = PenmainInput()
            outinput.read(fileobj)
        finally:
            fileobj.close()

        return outinput

    def _test_example1_disc(self, input):
        kparp, = input.SKPAR.get()
        self.assertEqual(KPAR.ELECTRON, kparp)

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

        self.assertEqual('disc.geo', input.GEOMFN.get()[0])

        parinps, = input.PARINP.get()
        self.assertEqual(2, len(parinps))

        ip, parinp = parinps[0]
        self.assertEqual(1, ip)
        self.assertAlmostEqual(0.005, parinp, 5)

        ip, parinp = parinps[1]
        self.assertEqual(2, ip)
        self.assertAlmostEqual(0.01, parinp, 5)

        dsmaxs, = input.DSMAX.get()
        self.assertEqual(1, len(dsmaxs))

        kb, dsmax = dsmaxs[0]
        self.assertEqual(1, kb)
        self.assertAlmostEqual(1e-4, dsmax, 5)

        iforces, = input.IFORCE.get()
        self.assertEqual(2, len(iforces))

        kb, kpar, icol, forcer, wlow, whig = iforces[0]
        self.assertEqual(1, kb)
        self.assertEqual(KPAR.ELECTRON, kpar)
        self.assertEqual(ICOL.HARD_BREMSSTRAHLUNG_EMISSION, icol)
        self.assertAlmostEqual(2000, forcer, 5)
        self.assertAlmostEqual(0.1, wlow, 5)
        self.assertAlmostEqual(2.0, whig, 5)

        kb, kpar, icol, forcer, wlow, whig = iforces[1]
        self.assertEqual(1, kb)
        self.assertEqual(KPAR.ELECTRON, kpar)
        self.assertEqual(ICOL.INNER_SHELL_IMPACT_IONISATION, icol)
        self.assertAlmostEqual(200, forcer, 5)
        self.assertAlmostEqual(0.1, wlow, 5)
        self.assertAlmostEqual(2.0, whig, 5)

        ibrspls, = input.IBRSPL.get()
        self.assertEqual(1, len(ibrspls))

        kb, factor = ibrspls[0]
        self.assertEqual(1, kb)
        self.assertAlmostEqual(2.0, factor, 5)

        ixrspls, = input.IXRSPL.get()
        self.assertEqual(1, len(ixrspls))

        kb, factor = ixrspls[0]
        self.assertEqual(1, kb)
        self.assertAlmostEqual(2.0, factor, 5)

        el, eu, nbe = input.NBE.get()
        self.assertAlmostEqual(0.0, el, 5)
        self.assertAlmostEqual(0.0, eu, 5)
        self.assertEqual(100, nbe)

        nbth, nbph = input.NBANGL.get()
        self.assertEqual(45, nbth)
        self.assertEqual(18, nbph)

        impact_detectors, = input.impact_detectors.get()
        self.assertEqual(1, len(impact_detectors))

        (el, eu, nbe, ipsf, idcut,
         spectrum_filename, psf_filename, fln_filename,
         agel, ageu, nage, age_filename, kbs, kpars) = impact_detectors[0]
        self.assertAlmostEqual(0.0, el, 5)
        self.assertAlmostEqual(0.0, eu, 5)
        self.assertEqual(100, nbe)
        self.assertEqual(0, ipsf)
        self.assertEqual(2, idcut)
        self.assertIsNone(spectrum_filename)
        self.assertIsNone(psf_filename)
        self.assertIsNone(fln_filename)
        self.assertIsNone(agel)
        self.assertIsNone(ageu)
        self.assertIsNone(nage)
        self.assertIsNone(age_filename)
        self.assertEqual(1, len(kbs))
        self.assertEqual(0, len(kpars))

        energy_deposition_detectors, = input.energy_deposition_detectors.get()
        self.assertEqual(1, len(energy_deposition_detectors))

        el, eu, nbe, spectrum_filename, kbs = energy_deposition_detectors[0]
        self.assertAlmostEqual(0.0, el, 5)
        self.assertAlmostEqual(0.0, eu, 5)
        self.assertEqual(100, nbe)
        self.assertIsNone(spectrum_filename)
        self.assertEqual(1, len(kbs))

        zl, zu, ndbz = input.GRIDZ.get()
        self.assertAlmostEqual(0.0, zl, 5)
        self.assertAlmostEqual(0.005, zu, 5)
        self.assertEqual(100, ndbz)

        ru, ndbr = input.GRIDR.get()
        self.assertAlmostEqual(0.01, ru, 5)
        self.assertEqual(50, ndbr)

        filename, = input.RESUME.get()
        self.assertEqual('dump.dat', filename)

        filename, = input.DUMPTO.get()
        self.assertEqual('dump.dat', filename)

        dumpp, = input.DUMPP.get()
        self.assertAlmostEqual(60.0, dumpp, 5)

        dshn, = input.NSIMSH.get()
        self.assertAlmostEqual(2e9, dshn, 5)

        timea, = input.TIME.get()
        self.assertAlmostEqual(600.0, timea, 5)

    def test_example1_disc_write(self):
        input = create_example1_disc()
        input = self._write_read_input(input)
        self._test_example1_disc(input)

    def test_example1_disc_read(self):
        filepath = os.path.join(self.testdatadir, '1-disc', 'disc.in')
        input = PenmainInput()
        with open(filepath, 'r') as fp:
            input.read(fp)
        self._test_example1_disc(input)

    def _test_example2_plane(self, input):
        kparp, = input.SKPAR.get()
        self.assertEqual(KPAR.PHOTON, kparp)

        se0, = input.SENERG.get()
        self.assertAlmostEqual(3e7, se0, 5)

        sx0, sy0, sz0 = input.SPOSIT.get()
        self.assertAlmostEqual(0.0, sx0, 5)
        self.assertAlmostEqual(0.0, sy0, 5)
        self.assertAlmostEqual(-25.0, sz0, 5)

        theta, phi, alpha = input.SCONE.get()
        self.assertAlmostEqual(0.0, theta, 5)
        self.assertAlmostEqual(0.0, phi, 5)
        self.assertAlmostEqual(5.0, alpha, 5)

        materials, = input.materials.get()
        self.assertEqual(1, len(materials))

        filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[0]
        self.assertEqual('H2O.mat', filename)
        self.assertAlmostEqual(1e5, eabs1, 5)
        self.assertAlmostEqual(1e4, eabs2, 5)
        self.assertAlmostEqual(1e5, eabs3, 5)
        self.assertAlmostEqual(0.05, c1, 5)
        self.assertAlmostEqual(0.05, c2, 5)
        self.assertAlmostEqual(5e3, wcc, 5)
        self.assertAlmostEqual(5e3, wcr, 5)

        self.assertEqual('plane.geo', input.GEOMFN.get()[0])

        el, eu, nbe = input.NBE.get()
        self.assertAlmostEqual(1e5, el, 5)
        self.assertAlmostEqual(3e7, eu, 5)
        self.assertEqual(100, nbe)

        nbth, nbph = input.NBANGL.get()
        self.assertEqual(45, nbth)
        self.assertEqual(18, nbph)

        impact_detectors, = input.impact_detectors.get()
        self.assertEqual(1, len(impact_detectors))

        (el, eu, nbe, ipsf, idcut,
         spectrum_filename, psf_filename, fln_filename,
         agel, ageu, nage, age_filename, kbs, kpars) = impact_detectors[0]
        self.assertAlmostEqual(1e5, el, 5)
        self.assertAlmostEqual(0.0, eu, 5)
        self.assertEqual(100, nbe)
        self.assertEqual(0, ipsf)
        self.assertEqual(2, idcut)
        self.assertIsNone(spectrum_filename)
        self.assertIsNone(psf_filename)
        self.assertIsNone(fln_filename)
        self.assertIsNone(agel)
        self.assertIsNone(ageu)
        self.assertIsNone(nage)
        self.assertIsNone(age_filename)
        self.assertEqual(1, len(kbs))
        self.assertEqual(0, len(kpars))

        zl, zu, ndbz = input.GRIDZ.get()
        self.assertAlmostEqual(0.0, zl, 5)
        self.assertAlmostEqual(30.0, zu, 5)
        self.assertEqual(60, ndbz)

        ru, ndbr = input.GRIDR.get()
        self.assertAlmostEqual(30.0, ru, 5)
        self.assertEqual(60, ndbr)

        filename, = input.RESUME.get()
        self.assertEqual('dump.dat', filename)

        filename, = input.DUMPTO.get()
        self.assertEqual('dump.dat', filename)

        dumpp, = input.DUMPP.get()
        self.assertAlmostEqual(60.0, dumpp, 5)

        dshn, = input.NSIMSH.get()
        self.assertAlmostEqual(1e7, dshn, 5)

        timea, = input.TIME.get()
        self.assertAlmostEqual(2e9, timea, 5)

    def test_example2_plane_write(self):
        input = create_example2_plane()
        input = self._write_read_input(input)
        self._test_example2_plane(input)

    def test_example2_plane_read(self):
        filepath = os.path.join(self.testdatadir, '2-plane', 'plane.in')
        input = PenmainInput()
        with open(filepath, 'r') as fp:
            input.read(fp)
        self._test_example2_plane(input)

if __name__ == '__main__': #pragma: no cover
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
