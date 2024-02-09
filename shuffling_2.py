        bin1 = galaxies_poblacion[bin_feature+' bin'].iloc[0]
        bin2 = galaxies_poblacion[sub_bin_feature+' bin'].iloc[0]
        
        halos_bin = halos.loc[halos[bin_feature+' bin']==bin1].loc[halos[sub_bin_feature+' bin']==bin2]
        
        halos_permutated = halos_bin.sample(frac=1).copy() # Genera una permutación del dataframe
        
        
        ID_halo_nuevo = r.choice(halos.loc[halos[bin_feature+' bin']==bin1].loc[halos[sub_bin_feature+' bin']==bin2, 'HaloID'], size=1, replace=False)[0]
        
        # # Permutación de los halos dentro del bin y elegir los halos de uno en adelante para el shuffle
        galaxies_poblacion_nuevo = pd.DataFrame(data=np.zeros(galaxies_poblacion.shape), columns=galaxies_poblacion.columns)