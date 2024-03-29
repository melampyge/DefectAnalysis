
/* miscellanous tools */

#pragma once
#include <iostream>
#include <fstream>
#include <cmath>

inline int ifloor (double doubval) {
  return ( doubval >= 0. ? (int)(doubval) : ((int)doubval)-1 );
}


inline int inearbyint (double doubval) {
  return ( doubval >= 0. ? (int)(doubval + 0.5) : (int)(doubval - 0.5) );
}


inline long double dnearbyint (double doubval) {
  return ( doubval >= 0. ? (long)(doubval + 0.5) : (long)(doubval - 0.5) );
}

/* find the minimum image distance between two particles inside the central box */
double neigh_min_central (double dx, double lx); 

/* find the minimum image distance between two particles inside the central box */
double neigh_min (double dx, double lx);

/* find the minimum image distance between two particles inside the central box */
double calc_img_pos (double xi, double lx);

/* generate a hashed linked list to browse data points via positions */
void gen_linked_list (double *llist, double *head, double rcut, int nsegx, int nsegy, 
		      int nseg, int nbeads, double *x, double *y, double lx, double ly);
		      
/* calculate bead orientations with line symmetry 
 * through bond angles between successive beads of filaments */    
void calc_headless_orient(double *phi, double *x, double *y, double lx, double ly, int nfils, int nbpf);

