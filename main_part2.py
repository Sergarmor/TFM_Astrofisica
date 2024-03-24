import numpy as np
import numpy.random as r
import pandas as pd
from datetime import datetime
from Corrfunc.theory import xi

# Importing custom functions
from calculo_bins import calculo_bins
from shuffling import galaxies_shuffle_optimized, galaxies_shuffling_many
from ploting_script import ploting_2pcf_ratio
from calculo_2pcf import calculo_2pcf

# Simulation parameters
L = 205                                      # Side length of simulation box
h = 0.6774                                   # Little Hubble constant

# Analisys parameters
mass_cut = 10.5                           # We cut the galaxies by mass into a sample
N_shufflings = 100
spatial_bin_number = 25                      # Bin number in spatial bins (2PCF calculation)
n_threads = 1                                # Number of threads to use to calculate the 2PCF

# Plotting parameters
n = 3                                        # Number of sigmas in the plot


lista_xis = []
for q in range(100):
    # We extract one DataFrame of shuffled galaxies
    galaxies_shuffled = pd.read_csv(f'Resultados/Shuffled/Galaxies/galaxies_shuffled{q}.csv')
    
    # We extract the 2PCF value of the shuffled galaxies (one iteration) and save it to use later
    pcf_shuffled = calculo_2pcf(galaxies_shuffled, L, spatial_bin_number, n_threads)
    
    pcf_shuffled.to_csv(f'Resultados/Shuffled/PCF/pcf_shuffled{q}.csv', index=False) # We save the shuffled 2pcf
    
    
    pcf_shuffled_xi = pcf_shuffled['xi']
    lista_xis.append(pcf_shuffled_xi)

# We unite all the shuffled 2PCF and compute the mean and std
pcf_shuffled_xi = pd.concat(lista_xis, axis=1)

pcf_shuffled_xi = pcf_shuffled_xi.assign(mean=pcf_shuffled_xi.mean(axis=1))
pcf_shuffled_xi = pcf_shuffled_xi.assign(std=pcf_shuffled_xi.std(axis=1))
pcf_shuffled_xi = pcf_shuffled_xi.loc[:, ['mean', 'std']] # We discard all the 2PCFs and maintain the mean and std. Then we save it
pcf_shuffled_xi.to_csv('Resultados/pcf_shuffled_mean.csv', index=False)




# We plot the results

ploting_2pcf_ratio(pcf_original, pcf_shuffled_xi, n, L, features, N_shufflings)