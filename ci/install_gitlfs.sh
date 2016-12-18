#!/bin/bash

mkdir -p $HOME/bin
wget https://github.com/git-lfs/git-lfs/releases/download/v1.5.3/git-lfs-linux-amd64-1.5.3.tar.gz
tar xvfz git-lfs-linux-amd64-1.5.3.tar.gz
mv git-lfs-1.5.3/git-lfs $HOME/bin/git-lfs
export PATH=$PATH:$HOME/bin/

git lfs pull