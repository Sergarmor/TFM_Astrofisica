import numpy as np
import pandas as pd
from Corrfunc.theory import xi

# Simulation parameters
L = 205 # Side length of simulation box
h = 0.6774 # Little Hubble constant

galaxies_shuffled = pd.read_csv('Resultados/galaxies_shuffled.csv')

def correlation_fun(L, X, Y, Z):

    bins_espaciales = np.log10(L/2-0.1)

    # X = galaxies_shuffled['Gal_x_new']
    # Y = galaxies_shuffled['Gal_y_new']
    # Z = galaxies_shuffled['Gal_z_new']

    weights = np.ones_like(X)

    binfile = np.logspace(np.log10(0.1), bins_espaciales, 100)

    correlation_function = xi(L, 1, binfile, X, Y, Z, weights = weights)

np.save('correlation_function_data', correlation_function)