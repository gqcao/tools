#!/bin/bash
#SBATCH -J mpi0 
# time 2 day and 23 hour, in parallel partition, you can only run one day max, and the number of jobs has to be dozens
#SBATCH -o mpi.out
#SBATCH -e mpi.err
#SBATCH -N 1 
#SBATCH -n 6 
#SBATCH --time=2-23:59:0
#SBATCH --mem-per-cpu=4000

# module swap intel/13.1.0 gcc/4.8.2
module load intelmpi/4.1.0 
cd ~/misc/tools
srun ./getSlides_mpi.py 
