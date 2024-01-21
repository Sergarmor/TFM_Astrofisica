import numpy as np
import pandas as pd

galaxies=pd.read_csv('Resultados/galaxies.csv')

m=galaxies['Halo mass']
bin_col=np.ones(len(m), dtype=int)
for j in range(10):
    for i in range(len(bins_masa)):
        if m[j] > bins_masa[i] and m[j] < bins_masa[i+1]:
            bin_col[j]=int(i+1)
            
            break
        else:
            continue
galaxies['Mass bin'] = bin_col
galaxies.to_csv('Resultados/galaxies.csv', index=False)