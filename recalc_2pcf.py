#
# Copyright 2023-2024 
#
# This file is part of Sergio García's Master's Thesis (TFM)
#
# SPDX-License-Identifier: 
# License-Filename: LICENSE.txt
#

import numpy as np
import pandas as pd
from calculo_2pcf import calculo_2pcf

L=205
N_shufflings=100
spatial_bin_number=25
n_threads=1
minimal_sample = 10.5
max_mass_sample = 13.0

shuffling_type=input('Which secondary property are you shuffling?: ')

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

path = feature_file_dict[shuffling_type]

mass_cuts = [10.5, 10.75, 13.0]

for i in range(2):
    mass_cut_1 = mass_cuts[i]
    mass_cut_2 = mass_cuts[i+1]
    print(f'Mass bin number {i} out of 2')

    if mass_cut_1 < minimal_sample:
        raise ValueError(f'Mass cut 1 must be greater than {minimal_sample}')
    
    if mass_cut_2 > max_mass_sample:
        raise Warning(f'Mass cut 2 is too big. Reset to {max_mass_sample}')
    
    galaxies_list=[]

    print('Reading data')
    for i in range(N_shufflings):
        # print(f'Shuffle number {i+1} out of {N_shufflings}')
        galaxies_temp = pd.read_csv(f'Resultados/{path}/Shuffled/Galaxies/galaxies_shuffled{i}.csv')
        galaxies_list.append(galaxies_temp)

    print("Recalculating 2pcf's")
    lista_xis = []
    for q in range(len(galaxies_list)):

        # We extract one DataFrame of shuffled galaxies
        galaxies_shuffled = galaxies_list[q] 
        
        # Keep one mass bin (remove the rest)
        galaxies_shuffled = galaxies_shuffled[galaxies_shuffled.loc[:, 'Stellar mass'] > mass_cut_1].copy()
        galaxies_shuffled = galaxies_shuffled[galaxies_shuffled.loc[:, 'Stellar mass'] < mass_cut_2].copy()

        # We extract the 2PCF value of the shuffled galaxies (one iteration) and save it to use later
        pcf_shuffled = calculo_2pcf(galaxies_shuffled, L, spatial_bin_number, n_threads)
        pcf_shuffled.to_csv(f'Resultados/{path}/Shuffled/PCF/pcf_shuffled{q}.csv', index=False) # We save the shuffled 2pcf
        
        # Save the 2PCF values of all shuffled samples
        pcf_shuffled_xi = pcf_shuffled['xi']
        lista_xis.append(pcf_shuffled_xi)

    # We unite all the shuffled 2PCF and compute the mean and std
    pcf_shuffled_xi = pd.concat(lista_xis, axis=1)

    pcf_shuffled_xi = pcf_shuffled_xi.assign(mean=pcf_shuffled_xi.mean(axis=1))
    pcf_shuffled_xi = pcf_shuffled_xi.assign(std=pcf_shuffled_xi.std(axis=1))
    pcf_shuffled_xi = pcf_shuffled_xi.loc[:, ['mean', 'std']] # We discard all the 2PCFs and maintain the mean and std. Then we save it
    pcf_shuffled_xi.to_csv(f'Resultados/{path}/pcf_shuffled_mean_{mass_cut_1}_{mass_cut_2}.csv', index=False)