#
# Copyright 2023-2024 
#
# This file is part of Sergio García's Master's Thesis (TFM)
#

import numpy as np
import pandas as pd

feature_dict = {'part1' : ['Halo mass', 
                            'Halo concentration', 'Halo spin'],
                'part2' : ['Halo mass', 
                            'Halo mrank 1', 'Halo mrank 2', 'Halo mrank 3', 
                            'Halo mrank 4', 'Halo mrank 5', 'Halo mrank 6', 
                            'Halo vrank 1', 'Halo vrank 2', 'Halo vrank 3', 
                            'Halo vrank 4', 'Halo vrank 5', 'Halo vrank 6'],
                'part3' : ['Halo mass', 
                            'Halo tmform 1', 'Halo tmform 2', 'Halo tmform 3', 
                            'Halo tmform 4', 'Halo tmform 5',
                            'Halo tvform 1', 'Halo tvform 2', 'Halo tvform 3',
                            'Halo av_nu']}

big_scale_bin_number = 2
bin_number=100

for i in range(3):
    file_part = 'part'+str(i+1)

    features = feature_dict[file_part]

    halos = pd.read_csv('Resultados/halos_'+file_part+'.csv')
    galaxies = pd.read_csv('Resultados/galaxies_'+file_part+'.csv')


    for j in features:
            
        bin_feature = j
        halos_max = halos.loc[:, bin_feature].max()*1.004 # Se extienden los límites en un 0.4% para incluir los elementos límite
        halos_min = halos.loc[:, bin_feature].min()*0.996

        limit = halos.loc[:, bin_feature].max()*0.95 # Se establece un corte para aumentar la anchura de los bins a un 95% del máximo
        
        bins_small = np.linspace(halos_min, limit, bin_number-big_scale_bin_number)
        bins_big = np.linspace(limit, halos_max, big_scale_bin_number+1)[1:]

        bins = np.concatenate((bins_small, bins_big))


        halos[bin_feature+' bin'] = pd.cut(halos[bin_feature], bins, labels=False, include_lowest=True)
        galaxies[bin_feature+' bin'] = pd.cut(galaxies[bin_feature], bins, labels=False, include_lowest=True)

    galaxies.to_csv('Resultados/galaxies_'+file_part+'.csv', index=False)

    halos.to_csv('Resultados/halos_'+file_part+'.csv', index=False)
