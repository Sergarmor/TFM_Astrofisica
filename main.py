#
# Copyright 2023-2024 
#
# This file is part of Sergio García's Master's Thesis (TFM)
#

import numpy as np
import numpy.random as r
import pandas as pd
from datetime import datetime
from Corrfunc.theory import xi

# Importing custom functions
from shuffling import galaxies_shuffle_one, galaxies_shuffling_many
from calculo_2pcf import calculo_2pcf


# Simulation parameters
L = 205                                      # Side length of simulation box

# Analisys parameters
mass_cut = 10.5                           # We cut the galaxies by mass into a sample

# Features used to do the binning and shuffle the galaxies
features=['Halo mass']

secondary_feature = input('Which feature do you want?: ')

features.append(secondary_feature)


feature_part_dict = {'None'          : 'part1',
                     'Halo mrank 1'  : 'part2',
                     'Halo mrank 2'  : 'part2',
                     'Halo mrank 3'  : 'part2',
                     'Halo mrank 4'  : 'part2',
                     'Halo mrank 5'  : 'part2',
                     'Halo mrank 6'  : 'part2',
                     'Halo vrank 1'  : 'part2',
                     'Halo vrank 2'  : 'part2',
                     'Halo vrank 3'  : 'part2',
                     'Halo vrank 4'  : 'part2',
                     'Halo vrank 5'  : 'part2',
                     'Halo vrank 6'  : 'part2',
                     'Halo tmform 1' : 'part3',
                     'Halo tmform 2' : 'part3',
                     'Halo tmform 3' : 'part3',
                     'Halo tmform 4' : 'part3',
                     'Halo tmform 5' : 'part3',
                     'Halo tvform 1' : 'part3',
                     'Halo tvform 2' : 'part3',
                     'Halo tvform 3' : 'part3',
                     'Halo av_nu'    : 'part3',
                     }

feature_file_dict = {'None'          : 'Halo_mass',
                     'Halo mrank 1'  : 'Halo_mass_mrank1',
                     'Halo mrank 2'  : 'Halo_mass_mrank2',
                     'Halo mrank 3'  : 'Halo_mass_mrank3',
                     'Halo mrank 4'  : 'Halo_mass_mrank4',
                     'Halo mrank 5'  : 'Halo_mass_mrank5',
                     'Halo mrank 6'  : 'Halo_mass_mrank6',
                     'Halo vrank 1'  : 'Halo_mass_vrank1',
                     'Halo vrank 2'  : 'Halo_mass_vrank2',
                     'Halo vrank 3'  : 'Halo_mass_vrank3',
                     'Halo vrank 4'  : 'Halo_mass_vrank4',
                     'Halo vrank 5'  : 'Halo_mass_vrank5',
                     'Halo vrank 6'  : 'Halo_mass_vrank6',
                     'Halo tmform 1' : 'Halo_mass_tmform1',
                     'Halo tmform 2' : 'Halo_mass_tmform2',
                     'Halo tmform 3' : 'Halo_mass_tmform3',
                     'Halo tmform 4' : 'Halo_mass_tmform4',
                     'Halo tmform 5' : 'Halo_mass_tmform5',
                     'Halo tvform 1' : 'Halo_mass_tvform1',
                     'Halo tvform 2' : 'Halo_mass_tvform2',
                     'Halo tvform 3' : 'Halo_mass_tvform3',
                     'Halo av_nu'    : 'Halo_mass_av_nu',
                     }

path = feature_file_dict[secondary_feature]

file_part = feature_part_dict[secondary_feature]

if file_part == 'part2': # Due to memory error in cluster (files too big?)
    N_shufflings = 20
    part = int(input('Execution part [0/1/2/3/4]: ')) # Designed max 100 shufflings
else:
    N_shufflings = 100
    part=0

bin_number=100                               # Number of bins for each feature
spatial_bin_number = 25                      # Bin number in spatial bins (2PCF calculation)
n_threads = 1                                # Number of threads to use to calculate the 2PCF
n = 3                                        # Number of sigmas in the plot




recalc = input('Do you want to recalculate the DataFrames? [yes/no]: ')

if recalc == 'yes':

    # Calculation of original data
    import calculo_dataframe

    # Calculation of binned dataframes of halos and galaxies
    import property_bins

elif recalc == 'no':

    # Calculation of binned dataframes of halos and galaxies
    rebin = input('Do you want to recalculate the binning of the DataFrames? [yes/no]: ')
    if rebin == 'yes':
        import property_bins

else:
    raise SyntaxError(f'{recalc} is not a valid answer, only yes or no.')


# We read the data
halos = pd.read_csv('Resultados/halos_'+file_part+'.csv')
galaxies = pd.read_csv('Resultados/galaxies_'+file_part+'.csv')
    
# We get the sample by cutting in stellar mass
galaxies_sample = galaxies[galaxies.loc[:, 'Stellar mass'] > mass_cut].copy()

# Add bin to the feature keywords
features_bins=[]
for p in range(len(features)):
    features_bins.append(features[p] + ' bin')


# Calculate the original 2PCF
pcf_original = calculo_2pcf(galaxies_sample, L, spatial_bin_number, n_threads)
pcf_original.to_csv('Resultados/pcf_original.csv', index=False) # We save the original 2PCF


# Calculate the 2PCF shuffled
time_ini = datetime.now() # Shuffling and 2PCF calculation start time
lista_DataFrames = galaxies_shuffling_many(halos, galaxies_sample, features_bins, N_shufflings, L, part, path)


lista_xis = []
for q in range(len(lista_DataFrames)):

    # We extract one DataFrame of shuffled galaxies
    galaxies_shuffled = lista_DataFrames[q]
    
    # We calculate the 2PCF value of the shuffled galaxies (one iteration) and save it to use later
    pcf_shuffled = calculo_2pcf(galaxies_shuffled, L, spatial_bin_number, n_threads)
    pcf_shuffled.to_csv(f'Resultados/{path}/Shuffled/PCF/pcf_shuffled{q+part*20}.csv', index=False) # We save the shuffled 2pcf
    
    # Save the 2PCF values of all shuffled samples
    pcf_shuffled_xi = pcf_shuffled['xi']
    lista_xis.append(pcf_shuffled_xi)

# We unite all the shuffled 2PCF and compute the mean and std
pcf_shuffled_xi = pd.concat(lista_xis, axis=1)

pcf_shuffled_xi = pcf_shuffled_xi.assign(mean=pcf_shuffled_xi.mean(axis=1))
pcf_shuffled_xi = pcf_shuffled_xi.assign(std=pcf_shuffled_xi.std(axis=1))
pcf_shuffled_xi = pcf_shuffled_xi.loc[:, ['mean', 'std']] # We discard all the 2PCFs and maintain the mean and std. Then we save it
pcf_shuffled_xi.to_csv(f'Resultados/{path}/pcf_shuffled_mean.csv', index=False)

time_end = datetime.now() # Shuffling and 2PCF calculation finish time
print(f"Initial time...: {time_ini}")
print(f"Final time.....: {time_end}")
print(f"Excecution time: {time_end-time_ini}")
print(f"Excecution time per iteration: {(time_end-time_ini)/N_shufflings}")