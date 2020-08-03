#!/bin/bash
# A simple code to run an existing Singularity image

singularity exec --bind /home/gcao/Datasets:/data --bind /home/gcao/Projects:/root/Projects \
    /vcc/cads/cads4/Development/ADIntelligence/Singularity/geo.sif python -c "help('geopandas')" 
