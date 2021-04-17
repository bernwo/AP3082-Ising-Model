import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import Boltzmann as kB
from Metropolis_functions import*

# INITIALISATION.
N = 200000 # total number of runs in each Metropolis2D simulation
T_factor = 1.1 # for taking fractions of the critical temperature
J = 2 # J > 0 is a coupling constant
Tc = 2.27 * J/kB # critical temperature for 2D square lattice Ising model
T = T_factor * Tc
L = 40 # number of sites along a direction
h = 0 # external magnetic field
spins = init_rand_lattice(L) # Begin from a uniformly random spin lattice.

# Begin 1 set of Metropolis2D simulation with N runs.
final_spins = Metropolis2D(N,spins,J,T,h,creategif=False,plot_interval=5000)
print("Check the gif in the simulations_images folder.")

plt.imshow(final_spins,cmap='magma')
plt.colorbar(ticks=[-1, 0, 1])
plt.clim(-1,1)
plt.title(f"Final run. $J$={J}. $T/T_c$={np.round(T/(2.27 * J/kB),4)}. $h$={h}.")
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.show()
