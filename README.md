#pyPENELOPEtools

[![PyPI](https://img.shields.io/pypi/v/pypenelopetools.svg)]()
[![TravisCI](https://travis-ci.org/pymontecarlo/pypenelopetools.svg?branch=master)]()
[![Codecov](https://codecov.io/github/pymontecarlo/pypenelopetools/coverage.svg?branch=master)]()

**pyPENELOPEtools** is an open-source software to facilitate the use of the 
Monte Carlo code PENELOPE and its main programs such as PENEPMA. 
It is a programming interface to setup, run and analyze Monte Carlo simulations.
Most of the code was adapted from [pyPENELOPE](http://pypenelope.sourceforge.net/), but
with the goal to facilitate the integration with [pyMonteCarlo](https://github.com/pymontecarlo/pymontecarlo).

**pyPENELOPEtools** is currently under development.

##What is PENELOPE?

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
[OECD/NEA Data Bank](http://www.nea.fr). 
The distribution package includes a report :cite:`Salvat2006` that provides 
detailed information on the physical models and random sampling algorithms 
adopted in PENELOPE, on the PENGEOM geometry package, and on the structure and 
operation of the simulation routines.

PENELOPE is coded as a set of [FORTRAN](http://en.wikipedia.org/wiki/Fortran) 
subroutines, which perform the random sampling of interactions and the tracking 
of particles (either electrons, positrons or photons). 
In principle, the user should provide a main steering program to follow the 
particle histories through the material structure and to keep score of 
quantities of interest.

##Authors

- [Philippe T. Pinard](https://github.com/ppinard) (High Wycombe, United Kingdom)
- [Hendrix Demers](https://github.com/drix00) (McGill University, Montreal, Canada)
