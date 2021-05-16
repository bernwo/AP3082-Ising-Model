import numpy as np
from scipy.constants import Boltzmann as kB
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
import os
import imageio # sudo pip3 install imageio

def get_energy_difference_with_trial_state(J,h,i,j,spins):
    """
    Computes the energy difference of a spin configuration with one spin flipped
    versus the configuration given in spins.
    
    Parameters:
    -----------
        J: float
            Coupling constant
        h: float
            Magnetic field
        i: int
            spin index
        j: int
            spin index
        spins: nd.array
            Spin configurations
    Returns:
    --------
        dE: float
            Energy difference with trial state
    """
    Lx = spins.shape[0]
    Ly = spins.shape[1]
    neighbour_sum = (spins[(i+1)%Lx,j]+spins[(i-1)%Lx,j]+spins[i,(j+1)%Ly]+spins[i,(j-1)%Ly])
    dE = (-J * np.negative(spins[i,j])*neighbour_sum - h * np.negative(spins[i,j])) - (-J * spins[i,j]*neighbour_sum - h * spins[i,j])
    return dE

def metropolis_evolution(spins,T,h,J=1):
    """
    Executes the Metropolis algorithm for the 2D Ising model.

    Parameters:
    -----------
        N: int
            Total number of steps in the Metropolis algorithm to run.
        spins: numpy.ndarray
            The lattice containing spins.
        J: float
            Coupling constant. J should always be J > 0.
        T: float
            Temperature of the system.
        h: float
            External magnetic field strength.
        dT: float
            Change in temperature in each step of simulation
    Return:
    --------
        final_spins: numpy.ndarray
            The resulting lattice after executing the Metropolis algorithm after N steps.
    """
    # begin Metropolis algorithm
    #print(f"Start Metropolis2D algorithm.")
    #print(f"Temperature ratio, T/Tc = {np.round(T/(2.27 * J/kB),4)}")

    L = len(spins)
    x_index = np.random.randint(low=0,high=L)
    y_index = np.random.randint(low=0,high=L)

    dE = get_energy_difference_with_trial_state(J,h,x_index,y_index,spins)

    if (dE <= 0):
        # spins = spins_trial # take new state
        spins[x_index,y_index] = np.negative(spins[x_index,y_index]) # take new state
    else:
        r = np.random.rand()
        W = np.exp(-1/(T)*dE)
        if (r < W):
            # spins = spins_trial  # take new state
            spins[x_index,y_index] = np.negative(spins[x_index,y_index]) # take new state
                # end
        #trial_sus.append(get_susceptibility(T,spins))
    return spins
