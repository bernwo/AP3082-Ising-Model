import numpy as np
from scipy.constants import Boltzmann as kB
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
import os
import imageio # sudo pip3 install imageio

# Let the total number of sites be N × N where N∈ℤ
def init_rand_lattice(L):
    """Generate a uniform random sample from np.array([-1,1],dtype=int) of size (L,L)"""
    return np.random.choice(np.array([-1,1],dtype=int), (L,L))

def init_pos_lattice(L):
    """Generate a homogeneous spin lattice with spins = +1"""
    return np.ones([L,L],dtype=int)

def init_neg_lattice(L):
    """Generate a homogeneous spin lattice with spins = -1"""
    return -np.ones([L,L],dtype=int)

def get_energy_singlespin(J,h,neighbour_sums,spins):
    return -J/2 * neighbour_sums * spins - h * spins

def get_energy_total(E):
    return np.sum(E)

def flip_a_spin(spins):
    Lx = spins.shape[0]
    Ly = spins.shape[1]
    temp = np.copy(spins) # use np.copy() so it doesn't mutate the original numpy array.
    i = np.random.randint(low=0,high=Lx)
    j = np.random.randint(low=0,high=Ly)
    temp[i,j] = np.negative(temp[i,j])
    return temp

def Metropolis2D(N,spins,J,T,h,creategif=False,plot_interval=100):
    # begin Metropolis algorithm
    print(f"Start Metropolis2D algorithm with {N} runs.")
    print(f"Temperature ratio, T/Tc = {np.round(T/(2.27 * J/kB),4)}")
    kernel = np.array([[0, 1, 0],[1, 0, 1],[0, 1, 0]]) # specific for 2D
    used_intervalSavePic = []
    for i in range(N):
        neighbour_sums = convolve(spins, kernel, mode='wrap')

        E = get_energy_singlespin(J,h,neighbour_sums,spins)
        E_tot = get_energy_total(E)

        spins_trial = flip_a_spin(spins)
        E_trial = get_energy_singlespin(J,h,neighbour_sums,spins_trial)
        E_trial_tot = get_energy_total(E_trial)

        dE = E_trial_tot - E_tot

        if (dE <= 0):
            spins = np.copy(spins_trial) # take new state
        else:
            r = np.random.rand()
            W = np.exp(-1/(kB*T)*dE)
            if (r < W):
                spins = np.copy(spins_trial)  # take new state
                # end
        
        if (((i%plot_interval==0) or (i==N-1)) and creategif):
            print(f"Saving pic... run #{i} out of {N-1}.")
            used_intervalSavePic.append(i)
            plt.imshow(spins,cmap='magma')
            plt.colorbar(ticks=[-1, 0, 1])
            plt.clim(-1,1)
            plt.title(f"Run #{i}. $J$={J}. $T/T_c$={np.round(T/(2.27 * J/kB),4)}. $h$={h}.")
            plt.xlabel("$x$")
            plt.ylabel("$y$")
            plt.savefig(f"simulation_images/Metropolis_{i}.png", dpi=200, bbox_inches='tight')
            plt.close()

    if creategif:
        with imageio.get_writer("simulation_images/Metropolis.gif", mode='I') as writer:
            print(f"Creating gif and clearing the temporary images...")
            for i in used_intervalSavePic:
                filename=f"simulation_images/Metropolis_{i}.png"
                image = imageio.imread(filename)
                writer.append_data(image)
                os.remove(filename)
            print(f"Gif created.")

    return np.copy(spins)
