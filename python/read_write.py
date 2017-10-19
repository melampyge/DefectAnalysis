
""" read and write functionality"""

##############################################################################

import numpy as np
import os
import h5py

##############################################################################

def read_data(folder):
    """ read simulation data through hdf5 file"""

    ### access the file

    fpath = folder + '/out.h5'
    assert os.path.exists(fpath), "out.h5 does NOT exist for " + fpath
    fl = h5py.File(fpath, 'r')

    ### read in the positions of beads

    x = np.array(fl['/beads/xu'], dtype=np.float32)

    ### read in the general simulation info

    dt = fl['/params/dt'][...]
    lx = fl['/params/lx'][...]
    ly = fl['/params/ly'][...]
    nsteps = fl['/sim/nsteps'][...]
    nbeads = fl['/sim/nbeads'][...]
    npols = fl['/sim/npols'][...]
    nbpp = np.array(fl['/sim/nbpp'], dtype=np.float32)

    density = fl['/params/density'][...]
    kappa = fl['/params/kappa'][...]
    fp = fl['/params/fp'][...]
    bl = fl['/params/bl'][...]
    sigma = fl['/params/sigma'][...]

    ### close the file

    fl.close()

    sim = Simulation(lx, ly, dt, nsteps, nbeads, nbpp, \
        npols, density, kappa, fp, bl, sigma)
    beads = Beads(x, sim)

    return beads, sim

##############################################################################

def save_data(points, sfl):
    """ save the data on defect points"""

    fl = open(sfl, 'w')
    npoints = len(points)
    for j in range(npoints):
        fl.write(str(points[j][0]) + '\t' + str(points[j][1]) + '\t'
                 + str(points[j][2]) + '\t' + str(points[j][3]) + '\n')
    fl.close()

    return

##############################################################################

def load_data(loadfile):
    """ load the data on possible defect points"""

    data = np.transpose(np.loadtxt(loadfile, dtype=np.float64))

    return data

##############################################################################

def load_h5_data(loadfile):
    """ load the data on possible defect points"""

    fl = h5py.File(loadfile, 'r')
    x = np.array(fl['/xpos'], dtype=np.float32)
    y = np.array(fl['/ypos'], dtype=np.float32)
    d = np.array(fl['/dstr'], dtype=np.float32)
    data = [x, y, d]

    return data

##############################################################################

