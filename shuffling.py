
def halo_shuffling(L, bin_width, seed_number, corte_masa)

    import numpy as np
    import pandas as pd
    import numpy.random as r

    galaxies = pd.read_csv('Resultados/galaxies.csv')
    halos = pd.read_csv('Resultados/halos.csv')

    galaxies_sample = galaxies[galaxies['Stellar mass']>corte_masa]


    bins_masa=np.arange(10.7, 15.2, bin_width)


    seeds = np.arange(0, seed_number)
    lista_DataFrames=[]

    for q in range(len(seeds)):
        seed = seeds[q]
        r.seed(seed)
        galaxies_nuevo = pd.DataFrame(columns=['Host_original', 'Host_new', 'Halo_mass_original', 'Halo_mass_new', 'Stellar mass', 
                                               'Gal_x_new', 'Gal_y_new', 'Gal_z_new', 
                                               'COP_x', 'COP_y', 'COP_z', 
                                               'Mass bin'])
        for bin_masa in range(1, len(bins_masa)):
            galaxies_sample_bin = galaxies_sample[galaxies_sample['Mass bin']==bin_masa].reset_index()
            halos_bin = halos[halos['Mass bin']==bin_masa].reset_index()
            N_gal=len(galaxies_sample_bin)
            N_halo=len(halos_bin)

            indices=r.choice(N_halo, size=N_halo, replace=False)
            indices_gal = np.zeros(N_gal)
            galaxies_nuevo_bin = pd.DataFrame(columns=['Host_original', 'Host_new', 'Halo_mass_original', 'Halo_mass_new', 'Stellar mass', 
                                                   'Gal_x_new', 'Gal_y_new', 'Gal_z_new', 
                                                   'COP_x', 'COP_y', 'COP_z', 
                                                   'Mass bin'])
            k=0
            data = np.zeros([1, len(galaxies_nuevo.columns)])
            for i in range(N_gal):
                galaxy_to_shuffle = galaxies_sample_bin.iloc[[i]]
                ID1=int(galaxy_to_shuffle['HostID'])

                if i != N_gal-1:
                    next_galaxy_to_shuffle = galaxies_sample_bin.iloc[[i+1]]
                    ID2=int(next_galaxy_to_shuffle['HostID'])



                if ID1 == ID2 and i!= N_gal-1:
                    indices_gal[i] = indices[k]
                    indices_gal[i+1] = indices[k]
                elif ID1 == ID2 and i== N_gal-1:
                    indices_gal[i] = indices[k]
                else:
                    indices_gal[i] = indices[k]


                halo_nuevo = halos_bin.iloc[[indices[k]]]
                data[0, 0] = galaxy_to_shuffle['HostID']
                data[0, 1] = halo_nuevo['HaloID']
                data[0, 2] = galaxy_to_shuffle['Halo mass']
                data[0, 3] = halo_nuevo['Halo mass']
                data[0, 4] = galaxy_to_shuffle['Stellar mass']
                data[0, 5] = (halo_nuevo['x'].iloc[0]) + (galaxy_to_shuffle['COP_x'].iloc[0])
                data[0, 6] = (halo_nuevo['y'].iloc[0]) + (galaxy_to_shuffle['COP_y'].iloc[0])
                data[0, 7] = (halo_nuevo['z'].iloc[0]) + (galaxy_to_shuffle['COP_z'].iloc[0])
                data[0, 8] = galaxy_to_shuffle['COP_x']
                data[0, 9] = galaxy_to_shuffle['COP_y']
                data[0, 10] = galaxy_to_shuffle['COP_z']
                data[0, 11] = galaxy_to_shuffle['Mass bin']
                
                # Condiciones periódicas
                # Coord. x
                if data[0, 5] > L:
                    data[0, 5] = data[0, 5] - L
                elif data[0, 5] < 0:
                    data[0, 5] = data[0, 5] + L
                    
                # Coord. y
                if data[0, 6] > L:
                    data[0, 6] = data[0, 6] - L
                elif data[0, 6] < 0:
                    data[0, 6] = data[0, 6] + L
                    
                # Coord. z
                if data[0, 7] > L:
                    data[0, 7] = data[0, 7] - L
                elif data[0, 7] < 0:
                    data[0, 7] = data[0, 7] + L
                    
                
                galaxy_new_row = pd.DataFrame(data=data, columns=['Host_original', 'Host_new', 'Halo_mass_original', 'Halo_mass_new', 'Stellar mass', 
                                                       'Gal_x_new', 'Gal_y_new', 'Gal_z_new', 
                                                       'COP_x', 'COP_y', 'COP_z', 
                                                       'Mass bin'])
                galaxy_new_row['Host_original'] = galaxy_new_row['Host_original'].astype(int)
                galaxy_new_row['Host_new'] = galaxy_new_row['Host_new'].astype(int)
                galaxy_new_row['Mass bin'] = galaxy_new_row['Mass bin'].astype(int)

                galaxies_nuevo_bin=pd.concat([galaxies_nuevo_bin, galaxy_new_row], ignore_index=True)
                if ID1 != ID2:
                    k+=1

            galaxies_nuevo = pd.concat([galaxies_nuevo, galaxies_nuevo_bin], ignore_index=True)
            
        lista_DataFrames.append(galaxies_nuevo)
    return lista_DataFrames