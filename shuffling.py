

# Función que hace el shuffling de cada bin. Este bin puede estar definido de cualquier manera (en función de un parámetro arbitrario, o varios).
# Toma como input el DataFrame de galaxias del bin y las id de los halos dentro de ese bin.
# Devuelve una LISTA de DataFrames, donde cada DataFrame es una población con el mismo halo original.
def galaxies_shuffle_bin(galaxies_bin, id_halos):
    
    # Inicializamos la lista de dataframes
    galaxies_list=[]
    
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

        galaxies_list.append(galaxies_poblacion)
        
    return galaxies_list
    

# Función que realiza el shuffling de las galaxias. Los bins se definen según la masa. 
# Toma como  input el DataFrame de galaxias a las que aplicar el shuffling, el número de bins y la seed a utilizar.
# Devuelve un DataFrame con las galaxias después de aplicar el shuffling.
def galaxies_shuffle(galaxies_sample, N_bins, seed):

    r.seed(seed)
    galaxies_bin_list=[]

    # Bucle por cada bin
    for i in range(1, N_bins):

        # Tomamos un bin
        galaxies_bin = galaxies_sample[galaxies_sample['Mass bin'] == i]
        id_halos = list(halos.loc[halos['Mass bin']==i, 'HaloID'])

        galaxies_bin_list+=galaxies_shuffle_bin(galaxies_bin, id_halos)

    galaxies_nuevo=pd.concat(galaxies_bin_list)
    return galaxies_nuevo
    
