import numpy as np
import observables as bs
import matplotlib.pyplot as plt
import lattice_functions as lf
import errors as er
from scipy.constants import Boltzmann as kB
import imageio
import os

def create_gif(n_frames,relax):
    with imageio.get_writer("../simulation_images/Metropolis.gif", mode='I') as writer:
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
        plt.title(f"Ising model (Metropolis) Run #{i}.")
        plt.subplot(1,2,2)
        plt.errorbar(magnetization[0],magnetization[1],color='b',ecolor='r',yerr=magnetization[2])
        plt.title(f"Magnetization.")
        plt.xlabel('T/Tc')
        plt.ylim(0,1.1)
        plt.savefig(f"../simulation_images/wolff_{i}.png", dpi=200)

        plt.close()


def get_observables(T, lat):
    """
    Calculate observables for a lattice configuration at a given temperature.
    """
    obs = [bs.get_magnetization(lat), bs.get_specific_heat(T, lat), bs.get_susceptibility(T, lat)]
    return obs


def evolution(f, relax, L, T_init, T_max, dT, h=0, J=1):
    """
    Simulates Ising model for a temperature range between T_init to T_max*T_c
    with step dT.

    Parameters:
    -----------
        f: function
            evolution method
        relax: int
            number of relaxation steps
        L: int
            size of the system
        T_init: float
            initial temperature
        T_max: float
            final temperature in units of T_c
        dT: float
            temperature step
        h: float
            magnetic field
        J: float
            interaction constant

    Returns:
    --------
        frames: nd.array
            Array of snapshots for each T after the system relaxes.
        observables: nd.array
            Array of observables w.r.t temperature:
                [0]: magnetization
                [1]: specific heat
                [2]: susceptibility
        obs_errors: nd.array
            Array of errors for each temperature for each observable
        tems: nd.array
            Array of temperatures
    """

    lat = lf.init_pos_lattice(L)
    i = 0
    observables = []
    #obs_errors = []
    #obs_no_relax = []
    frames = []
    temps = []
    T = T_init

    while T/2.27 < T_max and T > 0:
        lat = f(lat, T, h)
        #obs_no_relax.append(get_observables(T, lat))
        if i % relax == 0 and i != 0:
            #obs_no_relax = np.transpose(np.array(obs_no_relax))
            #obs_errors.append([er.get_error_observable(obs)[0] for obs in obs_no_relax])
            observables.append(get_observables(T, lat))
            frames.append(lat)
            temps.append(T)
            T += dT
            #obs_no_relax = []
            # save_frame(i,relax,lat,magnetization,T)
        i += 1
    # create_gif(i,relax)
    observables = np.transpose(np.array(observables))
    obs_errors = np.transpose(np.array(obs_errors))
    return frames, observables, temps
