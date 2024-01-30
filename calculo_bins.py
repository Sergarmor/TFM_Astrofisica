import numpy as np
import pandas as pd
import math

halos=pd.read_csv('Resultados/halos.csv')
galaxies=pd.read_csv('Resultados/galaxies.csv')

bin_feature = 'Halo mass'
sub_bin_feature = 'Halo mass squared'

bin_width=0.1
sub_bin_width=0.1

limite_inferior_main_bin = math.floor(min(galaxies[bin_feature]) * 10.0) / 10.0
limite_superior_main_bin = math.ceil(max(galaxies[bin_feature]) * 10.0) / 10.0+bin_width

limite_inferior_sub_bin = math.floor(min(galaxies[sub_bin_feature]) * 10.0) / 10.0
limite_superior_sub_bin = math.ceil(max(galaxies[sub_bin_feature]) * 10.0) / 10.0+sub_bin_width

main_bins = np.arange(limite_inferior_main_bin, limite_superior_main_bin, bin_width)
sub_bins = np.arange(limite_inferior_sub_bin, limite_superior_sub_bin, sub_bin_width)

bin_labels=np.arange(1, len(main_bins), 1)
sub_bin_labels=np.arange(1, len(sub_bins), 1)

galaxies[bin_feature+' bin'] = pd.cut(galaxies[bin_feature], main_bins, labels=bin_labels)
galaxies[sub_bin_feature+' bin'] = pd.cut(galaxies[sub_bin_feature], sub_bins, labels=sub_bin_labels)

halos[bin_feature+' bin'] = pd.cut(halos[bin_feature], main_bins, labels=bin_labels)
halos[sub_bin_feature+' bin'] = pd.cut(halos[sub_bin_feature], sub_bins, labels=sub_bin_labels)



galaxies.to_csv('Resultados/galaxies.csv', index=False)

halos.to_csv('Resultados/halos.csv', index=False)