#!/bin/bash

#set -e 

k=24.0
f=0.027

home=/usr/users/iff_th2/duman
loc=/local/duman/SIMULATIONS
script=/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/bin
path=kappa_${k}/fp_${f}
path2=kappa_${k}_fp_${f}
savefolder=${home}/HighDens_Filaments/DATA/Defects/${path2}
mkdir -p ${savefolder}

cd ../build
rm -r *
export CXX=/usr/local/gcc6/bin/g++
cmake -D CMAKE_CXX_COMPILER=/usr/local/gcc6/bin/g++ -D CMAKE_BUILD_TYPE=Debug ..
make install
cd ../bin
export LD_LIBRARY_PATH="/usr/users/iff_th2/duman/hdf5_parallel/lib:$LD_LIBRARY_PATH"
mpirun -np 4 ${script}/exec_debug ${loc}/HighDens_Filaments/Simulations/density_0.8/${path}/out.h5 ${savefolder}

