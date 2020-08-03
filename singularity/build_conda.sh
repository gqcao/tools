#!/bin/bash
# Wrap to a sif image based on the definition file
sudo singularity build geo.sif geopandas.def

# Wrap to a code image based on the definition file
#sudo singularity build --sandbox py37/ docker://continuumio/miniconda

# Wrap to a writable image based on the definition file
#sudo singularity shell --writable py37
