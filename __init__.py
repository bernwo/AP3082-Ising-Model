import numpy as np
import matplotlib.pyplot as plt

# Let the total number of sites be N × N where N∈ℤ
def init_lattice(N):
    return np.random.rand(N,N)

spins = init_lattice(20)

# Plot
plt.imshow(spins,cmap='magma')
plt.colorbar()
plt.clim(-1,1)
plt.show()




