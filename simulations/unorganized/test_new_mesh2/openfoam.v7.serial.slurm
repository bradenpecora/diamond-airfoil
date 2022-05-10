#!/bin/bash

# See https://portal.tacc.utexas.edu/user-guides/stampede2/#running 
# for more details

#SBATCH -J OF-finalproj      # Job name
#SBATCH -o job.o%j       # Name of stdout output file
#SBATCH -e job.e%j       # Name of stderr error file

#SBATCH -p normal          # Queue (partition) name
### #SBATCH -p development          # Queue (partition) name
### #SBATCH -p skx-normal          # Queue (partition) name

#SBATCH -N 1               # Total # of nodes
#SBATCH -n 64               # Total # of mpi tasks
#SBATCH -t 01:00:00        # Run time (hh:mm:ss)

#SBATCH -A COE-347-S22       # Allocation name (req'd if you have more than 1)

# Other commands must follow all #SBATCH directives...

module purge
module load intel/18.0.2  libfabric/1.7.0  impi/18.0.2 openfoam/7.0
module list

pwd
date

bash ./AllrunParallel

date
