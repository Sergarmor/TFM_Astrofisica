def galaxies_shuffle_optimized(halos, galaxies_sample, bin_feature, sub_bin_feature, L):
    
    """
    Función que realiza el shuffling de las galaxias. Los bins se definen según la masa. 
    Toma como  input el DataFrame de galaxias a las que aplicar el shuffling, el número de bins y la  a utilizar.
    Devuelve un DataFrame con las galaxias después de aplicar el shuffling.
    
    Tiempo estimado de ejecución: 30 sec
    """
    
    import numpy as np
    import numpy.random as r
    import pandas as pd

    # Inicializamos la lista de dataframes
    galaxies_poblacion_list=[]

    place_holder, indices_halos = np.unique(galaxies_sample['HostID'], return_index=True)

    for i in range(len(indices_halos)): 

        # Tomamos una población. Comprobar que da lo mismo que np.argwhere
        if i == len(indices_halos):
            galaxies_poblacion = galaxies_sample.iloc[indices_halos[i]:].copy()
        else:
            galaxies_poblacion = galaxies_sample.iloc[indices_halos[i]:indices_halos[i+1]].copy()

        if len(galaxies_poblacion) == 0:
            raise IndexError("This population has no galaxies. This shouldn't happen. Population number ", i)
            continue

        bin1 = galaxies_poblacion[bin_feature+' bin'].iloc[0]
        bin2 = galaxies_poblacion[sub_bin_feature+' bin'].iloc[0]
        
        halos_bin = halos.loc[halos[bin_feature+' bin']==bin1].loc[halos[sub_bin_feature+' bin']==bin2]
        
        halos_permutated = halos_bin.sample(frac=1).copy() # Genera una permutación del dataframe. frac=1 da la fracción de filas del dataframe a devolver.
        
        
        # # Permutación de los halos dentro del bin y elegir los halos de uno en adelante para el shuffle
        galaxies_poblacion_nuevo = pd.DataFrame(data=np.zeros(galaxies_poblacion.shape), columns=galaxies_poblacion.columns)
        
        ## Editamos la información de la población
        # Datos del nuevo halo
        galaxies_poblacion_nuevo['New HostID'] = ID_halo_nuevo
        galaxies_poblacion['Halo mass'] = float(halos.loc[halos['HaloID'] == ID_halo_nuevo, 'Halo mass'].iloc[0])

        # Coords. del nuevo halo
        galaxies_poblacion['Halo_x'] = float(halos.loc[halos['HaloID'] == ID_halo_nuevo, 'x'].iloc[0])
        galaxies_poblacion['Halo_y'] = float(halos.loc[halos['HaloID'] == ID_halo_nuevo, 'y'].iloc[0])
        galaxies_poblacion['Halo_z'] = float(halos.loc[halos['HaloID'] == ID_halo_nuevo, 'z'].iloc[0])
        
        # Coords de las galaxias
        galaxies_poblacion['Gal_x'] = galaxies_poblacion['Halo_x'] + galaxies_poblacion['COP_x']
        galaxies_poblacion['Gal_y'] = galaxies_poblacion['Halo_y'] + galaxies_poblacion['COP_y']
        galaxies_poblacion['Gal_z'] = galaxies_poblacion['Halo_z'] + galaxies_poblacion['COP_z']
        
        # Condiciones periódicas
        galaxies_poblacion.loc[galaxies_poblacion['Gal_x'] > L, 'Gal_x'] -= L
        galaxies_poblacion.loc[galaxies_poblacion['Gal_x'] < 0, 'Gal_x'] += L
        
        galaxies_poblacion.loc[galaxies_poblacion['Gal_y'] > L, 'Gal_y'] -= L
        galaxies_poblacion.loc[galaxies_poblacion['Gal_y'] < 0, 'Gal_y'] += L
        
        galaxies_poblacion.loc[galaxies_poblacion['Gal_z'] > L, 'Gal_z'] -= L
        galaxies_poblacion.loc[galaxies_poblacion['Gal_z'] < 0, 'Gal_z'] += L
        
        galaxies_poblacion_list.append(galaxies_poblacion)
        
    galaxies_nuevo=pd.concat(galaxies_poblacion_list)
    return galaxies_nuevo

def galaxies_shuffling_many(halos, galaxies_sample, bin_feature, sub_bin_feature, N_shufflings, L):
    
    """
    Función que realiza un número determinado de shufflings. Se basa en la función galaxies_shuffle.
    Toma como input el DataFrame de galaxias a las que aplicar el shuffling, el número total de bins y una lista o array de seeds que utilizar.
    Devuelve una lista de DataFrames con galaxias después de aplicar el shuffling. 
    
    Tiempo estimado de ejecución: 30 sec por cada shuffling.
    
    """
    
    import numpy as np
    import numpy.random as r
    import pandas as pd

    galaxies_list=[]

    for i in range(N_shufflings):
        print(f'Shuffle number {i} out of {N_shufflings}')
        galaxies_nuevo = galaxies_shuffle_optimized(halos, galaxies_sample, bin_feature, sub_bin_feature, L)
        galaxies_list.append(galaxies_nuevo)
        galaxies_nuevo.to_csv(f'Resultados/Shuffled/Galaxies/galaxies_shuffled{i}.csv', index=False)
    return galaxies_list