import numpy as np
import matplotlib.pyplot as plt
from metropolis import metropolis_evolution
from evolution import evolution


fields = np.linspace(-1,1,65)
phase_diagram = []
for h in fields:
    print(h)
    _, obsers_relax, T_relax = evolution(f=metropolis_evolution,relax=2000,L=50,T_init=0.1,T_max=2,dT=0.07/2.27,h=h)
    phase_diagram.append(obsers_relax[0])

np_phase_diagram = np.array(phase_diagram)


plt.close()
plt.imshow(np_phase_diagram, cmap='Spectral', extent=[0.1,2,1,-1])
plt.xlabel('$T/T_C$')
plt.ylabel('h')
cb=plt.colorbar(ticks=[-1, 0, 1])
cb.set_label('Magnetisation', rotation=270)
plt.clim(-1,1)
plt.savefig(f"simulation_images/phase_diagram.pdf",  bbox_inches='tight')