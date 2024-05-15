import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# import scienceplots

# plt.style.use('science')
# plt.rcParams.update({
#     "font.family": "lmodern",   # specify font family here
#     # "font.serif": ["Times"],  # specify font here
#     "font.size":11})          # specify font size here


L=205               # Box size
bin_number=25       # Number of bins for each feature
N_shufflings=100    # Number of shufflings done

path = 'PCF_recalculated/'
path_resultados = 'Resultados/' + path
path_figuras = 'Figuras/' + path

mass_cuts = [10.5, 10.75, 13.0]


feature_file_dict = {'Original'          : 'Halo_mass',
                     'Halo concentration' : 'Halo_mass_concentration',
                     'Halo spin'     : 'Halo_mass_spin',
                     'Halo mrank 1'  : 'Halo_mass_mrank1',
                     'Halo mrank 2'  : 'Halo_mass_mrank2',
                     'Halo mrank 3'  : 'Halo_mass_mrank3',
                     'Halo mrank 4'  : 'Halo_mass_mrank4',
                     'Halo mrank 5'  : 'Halo_mass_mrank5',
                     'Halo mrank 6'  : 'Halo_mass_mrank6',
                     'Halo vrank 1'  : 'Halo_mass_vrank1',
                     'Halo vrank 2'  : 'Halo_mass_vrank2',
                     'Halo vrank 3'  : 'Halo_mass_vrank3',
                     'Halo vrank 4'  : 'Halo_mass_vrank4',
                     'Halo vrank 5'  : 'Halo_mass_vrank5',
                     'Halo vrank 6'  : 'Halo_mass_vrank6',
                     'Halo tmform 1' : 'Halo_mass_tmform1',
                     'Halo tmform 2' : 'Halo_mass_tmform2',
                     'Halo tmform 3' : 'Halo_mass_tmform3',
                     'Halo tmform 4' : 'Halo_mass_tmform4',
                     'Halo tmform 5' : 'Halo_mass_tmform5',
                     'Halo tvform 1' : 'Halo_mass_tvform1',
                     'Halo tvform 2' : 'Halo_mass_tvform2',
                     'Halo tvform 3' : 'Halo_mass_tvform3',
                     'Halo av_nu'    : 'Halo_mass_av_nu',
                     }

feature_p0_dict   = {'Halo_mass'              : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_concentration' : [[0.05, 18, 0.1], [0.05, 18, 0.1]],
                    'Halo_mass_spin'          : [[0.05, 10, 0.25], [0.05, 10, 0.25]],
                    'Halo_mass_mrank1'        : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_mrank2'        : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_mrank3'        : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_mrank4'        : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_mrank5'        : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_mrank6'        : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_vrank1'        : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_vrank2'        : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_vrank3'        : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_vrank4'        : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_vrank5'        : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_vrank6'        : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_tmform1'       : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_tmform2'       : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_tmform3'       : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_tmform4'       : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_tmform5'       : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_tvform1'       : [[0.15, 15, 0.2], [0.15, 15, 0.2]],
                    'Halo_mass_tvform2'       : [[0.06, 15, 0.4], [0.04, 20, 0.5]],
                    'Halo_mass_tvform3'       : [[0.06, 15, 0.3], [0.05, 30, 0.6]],
                    'Halo_mass_av_nu'         : [[0.06, 10, 0.4], [0.06, 15, 0.3]],
                    }

############################################################  FUNCTIONS  ############################################################
def log_func(x, L, k, x0):
    return L/(1 + np.exp(-k * (x - x0))) + 1

def AB_calculator(pcf_org, pcf_mass, sigma_org, sigma_mass):
    '''
    Computes the ratio and uncertainty of said ratio between the 2pcf of a shuffled sample and the halo mass shuffled sample.
    
    Parameters
    ----------
    pcf_org : pandas Series
              Series with shuffled 2pcf calculation.
    pcf_mass: pandas Series
              Series with halo mass - shuffled 2pcf calculation.
    sigma_org : pandas Series
              Series with shuffled 2pcf uncertainty.
    sigma_mass: pandas Series
              Series with halo mass - shuffled 2pcf uncertainty.

    Returns
    -------
    ratio : ratio between the 2PCFs

    sigma : uncertainty of said ratio
    '''

    if len(pcf_org) != len(pcf_mass):
        raise  ValueError('2PCFs of different lengths. Subject length: ', len(pcf_org), ' Mass length: ', len(pcf_mass))

    ratio = pcf_org / pcf_mass
    sigma = np.sqrt( (sigma_org / pcf_mass)**2 + (- ratio * sigma_mass / pcf_mass )**2)
    
    return ratio, sigma

def AB_fit(ratio, ratio_sigma, ravg, p0=[0.15, 15, 0.2]):
    
    parameters, cov = curve_fit(log_func, np.log10(ravg), ratio, p0 = p0,  sigma = ratio_sigma, absolute_sigma=True)
    AB = parameters[0]
    sigma_AB = cov[0, 0]
    
    x_fit = np.log10(np.linspace(min(ravg), max(ravg), 1000))
    y_fit = log_func(x_fit, parameters[0], parameters[1], parameters[2])
    
    return AB, sigma_AB, x_fit, y_fit

############################################################  FUNCTIONS  ############################################################





# galaxies = pd.read_csv('Resultados/galaxies.csv')

for i in range(len(mass_cuts)-1):
    mass_cut_1 = mass_cuts[i]
    mass_cut_2 = mass_cuts[i+1]

    ## We read the data for the mass bin
    pcf_original = pd.read_csv(path_resultados + f'pcf_original_{mass_cut_1}_{mass_cut_2}.csv')
    ravg = pcf_original['ravg']

    names=['Feature', 'Assembly bias', '\pm', '\sigma', 'GAB fraction', 'Mean GAB fraction']
    resultados_df = pd.DataFrame(data=np.zeros([23, 6]), columns=names)
    
    ## We calculate the GAB level
    for feature in feature_file_dict.keys():

        feature_path = feature_file_dict[feature]
        pcf = pd.read_csv(path_resultados + f'{feature_path}/pcf_shuffled_mean_{mass_cut_1}_{mass_cut_2}.csv')


        ratio = pcf_original['xi'] / pcf['mean'] # Assembly bias
        sigma_ratio = abs(ratio*pcf['std']/pcf['mean']) # Assembly bias uncertainty

        p0 = feature_p0_dict[feature_path]
        AB, sigma_AB, x_fit, y_fit = AB_fit(ratio, sigma_ratio, ravg, p0=p0[i])

        if feature == 'Original':
            AB_original = AB

        resultados_df['Feature'] = feature
        resultados_df['Assembly bias'] = AB
        resultados_df['\sigma'] = sigma_AB
        resultados_df['GAB fraction'] = AB / AB_original

    # fig, ax = plt.subplots(1, 1, figsize=(6, 5))

    # # Halo mass
    # ax.plot(np.log10(ravg), (ratio_mass), label= 'Original Sample', linestyle='-', marker='+', color='C0')
    # ax.plot(x_fit_mass, y_fit_mass, label= 'Mass shuffle fit', linestyle='--', marker=',', color='C0')

    # # Halo mass + concentration
    # ax.plot(np.log10(ravg), (ratio_mass_concentration), label= 'Halo concentration', linestyle='-', marker=',', color='C1')
    # ax.plot(x_fit_concentration, y_fit_concentration, label= 'Concentration shuffle fit', linestyle='--', marker=',', color='C1')

    # # Halo mass + spin
    # ax.plot(np.log10(ravg), (ratio_mass_spin), label= 'Halo spin', linestyle='-', marker=',', color='C2')
    # ax.plot(x_fit_spin, y_fit_spin, label= 'Spin shuffle fit', linestyle='--', marker=',', color='C2')

    # # Reference lines
    # plt.vlines(np.log10(L*0.1), -0.5, 2.5, linestyle='--', color='C3')
    # ax.hlines(1, -(10), (100), linestyle='--', color='C3')

    # # Plot formating
    # ax.set_xlabel(r'Spatial scale $\log_{10}$ ([Mpc/h])')
    # ax.set_ylabel(r'$\xi$ / $\xi_{\rm{shuff (M_H)}}$')
    # ax.set_title(f'2PCF ratio ({N_shufflings} shufflings, stellar mass bin: {mass_cut_1}-{mass_cut_2})')

    # ax.set_ylim([0.9, 1.3])
    # ax.set_xlim([-0.5, np.log10((max(pcf_original['ravg'])))])
    # ax.legend(loc='upper left')
    # plt.savefig(path_figuras+f'/Joined_results_{mass_cut_1}_{mass_cut_2}.png', bbox_inches='tight')
    


    resultados_df.to_csv(f'Resultados/Results_bin{i}.csv', index=False)

resultados_bin1 = pd.read_csv('Resultados/Results_bin1.csv')
resultados_bin2 = pd.read_csv('Resultados/Results_bin2.csv')

resultados_bin1['Mean GAB fraction'] = (resultados_bin1['GAB fraction'] + resultados_bin2['GAB fraction'])/2
resultados_bin2['Mean GAB fraction'] = (resultados_bin1['GAB fraction'] + resultados_bin2['GAB fraction'])/2

resultados_bin1.to_csv('Resultados/Results_bin1_complete.csv')
resultados_bin2.to_csv('Resultados/Results_bin2_complete.csv')