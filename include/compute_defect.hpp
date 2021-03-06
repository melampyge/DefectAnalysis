
/* compute the defect strength of a point */

#pragma once
#include <iostream>
#include <cmath>
#include <Eigen/Dense>
#include "misc_tools.hpp"
#include "MersenneTwister.h"

/* average the elements of the order parameter matrix */
void average_order_param_matrix (double *qxx, double *qxy, double *qyy, int *counter, 
    int northants, double xd, double yd, double *x, double *y, double *phi, 
    double *head, double *llist, double rcut, int nsegx, int nsegy, double lx, double ly);

/* calculate the nematic director inside each orthant */
void calc_nematic_directors (double *directors, double *qxx, double *qxy, double *qyy, int northants);
  
/* compute the defect strength of a point */
double compute_single_defect (double xd, double yd, double *x, double *y, double *phi, 
    double *head, double *llist, double rcut, int nsegx, int nsegy, double lx, double ly);

/* search the main points to compute defects */
void search_main_pts (double *xdefects, double *ydefects, double *ddefects, int *check_again, 
    int &cnt_defects, double *xpoints, double *ypoints, int npoints, 
    double *x, double *y, double *phi, double *head, double *llist, double rcut, 
    int nsegx, int nsegy, double rn, int nn, int nr, double dcut, 
    double lx, double ly, MTRand randi);

/* search the neighborhood of the main point to compute defects */
void search_neighborhood (double xd, double yd, double dmax, double dlabel, 
    double *xdefects, double *ydefects, double *ddefects, int &cnt_defects, 
    double *x, double *y, double *phi, double *head, double *llist, double rcut, 
    int nsegx, int nsegy, double rn, int nn, int nr, double dcut, 
    double lx, double ly, MTRand randi, int cnt_recursion);


