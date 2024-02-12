def galaxies_shuffle_optimized(halos, galaxies_sample, features, L):
    
    """
    Galaxy shuffling. Permutates the halos to select them for each population.
    Expected execution time: 1 minute
    
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

        
    ID_halos, index_halos = np.unique(galaxies_sample['HostID'], return_index=True)
    galaxies_population_list=[]
    halos_choose = halos.copy()

    for i in range(len(index_halos)):
        print(f'Population {i+1} out of {len(index_halos)}')
    
        galaxies_population = galaxies_sample.loc[galaxies_sample['HostID'] == ID_halos[i]]

        bins = galaxies_population.loc[:, features_bins].iloc[0]
        
        halos_bins = halos_choose.copy()
        for p in range(len(bins)):
            halos_bins = halos_bins[halos_bins[features_bins[p]] == int(bins.iloc[p])]

        ID_halo_nuevo = r.choice(halos_bins.loc[:, 'HaloID'], size=1, replace=False)[0]
        index_drop = halos_choose[halos_choose['HaloID']==ID_halo_nuevo].index[0]
        halos_choose = halos_choose.drop(index_drop, axis='index')
        
        
        halo_nuevo = halos_bins.loc[halos_bins['HaloID'] == ID_halo_nuevo]
        galaxies_population_shuffled = galaxies_population.copy()

        galaxies_population_shuffled['HostID'] = int(halo_nuevo['HaloID'].iloc[0])
        galaxies_population_shuffled['Host index'] = int(halos[halos['HaloID'] == ID_halo_nuevo].index[0])

        galaxies_population_shuffled['Halo mass'] = float(halo_nuevo['Halo mass'].iloc[0])
        galaxies_population_shuffled['Halo concentration'] = float(halo_nuevo['Halo concentration'].iloc[0])
        galaxies_population_shuffled['Halo spin'] = float(halo_nuevo['Halo spin'].iloc[0])

        galaxies_population_shuffled['Halo_x'] = float(halo_nuevo['x'].iloc[0])
        galaxies_population_shuffled['Halo_y'] = float(halo_nuevo['y'].iloc[0])
        galaxies_population_shuffled['Halo_z'] = float(halo_nuevo['z'].iloc[0])

        galaxies_population_shuffled['Halo_vel_x'] = float(halo_nuevo['Vel_x'].iloc[0])
        galaxies_population_shuffled['Halo_vel_y'] = float(halo_nuevo['Vel_y'].iloc[0])
        galaxies_population_shuffled['Halo_vel_z'] = float(halo_nuevo['Vel_z'].iloc[0])

        galaxies_population_shuffled['Pos_x'] = float(halo_nuevo['x'].iloc[0]) + galaxies_population_shuffled['COP_x']
        galaxies_population_shuffled['Pos_y'] = float(halo_nuevo['y'].iloc[0]) + galaxies_population_shuffled['COP_y']
        galaxies_population_shuffled['Pos_z'] = float(halo_nuevo['z'].iloc[0]) + galaxies_population_shuffled['COP_z']

        galaxies_population_shuffled['Vel_x'] = float(halo_nuevo['Vel_x'].iloc[0]) + galaxies_population_shuffled['COP_vel_x']
        galaxies_population_shuffled['Vel_y'] = float(halo_nuevo['Vel_y'].iloc[0]) + galaxies_population_shuffled['COP_vel_y']
        galaxies_population_shuffled['Vel_z'] = float(halo_nuevo['Vel_z'].iloc[0]) + galaxies_population_shuffled['COP_vel_z']

        galaxies_population_shuffled['Halo mass bin'] = int(halo_nuevo['Halo mass bin'].iloc[0])
        galaxies_population_shuffled['Halo concentration bin'] = int(halo_nuevo['Halo concentration bin'].iloc[0])
        galaxies_population_shuffled['Halo spin bin'] = int(halo_nuevo['Halo spin bin'].iloc[0])


        # Condiciones periódicas
        galaxies_population_shuffled.loc[galaxies_population_shuffled['Pos_x'] > L, 'Pos_x'] -= L
        galaxies_population_shuffled.loc[galaxies_population_shuffled['Pos_x'] < 0, 'Pos_x'] += L

        galaxies_population_shuffled.loc[galaxies_population_shuffled['Pos_y'] > L, 'Pos_y'] -= L
        galaxies_population_shuffled.loc[galaxies_population_shuffled['Pos_y'] < 0, 'Pos_y'] += L

        galaxies_population_shuffled.loc[galaxies_population_shuffled['Pos_z'] > L, 'Pos_z'] -= L
        galaxies_population_shuffled.loc[galaxies_population_shuffled['Pos_z'] < 0, 'Pos_z'] += L

        galaxies_population_list.append(galaxies_population_shuffled)
        
    galaxies_shuffled=pd.concat(galaxies_population_list)
    return galaxies_shuffled


















def galaxies_shuffling_many(halos, galaxies_sample, features, N_shufflings, L):
    
    """
    Multiple galaxy shufflings.
    Expected execution time: 1 minute for each shuffling.
    
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