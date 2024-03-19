import numpy as np
import pandas as pd
from Corrfunc.theory import xi

# Simulation parameters
L = 205                                      # Side length of simulation box
h = 0.6774                                   # Little Hubble constant

spatial_bin_number = 25                      # Bin number in spatial bins (2PCF calculation)
n_threads = 1                                # Number of threads to use to calculate the 2PCF

# We read the data
halos = pd.read_csv('Resultados/halos.csv')

# Coordenadas de las galaxias
X = halos['x']
Y = halos['y']
Z = halos['z']

# Parámetros del cálculo de la 2PCF
weights = np.ones_like(X)
limit_spatial_bins = np.log10(25)
spatial_bins = np.logspace(np.log10(0.1), limit_spatial_bins, spatial_bin_number+1)

# Cálculo de la 2PCF
halo_pcf = xi(L, n_threads, spatial_bins, X, Y, Z, weights = weights)
halo_pcf = pd.DataFrame(halo_pcf, columns=['rmin', 'rmax', 'ravg', 'xi', 'npairs', 'weightavg'])

halo_pcf['ravg'] = (halo_pcf['rmax'] + halo_pcf['rmin'])/2

halo_pcf.to_csv('Resultados/halo_pcf.csv', index=False) # We save the original 2PCF
