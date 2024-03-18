def calculo_2pcf(galaxies, L, bin_number, n_threads):

    """
    Función que calcula la 2PCF a partir de un set de galaxias.
    
    Parameters
    ----------
    galaxies : DataFrame
              Galaxias. Debe contener las columnas 'Pos_x/y/z'.
    L : float
        Anchura de caja.
    bin_number : int
                 Número de bins espaciales.
    n_threads : int
                Número de threads a usar en el cálculo de la 2PCF.
                
    Returns
    -------
    pcf : DataFrame
          DataFrame conteniendo la información de la 2PCF frente a escala
    """
    
    import numpy as np
    import pandas as pd
    from Corrfunc.theory import xi
    
    # Coordenadas de las galaxias
    X = galaxies['Pos_x']
    Y = galaxies['Pos_y']
    Z = galaxies['Pos_z']
    
    # Parámetros del cálculo de la 2PCF
    weights = np.ones_like(X)
    limit_spatial_bins = np.log10(25)
    spatial_bins = np.logspace(np.log10(0.1), limit_spatial_bins, bin_number+1)

    # Cálculo de la 2PCF
    pcf = xi(L, n_threads, spatial_bins, X, Y, Z, weights = weights)
    pcf = pd.DataFrame(pcf, columns=['rmin', 'rmax', 'ravg', 'xi', 'npairs', 'weightavg'])
    
    pcf['ravg'] = (pcf['rmax'] + pcf['rmin'])/2
    
    return pcf