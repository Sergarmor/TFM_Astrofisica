import numpy as np
import pandas as pd
from Corrfunc.theory import xi

# Simulation parameters
L = 205 # Side length of simulation box
h = 0.6774 # Little Hubble constant

galaxies = np.load('galaxies.npy')

galaxies_sample = galaxies[galaxies['Stellar mass']>10.75]

X = galaxies_sample['Gal_x']
Y = galaxies_sample['Gal_y']
Z = galaxies_sample['Gal_z']
weights = np.ones_like(X)

binfile = np.logspace(np.log10(0.1), np.log10(L/2-0.1), 100)

results = xi(L, 1, binfile, X, Y, Z, weights = weights)

np.save('results', results)