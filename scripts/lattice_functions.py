import numpy as np
from scipy.constants import Boltzmann as kB

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
