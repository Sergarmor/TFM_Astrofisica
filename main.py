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

# Features used to do the binning and shuffle the galaxies
features=['Halo mass', 'Halo tvform 1']

# new_feature = input('Which feature do you want to add? Press 0 to add none: ')
N_shufflings = 20
part = int(input('Execution part [0/1/2/3/4]: ')) # Designed max 100 shufflings

# if not new_feature == 0:
    # print(type(new_feature))
    # features.append(new_feature)


bin_number=100                               # Number of bins for each feature
# N_shufflings = 100                           # We shuffle N_shufflings times and compute the mean and std
spatial_bin_number = 25                      # Bin number in spatial bins (2PCF calculation)
n_threads = 1                                # Number of threads to use to calculate the 2PCF
# Definir bin_width con max y min de los datos. Normalizar con los percentiles 95 y 5
# Plotting parameters
n = 3                                        # Number of sigmas in the plot




recalc = input('Do you want to recalculate the DataFrames? [yes/no]: ')

if recalc == 'yes':
    # Calculation of original data
    import calculo_dataframe
    



# We read the data
halos = pd.read_csv('Resultados/halos.csv')
galaxies = pd.read_csv('Resultados/galaxies.csv')

# Calculation of binned dataframes of halos and galaxies
rebin = input('Do you want to recalculate the binning of the DataFrames? [yes/no]: ')

if rebin == 'yes':
    halos, galaxies = calculo_bins(halos, galaxies, bin_number)
else:
    pass
    
# We get the sample by cutting in stellar mass
galaxies_sample = galaxies[galaxies.loc[:, 'Stellar mass'] > mass_cut].copy()


# Execution time estimation and execution confirmation
features_bins=[]
for p in range(len(features)):
    features_bins.append(features[p] + ' bin')


# Calculate the original 2PCF

pcf_original = calculo_2pcf(galaxies_sample, L, spatial_bin_number, n_threads)

pcf_original.to_csv('Resultados/pcf_original.csv', index=False) # We save the original 2PCF


# Calculate the 2PCF shuffled
time_ini = datetime.now()
lista_DataFrames = galaxies_shuffling_many(halos, galaxies_sample, features_bins, N_shufflings, L, part)

time_end = datetime.now()
print(f"Initial time...: {time_ini}")
print(f"Final time.....: {time_end}")
print(f"Excecution time: {time_end-time_ini}")
print(f"Excecution time per iteration: {(time_end-time_ini)/N_shufflings}")