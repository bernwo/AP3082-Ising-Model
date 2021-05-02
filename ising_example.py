import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import Boltzmann as kB
from Metropolis_functions_modified import*

# INITIALISATION.
N = 2000000 # total number of runs in each Metropolis2D simulation
T_factor = 0.01 # for taking fractions of the critical temperature
J = 1 # J > 0 is a coupling constant
Tc = 2.27 * J/kB # critical temperature for 2D square lattice Ising model
T = T_factor * Tc
L = 100 # number of sites along a direction
h = 0 # external magnetic field
dT = 0.05

spins = init_pos_lattice(L) # Begin from a uniformly random spin lattice.

# Begin 1 set of Metropolis2D simulation with N runs.
final_spins = Metropolis2D(N,spins,J,T,h,L,dT)
