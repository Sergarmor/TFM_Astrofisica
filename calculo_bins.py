

def calculo_bins(halos, galaxies, features, bin_number):

    """
    Galaxy and halo DataFrame binning.
    
    Parameters
    ----------
    
    features : list
               List of labels for the binning
    bin_number : list
               Number of bins for each feature. Must have same length as features.
               
    Returns
    -------
    
    halos : DataFrame
            DataFrame of binned halos
    galaxies : DataFrame
            DataFrame of binned galaxies
    
    """

    import numpy as np
    import pandas as pd

    if len(bin_number) != len(features):
    raise IndexError('Feature and bin number must have the same length. Currently features:', 
                     len(features), 'and bins:', len(bin_number))
    #

    halos_max = halos.loc[:, features].max() + halos_max[i]*0.01
    halos_min = halos.loc[:, features].min() - halos_min[i]*0.01

    bin_width = (halos.loc[:, features].max() - halos.loc[:, features].min())/bin_number

    for i in range(len(features)):
        bin_feature = features[i]
        bins = np.arange(halos_min[i], halos_max[i], bin_width[i])
        halos[bin_feature+' bin'] = pd.cut(halos[bin_feature], bins, labels=False)
        galaxies[bin_feature+' bin'] = pd.cut(galaxies[bin_feature], bins, labels=False)



    galaxies.to_csv('Resultados/galaxies.csv', index=False)

    halos.to_csv('Resultados/halos.csv', index=False)
    
    return galaxies, halos