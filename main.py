import numpy as np
import numpy.random as r
import pandas as pd
from datetime import datetime
from Corrfunc.theory import xi

# Importing custom functions
from calculo_bins import calculo_bins
from shuffling import galaxies_shuffle_optimized, galaxies_shuffling_many
from ploting_script import ploting_2pcf_ratio
from calculo_2pcf import calculo_2pcf


# Simulation parameters
L = 205                                      # Side length of simulation box
h = 0.6774                                   # Little Hubble constant

# Analisys parameters
corte_masa = 10.75                           # We cut the galaxies by mass into a sample

# Features used to do the binning and shuffle the galaxies
features=['Halo mass', 'Halo concentration']

bin_number=100            # Number of bins for each feature
N_shufflings = 25                            # We shuffle N_shufflings times and compute the mean and std
spatial_bin_number = 100                     # Bin number in spatial bins (2PCF calculation)
n_threads = 1                                # Number of threads to use to calculate the 2PCF
# Definir bin_width con max y min de los datos. Normalizar con los percentiles 95 y 5. Input: número de bines
# Plotting parameters
n = 3                                        # Number of sigmas in the plot

    
t = 46 # Execution time per shuffling in seconds

h=np.floor(N_shufflings*t/3600) # Number of hours
m=np.floor((N_shufflings*t/3600 - np.floor(N_shufflings*t/3600))*60) # Number of minutes
s=round(((N_shufflings*t/3600 - np.floor(N_shufflings*t/3600))*60 - np.floor((N_shufflings*t/3600 - np.floor(N_shufflings*t/3600))*60)) * 60) # Number of seconds

print(f'The shuffling script is estimated to run for {h} hours, {m} minutes and {s} seconds.')
confirmation = input('Do you want to continue? [yes/no]: ')
conf = 0
while conf == 0:
    if confirmation == 'yes':
        conf = 1
    elif confirmation == 'no':
        N_shufflings = int(input(f'Please set a new number of shufflings to calculate. Currently {N_shufflings}: '))
        
        h=np.floor(N_shufflings*t/3600) # Number of hours
        m=np.floor((N_shufflings*t/3600 - np.floor(N_shufflings*t/3600))*60) # Number of minutes
        s=((N_shufflings*t/3600 - np.floor(N_shufflings*t/3600))*60 - np.floor((N_shufflings*t/3600 - np.floor(N_shufflings*t/3600))*60)) * 60 # Number of seconds
        
        print(f'The shuffling script is estimated to run for {h} hours, {m} minutes and {s} seconds.')
        confirmation = input('Do you want to continue? [yes/no]: ')
        
    elif confirmation != 'yes' and confirmation != 'no':
        print(" Please write 'yes' or 'no' ")
        confirmation = input('Do you want to continue? [yes/no]: ')


recalc = input('Do you want to recalculate the DataFrames? [yes/no]: ')

if recalc == 'yes':
    # Calculation of original data
    import calculo_dataframe
    
timeit = input('Do you want to time the shuffling time? [yes/no]: ')



# We read the data
halos = pd.read_csv('Resultados/halos.csv')
galaxies = pd.read_csv('Resultados/galaxies.csv')

# Calculation of binned dataframes of halos and galaxies
rebin = input('Do you want to recalculate the binning of the DataFrames? [yes/no]: ')

if rebin == 'yes':
    halos, galaxies = calculo_bins(halos, galaxies, bin_number)
else:
    pass
    
# We get the sample by cutting in stellar mass
galaxies_sample = galaxies[galaxies.loc[:, 'Stellar mass'] > corte_masa].copy()

# Calculate the original 2PCF

pcf_original = calculo_2pcf(galaxies_sample, L, spatial_bin_number, n_threads)

pcf_original.to_csv('Resultados/pcf_original.csv', index=False) # We save the original 2PCF


# Calculate the 2PCF shuffled
if timeit == 'yes':
    N_shufflings = 1
    time_ini = datetime.now()
    lista_DataFrames = galaxies_shuffling_many(halos, galaxies_sample, features, N_shufflings, L)
    
    time_end = datetime.now()
    print(f"Initial time...: {time_ini}")
    print(f"Final time.....: {time_end}")
    print(f"Excecution time: {time_end-time_ini}")
    
else:
    lista_DataFrames = galaxies_shuffling_many(halos, galaxies_sample, features, N_shufflings, L)
    
lista_xis = []
for q in range(len(lista_DataFrames)):
    # We extract one DataFrame of shuffled galaxies
    galaxies_shuffled = lista_DataFrames[q] 
    
    # We extract the 2PCF value of the shuffled galaxies (one iteration) and save it to use later
    pcf_shuffled = calculo_2pcf(galaxies_shuffled, L, spatial_bin_number, n_threads)
    
    pcf_shuffled.to_csv(f'Resultados/Shuffled/PCF/pcf_shuffled{q}.csv', index=False) # We save the shuffled 2pcf
    
    
    pcf_shuffled_xi = pcf_shuffled['xi']
    lista_xis.append(pcf_shuffled_xi)

# We unite all the shuffled 2PCF and compute the mean and std
pcf_shuffled_xi = pd.concat(lista_xis, axis=1)

pcf_shuffled_xi = pcf_shuffled_xi.assign(mean=pcf_shuffled_xi.mean(axis=1))
pcf_shuffled_xi = pcf_shuffled_xi.assign(std=pcf_shuffled_xi.std(axis=1))
pcf_shuffled_xi = pcf_shuffled_xi.loc[:, ['mean', 'std']] # We discard all the 2PCFs and maintain the mean and std. Then we save it
pcf_shuffled_xi.to_csv('Resultados/pcf_shuffled_mean.csv', index=False)


b = pcf_original['xi'] / pcf_shuffled_xi['mean'] # Assembly bias
sigma = pcf_original['xi']/pcf_shuffled_xi['mean'] * pcf_shuffled_xi['std'] # Assembly bias uncertainty


# We plot the results

ploting_2pcf_ratio(pcf_original, pcf_shuffled_xi, n, L, features, N_shufflings)