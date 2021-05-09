import numpy as np

def get_error_mag(Temperature,J=1):
    anal_M = np.nan_to_num(pow(1-pow(np.sinh(2*(1/(Temperature))*J),-4),1/8))
    return anal_M

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

def plot_observables():

    for observable in observables:
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


def get_observables(spins,T):
    M = get_magnetization(spins)
    chi = get_susceptibility(T,spins)
