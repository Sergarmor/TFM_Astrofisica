def galaxies_shuffle_optimized(halos, galaxies_sample, features, L):
    
    """
    Galaxy shuffling. Permutates the halos to select them for each population.
    Expected execution time: 46 seconds
    
    Parameters
    ----------
    
    halos : DataFrame
            DataFrame of binned halos.
    
    galaxies_sample : DataFrame
            DataFrame of binned galaxies.
    
    features : list
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

    features_bins=[]
    for p in range(len(features)):
        features_bins.append(features[p] + ' bin')
        
    if len(features_bins) == 1:
        features_bins = features_bins[0]


    halos_grouped = halos.groupby(by=features_bins)
    galaxies_grouped = galaxies_sample.groupby(by=features_bins)
    population_list=[]

    # Loop in bins considered
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
            
            # Halo caracteristics
            population['Halo mass'] = float(halo_new['Halo mass'])
            population['Halo concentration'] = float(halo_new['Halo concentration'])
            population['Halo spin'] = float(halo_new['Halo spin'])
            
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
                    population['Halo mass bin'] = int(halo_new['Halo mass bin'])
                    population['Halo concentration bin'] = int(halo_new['Halo concentration bin'])
                    population['Halo spin bin'] = int(halo_new['Halo spin bin'])
            else:
                if not population[features_bins].iloc[0].equals(halo_new[features_bins].astype('int64')):
                    raise ValueError('Error in group selection')
                else:
                    population['Halo mass bin'] = int(halo_new['Halo mass bin'])
                    population['Halo concentration bin'] = int(halo_new['Halo concentration bin'])
                    population['Halo spin bin'] = int(halo_new['Halo spin bin'])
            
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


















def galaxies_shuffling_many(halos, galaxies_sample, features, N_shufflings, L):
    
    """
    Multiple galaxy shufflings.
    Expected execution time: 46 seconds for each shuffling.
    
    Parameters
    ----------
    
    halos : DataFrame
            DataFrame of binned halos.
    
    galaxies_sample : DataFrame
            DataFrame of binned galaxies.
    
    features : list
            List of labels for the binning. Labels must be strings.
            
    N_shufflings : int
            Number of shufflings to execute.
    
    L : float
            Box size in same units as positions.
            
    Returns
    -------
    
    galaxies_list : List
            List of DataFrames of shuffled galaxies.
    
    """
    
    import numpy as np
    import numpy.random as r
    import pandas as pd

    galaxies_list=[]

    for i in range(N_shufflings):
        print(f'Shuffle number {i+1} out of {N_shufflings}')
        galaxies_shuffled = galaxies_shuffle_optimized(halos, galaxies_sample, features, L)
        galaxies_list.append(galaxies_shuffled)
        galaxies_shuffled.to_csv(f'Resultados/Shuffled/Galaxies/galaxies_shuffled{i}.csv', index=False)
    return galaxies_list