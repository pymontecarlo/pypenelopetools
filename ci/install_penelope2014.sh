#!/bin/bash

openssl aes-256-cbc -K $encrypted_8ed1e0a06d33_key -iv $encrypted_8ed1e0a06d33_iv
  -in fortran/penelope2014.zip.enc -out fortran/penelope2014.zip -d

cd fortran
unzip penelope2014.zip

cd penelope/fsource
gfortran material.f -o material

