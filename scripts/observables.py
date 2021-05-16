import numpy as np
from scipy.ndimage import convolve
import lattice_functions as lf

def analytic_mag(Temperature,J=1):
    anal_M = np.nan_to_num(pow(1-pow(np.sinh(2*(1/(Temperature))*J),-4),1/8))
    return anal_M

def get_magnetization(spins,power=1):
    return np.mean(spins**power)

def get_susceptibility(temp,spins):
    return (np.mean(spins**2)-np.mean(spins)**2)*len(spins)**2/(temp)

def get_error_sus(T,J):
    Tc=2.27 
    error = np.nan_to_num(1/(kB*(T-Tc)))
    return error

def get_energy_total(spins,h=0,J=1,power=1):
    """
    Calculates the total spin energy contribution of the lattice.

    Parameters:
    -----------
    J: float
        Coupling constant. J should always be J > 0.
    h: float
        External magnetic field strength.
    spins: numpy.ndarray
        The lattice containing spins.
    
    Return:
    --------
    E_tot: float
        The total spin energy contribution of the lattice.
    """
    kernel = np.array([[0, 1, 0],[1, 0, 1],[0, 1, 0]])
    neighbour_sums = convolve(spins, kernel, mode='wrap')
    E = -J/2 * neighbour_sums * spins - h * spins
    E_tot = np.sum(E**power)
    return E_tot

def get_specific_heat(T,lat):
    return (get_energy_total(lat)**2-get_energy_total(lat,power=2))*T/len(lat)

