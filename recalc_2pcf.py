
import numpy as np
import pandas as pd

L=205
N_shufflings=100
spatial_bin_number=50
n_threads=1

galaxies_list=[]

for i in range(N_shufflings):
    # print(f'Shuffle number {i+1} out of {N_shufflings}')
    galaxies_temp = pd.read_csv(f'Resultados/Shuffled/Galaxies/galaxies_shuffled{i}.csv')
    galaxies_list.append(galaxies_temp)

lista_xis = []
for q in range(len(galaxies_list)):
    # We extract one DataFrame of shuffled galaxies
    galaxies_shuffled = galaxies_list[q] 
    
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