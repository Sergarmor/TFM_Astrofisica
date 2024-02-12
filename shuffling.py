def galaxies_shuffle_optimized(halos, galaxies_sample, features, L):
    
    """
    Galaxy shuffling. Permutates the halos to select them for each population.
    Expected execution time: 
    
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

        
    halos_permutated = halos.groupby(by=features_bins, axis=0, sort=True).sample(frac=1).copy() # Genera una permutación del dataframe. frac=1 da la fracción de filas del dataframe a devolver.

    ID_halos, index_halos = np.unique(galaxies_sample['HostID'], return_index=True)
    galaxies_population_list=[]
    bins_old = np.zeros([len(features_bins), ])
    k=0

    for i in range(len(index_halos)):
    
        galaxies_population = galaxies_sample.loc[galaxies_sample['HostID'] == ID_halos[i]]

        bins = galaxies_population.loc[:, features_bins].iloc[0]
        halos_bins = halos_permutated
        for p in range(len(bins)):
            halos_bins = halos_bins.loc[halos_bins.loc[:, features_bins[p]] == bins[p]]

        len_halos_bin = len(halos_bins)

        if (bins_old != bins).any():
            k=0
            bins_old = bins
        else:
            k+=1

        if len_halos_bin <= k:
            raise ValuError("Length of halos in bin too short")

        halo_nuevo = halos_bins.iloc[k]
        galaxies_population_shuffled = galaxies_population.copy()

        galaxies_population_shuffled['HostID'] = int(halo_nuevo['HaloID'])
        galaxies_population_shuffled['Host index'] = int(halos[halos['HaloID'] == halo_nuevo['HaloID']].index[0])

        galaxies_population_shuffled['Halo mass'] = float(halo_nuevo['Halo mass'])
        galaxies_population_shuffled['Halo concentration'] = float(halo_nuevo['Halo concentration'])
        galaxies_population_shuffled['Halo spin'] = float(halo_nuevo['Halo spin'])

        galaxies_population_shuffled['Halo_x'] = float(halo_nuevo['x'])
        galaxies_population_shuffled['Halo_y'] = float(halo_nuevo['y'])
        galaxies_population_shuffled['Halo_z'] = float(halo_nuevo['z'])

        galaxies_population_shuffled['Halo_vel_x'] = float(halo_nuevo['Vel_x'])
        galaxies_population_shuffled['Halo_vel_y'] = float(halo_nuevo['Vel_y'])
        galaxies_population_shuffled['Halo_vel_z'] = float(halo_nuevo['Vel_z'])

        galaxies_population_shuffled['Pos_x'] = float(halo_nuevo['x']) + galaxies_population_shuffled['COP_x']
        galaxies_population_shuffled['Pos_y'] = float(halo_nuevo['y']) + galaxies_population_shuffled['COP_y']
        galaxies_population_shuffled['Pos_z'] = float(halo_nuevo['z']) + galaxies_population_shuffled['COP_z']

        galaxies_population_shuffled['Vel_x'] = float(halo_nuevo['Vel_x']) + galaxies_population_shuffled['COP_vel_x']
        galaxies_population_shuffled['Vel_y'] = float(halo_nuevo['Vel_y']) + galaxies_population_shuffled['COP_vel_y']
        galaxies_population_shuffled['Vel_z'] = float(halo_nuevo['Vel_z']) + galaxies_population_shuffled['COP_vel_z']

        galaxies_population_shuffled['Halo mass bin'] = int(halo_nuevo['Halo mass bin'])
        galaxies_population_shuffled['Halo concentration bin'] = int(halo_nuevo['Halo concentration bin'])
        galaxies_population_shuffled['Halo spin bin'] = int(halo_nuevo['Halo spin bin'])


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
    Expected execution time: e for each shuffling.
    
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
        print(f'Shuffle number {i} out of {N_shufflings}')
        galaxies_shuffled = galaxies_shuffle_optimized(halos, galaxies_sample, features, L)
        galaxies_list.append(galaxies_shuffled)
        galaxies_shuffled.to_csv(f'Resultados/Shuffled/Galaxies/galaxies_shuffled{i}.csv', index=False)
    return galaxies_list