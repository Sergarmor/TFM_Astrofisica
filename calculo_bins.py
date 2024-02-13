

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

 
    bin_feature = 'Halo mass'
    halos_max = halos.loc[:, bin_feature].max()*1.004 # Se extienden los límites en un 0.4% para incluir los elementos límite
    halos_min = halos.loc[:, bin_feature].min()*0.996

    bin_width = (halos_max - halos_min)/(bin_number)


    bins = np.arange(halos_min, halos_max, bin_width)
    halos[bin_feature+' bin'] = pd.cut(halos[bin_feature], bins, labels=False)
    galaxies[bin_feature+' bin'] = pd.cut(galaxies[bin_feature], bins, labels=False)

    bin_feature = 'Halo concentration'
    halos_max = halos.loc[:, bin_feature].max()*1.01  # Se extienden los límites en un 1.0% para incluir los elementos límite
    halos_min = halos.loc[:, bin_feature].min()*0.99

    bin_width = (halos_max - halos_min)/(bin_number)


    bins = np.arange(halos_min, halos_max, bin_width)
    halos[bin_feature+' bin'] = pd.cut(halos[bin_feature], bins, labels=False)
    galaxies[bin_feature+' bin'] = pd.cut(galaxies[bin_feature], bins, labels=False)

    bin_feature = 'Halo spin'
    halos_max = halos.loc[:, bin_feature].max()*1.02  # Se extienden los límites en un 2.0% para incluir los elementos límite
    halos_min = halos.loc[:, bin_feature].min()*0.98

    bin_width = (halos_max - halos_min)/(bin_number)


    bins = np.arange(halos_min, halos_max, bin_width)
    halos[bin_feature+' bin'] = pd.cut(halos[bin_feature], bins, labels=False)
    galaxies[bin_feature+' bin'] = pd.cut(galaxies[bin_feature], bins, labels=False)



    galaxies.to_csv('Resultados/galaxies.csv', index=False)

    halos.to_csv('Resultados/halos.csv', index=False)
    
    return galaxies, halos