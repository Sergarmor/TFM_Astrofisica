import numpy as np
import numpy.random as r
import pandas as pd
from Corrfunc.theory import xi
from shuffling import halo_shuffling

# Simulation parameters
L = 205 # Side length of simulation box
h = 0.6774 # Little Hubble constant

halos = pd.read_csv('Resultados/halos.csv')
galaxies = pd.read_csv('Resultados/galaxies.csv')

corte_masa = 10.75
galaxies_sample = galaxies[galaxies['Stellar mass']>corte_masa]

bin_width=0.1

bins_espaciales = np.log10(L/2-0.1)

X = galaxies_sample['Gal_x']
Y = galaxies_sample['Gal_y']
Z = galaxies_sample['Gal_z']

weights = np.ones_like(X)
binfile = np.logspace(np.log10(0.1), bins_espaciales, 100)

pcf_original = xi(L, 1, binfile, X, Y, Z, weights = weights)
np.save('Resultados/pcf_original', pcf_original)

seed_number=100

lista_DataFrames = halo_shuffling(L, bin_width, seed_number, corte_masa)
lista_xis = []
for q in range(len(lista_DataFrames)):
    galaxies_shuffled = lista_DataFrames[q]

    X_shuffled = galaxies_shuffled['Gal_x_new']
    Y_shuffled = galaxies_shuffled['Gal_y_new']
    Z_shuffled = galaxies_shuffled['Gal_z_new']

    pcf_shuffled = xi(L, 1, binfile, X_shuffled, Y_shuffled, Z_shuffled, weights = weights)
    pcf_shuffled = pd.DataFrame(pcf_shuffled, columns=['rmin', 'rmax', 'ravg', 'xi', 'npairs', 'weightavg'])
    
    pcf_shuffled_xi = pcf_shuffled['xi']
    lista_xis.append(pcf_shuffled_xi)
    
pcf_shuffled_xi = pd.concat(lista_xis, axis=1)

pcf_shuffled_xi = pcf_shuffled_xi.assign(mean=pcf_shuffled_xi.mean(axis=1))
pcf_shuffled_xi = pcf_shuffled_xi.assign(std=pcf_shuffled_xi.std(axis=1))
pcf_shuffled_xi = pcf_shuffled_xi.loc[:, ['mean', 'std']]

pcf_shuffled_xi.to_csv('Resultados/pcf_shuffled_mean.csv', index=False)


