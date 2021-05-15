import timeit
import numpy as np
import matplotlib.pyplot as plt

"""
benchmark.py
------------

This file runs and benchmark the time needed to run Metropolis
and Wolff algorithm starting from a completely positive spin lattice
until the absolute average magnetisation reach a threshold value
which we define to be 0.1.

We repeat this number=10 times for each value of temperature.
The temperature range we chose to benchmark is np.linspace(1.2,2.0,nT=20).

Running this file yields the plot with the results and saves it in .pdf format.
"""

import_module = '''import os
os.chdir('/usr/local/etc/Python_Development/AP3082/Project-2---Ising_juandaanieel_kwo/scripts')
import numpy as np
from scipy.constants import Boltzmann as kB
import matplotlib.pyplot as plt
from metropolis import metropolis_evolution
from wolff import wolff_evolution
from lattice_functions import init_rand_lattice, init_pos_lattice, init_neg_lattice
import sys
sys.setrecursionlimit(10000000)
os.chdir('/usr/local/etc/Python_Development/AP3082/Project-2---Ising_juandaanieel_kwo')
'''

def testwolff(T):
    testcode = f'''
L = 64 # number of sites along a direction
h = 0 # external magnetic field
spinsw = init_pos_lattice(L)
threshold_M = 0.1

Mw = 1
while Mw > threshold_M:
    final_wspins = wolff_evolution(spinsw,{T},h,J=1)
    Mw = np.abs(np.mean(final_wspins))
'''
# print(f"M for wolff algorithm has reach the threshold value "+ str(threshold_M))
    return testcode

def testmetropolis(T):
    testcode = f'''
L = 64 # number of sites along a direction
h = 0 # external magnetic field
spinsm = init_pos_lattice(L)
threshold_M = 0.1

Mm = 1
while Mm > threshold_M:
    final_mspins = metropolis_evolution(spinsm,{T},h,J=1)
    Mm = np.abs(np.mean(final_mspins))
'''
# print("M for metropolis algorithm has reach the threshold value "+ str(threshold_M))
    return testcode

Tc = 2.27
number = 10
nT = 20
T = np.linspace(1.2,2.0,nT) * Tc

metropolis_time = np.zeros(nT)
wolff_time = np.zeros(nT)

for i in range(nT):
    metropolis_time[i] = timeit.timeit(stmt=testmetropolis(T[i]), setup=import_module, number=number)
    print(f"metropolis time: {metropolis_time[i]/number}")

    wolff_time[i] = timeit.timeit(stmt=testwolff(T[i]), setup=import_module, number=number)
    print(f"wolff time: {wolff_time[i]/number}")


plt.close()
plt.plot(T/Tc,metropolis_time/number,'r.')
plt.plot(T/Tc,wolff_time/number,'b.')
plt.xlabel("$T/T_C\\; (a.u.)$")
plt.ylabel("$\\bar t\\; (s)$")
plt.legend(['Metropolis algorithm','Wolff algorithm'])
plt.grid()

plt.savefig(f"simulation_images/benchmark.pdf",  bbox_inches='tight')
