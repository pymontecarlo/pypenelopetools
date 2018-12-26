#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import io
import os

# Third party modules.
import pyxray

# Local modules.
from pypenelopetools.penelope.enums import KPAR, ICOL
from pypenelopetools.penepma.input import PenepmaInput
from pypenelopetools.material import Material
from pypenelopetools.pengeom.surface import xplane, zplane, cylinder
from pypenelopetools.pengeom.module import Module, SidePointer
from pypenelopetools.pengeom.geometry import Geometry
from pypenelopetools.penepma.utils import convert_xrayline_to_izs1s200

# Globals and constants variables.

MATERIAL_CU = Material('Cu', {29: 1.0}, 8.9)
MATERIAL_FE = Material('Fe', {26: 1.0}, 7.874)
XRAYLINE_CU_KA2 = pyxray.xray_line(29, 'Ka2')
XRAYLINE_FE_KA2 = pyxray.xray_line(26, 'Ka2')

def create_epma1():
    # Create geometry
    module = Module(MATERIAL_CU, 'Sample')
    module.add_surface(zplane(0.0), SidePointer.NEGATIVE)
    module.add_surface(zplane(-0.1), SidePointer.POSITIVE)
    module.add_surface(cylinder(1.0), SidePointer.NEGATIVE)

    geometry = Geometry('Cylindrical homogeneous foil')
    geometry.add_module(module)

    index_lookup = geometry.indexify()

    # Create input
    input = PenepmaInput()

    input.TITLE.set('A Cu slab')
    input.SENERG.set(15e3)
    input.SPOSIT.set(0.0, 0.0, 1.0)
    input.SDIREC.set(180, 0.0)
    input.SAPERT.set(0.0)

    input.materials.add(index_lookup[MATERIAL_CU], MATERIAL_CU.filename, 1e3, 1e3, 1e3, 0.2, 0.2, 1e3, 1e3)

    input.GEOMFN.set('epma1.geo')
    input.DSMAX.add(index_lookup[module], 1e-4)

    input.IFORCE.add(index_lookup[module], KPAR.ELECTRON, ICOL.HARD_BREMSSTRAHLUNG_EMISSION, -5, 0.9, 1.0)
    input.IFORCE.add(index_lookup[module], KPAR.ELECTRON, ICOL.INNER_SHELL_IMPACT_IONISATION, -250, 0.9, 1.0)
    input.IFORCE.add(index_lookup[module], KPAR.PHOTON, ICOL.INCOHERENT_SCATTERING, 10, 1e-3, 1.0)
    input.IFORCE.add(index_lookup[module], KPAR.PHOTON, ICOL.PHOTOELECTRIC_ABSORPTION, 10, 1e-3, 1.0)
    input.IBRSPL.add(index_lookup[module], 2)
    input.IXRSPL.add(index_lookup[module], 2)

    input.NBE.set(0, 0, 300)
    input.NBANGL.set(45, 30)

    input.photon_detectors.add(0, 90, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(5, 15, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(15, 25, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(25, 35, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(35, 45, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(45, 55, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(55, 65, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(65, 75, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(75, 85, 0, 360, 0, 0.0, 0.0, 1000)

    input.GRIDX.set(-4e-5, 4e-5, 60)
    input.GRIDY.set(-4e-5, 4e-5, 60)
    input.GRIDZ.set(-6e-5, 0.0, 60)
    input.XRLINE.add(convert_xrayline_to_izs1s200(XRAYLINE_CU_KA2))

    input.RESUME.set('dump1.dat')
    input.DUMPTO.set('dump1.dat')
    input.DUMPP.set(60)

    input.RSEED.set(-10, 1)
    input.REFLIN.set(convert_xrayline_to_izs1s200(XRAYLINE_CU_KA2), 1, 1.25e-3)
    input.NSIMSH.set(2e9)
    input.TIME.set(2e9)

    return input

def create_epma2():
    # Create geometry
    surface_top = zplane(0.0)
    surface_bottom = zplane(-0.1)
    surface_cylinder = cylinder(1.0)
    surface_divider = xplane(0.0)

    module_right = Module(MATERIAL_CU, 'Right half of the sample')
    module_right.add_surface(surface_top, SidePointer.NEGATIVE)
    module_right.add_surface(surface_bottom, SidePointer.POSITIVE)
    module_right.add_surface(surface_cylinder, SidePointer.NEGATIVE)
    module_right.add_surface(surface_divider, SidePointer.POSITIVE)

    module_left = Module(MATERIAL_FE, 'Left half of the sample')
    module_left.add_surface(surface_top, SidePointer.NEGATIVE)
    module_left.add_surface(surface_bottom, SidePointer.POSITIVE)
    module_left.add_surface(surface_cylinder, SidePointer.NEGATIVE)
    module_left.add_module(module_right)

    geometry = Geometry('Cylindrical homogeneous foil')
    geometry.add_module(module_right)
    geometry.add_module(module_left)

    index_lookup = geometry.indexify()
    index_lookup[MATERIAL_CU] = 1
    index_lookup[MATERIAL_FE] = 2

    # Create input
    input = PenepmaInput()

    input.TITLE.set('A CU-Fe couple')
    input.SENERG.set(15e3)
    input.SPOSIT.set(2e-5, 0.0, 1.0)
    input.SDIREC.set(180, 0.0)
    input.SAPERT.set(0.0)

    input.materials.add(index_lookup[MATERIAL_FE], MATERIAL_FE.filename, 1e3, 1e3, 1e3, 0.2, 0.2, 1e3, 1e3) # Note inversion
    input.materials.add(index_lookup[MATERIAL_CU], MATERIAL_CU.filename, 1e3, 1e3, 1e3, 0.2, 0.2, 1e3, 1e3)

    input.GEOMFN.set('epma2.geo')
    input.DSMAX.add(index_lookup[module_right], 1e-4)
    input.DSMAX.add(index_lookup[module_left], 1e-4)

    input.IFORCE.add(index_lookup[module_right], KPAR.ELECTRON, ICOL.HARD_BREMSSTRAHLUNG_EMISSION, -5, 0.9, 1.0)
    input.IFORCE.add(index_lookup[module_right], KPAR.ELECTRON, ICOL.INNER_SHELL_IMPACT_IONISATION, -250, 0.9, 1.0)
    input.IFORCE.add(index_lookup[module_right], KPAR.PHOTON, ICOL.INCOHERENT_SCATTERING, 10, 1e-3, 1.0)
    input.IFORCE.add(index_lookup[module_right], KPAR.PHOTON, ICOL.PHOTOELECTRIC_ABSORPTION, 10, 1e-3, 1.0)
    input.IFORCE.add(index_lookup[module_left], KPAR.ELECTRON, ICOL.HARD_BREMSSTRAHLUNG_EMISSION, -5, 0.9, 1.0)
    input.IFORCE.add(index_lookup[module_left], KPAR.ELECTRON, ICOL.INNER_SHELL_IMPACT_IONISATION, -7, 0.9, 1.0)
    input.IFORCE.add(index_lookup[module_left], KPAR.PHOTON, ICOL.INCOHERENT_SCATTERING, 10, 1e-3, 1.0)
    input.IFORCE.add(index_lookup[module_left], KPAR.PHOTON, ICOL.PHOTOELECTRIC_ABSORPTION, 10, 1e-3, 1.0)

    input.IBRSPL.add(index_lookup[module_right], 2)
    input.IBRSPL.add(index_lookup[module_left], 2)

    input.IXRSPL.add(index_lookup[module_right], 2)
    input.IXRSPL.add(index_lookup[module_left], 2)

    input.NBE.set(0, 0, 300)
    input.NBANGL.set(45, 30)

    input.photon_detectors.add(0, 90, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(5, 15, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(15, 25, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(25, 35, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(35, 45, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(45, 55, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(55, 65, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(65, 75, 0, 360, 0, 0.0, 0.0, 1000)
    input.photon_detectors.add(75, 85, 0, 360, 0, 0.0, 0.0, 1000)

    input.GRIDX.set(-1e-5, 5e-5, 60)
    input.GRIDY.set(-3e-5, 3e-5, 60)
    input.GRIDZ.set(-6e-5, 0.0, 60)
    input.XRLINE.add(convert_xrayline_to_izs1s200(XRAYLINE_FE_KA2))
    input.XRLINE.add(convert_xrayline_to_izs1s200(XRAYLINE_CU_KA2))

    input.RESUME.set('dump2.dat')
    input.DUMPTO.set('dump2.dat')
    input.DUMPP.set(60)

    input.RSEED.set(-10, 1)
    input.REFLIN.set(convert_xrayline_to_izs1s200(XRAYLINE_FE_KA2), 1, 1.5e-3)
    input.NSIMSH.set(2e9)
    input.TIME.set(2e9)

    return input

class TestPenmainInput(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.testdatadir = os.path.join(os.path.dirname(__file__),
                                        '..', 'testdata', 'penepma')

    def _write_read_input(self, input):
        fileobj = io.StringIO()

        try:
            input.write(fileobj)

            fileobj.seek(0)
            outinput = PenepmaInput()
            outinput.read(fileobj)
        finally:
            fileobj.close()

        return outinput

    def _test_epma1(self, input):
        se0, = input.SENERG.get()
        self.assertAlmostEqual(15e3, se0, 5)

        sx0, sy0, sz0 = input.SPOSIT.get()
        self.assertAlmostEqual(0.0, sx0, 5)
        self.assertAlmostEqual(0.0, sy0, 5)
        self.assertAlmostEqual(1.0, sz0, 5)

        theta, phi = input.SDIREC.get()
        self.assertAlmostEqual(180.0, theta, 5)
        self.assertAlmostEqual(0.0, phi, 5)

        alpha, = input.SAPERT.get()
        self.assertAlmostEqual(0.0, alpha, 5)

        materials, = input.materials.get()
        self.assertEqual(1, len(materials))

        filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[0]
        self.assertEqual('Cu.mat', filename)
        self.assertAlmostEqual(1e3, eabs1, 5)
        self.assertAlmostEqual(1e3, eabs2, 5)
        self.assertAlmostEqual(1e3, eabs3, 5)
        self.assertAlmostEqual(0.2, c1, 5)
        self.assertAlmostEqual(0.2, c2, 5)
        self.assertAlmostEqual(1e3, wcc, 5)
        self.assertAlmostEqual(1e3, wcr, 5)

        self.assertEqual('epma1.geo', input.GEOMFN.get()[0])

        dsmaxs, = input.DSMAX.get()
        self.assertEqual(1, len(dsmaxs))

        kb, dsmax = dsmaxs[0]
        self.assertEqual(1, kb)
        self.assertAlmostEqual(1e-4, dsmax, 5)

        iforces, = input.IFORCE.get()
        self.assertEqual(4, len(iforces))

        kb, kpar, icol, forcer, wlow, whig = iforces[0]
        self.assertEqual(1, kb)
        self.assertEqual(1, kpar)
        self.assertEqual(4, icol)
        self.assertAlmostEqual(-5, forcer, 5)
        self.assertAlmostEqual(0.9, wlow, 5)
        self.assertAlmostEqual(1.0, whig, 5)

        kb, kpar, icol, forcer, wlow, whig = iforces[1]
        self.assertEqual(1, kb)
        self.assertEqual(1, kpar)
        self.assertEqual(5, icol)
        self.assertAlmostEqual(-250, forcer, 5)
        self.assertAlmostEqual(0.9, wlow, 5)
        self.assertAlmostEqual(1.0, whig, 5)

        kb, kpar, icol, forcer, wlow, whig = iforces[2]
        self.assertEqual(1, kb)
        self.assertEqual(2, kpar)
        self.assertEqual(2, icol)
        self.assertAlmostEqual(10, forcer, 5)
        self.assertAlmostEqual(1e-3, wlow, 5)
        self.assertAlmostEqual(1.0, whig, 5)

        kb, kpar, icol, forcer, wlow, whig = iforces[3]
        self.assertEqual(1, kb)
        self.assertEqual(2, kpar)
        self.assertEqual(3, icol)
        self.assertAlmostEqual(10, forcer, 5)
        self.assertAlmostEqual(1e-3, wlow, 5)
        self.assertAlmostEqual(1.0, whig, 5)

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
        self.assertEqual(300, nbe)

        nbth, nbph = input.NBANGL.get()
        self.assertEqual(45, nbth)
        self.assertEqual(30, nbph)

        photon_detectors, = input.photon_detectors.get()
        self.assertEqual(9, len(photon_detectors))

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[0]
        self.assertAlmostEqual(0.0, theta1, 5)
        self.assertAlmostEqual(90.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[1]
        self.assertAlmostEqual(5.0, theta1, 5)
        self.assertAlmostEqual(15.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[2]
        self.assertAlmostEqual(15.0, theta1, 5)
        self.assertAlmostEqual(25.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[3]
        self.assertAlmostEqual(25.0, theta1, 5)
        self.assertAlmostEqual(35.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[4]
        self.assertAlmostEqual(35.0, theta1, 5)
        self.assertAlmostEqual(45.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[5]
        self.assertAlmostEqual(45.0, theta1, 5)
        self.assertAlmostEqual(55.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[6]
        self.assertAlmostEqual(55.0, theta1, 5)
        self.assertAlmostEqual(65.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[7]
        self.assertAlmostEqual(65.0, theta1, 5)
        self.assertAlmostEqual(75.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[8]
        self.assertAlmostEqual(75.0, theta1, 5)
        self.assertAlmostEqual(85.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        xl, xu, ndbx = input.GRIDX.get()
        self.assertAlmostEqual(-4e-5, xl, 5)
        self.assertAlmostEqual(4e-5, xu, 5)
        self.assertEqual(60, ndbx)

        yl, yu, ndby = input.GRIDY.get()
        self.assertAlmostEqual(-4e-5, yl, 5)
        self.assertAlmostEqual(4e-5, yu, 5)
        self.assertEqual(60, ndby)

        zl, zu, ndbz = input.GRIDZ.get()
        self.assertAlmostEqual(-6e-5, zl, 5)
        self.assertAlmostEqual(0.0, zu, 5)
        self.assertEqual(60, ndbz)

        xrlines, = input.XRLINE.get()
        self.assertEqual(1, len(xrlines))

        izs1s200, = xrlines[0]
        self.assertEqual(29010300, izs1s200)

        filename, = input.RESUME.get()
        self.assertEqual('dump1.dat', filename)

        filename, = input.DUMPTO.get()
        self.assertEqual('dump1.dat', filename)

        dumpp, = input.DUMPP.get()
        self.assertAlmostEqual(60.0, dumpp, 5)

        seed1, seed2 = input.RSEED.get()
        self.assertEqual(-10, seed1)
        self.assertEqual(1, seed2)

        izs1s200, idet, tol = input.REFLIN.get()
        self.assertEqual(29010300, izs1s200)
        self.assertEqual(1, idet)
        self.assertAlmostEqual(1.25e-3, tol, 5)

        dshn, = input.NSIMSH.get()
        self.assertAlmostEqual(2e9, dshn, 5)

        timea, = input.TIME.get()
        self.assertAlmostEqual(2e9, timea, 5)

    def test_epma1_skeleton(self):
        input = create_epma1()
        self._test_epma1(input)

    def test_epma1_write(self):
        input = create_epma1()
        input = self._write_read_input(input)
        self._test_epma1(input)

    def test_epma1_read(self):
        filepath = os.path.join(self.testdatadir, 'epma1.in')
        input = PenepmaInput()
        with open(filepath, 'r') as fp:
            input.read(fp)
        self._test_epma1(input)

    def _test_epma2(self, input):
        se0, = input.SENERG.get()
        self.assertAlmostEqual(15e3, se0, 5)

        sx0, sy0, sz0 = input.SPOSIT.get()
        self.assertAlmostEqual(2e-5, sx0, 8)
        self.assertAlmostEqual(0.0, sy0, 5)
        self.assertAlmostEqual(1.0, sz0, 5)

        theta, phi = input.SDIREC.get()
        self.assertAlmostEqual(180.0, theta, 5)
        self.assertAlmostEqual(0.0, phi, 5)

        alpha, = input.SAPERT.get()
        self.assertAlmostEqual(0.0, alpha, 5)

        materials, = input.materials.get()
        self.assertEqual(2, len(materials))

        filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[0]
        self.assertEqual('Cu.mat', filename)
        self.assertAlmostEqual(1e3, eabs1, 5)
        self.assertAlmostEqual(1e3, eabs2, 5)
        self.assertAlmostEqual(1e3, eabs3, 5)
        self.assertAlmostEqual(0.2, c1, 5)
        self.assertAlmostEqual(0.2, c2, 5)
        self.assertAlmostEqual(1e3, wcc, 5)
        self.assertAlmostEqual(1e3, wcr, 5)

        filename, eabs1, eabs2, eabs3, c1, c2, wcc, wcr = materials[1]
        self.assertEqual('Fe.mat', filename)
        self.assertAlmostEqual(1e3, eabs1, 5)
        self.assertAlmostEqual(1e3, eabs2, 5)
        self.assertAlmostEqual(1e3, eabs3, 5)
        self.assertAlmostEqual(0.2, c1, 5)
        self.assertAlmostEqual(0.2, c2, 5)
        self.assertAlmostEqual(1e3, wcc, 5)
        self.assertAlmostEqual(1e3, wcr, 5)

        self.assertEqual('epma2.geo', input.GEOMFN.get()[0])

        dsmaxs, = input.DSMAX.get()
        self.assertEqual(2, len(dsmaxs))

        kb, dsmax = dsmaxs[0]
        self.assertEqual(1, kb)
        self.assertAlmostEqual(1e-4, dsmax, 5)

        kb, dsmax = dsmaxs[1]
        self.assertEqual(2, kb)
        self.assertAlmostEqual(1e-4, dsmax, 5)

        iforces, = input.IFORCE.get()
        self.assertEqual(8, len(iforces))

        kb, kpar, icol, forcer, wlow, whig = iforces[0]
        self.assertEqual(1, kb)
        self.assertEqual(1, kpar)
        self.assertEqual(4, icol)
        self.assertAlmostEqual(-5, forcer, 5)
        self.assertAlmostEqual(0.9, wlow, 5)
        self.assertAlmostEqual(1.0, whig, 5)

        kb, kpar, icol, forcer, wlow, whig = iforces[1]
        self.assertEqual(1, kb)
        self.assertEqual(1, kpar)
        self.assertEqual(5, icol)
        self.assertAlmostEqual(-250, forcer, 5)
        self.assertAlmostEqual(0.9, wlow, 5)
        self.assertAlmostEqual(1.0, whig, 5)

        kb, kpar, icol, forcer, wlow, whig = iforces[2]
        self.assertEqual(1, kb)
        self.assertEqual(2, kpar)
        self.assertEqual(2, icol)
        self.assertAlmostEqual(10, forcer, 5)
        self.assertAlmostEqual(1e-3, wlow, 5)
        self.assertAlmostEqual(1.0, whig, 5)

        kb, kpar, icol, forcer, wlow, whig = iforces[3]
        self.assertEqual(1, kb)
        self.assertEqual(2, kpar)
        self.assertEqual(3, icol)
        self.assertAlmostEqual(10, forcer, 5)
        self.assertAlmostEqual(1e-3, wlow, 5)
        self.assertAlmostEqual(1.0, whig, 5)

        kb, kpar, icol, forcer, wlow, whig = iforces[4]
        self.assertEqual(2, kb)
        self.assertEqual(1, kpar)
        self.assertEqual(4, icol)
        self.assertAlmostEqual(-5, forcer, 5)
        self.assertAlmostEqual(0.9, wlow, 5)
        self.assertAlmostEqual(1.0, whig, 5)

        kb, kpar, icol, forcer, wlow, whig = iforces[5]
        self.assertEqual(2, kb)
        self.assertEqual(1, kpar)
        self.assertEqual(5, icol)
        self.assertAlmostEqual(-7, forcer, 5)
        self.assertAlmostEqual(0.9, wlow, 5)
        self.assertAlmostEqual(1.0, whig, 5)

        kb, kpar, icol, forcer, wlow, whig = iforces[6]
        self.assertEqual(2, kb)
        self.assertEqual(2, kpar)
        self.assertEqual(2, icol)
        self.assertAlmostEqual(10, forcer, 5)
        self.assertAlmostEqual(1e-3, wlow, 5)
        self.assertAlmostEqual(1.0, whig, 5)

        kb, kpar, icol, forcer, wlow, whig = iforces[7]
        self.assertEqual(2, kb)
        self.assertEqual(2, kpar)
        self.assertEqual(3, icol)
        self.assertAlmostEqual(10, forcer, 5)
        self.assertAlmostEqual(1e-3, wlow, 5)
        self.assertAlmostEqual(1.0, whig, 5)

        ibrspls, = input.IBRSPL.get()
        self.assertEqual(2, len(ibrspls))

        kb, factor = ibrspls[0]
        self.assertEqual(1, kb)
        self.assertAlmostEqual(2.0, factor, 5)

        kb, factor = ibrspls[1]
        self.assertEqual(2, kb)
        self.assertAlmostEqual(2.0, factor, 5)

        ixrspls, = input.IXRSPL.get()
        self.assertEqual(2, len(ixrspls))

        kb, factor = ixrspls[0]
        self.assertEqual(1, kb)
        self.assertAlmostEqual(2.0, factor, 5)

        kb, factor = ixrspls[1]
        self.assertEqual(2, kb)
        self.assertAlmostEqual(2.0, factor, 5)

        el, eu, nbe = input.NBE.get()
        self.assertAlmostEqual(0.0, el, 5)
        self.assertAlmostEqual(0.0, eu, 5)
        self.assertEqual(300, nbe)

        nbth, nbph = input.NBANGL.get()
        self.assertEqual(45, nbth)
        self.assertEqual(30, nbph)

        photon_detectors, = input.photon_detectors.get()
        self.assertEqual(9, len(photon_detectors))

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[0]
        self.assertAlmostEqual(0.0, theta1, 5)
        self.assertAlmostEqual(90.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[1]
        self.assertAlmostEqual(5.0, theta1, 5)
        self.assertAlmostEqual(15.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[2]
        self.assertAlmostEqual(15.0, theta1, 5)
        self.assertAlmostEqual(25.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[3]
        self.assertAlmostEqual(25.0, theta1, 5)
        self.assertAlmostEqual(35.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[4]
        self.assertAlmostEqual(35.0, theta1, 5)
        self.assertAlmostEqual(45.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[5]
        self.assertAlmostEqual(45.0, theta1, 5)
        self.assertAlmostEqual(55.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[6]
        self.assertAlmostEqual(55.0, theta1, 5)
        self.assertAlmostEqual(65.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[7]
        self.assertAlmostEqual(65.0, theta1, 5)
        self.assertAlmostEqual(75.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        (theta1, theta2, phi1, phi2, ipsf,
         edel, edeu, nche, emission_filename) = photon_detectors[8]
        self.assertAlmostEqual(75.0, theta1, 5)
        self.assertAlmostEqual(85.0, theta2, 5)
        self.assertAlmostEqual(0.0, phi1, 5)
        self.assertAlmostEqual(360.0, phi2, 5)
        self.assertEqual(0, ipsf)
        self.assertAlmostEqual(0.0, edel, 5)
        self.assertAlmostEqual(0.0, edeu, 5)
        self.assertEqual(1000, nche)
        self.assertIsNone(emission_filename)

        xl, xu, ndbx = input.GRIDX.get()
        self.assertAlmostEqual(-1e-5, xl, 5)
        self.assertAlmostEqual(5e-5, xu, 5)
        self.assertEqual(60, ndbx)

        yl, yu, ndby = input.GRIDY.get()
        self.assertAlmostEqual(-3e-5, yl, 5)
        self.assertAlmostEqual(3e-5, yu, 5)
        self.assertEqual(60, ndby)

        zl, zu, ndbz = input.GRIDZ.get()
        self.assertAlmostEqual(-6e-5, zl, 5)
        self.assertAlmostEqual(0.0, zu, 5)
        self.assertEqual(60, ndbz)

        xrlines, = input.XRLINE.get()
        self.assertEqual(2, len(xrlines))

        izs1s200, = xrlines[0]
        self.assertEqual(26010300, izs1s200)

        izs1s200, = xrlines[1]
        self.assertEqual(29010300, izs1s200)

        filename, = input.RESUME.get()
        self.assertEqual('dump2.dat', filename)

        filename, = input.DUMPTO.get()
        self.assertEqual('dump2.dat', filename)

        dumpp, = input.DUMPP.get()
        self.assertAlmostEqual(60.0, dumpp, 5)

        seed1, seed2 = input.RSEED.get()
        self.assertEqual(-10, seed1)
        self.assertEqual(1, seed2)

        izs1s200, idet, tol = input.REFLIN.get()
        self.assertEqual(26010300, izs1s200)
        self.assertEqual(1, idet)
        self.assertAlmostEqual(1.5e-3, tol, 5)

        dshn, = input.NSIMSH.get()
        self.assertAlmostEqual(2e9, dshn, 5)

        timea, = input.TIME.get()
        self.assertAlmostEqual(2e9, timea, 5)

    def test_epma2_skeleton(self):
        input = create_epma2()
        self._test_epma2(input)

    def test_epma2_write(self):
        input = create_epma2()
        input = self._write_read_input(input)
        self._test_epma2(input)

    def test_epma2_read(self):
        filepath = os.path.join(self.testdatadir, 'epma2.in')
        input = PenepmaInput()
        with open(filepath, 'r') as fp:
            input.read(fp)
        self._test_epma2(input)

if __name__ == '__main__': #pragma: no cover
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
