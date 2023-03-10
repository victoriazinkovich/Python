from datetime import datetime
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random
import math
import time
import matplotlib

'''
Metropolis Algorithm: the energy of the "old" configuration E1 and the "new" E2 is calculated. The energy of the "new" configuration
is compared with the energy of the "old" configuration. The "new" configuration is accepted and becomes the initial one for the next step
if E1>E2, otherwise the probability of a reversal of this spin p(E1→E2) is calculated:
'''
# Creating a chain
def make_chain(n, m):
    return [[-1 if random.randint(0, 1) else 1 for _ in range(m)] for _ in range(n)]

# The energy of one spin
def energy(i, j, chain):
    n = len(chain)
    m = len(chain[0])
    return -(chain[i-1][j] * chain[i][j] + chain[i][j] * chain[(i+1)%n][j] +
            chain[i][j-1] * chain[i][j] + chain[i][j] * chain[i][(j+1)%m])

'''
The difference between the trial energy and the current
one is *(-2) because the change in energy during the flip of one spin out of three is -4 -> 4, -2 -> 2, 0 -> 0 -- either 8, or 4, or 0
that is, in any case, you can multiply the initial energy by (-2) and get the difference in energy
'''
def try_energy(i, j, chain):
    E = energy(i, j, chain)
    return E * (-2)

# The energy of the whole chain
def calc_tot_en(chain):
    n = len(chain)
    m = len(chain[0])
    tot_en = 0.0
    for i in range(n):
        for j in range(m):
            tot_en = tot_en + energy(i, j, chain)
    return tot_en / 4     # /4, the same interactions are taken into account 4 times (4 neighbors)

# We turn the spins 100 times, we get the equilibrium energy
def average_E(chain, T, Niter=100):
    tot_en = calc_tot_en(chain)
    avg_en = 0.0
    n = len(chain)
    m = len(chain[0])
    for i in range(Niter):
        try_i = random.randint(0, n-1)
        try_j = random.randint(0, m-1)
        delta_E = try_energy(try_i, try_j, chain)
        if delta_E < 0:                                      # if the "new" is less than the "old", turn the spin, change the energy to the "new"
            tot_en += delta_E
            chain[try_i][try_j] = -chain[try_i][try_j] 
        else:
            if random.uniform(0,1) < math.exp(-(delta_E)/T): # otherwise, we calculate the probability that such an event will still happen
                tot_en += delta_E                            # must satisfy the inequality probability of this event
                chain[try_i][try_j] = -chain[try_i][try_j] 
        avg_en += tot_en/Niter                               # the average energy over all the turns of the spins
    return avg_en
     
    
'''
Metropolis Algorithm
provides convergence of states to equilibrium in a reasonable number of steps
we conduct a bunch of "tests" (100) on the spin flip so that the energy converges
'''
def metropolis(chain, T, etol=0.0001, steps_per_cycle=100):
    avg_en = 0.0
    avg_en_prev = -100*etol
    Ncycles  = 0
    energies = []
    while math.fabs(avg_en - avg_en_prev) > etol:                 # until the energy in the previous step converges to the current one
        avg_en_prev = avg_en
        avg_en = average_E(chain, T, steps_per_cycle)
        energies.append(avg_en)
        avg_en = (avg_en_prev * Ncycles + avg_en) / (Ncycles + 1) # added with the previous energy and divided into
        Ncycles += 1                                              # the number of iterations to get the average
    return energies
    

------- Adding an external magnetic field ------- 

def M(chain):
    n = len(chain)
    m = len(chain[0])
    M = 0
    for i in range(n):
        for j in range(m):
            M = M + chain[i][j]
    return M
    
def make_chain(n, m):
    return [[-1 if random.randint(0, 1) else 1 for _ in range(m)] for _ in range(n)]

def magfield(i, j, H, chain):
     return -(H * chain[i][j])

def energy(i, j, chain):
    n = len(chain)
    m = len(chain[0])
    return -(chain[i-1][j] * chain[i][j] + chain[i][j] * chain[(i+1)%n][j] +
            chain[i][j-1] * chain[i][j] + chain[i][j] * chain[i][(j+1)%m])

def try_energy(i, j, H, chain):
    E = energy(i, j, chain) + magfield(i, j, H, chain)
    return E * (-2)

def calc_tot_en(chain, H):
    n = len(chain)
    m = len(chain[0])
    tot_en = 0.0
    for i in range(n):
        for j in range(m):
            tot_en = tot_en + energy(i, j, chain)/4 + magfield(i, j, H, chain)
    return tot_en

def average_E(chain, T, H, Niter=100):
    tot_en = calc_tot_en(chain, H)
    avg_en = 0.0
    n = len(chain)
    m = len(chain[0])
    for i in range(Niter):
        try_i = random.randint(0, n-1)
        try_j = random.randint(0, m-1)
        delta_E = try_energy(try_i, try_j, H, chain)
        if delta_E < 0:
            tot_en += delta_E
            chain[try_i][try_j] = -chain[try_i][try_j] 
        else:
            if random.uniform(0,1) < math.exp(-(delta_E)/T): 
                tot_en += delta_E                          
                chain[try_i][try_j] = -chain[try_i][try_j] 
        avg_en += tot_en/Niter                              
    return avg_en
     
def metropolis(chain, T, H, etol=0.0001, steps_per_cycle=100):
    avg_en = 0.0
    avg_en_prev = -100*etol
    Ncycles  = 0
    energies = []
    xi = []
    while math.fabs(avg_en - avg_en_prev) > etol: 
        avg_en_prev = avg_en
        avg_en = average_E(chain, T, H, steps_per_cycle)
        xi.append(M(chain)/H)
        energies.append(avg_en)
        avg_en = (avg_en_prev * Ncycles + avg_en) / (Ncycles + 1)
        Ncycles += 1                                           
    return energies, xi

xi = []
temps = []

T = 0.05
T_end = 4
gap = 0.05
n = 10
m = 10
N = n * m
H = 1

while T <= T_end:
    start_time = datetime.now()
    
    chain = make_chain(n, m)
    energies, xi_tmp = metropolis(chain, T, H, etol=1e-6)
    
    average_xi = sum(xi_tmp)/len(xi_tmp)
    xi.append(average_xi)
    temps.append(T)
    
    print("done: T =", T)
    print('Время выполнения: {}'.format(datetime.now() - start_time))
    T += gap
    T = round(T, 2)
