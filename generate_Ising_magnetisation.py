import numpy as np
from scipy.constants import Boltzmann as kB
import matplotlib.pyplot as plt
from Metropolis_functions import*

# INITIALISATION.
N = 200000 # total number of runs in each Metropolis2D simulation
n = 20 # total number of Metropolis2D simulations
min_T_factor = 0.001
max_T_factor = 1.5
T_factor = np.linspace(min_T_factor,max_T_factor,n) # for taking fractions of the critical temperature
J = 1 # J > 0 is a coupling constant
Tc = 2.27 * J/kB # critical temperature for 2D square lattice Ising model
T = T_factor * Tc
L = 64 # number of sites along a direction
h = 0 # external magnetic field
spins = init_pos_lattice(L) # Begin from a uniformly random spin lattice.

# Begin n sets of Metropolis2D simulations each with N runs.
M = np.zeros(n)
for i in range(n):
    print(f"\nMetropolis2D simulation #{i} out of {n-1}.")
    final_spins = Metropolis2D(N,spins,J,T[i],h,creategif=False)
    M[i] = np.abs(np.mean(final_spins))
    print(f"M[{i}]={np.round(M[i],4)}")

# Save plot.
plt.plot(T/Tc,M,'-rx')
plt.title(f"Absolute average magnetisation, |⟨M⟩|. L={L}, N={N}, J={J}, h={h}.")
plt.xlabel("$T/T_c$")
plt.ylabel("|⟨M⟩|")
plt.savefig(f"simulation_images/Absolute_magnetisation.png", dpi=200, bbox_inches='tight')
plt.show()
print("Plot saved. Check simulations_images folder.")