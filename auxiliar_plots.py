import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from corner import corner
import seaborn as sns
import scienceplots

plt.style.use('science')
plt.rcParams.update({
    "font.family": "lmodern",   # specify font family here
    # "font.serif": ["Times"],  # specify font here
    "font.size":11})          # specify font size here




# Stellar mass bins histogram
path = 'Auxiliar_plots/'
# path_resultados = 'Resultados/' + path
path_figuras = 'Figuras/' + path

galaxies = pd.read_csv('Resultados/galaxies.csv')
galaxies_sample = galaxies[galaxies.loc[:, 'Stellar mass'] > 10.5].copy()
galaxies_sample = galaxies_sample[galaxies_sample.loc[:, 'Stellar mass'] < 10.75].copy()

mass_bins=[10.5, 10.75, 13.0]
counts_2, bins_2 = np.histogram(galaxies_sample['Stellar mass'], bins=mass_bins)


ploted_bins = np.array([10.5, 10.75, 13.0])
bins, bin_width=np.linspace(10.5, 13.0, retstep=True)
bin_width = bin_width/2

fig, ax = plt.subplots(1, 1, figsize=(6, 5))
counts, bins = np.histogram(galaxies['Stellar mass'], bins=bins)
ax.hist(bins[0:-1]+bin_width, bins=bins, weights=(counts/bin_width), edgecolor='black')
for i in range(len(ploted_bins)):
    ax.vlines(ploted_bins[i], 0, 1e6, linestyle='--', color='C3')

ax.set_yscale('log')
ax.set_ylim([0.5, 2e5])
ax.set_xlabel(r'log(M$_{\ast}$ [M$_{\odot}$/h])')
ax.set_ylabel(r'\# Galaxies/dex')
ax.text(11.2, 0.7e5, f'Most massive bin: {counts_2[0]} galaxies in total')
ax.text(11.185, 0.4e5, f'Least massive bin: {counts_2[1]} galaxies in total')
plt.savefig(path_figuras+f'Analyzed_stellar_mass_bins.png', bbox_inches='tight')




# Pair-plots
renamed_sample = galaxies_sample.copy()
renamed_sample = renamed_sample.rename(columns={'Halo mass'    : r'log(M$_{h}$ [M$_{\odot}$/h])', 
                                                'Stellar mass' : r'log(M$_{\ast}$ [M$_{\odot}$/h])'})

g = sns.pairplot(renamed_sample,
             vars=[r'log(M$_{h}$ [M$_{\odot}$/h])', r'log(M$_{\ast}$ [M$_{\odot}$/h])', 'Halo spin', 'Halo concentration'],
             kind='hist', # Si se usa kde, en plot_kws añadir cortes en sigma para plotear
             diag_kind='hist',
             height=2.5,
             aspect=1,
             corner=True,
             plot_kws=dict(cmap='viridis'),
             diag_kws=dict(bins=20))
plt.savefig(path_figuras+'Corner_plot_seaborn_sample.png', bbox_inches='tight')


g = sns.pairplot(renamed_sample,
             vars=[r'log(M$_{h}$ [M$_{\odot}$/h])', r'log(M$_{\ast}$ [M$_{\odot}$/h])', 'Halo spin', 'Halo concentration'],
             kind='kde',
             diag_kind='hist',
             height=2,
             aspect=1,
             corner=True,
             plot_kws=dict(cmap='viridis', fill=False, levels=[0.1, 0.5, 0.68, 0.95]),
             diag_kws=dict(bins=20))
plt.savefig(path_figuras+'Corner_plot_seaborn_sample_kde.png', bbox_inches='tight')

g = sns.pairplot(renamed_sample,
             vars=[r'log(M$_{h}$ [M$_{\odot}$/h])', r'log(M$_{\ast}$ [M$_{\odot}$/h])', 'Halo spin', 'Halo concentration'],
             kind='kde',
             diag_kind='hist',
             height=2,
             aspect=1,
             corner=True,
             plot_kws=dict(cmap='viridis', fill=True, levels=[0, 0.1, 0.5, 0.68, 0.95]),
             diag_kws=dict(bins=20))
plt.savefig(path_figuras+'Corner_plot_seaborn_sample_kde_filled.png', bbox_inches='tight')