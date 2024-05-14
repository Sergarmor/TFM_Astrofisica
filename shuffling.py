#
# Copyright 2023-2024 
#
# This file is part of Sergio García's Master's Thesis (TFM)
#
# SPDX-License-Identifier: 
# License-Filename: LICENSE.txt
#

def galaxies_shuffle_one(halos, galaxies_sample, features_bins, L, file_part):
    
    """
    Galaxy shuffling. Permutates the halos to select them for each population.
    Expected execution time: 46 seconds
    
    Parameters
    ----------
    
    halos : DataFrame
            DataFrame of binned halos.
    
    galaxies_sample : DataFrame
            DataFrame of binned galaxies.
    
    features_bins : list
            List of labels for the binning. Labels must be strings.
    
    L : float
            Box size in same units as positions.
            
    Returns
    -------
    
    galaxies_shuffled : DataFrame
            DataFrame of shuffled galaxies.
    """
    
    import numpy as np
    import numpy.random as r
    import pandas as pd


        
    if len(features_bins) == 1:
        features_bins = features_bins[0]


    halos_grouped = halos.groupby(by=features_bins)
    galaxies_grouped = galaxies_sample.groupby(by=features_bins)
    population_list=[]

    # Loop on bins considered
    for bins, galaxies_bin in galaxies_grouped:
        halos_bin = halos_grouped.get_group(bins).sample(frac=1)
        
        ID_halos, index_halos = np.unique(galaxies_bin['HostID'], return_index=True)
        
        galaxies_population_grouped = galaxies_bin.groupby(by='HostID')
        i=0
        
        # Loop on populations in bin
        for (halo_id), population in galaxies_population_grouped:
            halo_new = halos_bin.iloc[i]
            i+=1
            
            population['New HostID'] = int(halo_new['HaloID'])
            population['New Host index'] = int(halo_new.name)

            population['Halo mass'] = float(halo_new['Halo mass'])

            # Halo caracteristics
            if file_part == 'part1':

                
                population['Halo concentration'] = float(halo_new['Halo concentration'])
                population['Halo spin'] = float(halo_new['Halo spin'])

            elif file_part == 'part2':

                # Mass ranking
                population['Halo mrank 1'] = float(halo_new['Halo mrank 1'])
                population['Halo mrank 2'] = float(halo_new['Halo mrank 2'])
                population['Halo mrank 3'] = float(halo_new['Halo mrank 3'])
                population['Halo mrank 4'] = float(halo_new['Halo mrank 4'])
                population['Halo mrank 5'] = float(halo_new['Halo mrank 5'])
                population['Halo mrank 6'] = float(halo_new['Halo mrank 6'])
                
                # Velocity ranking
                population['Halo vrank 1'] = float(halo_new['Halo vrank 1'])
                population['Halo vrank 2'] = float(halo_new['Halo vrank 2'])
                population['Halo vrank 3'] = float(halo_new['Halo vrank 3'])
                population['Halo vrank 4'] = float(halo_new['Halo vrank 4'])
                population['Halo vrank 5'] = float(halo_new['Halo vrank 5'])
                population['Halo vrank 6'] = float(halo_new['Halo vrank 6'])
            
            elif file_part == 'part3':
                # Formation time, mass
                population['Halo tmform 1'] = float(halo_new['Halo tmform 1'])
                population['Halo tmform 2'] = float(halo_new['Halo tmform 2'])
                population['Halo tmform 3'] = float(halo_new['Halo tmform 3'])
                population['Halo tmform 4'] = float(halo_new['Halo tmform 4'])
                population['Halo tmform 5'] = float(halo_new['Halo tmform 5'])
                
                # Formation time, velocity
                population['Halo tvform 1'] = float(halo_new['Halo tvform 1'])
                population['Halo tvform 2'] = float(halo_new['Halo tvform 2'])
                population['Halo tvform 3'] = float(halo_new['Halo tvform 3'])

                # av_nu
                population['Halo av_nu'] = float(halo_new['Halo av_nu'])

            else:

                raise KeyError("Error in file part selection (shouldn't be possible)")

            
            
            # Halo coords
            population['Halo_x'] = float(halo_new['x'])
            population['Halo_y'] = float(halo_new['y'])
            population['Halo_z'] = float(halo_new['z'])
            
            # Halo vel
            population['Halo_vel_x'] = float(halo_new['Vel_x'])
            population['Halo_vel_y'] = float(halo_new['Vel_y'])
            population['Halo_vel_z'] = float(halo_new['Vel_z'])
            
            # Galaxy coords
            population['Pos_x'] = float(halo_new['x']) + population['COP_x']
            population['Pos_y'] = float(halo_new['y']) + population['COP_y']
            population['Pos_z'] = float(halo_new['z']) + population['COP_z']
            
            # Galaxy vel
            population['Vel_x'] = float(halo_new['Vel_x']) + population['COP_vel_x']
            population['Vel_y'] = float(halo_new['Vel_y']) + population['COP_vel_y']
            population['Vel_z'] = float(halo_new['Vel_z']) + population['COP_vel_z']
            
            # Check for equal bins
            if type(features_bins) == str:
                if not population[features_bins].iloc[0] == halo_new[features_bins].astype('int64'):
                    raise ValueError('Error in group selection')
            else:
                if not population[features_bins].iloc[0].equals(halo_new[features_bins].astype('int64')):
                    raise ValueError('Error in group selection')
            
            # Periodic conditions
            population.loc[population['Pos_x'] > L, 'Pos_x'] -= L
            population.loc[population['Pos_x'] < 0, 'Pos_x'] += L

            population.loc[population['Pos_y'] > L, 'Pos_y'] -= L
            population.loc[population['Pos_y'] < 0, 'Pos_y'] += L

            population.loc[population['Pos_z'] > L, 'Pos_z'] -= L
            population.loc[population['Pos_z'] < 0, 'Pos_z'] += L
            
            population_list.append(population)

    galaxies_shuffled = pd.concat(population_list)

    return galaxies_shuffled



def galaxies_shuffling_many(halos, galaxies_sample, features_bins, N_shufflings, L, part, path):
    
    """
    Multiple galaxy shufflings.
    
    Parameters
    ----------
    
    halos : DataFrame
            DataFrame of binned halos.
    
    galaxies_sample : DataFrame
            DataFrame of binned galaxies.
    
    features_bins : list
            List of labels for the binning. Labels must be strings.
            
    N_shufflings : int
            Number of shufflings to execute.
    
    L : float
            Box size in same units as positions.
            
    part : int
            Execution part. Used to number each file. Implemented due to memory limitations.
            
    Returns
    -------
    
    galaxies_list : List
            List of DataFrames of shuffled galaxies.
    galaxies_shuffled.csv : Saved as .csv file in order for it to be available later
    
    """
    
    import numpy as np
    import numpy.random as r
    import pandas as pd
    from tqdm import trange

    galaxies_list=[]

    feature_file_dict = {'Halo_mass'              : 'part1',
                        'Halo_mass_concentration' : 'part1',
                        'Halo_mass_spin'          : 'part1',
                        'Halo_mass_mrank1'        : 'part2',
                        'Halo_mass_mrank2'        : 'part2',
                        'Halo_mass_mrank3'        : 'part2',
                        'Halo_mass_mrank4'        : 'part2',
                        'Halo_mass_mrank5'        : 'part2',
                        'Halo_mass_mrank6'        : 'part2',
                        'Halo_mass_vrank1'        : 'part2',
                        'Halo_mass_vrank2'        : 'part2',
                        'Halo_mass_vrank3'        : 'part2',
                        'Halo_mass_vrank4'        : 'part2',
                        'Halo_mass_vrank5'        : 'part2',
                        'Halo_mass_vrank6'        : 'part2',
                        'Halo_mass_tmform1'       : 'part3',
                        'Halo_mass_tmform2'       : 'part3',
                        'Halo_mass_tmform3'       : 'part3',
                        'Halo_mass_tmform4'       : 'part3',
                        'Halo_mass_tmform5'       : 'part3',
                        'Halo_mass_tvform1'       : 'part3',
                        'Halo_mass_tvform2'       : 'part3',
                        'Halo_mass_tvform3'       : 'part3',
                        'Halo_mass_av_nu'         : 'part3',
                        }
    
    file_part = feature_file_dict[path]

    for i in trange(N_shufflings):
        galaxies_shuffled = galaxies_shuffle_one(halos, galaxies_sample, features_bins, L, file_part)
        galaxies_list.append(galaxies_shuffled)
        galaxies_shuffled.to_csv(f'Resultados/{path}/Shuffled/Galaxies/galaxies_shuffled{i+part*20}.csv', index=False)
    return galaxies_list