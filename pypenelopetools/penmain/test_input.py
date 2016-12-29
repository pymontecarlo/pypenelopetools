#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import io
import os

# Third party modules.

# Local modules.
from pypenelopetools.penmain.input import PenmainInput
from pypenelopetools.material.material import Material
from pypenelopetools.pengeom.surface import sphere, zplane
from pypenelopetools.pengeom.module import Module, SIDEPOINTER_NEGATIVE, SIDEPOINTER_POSITIVE
from pypenelopetools.pengeom.geometry import Geometry

# Globals and constants variables.

def create_example1_disc():
    penmain = PenmainInput()

    penmain.TITLE.set('Point source and a homogeneous cylinder.')
    penmain.SKPAR.set(1)
    penmain.SENERG.set(40e3)
    penmain.SPOSIT.set(0.0, 0.0, -0.0001)
    penmain.SCONE.set(0.0, 0.0, 5.0)

    penmain.materials.add("Cu.mat", 1e3, 1e3, 1e3, 0.05, 0.05, 1e3, 1e3)

    penmain.GEOMFN.set('disc.geo')
    penmain.PARINP.add(1, 0.005)
    penmain.PARINP.add(2, 0.01)
    penmain.DSMAX.add(1, 1e-4)

    penmain.IFORCE.add(1, 1, 4, 2000, 0.1, 2.0)
    penmain.IFORCE.add(1, 1, 5, 200, 0.1, 2.0)
    penmain.IBRSPL.add(1, 2)
    penmain.IXRSPL.add(1, 2)

    penmain.NBE.set(0, 0, 100)
    penmain.NBANGL.set(45, 18)

    penmain.impact_detectors.add(0.0, 0.0, 100, 0, 2, kb=1)

    penmain.energy_deposition_detectors.add(0, 0, 100, kb=1)

    penmain.GRIDZ.set(0, 0.005, 100)
    penmain.GRIDR.set(0.01, 50)

    penmain.RESUME.set('dump.dat')
    penmain.DUMPTO.set('dump.dat')
    penmain.DUMPP.set(60)

    penmain.NSIMSH.set(2e9)
    penmain.TIME.set(600)

    return penmain, {}

def create_example2_plane():
    # Create materials
    material_h2o = Material('H2O', {8: 0.8881, 1: 0.1119}, 1.0)

    # Create geometry
    module_detector = Module(material_h2o, 'Fluence detector')
    module_detector.add_surface(sphere(2.0), SIDEPOINTER_NEGATIVE)

    module_phantom = Module(material_h2o, 'Water phantom')
    module_phantom.add_surface(zplane(0.0), SIDEPOINTER_POSITIVE)
    module_phantom.add_surface(zplane(30.0), SIDEPOINTER_NEGATIVE)

    geometry = Geometry('Semi-infinite water phantom')
    geometry.add_module(module_detector)
    geometry.add_module(module_phantom)

    index_table = geometry.indexify()
    geometry.to_geo(index_table) # Optional

    # Create penmain
    penmain = PenmainInput()

    penmain.TITLE.set('Dose in a water phantom with a spherical impact detector')
    penmain.SKPAR.set(2)
    penmain.SENERG.set(3e7)
    penmain.SPOSIT.set(0.0, 0.0, -25.0)
    penmain.SCONE.set(0.0, 0.0, 5.0)

    penmain.materials.add(material_h2o, 1e5, 1e4, 1e5, 0.05, 0.05, 5e3, 5e3)

    penmain.GEOMFN.set('plane.geo')

    penmain.NBE.set(1e5, 3e7, 100)
    penmain.NBANGL.set(45, 18)

    penmain.impact_detectors.add(1e5, 0.0, 100, 0, 2, kb=module_detector)

    penmain.GRIDZ.set(0, 30.0, 60)
    penmain.GRIDR.set(30.0, 60.0)

    penmain.RESUME.set('dump.dat')
    penmain.DUMPTO.set('dump.dat')
    penmain.DUMPP.set(60)

    penmain.NSIMSH.set(1e7)
    penmain.TIME.set(2e9)

    return penmain, index_table

class TestPenmainInput(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.testdatadir = os.path.join(os.path.dirname(__file__),
                                        '..', 'testdata', 'penmain')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def _write_read_penmain(self, penmain, index_table):
        outfileobj = io.StringIO()
        penmain.write(outfileobj, index_table)

        infileobj = io.StringIO(outfileobj.getvalue())
        outpenmain = PenmainInput()
        outpenmain.read(infileobj)

        outfileobj.close()
        infileobj.close()

        return outpenmain

    def _test_example1_disc(self, penmain):
        kparp, = penmain.SKPAR.get()
        self.assertEqual(1, kparp)

        se0, = penmain.SENERG.get()
        self.assertAlmostEqual(40e3, se0, 5)

        sx0, sy0, sz0 = penmain.SPOSIT.get()
        self.assertAlmostEqual(0.0, sx0, 5)
        self.assertAlmostEqual(0.0, sy0, 5)
        self.assertAlmostEqual(-0.0001, sz0, 5)

        theta, phi, alpha = penmain.SCONE.get()
        self.assertAlmostEqual(0.0, theta, 5)
        self.assertAlmostEqual(0.0, phi, 5)
        self.assertAlmostEqual(5.0, alpha, 5)

        materials = penmain.materials.get()
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

        self.assertEqual('disc.geo', penmain.GEOMFN.get()[0])

        parinps = penmain.PARINP.get()
        self.assertEqual(2, len(parinps))

        ip, parinp = parinps[0]
        self.assertEqual(1, ip)
        self.assertAlmostEqual(0.005, parinp, 5)

        ip, parinp = parinps[1]
        self.assertEqual(2, ip)
        self.assertAlmostEqual(0.01, parinp, 5)

        dsmaxs = penmain.DSMAX.get()
        self.assertEqual(1, len(dsmaxs))

        kb, dsmax = dsmaxs[0]
        self.assertEqual(1, kb)
        self.assertAlmostEqual(1e-4, dsmax, 5)

        iforces = penmain.IFORCE.get()
        self.assertEqual(2, len(iforces))

        kb, kpar, icol, forcer, wlow, whig = iforces[0]
        self.assertEqual(1, kb)
        self.assertEqual(1, kpar)
        self.assertEqual(4, icol)
        self.assertAlmostEqual(2000, forcer, 5)
        self.assertAlmostEqual(0.1, wlow, 5)
        self.assertAlmostEqual(2.0, whig, 5)

        kb, kpar, icol, forcer, wlow, whig = iforces[1]
        self.assertEqual(1, kb)
        self.assertEqual(1, kpar)
        self.assertEqual(5, icol)
        self.assertAlmostEqual(200, forcer, 5)
        self.assertAlmostEqual(0.1, wlow, 5)
        self.assertAlmostEqual(2.0, whig, 5)

        ibrspls = penmain.IBRSPL.get()
        self.assertEqual(1, len(ibrspls))

        kb, factor = ibrspls[0]
        self.assertEqual(1, kb)
        self.assertAlmostEqual(2.0, factor, 5)

        ixrspls = penmain.IXRSPL.get()
        self.assertEqual(1, len(ixrspls))

        kb, factor = ibrspls[0]
        self.assertEqual(1, kb)
        self.assertAlmostEqual(2.0, factor, 5)

        el, eu, nbe = penmain.NBE.get()
        self.assertAlmostEqual(0.0, el, 5)
        self.assertAlmostEqual(0.0, eu, 5)
        self.assertEqual(100, nbe)

        nbth, nbph = penmain.NBANGL.get()
        self.assertEqual(45, nbth)
        self.assertEqual(18, nbph)

        impact_detectors = penmain.impact_detectors.get()
        self.assertEqual(1, len(impact_detectors))

        (el, eu, nbe, ipsf, idcut,
         spectrum_filename, psf_filename, fln_filename,
         agel, ageu, nage, age_filename, kb, kpar) = impact_detectors[0]
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
        self.assertEqual(1, kb[0])
        self.assertEqual(0, len(kpar))

        energy_deposition_detectors = penmain.energy_deposition_detectors.get()
        self.assertEqual(1, len(energy_deposition_detectors))

        el, eu, nbe, spectrum_filename, kb = energy_deposition_detectors[0]
        self.assertAlmostEqual(0.0, el, 5)
        self.assertAlmostEqual(0.0, eu, 5)
        self.assertEqual(100, nbe)
        self.assertIsNone(spectrum_filename)
        self.assertEqual(1, kb[0])

        zl, zu, ndbz = penmain.GRIDZ.get()
        self.assertAlmostEqual(0.0, zl, 5)
        self.assertAlmostEqual(0.005, zu, 5)
        self.assertEqual(100, ndbz)

        ru, ndbr = penmain.GRIDR.get()
        self.assertAlmostEqual(0.01, ru, 5)
        self.assertEqual(50, ndbr)

        filename, = penmain.RESUME.get()
        self.assertEqual('dump.dat', filename)

        filename, = penmain.DUMPTO.get()
        self.assertEqual('dump.dat', filename)

        dumpp, = penmain.DUMPP.get()
        self.assertAlmostEqual(60.0, dumpp, 5)

        dshn, = penmain.NSIMSH.get()
        self.assertAlmostEqual(2e9, dshn, 5)

        timea, = penmain.TIME.get()
        self.assertAlmostEqual(600.0, timea, 5)

    def test_example1_disc_write(self):
        penmain, index_table = create_example1_disc()
        penmain = self._write_read_penmain(penmain, index_table)
        self._test_example1_disc(penmain)

    def test_example1_disc_read(self):
        filepath = os.path.join(self.testdatadir, '1-disc', 'disc.in')
        penmain = PenmainInput()
        with open(filepath, 'r') as fp:
            penmain.read(fp)
        self._test_example1_disc(penmain)

    def _test_example2_plane(self, penmain):
        kparp, = penmain.SKPAR.get()
        self.assertEqual(2, kparp)

        se0, = penmain.SENERG.get()
        self.assertAlmostEqual(3e7, se0, 5)

        sx0, sy0, sz0 = penmain.SPOSIT.get()
        self.assertAlmostEqual(0.0, sx0, 5)
        self.assertAlmostEqual(0.0, sy0, 5)
        self.assertAlmostEqual(-25.0, sz0, 5)

        theta, phi, alpha = penmain.SCONE.get()
        self.assertAlmostEqual(0.0, theta, 5)
        self.assertAlmostEqual(0.0, phi, 5)
        self.assertAlmostEqual(5.0, alpha, 5)

        materials = penmain.materials.get()
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

        self.assertEqual('plane.geo', penmain.GEOMFN.get()[0])

        el, eu, nbe = penmain.NBE.get()
        self.assertAlmostEqual(1e5, el, 5)
        self.assertAlmostEqual(3e7, eu, 5)
        self.assertEqual(100, nbe)

        nbth, nbph = penmain.NBANGL.get()
        self.assertEqual(45, nbth)
        self.assertEqual(18, nbph)

        impact_detectors = penmain.impact_detectors.get()
        self.assertEqual(1, len(impact_detectors))

        (el, eu, nbe, ipsf, idcut,
         spectrum_filename, psf_filename, fln_filename,
         agel, ageu, nage, age_filename, kb, kpar) = impact_detectors[0]
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
        self.assertEqual(1, kb[0])
        self.assertEqual(0, len(kpar))

        zl, zu, ndbz = penmain.GRIDZ.get()
        self.assertAlmostEqual(0.0, zl, 5)
        self.assertAlmostEqual(30.0, zu, 5)
        self.assertEqual(60, ndbz)

        ru, ndbr = penmain.GRIDR.get()
        self.assertAlmostEqual(30.0, ru, 5)
        self.assertEqual(60, ndbr)

        filename, = penmain.RESUME.get()
        self.assertEqual('dump.dat', filename)

        filename, = penmain.DUMPTO.get()
        self.assertEqual('dump.dat', filename)

        dumpp, = penmain.DUMPP.get()
        self.assertAlmostEqual(60.0, dumpp, 5)

        dshn, = penmain.NSIMSH.get()
        self.assertAlmostEqual(1e7, dshn, 5)

        timea, = penmain.TIME.get()
        self.assertAlmostEqual(2e9, timea, 5)

    def test_example2_plane_write(self):
        penmain, index_table = create_example2_plane()
        penmain = self._write_read_penmain(penmain, index_table)
        self._test_example2_plane(penmain)

    def test_example2_plane_read(self):
        filepath = os.path.join(self.testdatadir, '2-plane', 'plane.in')
        penmain = PenmainInput()
        with open(filepath, 'r') as fp:
            penmain.read(fp)
        self._test_example2_plane(penmain)

if __name__ == '__main__': #pragma: no cover
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
