import numpy as np
import matplotlib.pyplot as plt

# Let the total number of sites be N × N where N∈ℤ
def init_lattice(N):
    """Generate a uniform random sample from np.array([-1,1],dtype=int) of size (N,N)"""
    return np.random.choice(np.array([-1,1],dtype=int), (N,N))

spins = init_lattice(20)

# Plot
plt.imshow(spins,cmap='magma')
plt.colorbar()
plt.clim(-1,1)
plt.show()




