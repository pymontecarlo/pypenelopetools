#!/bin/bash

cd fortran

unzip penelope2014.zip

cd penelope/fsource
gfortran material.f -o material

cd $HOME/build/pymontecarlo/pypenelopetools
echo "[pypenelopetools.material.program:Material2014Program]" >> pypenelopetools.cfg
echo "name=material" >> pypenelopetools.cfg
echo "version=2014" >> pypenelopetools.cfg
echo "executable_path=$HOME/build/pymontecarlo/pypenelopetools/fortran/penelope/fsource/material" >> pypenelopetools.cfg
echo "pendbase_path=$HOME/build/pymontecarlo/pypenelopetools/fortran/penelope/pendbase/" >> pypenelopetools.cfg