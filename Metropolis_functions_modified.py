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

def get_magnetization(spins):
    return np.abs(np.mean(spins))

def get_magnetization_squared(spins):
    return np.abs(np.mean(spins**2))

def get_susceptibility(temp,spins):
    return (get_magnetization_squared(spins)-get_magnetization(spins)**2)*len(spins)/(kB*temp)

def get_error_sus(T,J):
    Tc=2.27 * J/kB
    error = np.nan_to_num(1/(kB*(T-Tc)))
    return error

def Metropolis2D(N,spins,J,T,h,L,dT):
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
    dT: float
        Change in temperature in each step of simulation
    Return:
    --------
    final_spins: numpy.ndarray
        The resulting lattice after executing the Metropolis algorithm after N steps.
    """
    # begin Metropolis algorithm
    print(f"Start Metropolis2D algorithm with {N} runs.")
    print(f"Temperature ratio, T/Tc = {np.round(T/(2.27 * J/kB),4)}")
    mag = [1]
    t=[0]
    susceptibility = [0]
    trial_sus = []
    errors_mag = [0]
    errors_sus = [0]
    num_spins = len(spins)
    print(num_spins)
    for i in range(N):

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
        #trial_sus.append(get_susceptibility(T,spins))
        if i%6000 == 0:
            anal_M = lambda Temperature,J: np.nan_to_num(pow(1-pow(np.sinh(2*(1/(kB*Temperature))*J),-4),1/8)) # analytical expression for 2D square lattice Ising model

            T += dT*J/kB
            t.append(T/(2.27 * J/kB))
            M = get_magnetization(spins)
            mag.append(M)
            errors_mag.append(M-anal_M(T,J))

            susceptibility.append(get_susceptibility(T,spins))
            errors_sus.append(susceptibility[-1]-get_error_sus(T,J))
            trial_sus = []
            plt.clf()
            plt.subplot(3, 1, 1)
            plt.errorbar(t, susceptibility, yerr=errors_sus, color='b')
            plt.ylabel('susceptibility')
            plt.xlabel('T/Tc')
            plt.ylim(0,30)

            plt.subplot(3, 1, 2)
            plt.errorbar(t, mag, yerr=errors_mag,color='b')
            plt.ylabel('magnetization')
            plt.xlabel('T/Tc')


            plt.subplot(3, 1, 3)
            plt.imshow(spins,cmap='magma')
            plt.title(f"Run #{i}. $J$={J}. $T/T_c$={np.round(T/(2.27 * J/kB),4)}. $h$={h}.")
            plt.draw()
            plt.pause(0.0000000001)



    final_spins = spins
    return final_spins
