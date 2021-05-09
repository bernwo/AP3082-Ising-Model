import numpy as np
from observables import get_magnetization, get_error_mag
import matplotlib.pyplot as plt
import lattice_functions as lf
from scipy.constants import Boltzmann as kB
import imageio
import os

def create_gif(n_frames,relax):
    with imageio.get_writer("simulation_images/Metropolis.gif", mode='I') as writer:
        print(f"Creating gif and clearing the temporary images...")
        for i in range(0,n_frames,relax):
            filename=f"simulation_images/wolff_{i}.png"
            image = imageio.imread(filename)
            writer.append_data(image)
            os.remove(filename)
        print(f"Gif created.")

def save_frame(i,relax,spins,magnetization,T,h=0,J=1):

        print(f"Saving pic... run #{i}.")

        plt.subplot(1,2,1)
        plt.imshow(spins,cmap='inferno',aspect="auto")
        plt.title(f"Ising model (Wolff) Run #{i}.")
        plt.subplot(1,2,2)
        plt.errorbar(magnetization[0],magnetization[1],color='b',ecolor='r',yerr=magnetization[2])
        plt.title(f"Magnetization.")
        plt.xlabel('T/Tc')
        plt.ylim(0,1.1)
        plt.savefig(f"simulation_images/wolff_{i}.png", dpi=200)

        plt.close()

def evolution(f,relax,L,T,dT,J=1,dJ=0):
    lat = lf.init_pos_lattice(L)
    i=0
    magnetization = [[],[],[]]

    while T/2.27<2.5 and T>0:
        lat = f(lat,T)
        if i%relax==0:
            M = get_magnetization(lat)
            magnetization[0].append(T/2.27)
            magnetization[1].append(M)
            magnetization[2].append(M-get_error_mag(T))
            T += dT
            J += dJ
            save_frame(i,relax,lat,magnetization,T)
        i += 1
    create_gif(i,relax)
