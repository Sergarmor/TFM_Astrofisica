def galaxies_shuffle_bin(halos, galaxies_bin, id_halos):

    """
    Función que hace el shuffling de cada bin. Este bin puede estar definido de cualquier manera (en función de un parámetro arbitrario, o varios).

    Parameters
    ----------
    
    galaxies_bin : DataFrame
                   DataFrame con las galaxias dentro del bin.
    id_halos : List
                   Lista con las ID de los halos dentro del bin.
    
    Returns
    -------
    galaxies_poblacion_list : List
                   Lista con DataFrames de las distintas poblaciones dentro del bin.
    """
    
    import numpy as np
    import numpy.random as r
    import pandas as pd
    
    # Inicializamos la lista de dataframes
    galaxies_poblacion_list=[]
    
    # Obtenemos índices y valores de los HostID únicos del bin
    place_holder, indices_halos = np.unique(galaxies_bin['HostID'], return_index=True)

    # Bucle en poblaciones
    for i in range(1, len(indices_halos)+1): 

        # Tomamos una población dentro del bin
        if i == len(indices_halos):
            galaxies_poblacion = galaxies_bin.iloc[indices_halos[i-1]:].copy()
        else:
            galaxies_poblacion = galaxies_bin.iloc[indices_halos[i-1]:indices_halos[i]].copy()

        if len(galaxies_poblacion) == 0:
            continue

        # Excluimos el halo viejo de las opciones para el shuffling
        ID_halo_viejo = galaxies_poblacion.iloc[0]['HostID']
        ID_halo_nuevo = r.choice(id_halos, size=1)

        # Seleccionamos el halo elegido aleatoriamente para la población
        halo_nuevo = halos[halos['HaloID']==int(ID_halo_nuevo[0])]

        ## Editamos la información de la población
        # Datos del nuevo halo
        galaxies_poblacion['Halo new ID'] = int(halo_nuevo['HaloID'].iloc[0])
        galaxies_poblacion['Halo mass'] = float(halo_nuevo['Halo mass'].iloc[0])

        # Coords. del nuevo halo
        galaxies_poblacion['Halo_x'] = float(halo_nuevo['x'].iloc[0])
        galaxies_poblacion['Halo_y'] = float(halo_nuevo['y'].iloc[0])
        galaxies_poblacion['Halo_z'] = float(halo_nuevo['z'].iloc[0])

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
        
    return galaxies_poblacion_list

def galaxies_shuffle(halos, galaxies_sample, bin_feature, sub_bin_feature, N_bins_feature, N_bins_sub_feature, seed):
    
    """
    Función que realiza el shuffling de las galaxias. Los bins se definen según la masa. 
    Toma como  input el DataFrame de galaxias a las que aplicar el shuffling, el número de bins y la seed a utilizar.
    Devuelve un DataFrame con las galaxias después de aplicar el shuffling.
    
    Tiempo estimado de ejecución: 1 minuto
    """
    
    import numpy as np
    import numpy.random as r
    import pandas as pd
    
    r.seed(seed)
    galaxies_bin_list=[]

    for i in range(1, N_bins_feature):
        for j in range(1, N_bins_sub_feature):

            # Tomamos un bin
            galaxies_bin = galaxies_sample.loc[galaxies_sample[bin_feature+' bin']==i].loc[galaxies_sample[sub_bin_feature+' bin']==j]
            id_halos = list(halos.loc[halos[bin_feature+' bin']==i].loc[halos[sub_bin_feature+' bin']==j, 'HaloID'])

            galaxies_bin_list+=galaxies_shuffle_bin(halos, galaxies_bin, id_halos)

    galaxies_nuevo=pd.concat(galaxies_bin_list)
    return galaxies_nuevo

def galaxies_shuffling_many(halos, galaxies_sample, bin_feature, sub_bin_feature, N_bins_feature, N_bins_sub_feature, seed):
    
    """
    Función que realiza un número determinado de shufflings. Se basa en la función galaxies_shuffle.
    Toma como input el DataFrame de galaxias a las que aplicar el shuffling, el número total de bins y una lista o array de seeds que utilizar.
    Devuelve una lista de DataFrames con galaxias después de aplicar el shuffling. 
    
    Tiempo estimado de ejecución: 1 minuto por cada seed.
    
    """
    
    import numpy as np
    import numpy.random as r
    import pandas as pd

    galaxies_list=[]

    for i in range(len(seed)):
        print(f'Shuffle number {i} out of {len(seed)}')
        galaxies_nuevo = galaxies_shuffle(halos, galaxies_sample, bin_feature, sub_bin_feature, N_bins_feature, N_bins_sub_feature, seed[i])
        galaxies_list.append(galaxies_nuevo)

    return galaxies_list