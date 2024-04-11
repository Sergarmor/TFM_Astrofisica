def galaxies_shuffle_optimized(halos, galaxies_sample, features_bins, L, file_part):
    
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
                               'Halo tvform 1', 'Halo tvform 2', 'Halo tvform 3']}
    
    feature_list = feature_dict[file_part]

    # Loop in bins considered
    for bins, galaxies_bin in galaxies_grouped:
        halos_bin = halos_grouped.get_group(bins).sample(frac=1)
        
        galaxies_population_grouped = galaxies_bin.groupby(by='HostID')
        i=0
        
        # Loop on populations in bin
        for (halo_id), population in galaxies_population_grouped:
            halo_new = halos_bin.iloc[i]
            i+=1
            
            population['New HostID'] = int(halo_new['HaloID'])
            population['New Host index'] = int(halo_new.name)
            
            # Halo caracteristics
            population[feature_list] = halo_new[feature_list]

        #     population['Halo mass'] = float(halo_new['Halo mass'])
        #     population['Halo concentration'] = float(halo_new['Halo concentration'])
        #     population['Halo spin'] = float(halo_new['Halo spin'])
        #         # New properties
        #     population['Halo mrank 1'] = float(halo_new['Halo mrank 1'])
        #     population['Halo mrank 2'] = float(halo_new['Halo mrank 2'])
        #     population['Halo mrank 3'] = float(halo_new['Halo mrank 3'])
            
        #     population['Halo vrank 1'] = float(halo_new['Halo vrank 1'])
        #     population['Halo vrank 2'] = float(halo_new['Halo vrank 2'])
        #     population['Halo vrank 3'] = float(halo_new['Halo vrank 3'])
            
        #     population['Halo tmform 1'] = float(halo_new['Halo tmform 1'])
        #     population['Halo tmform 2'] = float(halo_new['Halo tmform 2'])
        #     population['Halo tmform 3'] = float(halo_new['Halo tmform 3'])
            
        #     population['Halo tvform 1'] = float(halo_new['Halo tvform 1'])
        #     population['Halo tvform 2'] = float(halo_new['Halo tvform 2'])
        #     population['Halo tvform 3'] = float(halo_new['Halo tvform 3'])
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


















def galaxies_shuffling_many(halos, galaxies_sample, features_bins, N_shufflings, L, part, file_part):
    
    """
    Multiple galaxy shufflings.
    Expected execution time: 46 seconds for each shuffling.
    
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

    for i in trange(N_shufflings):
        # print(f'Shuffle number {i+1} out of {N_shufflings}')
        galaxies_shuffled = galaxies_shuffle_optimized(halos, galaxies_sample, features_bins, L, file_part)
        galaxies_list.append(galaxies_shuffled)
        galaxies_shuffled.to_csv(f'Resultados/Shuffled/Galaxies/galaxies_shuffled{i+part*20}.csv', index=False)
    return galaxies_list