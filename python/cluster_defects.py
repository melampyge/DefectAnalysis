
""" cluster the defect points"""

##############################################################################

import argparse
import numpy as np
import math
import performance_toolsWrapper
import data_structures
import misc_tools
import plot_defects
import read_write
import find_defects

##############################################################################

def find_clusters(x, y, dcrit, npoints, sim):
    """ search for clusters: two points are defined as being
        part of the same cluster if they are within dcrit distance of each other"""

    ### allocate required arrays

    clusters = np.zeros((npoints), dtype=np.int32)-1
    neighbors = np.zeros((npoints, npoints), dtype=np.int32)

    ### generate a linked list

    nsegx, nsegy, head, llist = misc_tools.gen_linked_list(x, y, \
        sim.lx, sim.ly, dcrit, npoints)

    ### buld a neighborhood matrix based on the criterion dcrit

    neighs = neighbors.ravel()
    performance_tools = performance_toolsWrapper.Performance_tools()
    performance_tools.fill_neigh_matrix(neighs, llist, head, nsegx, nsegy, \
        x, y, npoints, sim.lx, sim.ly, dcrit)

    ### recursive search for clusters within the neighbor matrix

    performance_tools.cluster_search(neighs, clusters, npoints)

    return clusters

##############################################################################

def transform_cluster_data(clusters, npoints):
    """ transform the data representation of clusters such that cluster list contains
    the points inside the cluster"""

    ### find the maximum number of clusters

    clmax = max(clusters)

    ### add empty lists to cluster list

    cl_list = []
    for j in range(clmax+1):
        cl_list.append([])

    ### fill lists with point ids

    for i in range(npoints):
        cid = clusters[i]
        cl_list[cid].append(i)

    return cl_list

##############################################################################

def correct_cluster_pbc(x, y, clusters, lx, ly, dcrit, npoints):
    """ correct the cluster point coordinates with periodic boundary conditions"""

    ### get number of clusters

    nclusters = len(clusters)

    ### initialize output clusters and isolated array

    xcluster = np.copy(x)
    ycluster = np.copy(y)
    isolated = np.ones((nclusters), dtype=int)

    ### loop over all clusters

    for i in range(nclusters):

        ### allocate array to store cluster + copies

        npts = len(clusters[i])

        ### expand cluster to periodic images

        xcl, ycl = expand_cluster(x, y, lx, ly, clusters, i)

        ### correct the pbcs point by point

        correct_pbc_single(xcl, ycl, lx, ly, npts)

        ### adjust center of mass of the entire cluster

        adjust_com_cluster(xcl, ycl, lx, ly, npts)

        ### copy coordinates to the cluster array

        for j in range(npts):
            mi = clusters[i][j]
            xcluster[mi] = xcl[j]
            ycluster[mi] = ycl[j]

    return xcluster, ycluster, isolated

##############################################################################

def expand_cluster(x, y, lx, ly, clusters, i):
    """ expand the current cluster to periodic images"""

    npts = len(clusters[i])
    xcl = np.zeros((9*npts))
    ycl = np.zeros((9*npts))

    ### create copies of the atoms of all clusters

    l = 0
    for j in range(npts):
        mi = clusters[i][j]
        xcl[l] = x[mi]
        ycl[l] = y[mi]
        l = l + 1

    ### add pbc copies

    for j in range(-1,2):
        for k in range(-1,2):
            if j == 0 and k == 0:
                continue
            for m in range(npts):
                xcl[l] = xcl[m] + j*lx
                ycl[l] = ycl[m] + k*ly
                l = l + 1

    return xcl, ycl

##############################################################################

def correct_pbc_single(xcl, ycl, lx, ly, npts):
    """ correct periodic boundary conditions of all points one by one separately"""

    ### loop over individual points in the cluster and connect nearest neighbors

    for j in range(npts-1):
        x0 = xcl[j]
        y0 = ycl[j]
        x1 = xcl[j+1]
        y1 = ycl[j+1]
        dx = nearest_neighbor(x0, x1, lx)
        dy = nearest_neighbor(y0, y1, ly)
        xcl[j+1] = x0 - dx
        ycl[j+1] = y0 - dy

    ### loop over all points in the cluster and adjust com position

#    for j in range(npts):
#        xcl[j] += -math.floor(xcl[j]/lx)*lx
#        ycl[j] += -math.floor(ycl[j]/ly)*ly

    return

##############################################################################

def adjust_com_cluster(xcl, ycl, lx, ly, npts):
    """ move cluster such that com is in periodic box"""

    comx = np.average(xcl[0:npts])
    comy = np.average(ycl[0:npts])
    xcl[0:npts] += -math.floor(comx/lx)*lx
    ycl[0:npts] += -math.floor(comy/ly)*ly

    return

##############################################################################

def find_com_clusters(xcl, ycl, clusters, lx, ly):
    """ find the center of mass of clusters"""

    ### get the number of clusters

    nclusters = len(clusters)
    xcm = np.zeros((nclusters), dtype=np.float64)
    ycm = np.zeros((nclusters), dtype=np.float64)

    ### run over the clusters

    for i in range(nclusters):

        ### run over the points in the cluster
        #print 'cluster', i, '\n\n'
        npts = len(clusters[i])
        for j in range(npts):
            mi = clusters[i][j]     # this accesses the particle index
            #if xcl[mi] < 0 or ycl[mi] < 0:
            #print xcl[mi]*2., ycl[mi]*2., lx, lx*2.
            xcm[i] += xcl[mi]
            ycm[i] += ycl[mi]
        xcm[i] /= npts
        ycm[i] /= npts
        #print 'COM=', xcm[i]*2., ycm[i]*2., '\n\n\n\n'
        #exit()
    ### put the center of masses back inside the box

    xcm += -np.floor(xcm/lx)*lx
    ycm += -np.floor(ycm/ly)*ly
    #print zip(xcm*2., ycm*2.)
    return xcm, ycm

##############################################################################

def find_com_clusters_weight(xcl, ycl, clusters, lx, ly, d):
    """ find the center of mass of clusters"""

    # clusters is a list containing the cluster id in the first dimension
    # and the number of points inside the cluster inside the each list element
    # d: is an array containing defect strength of the point
    # periodic boundary conditions are taken care of

    ### get the number of clusters

    nclusters = len(clusters)

    xcm = np.zeros((nclusters), dtype=np.float64)
    ycm = np.zeros((nclusters), dtype=np.float64)

    ### build weights array based on defect strengths

    dweight = np.zeros(d.shape)
    dtotal  = np.zeros(d.shape)         # normalization of weights
                                        # sum of wghts of defects in a cluster=1
    dmins = np.abs(d[d<0]+0.5)
    dplus = np.abs(d[d>0]-0.5)
    dmins[dmins==0.] = 0.00000001
    dplus[dplus==0.] = 0.00000001
    dweight[d<0] = 1./dmins    # -1/2 defect weights
    dweight[d>0] = 1./dplus    # +1/2 defect weights
    #dweight[d<0] = np.exp(-dmin**2/0.5)

    ### run over all clusters

    for i in range(nclusters):

        ### run over all points in the cluster

        npts = len(clusters[i])
        for j in range(npts):
            mi = clusters[i][j]         # accesses the particle index
            dtotal[i] += dweight[mi]    # adds up total weight of all defects

    ### run over the clusters

    for i in range(nclusters):

        ### run over the points in the cluster

        npts = len(clusters[i])
        for j in range(npts):
            mi = clusters[i][j]         # accesses the particle index
            xcm[i] += xcl[mi]*dweight[mi]
            ycm[i] += ycl[mi]*dweight[mi]
        xcm[i] /= dtotal[i]
        ycm[i] /= dtotal[i]

    ### put the center of masses back inside the box

    xcm += -np.floor(xcm/lx)*lx
    ycm += -np.floor(ycm/ly)*ly

    return xcm, ycm

##############################################################################

def separate_clusters(cl_list, clusters, d):
    """ separate clusters by their defect strength"""

    ### get the number of clusters

    nclusters = len(cl_list)
    cl_defect_strength = {}
    new_cluster_cnt = 0             # assign new clusters in case of a defect strength conflict

    ### run over the clusters

    for i in range(nclusters):

        ### assign a placeholder defect strength to the cluster

        cl_defect_strength[i] = 0
        cluster_is_separated = False

        ### run over the points in the cluster

        npts = len(cl_list[i])
        k = -1

        for j in range(npts):

            k += 1
            mi = cl_list[i][k]
            #print 'cluster_d = ', cl_defect_strength[i], ' / d = ', d[mi]

            ### if the defect strength is assigned for the first time ...

            if cl_defect_strength[i] == 0:
                #print 'Cluster ', i, ' is assigned ', d[mi], ' for the first time.'
                cl_defect_strength[i] = d[mi]

            ### if the defect strength of the current point is different than the assigned one ...

            elif cl_defect_strength[i] > 0 and d[mi] < 0:

                if cluster_is_separated == False:
                    cluster_is_separated = True
                    new_cluster_cnt += 1
                    new_cluster_id = len(cl_list)
                    cl_list.append([])
                    #print 'New cluster is created. new_cluster_cnt = ', new_cluster_cnt, 'new_cluster_id = ', new_cluster_id

                cl_defect_strength[new_cluster_id] = d[mi]
                clusters[mi] = new_cluster_id
                cl_list[new_cluster_id].append(mi)
                del cl_list[i][k]
                k -= 1

            ### if the defect strength of the current point is different than the assigned one ...

            elif cl_defect_strength[i] < 0 and d[mi] > 0:

                if cluster_is_separated == False:
                    cluster_is_separated = True
                    new_cluster_cnt += 1
                    new_cluster_id = len(cl_list)
                    cl_list.append([])
                    #print 'New cluster is created. new_cluster_cnt = ', new_cluster_cnt, 'new_cluster_id = ', new_cluster_id

                cl_defect_strength[new_cluster_id] = d[mi]
                clusters[mi] = new_cluster_id
                cl_list[new_cluster_id].append(mi)
                del cl_list[i][k]
                k -= 1

    return

##############################################################################

def threshold_clusters(cl_list, thrs):
    """ threshold the clusters by size, delete any cluster below the input size"""

    ### get the number of clusters

    nclusters = len(cl_list)

    ### run over the clusters deleting any cluster smaller than the threshold

    k = -1
    for i in range(nclusters):
        k += 1
        size = len(cl_list[k])
        if size < thrs:
            del cl_list[k]
            k -= 1

    return
##############################################################################

def find_best_of_clusters(x, y, d, cl_list, clusters):
    """ find the point with the best defect strength within the cluster"""

    ### allocate per cluster arrays

    nclusters = len(cl_list)
    xcm = np.zeros((nclusters), dtype=np.float64)
    ycm = np.zeros((nclusters), dtype=np.float64)

    ### loop over each cluster to find the point with the best defect strength within it

    for i in range(nclusters):

        npts = len(cl_list[i])
        dcluster = np.zeros((npts), dtype=np.float32)
        for j in range(npts):
            mi = cl_list[i][j]
            if d[mi] > 0:
                dcluster[j] = np.abs(d[mi]-0.5)
            else:
                dcluster[j] = np.abs(0.5+d[mi])
        bestd = min(dcluster)
        bestid = np.argmin(dcluster)
        mi = cl_list[i][bestid]
        xcm[i] = x[mi]
        ycm[i] = y[mi]
        print d[mi]

    return xcm, ycm

##############################################################################

def cluster_analysis(points, dcrit, ncrit, sim, step, xall, yall, cid):
    """ find clusters within the list of data points with a distance criterion"""

    ### discern information about the data points

    npoints = len(points[0])
    print 'possible points -> ', npoints
    x = np.array(points[0], dtype=np.float32)
    y = np.array(points[1], dtype=np.float32)
    d = np.array(points[2], dtype=np.float32)

    ### find the clusters among the data points
    # clusters is a per point array with each element representing the cluster id the point belongs to

    clusters = find_clusters(x, y, dcrit, npoints, sim)

    ### transform the cluster data such that each cluster contains a list of points in that cluster

    cl_list = transform_cluster_data(clusters, npoints)

    ### separate clusters by their defect strengths

    separate_clusters(cl_list, clusters, d)

    ### threshold the clusters -- note the per atom array clusters is not correct anymore below this point

    threshold_clusters(cl_list, ncrit)

    ### correct the cluster point positions with periodic boundary conditions

    xclusters, yclusters, isolated = correct_cluster_pbc(x, y, cl_list, sim.lx, sim.ly, dcrit, npoints)

    ### find the center of mass of clusters

    xcm, ycm = find_best_of_clusters(x, y, d, cl_list, clusters)
    #xcm, ycm = find_com_clusters(xclusters, yclusters, cl_list, sim.lx, sim.ly)
    #xcm, ycm = find_com_clusters_weight(xclusters, yclusters, cl_list, sim.lx, sim.ly, d)

    ### plot the clusters

    plot_defects.plot_clusters(xclusters, yclusters, \
        xcm, ycm, cl_list, clusters, sim, xall, yall, cid, step)

    return xcm, ycm

##############################################################################

def main():

    ### get the data folder

    parser = argparse.ArgumentParser()
    parser.add_argument("-sdfl", "--simdatafolder", \
                        help="Folder containing the simulation data")
    parser.add_argument("-dfl", "--datafolder", \
                        help="Folder containing analysis data")
    parser.add_argument("-sfl", "--savefolder", \
                        help="Folder to save the resulting analysis data inside")
    parser.add_argument("-figfl", "--figfolder", \
                        help="Folder to save the figures inside")
    parser.add_argument("-ti", "--inittime", nargs="?", const=10, \
                        type=int, help="Initial time step")
    parser.add_argument("-tf", "--fintime", nargs="?", const=100, \
                        type=int, help="Final timestep")
    parser.add_argument("-s","--savepdf", action="store_true", \
                        help="Decide whether to save in pdf or not")
    args = parser.parse_args()

    ### read the data and general information from the folder

    beads, sim = read_write.read_data(args.simdatafolder)

    rcut = 15.              # size of the interrogation circle
    dcut = 0.1              # defect strength cut
    dcrit = 8.              # clustering distance threshold criteria
    ncrit = 15              # clustering size threshold criteria

    for step in range(args.inittime, args.fintime):

        print 'step / last_step: ', step, args.fintime

        ### load the possible defect points

        sfilepath = args.datafolder + 'possible_defect_pts_cpp_' + str(step) + '.h5'
        possible_defect_pts = read_write.load_h5_data(sfilepath)

        ### cluster the possible defect points and plot the cluster

        xcm, ycm = cluster_analysis(possible_defect_pts, dcrit, ncrit, sim, step, \
            beads.xu[step, 0, :], beads.xu[step, 1, :], beads.cid)

        ### for each of the defect points found by clustering
        # calculate the defect strength and plot each point

        defect_pts = find_defects.recompute_defects(\
            xcm, ycm, beads, sim, rcut, dcut, step, args.figfolder)

        ### save the ultimate defect points

        sfilepath = args.savefolder + 'defect_pts_' + str(step) + '.txt'
        save_data(defect_pts, sfilepath)

    return

##############################################################################

if __name__ == '__main__':
    main()

##############################################################################

