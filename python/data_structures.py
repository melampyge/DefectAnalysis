
""" Data structures"""

##############################################################################

import numpy as np
import os
import h5py
import math
import misc_tools

##############################################################################

class Subplots:
    """ plot structure"""

    totcnt = -1             # Total number of subplots

    def __init__(self, f, l, s, b, t):
        self.fig = f        # Figure axes handle
        self.length = l     # Length of the subplot box
        self.sep = s        # Separation distance between subplots
        self.beg = b        # Beginning (offset) in the figure box
        self.tot = t        # Total number of subplots in the x direction

        return

    def addSubplot(self):
        """ add a subplot in the grid structure"""

        ### increase the number of subplots in the figure

        self.totcnt += 1

        ### get indices of the subplot in the figure

        self.nx = self.totcnt%(self.tot)
        self.ny = self.totcnt/(self.tot)

        self.xbeg = self.beg + self.nx*self.length + self.nx*self.sep
        self.ybeg = self.beg + self.ny*self.length + self.ny*self.sep

        return self.fig.add_axes([self.xbeg,self.ybeg,self.length,self.length])

##############################################################################

class linked_list:
    """ linked list data structure to browse beads based on their position"""

    def __init__(self, x, y, sim, rcut):

        ### define starting values

        self.rcut = rcut
        self.rcut2 = rcut**2
        self.nsegx = int(sim.lx/self.rcut)
        self.nsegy = int(sim.ly/self.rcut)
        self.llist = np.zeros((sim.nbeads), dtype = int) - 1
        self.head = np.zeros((self.nsegx*self.nsegy), dtype = int) - 1

        ### put all the beads inside the list

        for i in range(sim.nbeads):
            segx = int(x[i]/sim.lx*self.nsegx)
            segy = int(y[i]/sim.ly*self.nsegy)
            cell = segx*self.nsegy + segy
            self.llist[i] = self.head[cell]
            self.head[cell] = i

        return

##############################################################################

class Simulation:
    """ data structure for storing general simulation information"""

    def __init__(self, lx, ly, dt, nsteps, nbeads, nbpp, \
        npols, density, kappa, fp, bl, sigma):

        self.lx = float(lx)
        self.ly = float(ly)
        self.dt = float(dt)
        self.nsteps = int(nsteps)
        self.nbeads = int(nbeads)
        self.nbpp = nbpp[0]
        self.npols = npols
        self.density = density
        self.fp = fp
        self.kappa = kappa
        self.bl = bl
        self.sigma = sigma
        self.kT = 1.0
        self.gamma_n = 1.0

        ### define more simulation parameters

        self.length = self.nbpp*self.bl
        self.tau_diff = self.length**2 * self.gamma_n * self.nbpp / 4.0 / self.kT
        self.tau_adv = self.fp / self.gamma_n / self.length

        return

##############################################################################

class Beads:
    """ data structure for storing particle/bead information"""

    def __init__(self, x, sim):

        ### assign bead positions

        self.xu = x

        ### assign mol indices to beads

        self.cid = np.zeros((sim.nbeads), dtype=np.int32)-1
        k = 0
        for j in range(sim.npols):
            for n in range(sim.nbpp):
                self.cid[k] = j
                k += 1

        return

    def calc_img_pos(self, l):

        self.xi = self.xu - l*np.floor(self.xu/l)

        return

##############################################################################

