from scipy.constants import Boltzmann as kB
from Metropolis_functions import*

# INITIALISATION.
N = 100000 # total number of runs in each Metropolis2D simulation
T_factor = 1.5 # for taking fractions of the critical temperature
J = 2 # J > 0 is a coupling constant
Tc = 2.27 * J/kB # critical temperature for 2D square lattice Ising model
T = T_factor * Tc
L = 128 # number of sites along a direction
h = -20 # external magnetic field
spins = init_rand_lattice(L) # Begin from a random spin lattice.

# Begin 1 set of Metropolis2D simulation with N runs.
final_spins = Metropolis2D(N,spins,J,T,h,creategif=True,plot_interval=5000)
print("Check the gif in the simulations_images folder.")