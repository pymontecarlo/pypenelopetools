pyPENELOPEtools
===============

.. image:: https://img.shields.io/pypi/v/pypenelopetools.svg
.. image:: https://img.shields.io/travis/pymontecarlo/pypenelopetools.svg
.. image:: https://img.shields.io/codecov/c/github/pymontecarlo/pypenelopetools.svg

**pyPENELOPEtools** is an open-source software to facilitate the use of the
Monte Carlo code PENELOPE and its main programs such as PENEPMA.
It is a programming interface to setup, run and analyze Monte Carlo simulations.
Most of the code was adapted from `pyPENELOPE <http://pypenelope.sourceforge.net>`_, but
with the goal to facilitate the integration with
`pyMonteCarlo <https://github.com/pymontecarlo/pymontecarlo>`_.

What is PENELOPE?
-----------------

PENELOPE (*Penetration and ENErgy LOss of Positrons and Electrons*) is a
a general-purpose Monte Carlo code system for the simulation of coupled
electron-photon transport in arbitrary materials.
PENELOPE covers the energy range from 1 GeV down to, nominally, 50 eV.
The physical interaction models implemented in the code are
based on the most reliable information available at present, limited only by
the required generality of the code.
These models combine results from first-principles calculations, semi-empirical
models and evaluated data bases.
It should be borne in mind that although PENELOPE can run particles down to 50
eV, the interaction cross sections for energies below 1 keV may be affected by
sizeable uncertainties; the results for these energies should be considered as
semi-quantitative.

PENELOPE incorporates a flexible geometry package called PENGEOM that permits
automatic tracking of particles in complex geometries consisting of homogeneous
bodies limited by quadratic surfaces.
The PENELOPE code system is distributed by the
`OECD/NEA Data Bank <http://www.nea.fr>`_.

PENELOPE is coded as a set of `FORTRAN <http://en.wikipedia.org/wiki/Fortran>`_
subroutines, which perform the random sampling of interactions and the tracking
of particles (either electrons, positrons or photons).
In principle, the user should provide a main steering program to follow the
particle histories through the material structure and to keep score of
quantities of interest.

Documentation
-------------

The `documentation <http://pypenelopetools.readthedocs.io>`_ contains the
installation instructions, tutorials and API.

Release notes
-------------

1.1.1
^^^^^

* Add enums for KPAR and ICOL
* Add result from generated photon intensity

1.0.0
^^^^^

* First release

Authors
-------

- `Philippe T. Pinard <https://github.com/ppinard>`_
- `Hendrix Demers <https://github.com/drix00>`_

License
-------

License under Apache Software License 2.0.

Copyright (c) 2017-2018 Philippe Pinard
