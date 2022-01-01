#!/usr/bin/env python

# Standard library modules.
import os

# Third party modules.
from setuptools import setup, find_packages

# Local modules.
import versioneer

# Globals and constants variables.
BASEDIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(BASEDIR, "README.md"), "r") as fp:
    LONG_DESCRIPTION = fp.read()

PACKAGES = find_packages()

with open(os.path.join(BASEDIR, "requirements.txt"), "r") as fp:
    INSTALL_REQUIRES = fp.read().splitlines()

EXTRAS_REQUIRE = {}

CMDCLASS = versioneer.get_cmdclass()

ENTRY_POINTS = {}

setup(
    name="pyPENELOPEtools",
    version=versioneer.get_version(),
    url="https://github.com/pymontecarlo/pypenelopetools",
    description="Python interface to facilitate the use of the Monte Carlo code PENELOPE and its main programs",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Philippe T. Pinard",
    author_email="philippe.pinard@gmail.com",
    license="Apache License, Version 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    cmdclass=CMDCLASS,
    entry_points=ENTRY_POINTS,
)
