import numpy as np
import numpy.random as r
import pandas as pd
from Corrfunc.theory import xi

def calculo_2pcf(galaxies, L, bin_number, n_threads):
    X = galaxies['Gal_x']
    Y = galaxies['Gal_y']
    Z = galaxies['Gal_z']
    weights = np.ones_like(X)
    limit_spatial_bins = np.log10(L/2-0.1)
    spatial_bins = np.logspace(np.log10(0.1), limit_spatial_bins, bin_number+1)

    pcf = xi(L, n_threads, spatial_bins, X, Y, Z, weights = weights)
    pcf = pd.DataFrame(pcf, columns=['rmin', 'rmax', 'ravg', 'xi', 'npairs', 'weightavg'])
    
    pcf['ravg'] = (pcf['rmax'] + pcf['rmin'])/2
    
    return pcf