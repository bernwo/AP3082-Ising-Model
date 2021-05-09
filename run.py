from evolution import evolution
from wolff import wolff_evolution
from metropolis import metropolis_evolution
import sys
sys.setrecursionlimit(10000000)

evolution(metropolis_evolution,L=100,T=10E-10,dT=0.025,relax=20)
