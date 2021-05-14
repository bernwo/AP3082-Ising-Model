import numpy as np
from scipy.constants import Boltzmann as kB
from scipy.ndimage import convolve


def flip_coin():
    """
    Generates random number between 0 and 1.

    Return:
    --------
    int
        random number between 0 and 1.
    """
    return np.random.rand()

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

<<<<<<< HEAD
=======
def get_energy_total(J,h,spins):
    """
    Calculates the total spin energy contribution of the lattice.

    Parameters:
    -----------
    J: float
        Coupling constant. J should always be J > 0.
    h: float
        External magnetic field strength.
    spins: numpy.ndarray
        The lattice containing spins.
    
    Return:
    --------
    E_tot: float
        The total spin energy contribution of the lattice.
    """
    kernel = np.array([[0, 1, 0],[1, 0, 1],[0, 1, 0]])
    neighbour_sums = convolve(spins, kernel, mode='wrap')
    E = -J/2 * neighbour_sums * spins - h * spins
    E_tot = np.sum(E)
    return E_tot

>>>>>>> 5dc5a3a85ad7df68a29c4e398926f02593099348
def flip_a_spin(spins, turn):
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
    new_spin[i,j] = turn*new_spin[i,j]
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
