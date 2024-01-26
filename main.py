import numpy as np
import numpy.random as r
import pandas as pd
from Corrfunc.theory import xi
from shuffling import halo_shuffling
from ploting_script import ploting_results
from calculo_2pcf import calculo_2pcf

# Simulation parameters
L = 205                  # Side length of simulation box
h = 0.6774               # Little Hubble constant

# Analisys parameters
corte_masa = 10.75       # We cut the galaxies by mass into a sample
bin_width = 0.1          # Bin width in halo mass
bin_number = 100         # Bin number in spatial bins (2PCF calculation)
seed_number = 100        # We shuffle seed_number times and compute the mean and std
n = 3                    # Number of sigmas in the plot
n_threads = 1            # Number of threads to use to calculate the 2PCF

# We read the data
halos = pd.read_csv('Resultados/halos.csv')
galaxies = pd.read_csv('Resultados/galaxies.csv')

# We get the sample by cutting in stellar mass
galaxies_sample = galaxies[galaxies['Stellar mass']>corte_masa]

# Calculate the original 2PCF

pcf_original = calculo_2pcf(galaxies_sample, L, bin_number, n_threads)

pcf_original.to_csv('Resultados/pcf_original.csv', index=False) # We save the original 2PCF


# Calculate the 2PCF shuffled
lista_DataFrames = halo_shuffling(L, bin_width, seed_number, corte_masa) # We shuffle the galaxies into haloes of same mass bin
lista_xis = []
for q in range(len(lista_DataFrames)):
    # We extract one DataFrame of shuffled galaxies
    galaxies_shuffled = lista_DataFrames[q] 
    
    # We extract the 2PCF value of the shuffled galaxies (one iteration) and save it to use later
    pcf_shuffled = calculo_2pcf(galaxies_shuffled, L, bin_number, n_threads)
    pcf_shuffled_xi = pcf_shuffled['xi']
    lista_xis.append(pcf_shuffled_xi)
    print(q)

# We unite all the shuffled 2PCF and compute the mean and std
pcf_shuffled_xi = pd.concat(lista_xis, axis=1)

pcf_shuffled_xi = pcf_shuffled_xi.assign(mean=pcf_shuffled_xi.mean(axis=1))
pcf_shuffled_xi = pcf_shuffled_xi.assign(std=pcf_shuffled_xi.std(axis=1))
pcf_shuffled_xi = pcf_shuffled_xi.loc[:, ['mean', 'std']] # We discard all the 2PCFs and maintain the mean and std. Then we save it
pcf_shuffled_xi.to_csv('Resultados/pcf_shuffled_mean.csv', index=False)


b = pcf_original['xi'] / pcf_shuffled_xi['mean'] # Assembly bias
sigma = pcf_original['xi']/pcf_shuffled_xi['mean'] * pcf_shuffled_xi['std'] # Assembly bias uncertainty


# We plot the results

ploting_results(pcf_original, b, sigma, n, L)