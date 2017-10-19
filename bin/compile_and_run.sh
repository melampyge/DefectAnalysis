#!/bin/bash


export LD_LIBRARY_PATH="/usr/users/iff_th2/duman/hdf5_parallel/lib:$LD_LIBRARY_PATH"
mpicxx -Wl,-rpath=/usr/users/iff_th2/duman/hdf5_parallel/lib -L/usr/users/iff_th2/duman/hdf5_parallel/lib -I/usr/users/iff_th2/duman/hdf5_parallel/include -I/usr/users/iff_th2/duman/Eigen -I/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/include ../src/find_defects_multi.cpp ../src/compute_defect.cpp ../src/misc_tools.cpp ../src/read_write.cpp -o fdef_multi -l:/usr/users/iff_th2/duman/hdf5_parallel/lib/libhdf5.so.10 

