import numpy as np
from scipy.constants import Boltzmann as kB
import lattice_functions as lf

def wolff_evolution(lat,T,J=1):
    """
    Implementation of the Wolff algorithm for the evolution of the Ising model.

    Parameters:
    -----------
        np.darray: lat
            Initial configuration of the spins lattice
        float: T
            Temperature
        float: J
            Coupling constant

    Returns:
    --------
        np.darray:
    """

    threeshold =  1-np.exp(-2*J/(T))
    cluster = lf.flip_a_spin(np.copy(lat),turn=0)
    random_spin = np.where(cluster==0)
    make_cluster(lat,cluster,threeshold,random_spin)
    flip_cluster(lat,cluster)
    return lat

def make_cluster(lat,cluster,threeshold,random_spin):
    cluster=check_neighbours(lat,cluster,random_spin,threeshold)
    return cluster

def flip_cluster(lat,cluster):
    """
    Flip spins 0 in lat that belong to cluster.

    Parameters:
    -----------
        np.darray: lat
            Initial configuration of spin lattice.
        np.darray: cluster
            Copy of lat that contains a cluster of 0 spins.

    Returns:
    --------
        np.darray: Spin lattice with
    """
    lat[np.where(cluster == 0)] *= -1
    return lat

def check_neighbours(lat,cluster,spin,threeshold):
    """
    Iterative function that adds spins into the cluster.

    Parameters:
    -----------
        np.darray: lat
            Initial configuration of spins lattice
        np.darray: cluster

        tuple: spin

        float: threeshold

    """

    nn = np.array([-1,1])

    for i in nn:

        neighbors = [tuple([(x+y)%len(lat) for (x,y) in zip(spin,(i,0))]),tuple([(x+y)%len(lat) for (x,y) in zip(spin,(0,i))])]

        for neighbor in neighbors:

            if lat[spin] == lat[neighbor] and cluster[neighbor] != 0:

                if lf.flip_coin() < threeshold:

                    cluster[neighbor] = 0
                    check_neighbours(lat,cluster,neighbor,threeshold)
