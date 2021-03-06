
/* routines to read from and write to hdf5 files */

#pragma once
#include "/usr/users/iff_th2/duman/hdf5_parallel/include/hdf5.h"
//#include "/homec/jiff26/jiff2610/hdf/include/hdf5.h"
#include <iostream>
#include <fstream>
#include <cstdio>
#include <iomanip>
#include <cstdlib>
#include <cstring>
#include <sstream>
#include <algorithm>
#include "mpi.h"

/* wrapper to read integer data from hdf5 file 
 * --note that buffer needs to be an array of size 1 for single entries-- */
int read_integer_data (hid_t file, char *path_in_file, int *buffer);

/* wrapper to read double data from hdf5 file 
 * --note that buffer needs to be an array of size 1 for single entries-- */
double read_double_data (hid_t file, char *path_in_file, double *buffer);

/* wrapper to read integer array data from hdf5 file 
 * --note that buffer needs to be the array size-- */
void read_integer_array (char *filename, char *path_in_file, int *buffer);

/* wrapper to read double array data from hdf5 file 
 * --note that buffer needs to be the array size-- */
void read_double_array (char *filename, char *path_in_file, double *buffer);

/* read general simulation data in hdf5 format */
void read_sim_data (char *filename, int &nsteps, int &nbeads, int &npols, 
    double &lx, double &ly, double &dt, 
    double &density, double &kappa, double &fp, 
    double &bl, double &sigma);

/* read the position data at a single timestep */
void read_single_pos_data(int step, hid_t dataset, hid_t dataspace, 
    double *x, double *y, int natoms);

/* save the defect point data at this timestep */
void write_data (int step, double *x, double *y, double *d, int N);

/* save the defect point data at this timestep in hdf5 format */
void write_h5_data (char* savefolder, int step, double *x, double *y, 
    double *d, int N, int proc_rank, int procs_size, 
    int *counts, int *offsets, MPI_Comm comm);

