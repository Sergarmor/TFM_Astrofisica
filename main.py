import numpy as np
import numpy.random as r
import pandas as pd
from Corrfunc.theory import xi

# Simulation parameters
L = 205 # Side length of simulation box
h = 0.6774 # Little Hubble constant

halos = pd.read_csv('Resultados/halos.csv')
galaxies = pd.read_csv('Resultados/galaxies.csv')


galaxies_sample = galaxies[galaxies['Stellar mass']>10.75]

bins_espaciales = np.log10(L/2-0.1)

X = galaxies_sample['Gal_x']
Y = galaxies_sample['Gal_y']
Z = galaxies_sample['Gal_z']

weights = np.ones_like(X)
binfile = np.logspace(np.log10(0.1), bins_espaciales, 100)

pcf_original = xi(L, 1, binfile, X, Y, Z, weights = weights)

for q in range(10):
    galaxies_shuffled = pd.read_csv(f'Resultados/galaxies_shuffled{q}.csv')

    X_shuffled = galaxies_shuffled['Gal_x_new']
    Y_shuffled = galaxies_shuffled['Gal_y_new']
    Z_shuffled = galaxies_shuffled['Gal_z_new']

    pcf_shuffled = xi(L, 1, binfile, X_shuffled, Y_shuffled, Z_shuffled, weights = weights)

np.save('Resultados/pcf_original', pcf_original)
np.save('Resultados/pcf_shuffled', pcf_shuffled)