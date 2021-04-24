import numpy as np
from scipy.constants import Boltzmann as kB
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
import os
import imageio # sudo pip3 install imageio

# Let the total number of sites be N × N where N∈ℤ
def init_rand_lattice(L):
    """
    Generates a lattice of size L×L with spins randomly sampled from {-1,1} with uniform distribution.

    Parameters:
    -----------
    L: int
        Dimension of the lattice.

    Return:
    --------
    spins: numpy.ndarray
        The lattice containing spins.
    """
    spins = np.random.choice(np.array([-1,1],dtype=int), (L,L))
    return spins

def init_pos_lattice(L):
    """
    Generates a homogeneous lattice of size L×L with all spins = +1.

    Parameters:
    -----------
    L: int
        Dimension of the lattice.

    Return:
    --------
    spins: numpy.ndarray
        The lattice containing spins.
    """
    spins = np.ones([L,L],dtype=int)
    return spins

def init_neg_lattice(L):
    """
    Generates a homogeneous lattice of size L×L with all spins = -1.

    Parameters:
    -----------
    L: int
        Dimension of the lattice.

    Return:
    --------
    spins: numpy.ndarray
        The lattice containing spins.
    """
    spins = -np.ones([L,L],dtype=int)
    return spins

def get_energy_singlespin(J,h,neighbour_sums,spins):
    """
    Calculates the individual spin energy contribution of every spin in the lattice.

    Parameters:
    -----------
    J: float
        Coupling constant. J should always be J > 0.
    h: float
        External magnetic field strength.
    neighbour_sums: numpy.ndarray
        The sum of nearest-neighbours of each spin for every spins.
    spins: numpy.ndarray
        The lattice containing spins.
    
    Return:
    --------
    E: numpy.ndarray
        The individual spin energy contribution of every spin in the lattice.
    """ 
    E = -J/2 * neighbour_sums * spins - h * spins
    return E

def get_energy_total(E):
    """
    Calculates the total spin energy contribution of the lattice.

    Parameters:
    -----------
    E: numpy.ndarray
        The individual spin energy contribution of every spin in the lattice.
    
    Return:
    --------
    E_tot: float
        The total spin energy contribution of the lattice.
    """ 
    E_tot = np.sum(E)
    return E_tot

def flip_a_spin(spins):
    """
    Randomly flips a spin in the lattice.

    Parameters:
    -----------
    spins: numpy.ndarray
        The lattice containing spins.
    
    Return:
    --------
    new_spins: numpy.ndarray
        The lattice containing spins with a randomly flipped spin.
    """ 
    Lx = spins.shape[0]
    Ly = spins.shape[1]
    new_spin = np.copy(spins) # use np.copy() so it doesn't mutate the original numpy array.
    i = np.random.randint(low=0,high=Lx)
    j = np.random.randint(low=0,high=Ly)
    new_spin[i,j] = np.negative(new_spin[i,j])
    return new_spin

def get_energy_difference_with_trial_state(J,h,i,j,spins):
    Lx = spins.shape[0]
    Ly = spins.shape[1]
    neighbour_sum = (spins[(i+1)%Lx,j]+spins[(i-1)%Lx,j]+spins[i,(j+1)%Ly]+spins[i,(j-1)%Ly])
    dE = (-J * np.negative(spins[i,j])*neighbour_sum - h * np.negative(spins[i,j])) - (-J * spins[i,j]*neighbour_sum - h * spins[i,j])
    return dE

def Metropolis2D(N,spins,J,T,h,L,creategif=False,plot_interval=100):
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
    creategif: bool
        If True, the function creates an animated .gif, else it does not.
    plot_interval: int
        Specifies the interval between each frame in the animated .gif. Note that plot_interval should be smaller than N.

    Return:
    --------
    final_spins: numpy.ndarray
        The resulting lattice after executing the Metropolis algorithm after N steps.
    """
    # begin Metropolis algorithm
    print(f"Start Metropolis2D algorithm with {N} runs.")
    print(f"Temperature ratio, T/Tc = {np.round(T/(2.27 * J/kB),4)}")
    # kernel = np.array([[0, 1, 0],[1, 0, 1],[0, 1, 0]]) # specific for 2D
    used_intervalSavePic = []
    for i in range(N):
        # neighbour_sums = convolve(spins, kernel, mode='wrap')
        # E = get_energy_singlespin(J,h,neighbour_sums,spins)
        # E_tot = get_energy_total(E)

        x_index = np.random.randint(low=0,high=L)
        y_index = np.random.randint(low=0,high=L)

        dE = get_energy_difference_with_trial_state(J,h,x_index,y_index,spins)

        if (dE <= 0):
            # spins = spins_trial # take new state
            spins[x_index,y_index] = np.negative(spins[x_index,y_index]) # take new state
        else:
            r = np.random.rand()
            W = np.exp(-1/(kB*T)*dE)
            if (r < W):
                # spins = spins_trial  # take new state
                spins[x_index,y_index] = np.negative(spins[x_index,y_index]) # take new state
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

    final_spins = spins
    return final_spins
