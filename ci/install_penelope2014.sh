#!/bin/bash

cd fortran

unzip penelope2014.zip

cd penelope/fsource
gfortran material.f -o material

