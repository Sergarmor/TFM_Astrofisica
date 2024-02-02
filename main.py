import numpy as np
import numpy.random as r
import pandas as pd
from Corrfunc.theory import xi

# Importing custom functions
from calculo_bins import calculo_bins
from shuffling import galaxies_shuffle_bin, galaxies_shuffle, galaxies_shuffling_many
from ploting_script import ploting_2pcf_ratio
from calculo_2pcf import calculo_2pcf


# Simulation parameters
L = 205                                      # Side length of simulation box
h = 0.6774                                   # Little Hubble constant

# Analisys parameters
corte_masa = 10.75                           # We cut the galaxies by mass into a sample
bin_feature = 'Halo mass'                    # Main feature for the binning
sub_bin_feature = 'Halo mass squared'        # Sub feature for the binning
bin_width=0.1                                # Bin width in main feature
sub_bin_width=0.1                            # Bin width in sub feature
seed_number = 25                             # We shuffle seed_number times and compute the mean and std
spatial_bin_number = 100                     # Bin number in spatial bins (2PCF calculation)
n_threads = 1                                # Number of threads to use to calculate the 2PCF

# Plotting parameters
n = 3                                        # Number of sigmas in the plot


print(f'The script is estimated to run for {np.floor(seed_number*2/60)} hours and {(seed_number*2 - np.floor(seed_number*2/60)*60)} minutes')
confirmation = input('Do you want to continue? [yes/no]: ')
conf = 0
while conf == 0:
    if confirmation == 'yes':
        conf = 1
    elif confirmation == 'no':
        seed_number = int(input(f'Please set a new number of shufflings to calculate. Currently {seed_number}: '))
        print(f'The script is estimated to run for {np.floor(seed_number*2/60)} hours and {(seed_number*2 - np.floor(seed_number*2/60)*60)} minutes')
        confirmation = input('Do you want to continue? [yes/no]: ')
    elif confirmation != 'yes' and confirmation != 'no':
        print(" Please write 'yes' or 'no' ")
        confirmation = input('Do you want to continue? [yes/no]: ')


recalc = input('Do you want to recalculate the DataFrames? [yes/no]: ')

if recalc == 'yes':
    # Calculation of original data
    import calculo_dataframe

# We read the data
halos = pd.read_csv('Resultados/halos.csv')
galaxies = pd.read_csv('Resultados/galaxies.csv')

# Calculation of binned dataframes of halos and galaxies
halos, galaxies, main_bins, sub_bins = calculo_bins(halos, galaxies, bin_feature, sub_bin_feature, bin_width, sub_bin_width)

N_bins_feature = len(main_bins)
N_bins_sub_feature = len(sub_bins)
seed=np.arange(0, seed_number, 1)



# We get the sample by cutting in stellar mass
galaxies_sample = galaxies[galaxies['Stellar mass']>corte_masa]

# Calculate the original 2PCF

pcf_original = calculo_2pcf(galaxies_sample, L, spatial_bin_number, n_threads)

pcf_original.to_csv('Resultados/pcf_original.csv', index=False) # We save the original 2PCF


# Calculate the 2PCF shuffled
lista_DataFrames = galaxies_shuffling_many(halos, galaxies_sample, bin_feature, sub_bin_feature, N_bins_feature, N_bins_sub_feature, seed, L) # We shuffle the galaxies into haloes of same mass bin
lista_xis = []
for q in range(len(lista_DataFrames)):
    # We extract one DataFrame of shuffled galaxies
    galaxies_shuffled = lista_DataFrames[q] 
    
    # We extract the 2PCF value of the shuffled galaxies (one iteration) and save it to use later
    pcf_shuffled = calculo_2pcf(galaxies_shuffled, L, spatial_bin_number, n_threads)
    
    pcf_shuffled.to_csv(f'Resultados/Shuffled/PCF/pcf_shuffled{q}.csv', index=False) # We save the shuffled 2pcf
    
    
    pcf_shuffled_xi = pcf_shuffled['xi']
    lista_xis.append(pcf_shuffled_xi)
    print(q)

# We unite all the shuffled 2PCF and compute the mean and std
pcf_shuffled_xi = pd.concat(lista_xis, axis=1)

pcf_shuffled_xi = pcf_shuffled_xi.assign(mean=pcf_shuffled_xi.mean(axis=1))
pcf_shuffled_xi = pcf_shuffled_xi.assign(std=pcf_shuffled_xi.std(axis=1))
pcf_shuffled_xi = pcf_shuffled_xi.loc[:, ['mean', 'std']] # We discard all the 2PCFs and maintain the mean and std. Then we save it
pcf_shuffled_xi.to_csv('Resultados/pcf_shuffled_mean.csv', index=False)


b = pcf_original['xi'] / pcf_shuffled_xi['mean'] # Assembly bias
sigma = pcf_original['xi']/pcf_shuffled_xi['mean'] * pcf_shuffled_xi['std'] # Assembly bias uncertainty


# We plot the results

ploting_2pcf_ratio(pcf_original, pcf_shuffled, n, L, bin_feature, sub_bin_feature)