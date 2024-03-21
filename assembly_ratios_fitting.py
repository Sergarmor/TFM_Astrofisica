import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scienceplots

plt.style.use('science')
plt.rcParams.update({
    "font.family": "lmodern",   # specify font family here
    # "font.serif": ["Times"],  # specify font here
    "font.size":11})          # specify font size here


L=205               # Box size
bin_number=25       # Number of bins for each feature
N_shufflings=100    # Number of shufflings done

def log_func(x, L, k, x0):
    return L/(1 + np.exp(-k * (x - x0))) + 1

def assembly_bias_fit(ratio, ratio_sigma, ravg, p0=[0.15, 15, 0.2]):
    
    parameters, cov = curve_fit(log_func, np.log10(ravg), ratio, p0 = p0,  sigma = ratio_sigma, absolute_sigma=True)
    AB = parameters[0]
    sigma_AB = cov[0, 0]
    
    x_fit = np.log10(np.linspace(min(ravg), max(ravg), 1000))
    y_fit = log_func(x_fit, parameters[0], parameters[1], parameters[2])
    
    return AB, sigma_AB, x_fit, y_fit

path = 'PCF_recalculated/'
path_resultados = 'Resultados/' + path
path_figuras = 'Figuras/' + path

mass_cuts = [10.5, 10.75, 13.0]

names=['Mstar_low', 'Mstar_high', 'Mhalo_median', 'Total AB %', 'Total AB sigma', 'Conc. AB %', 'Conc. AB sigma', 'Spin AB %', 'Spin AB sigma']
resultados_df = pd.DataFrame(data=np.zeros([len(mass_cut_1_list), 9]), columns=names)

galaxies = pd.read_csv('Resultados/galaxies.csv')

for i in range(len(mass_cuts)-1):
    mass_cut_1 = mass_cuts[i]
    mass_cut_2 = mass_cuts[i+1]
    
    ## We read the data for the mass bin
    pcf_original = pd.read_csv(path_resultados + f'pcf_original_{mass_cut_1}_{mass_cut_2}.csv')
    pcf_mass = pd.read_csv(path_resultados + f'Halo_mass/pcf_shuffled_mean_{mass_cut_1}_{mass_cut_2}.csv') # _{mass_cut_1}_{mass_cut_2}
    pcf_concentration = pd.read_csv(path_resultados + f'Halo_mass_concentration/pcf_shuffled_mean_{mass_cut_1}_{mass_cut_2}.csv')
    pcf_spin = pd.read_csv(path_resultados + f'Halo_mass_spin/pcf_shuffled_mean_{mass_cut_1}_{mass_cut_2}.csv')

    ravg = pcf_original['ravg']
    
    
    ## We calculate the ratios os Assembly bias
    # Halo mass
    b_mass = pcf_original['xi'] / pcf_mass['mean'] # Assembly bias
    # sigma_mass = abs(pcf_original['xi']/pcf_mass['mean'] * pcf_mass['std']) # Assembly bias uncertainty
    sigma_mass = abs(b_mass*pcf_mass['std']/pcf_mass['mean']) # Assembly bias uncertainty

    # Halo mass + concentration
    # sigma_concentration = abs(pcf_original['xi']/pcf_concentration['mean'] * pcf_concentration['std'])

    sigma_concentration = pcf_concentration['std']
    ratio_mass_concentration = pcf_concentration['mean'] / pcf_mass['mean']
    sigma_ratio_mass_concentration = np.sqrt( (sigma_concentration/pcf_mass['mean'])**2 + 
                              (- ratio_mass_concentration * sigma_mass / pcf_mass['mean'] )**2)

    # Halo mass + spin
    sigma_spin = pcf_spin['std']
    ratio_mass_spin = pcf_spin['mean'] / pcf_mass['mean']
    sigma_ratio_mass_spin = np.sqrt( (sigma_spin/pcf_mass['mean'])**2 + 
                              (- ratio_mass_spin * sigma_mass / pcf_mass['mean'] )**2)


    AB_mass, sigma_AB_mass, x_fit_mass, y_fit_mass = assembly_bias_fit(b_mass, sigma_mass, ravg, p0=[0.15, 15, 0.2])
    AB_spin, sigma_AB_spin, x_fit_spin, y_fit_spin = assembly_bias_fit(b_spin, sigma_spin, ravg, p0=[0.05, 18, 0.1])
    AB_concentration, sigma_AB_concentration, x_fit_concentration, y_fit_concentration = assembly_bias_fit(b_concentration, sigma_concentration, ravg, p0=[0.04, 20, 0.5])


    fig, ax = plt.subplots(1, 1, figsize=(6, 5))

    # Halo mass
    ax.plot(np.log10(ravg), (b_mass), label= 'Original Sample', linestyle='-', marker='+', color='C0')
    ax.plot(x_fit_mass, y_fit_mass, label= 'Mass shuffle fit', linestyle='--', marker=',', color='C0')

    # Halo mass + concentration
    ax.plot(np.log10(ravg), (ratio_mass_concentration), label= 'Halo concentration', linestyle='-', marker=',', color='C1')
    ax.plot(x_fit_concentration, y_fit_concentration, label= 'Concentration shuffle fit', linestyle='--', marker=',', color='C1')

    # Halo mass + spin
    ax.plot(np.log10(ravg), (ratio_mass_spin), label= 'Halo spin', linestyle='-', marker=',', color='C2')
    ax.plot(x_fit_spin, y_fit_spin, label= 'Spin shuffle fit', linestyle='--', marker=',', color='C2')

    # Reference lines
    plt.vlines(np.log10(L*0.1), -0.5, 2.5, linestyle='--', color='C3')
    ax.hlines(1, -(10), (100), linestyle='--', color='C3')

    # Plot formating
    ax.set_xlabel(r'Spatial scale $\log_{10}$ ([Mpc/h])')
    ax.set_ylabel(r'$\xi$ / $\xi_{\rm{shuff (M_H)}}$')
    ax.set_title(f'2PCF ratio ({N_shufflings} shufflings, stellar mass bin: {mass_cut_1}-{mass_cut_2})')

    ax.set_ylim([0.9, 1.3])
    ax.set_xlim([-0.5, np.log10((max(pcf_original['ravg'])))])
    ax.legend(loc='upper left')
    plt.savefig(path_figuras+f'/Joined_results_{mass_cut_1}_{mass_cut_2}.png', bbox_inches='tight')
    
    resultados_df['Mstar_low'] = mass_cut_1_list
    resultados_df['Mstar_high'] = mass_cut_2_list
    resultados_df['Mhalo_median'].iloc[i] = galaxies_sample['Halo mass'].median()
    resultados_df['Total AB %'].iloc[i] = AB_mass
    resultados_df['Total AB sigma'].iloc[i] = np.sqrt(cov_mass[0,0])
    resultados_df['Conc. AB %'].iloc[i] = AB_concentration
    resultados_df['Conc. AB sigma'].iloc[i] = np.sqrt(cov_concentration[0,0])
    resultados_df['Spin AB %'].iloc[i] = AB_spin
    resultados_df['Spin AB sigma'].iloc[i] = np.sqrt(cov_spin[0,0])

resultados_df.to_csv('Resultados/Curve_fitting_2.csv', index=False)