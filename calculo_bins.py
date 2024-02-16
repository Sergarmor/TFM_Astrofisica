

def calculo_bins(halos, galaxies, bin_number):

    """
    Galaxy and halo DataFrame binning.
    
    Parameters
    ----------
    
    features : list
               List of labels for the binning
    bin_number : list
               Number of bins for each feature. Must have same length as features.
               
    halos : DataFrame
            DataFrame of halos without binning
    galaxies : DataFrame
            DataFrame of galaxies without binning
               
    Returns
    -------
    
    halos : DataFrame
            DataFrame of binned halos
    galaxies : DataFrame
            DataFrame of binned galaxies
    
    """

    import numpy as np
    import pandas as pd

    features = ['Halo mass', 'Halo concentration', 'Halo spin']
    big_scale_bin_number = 2
    for j in features:
        
        bin_feature = j
        halos_max = halos.loc[:, bin_feature].max()*1.004 # Se extienden los límites en un 0.4% para incluir los elementos límite
        halos_min = halos.loc[:, bin_feature].min()*0.996

        limit = halos.loc[:, bin_feature].max()*0.95 # Se establece un corte para aumentar la anchura de los bins a un 95% del máximo
        
        bins_small = np.linspace(halos_min, limit, bin_number-big_scale_bin_number)
        bins_big = np.linspace(limit, halos_max, big_scale_bin_number+1)[1:]

        bins = np.concatenate((bins_small, bins_big))
    
    
        halos[bin_feature+' bin'] = pd.cut(halos[bin_feature], bins, labels=False)
        galaxies[bin_feature+' bin'] = pd.cut(galaxies[bin_feature], bins, labels=False)



    galaxies.to_csv('Resultados/galaxies.csv', index=False)

    halos.to_csv('Resultados/halos.csv', index=False)
    
    return halos, galaxies