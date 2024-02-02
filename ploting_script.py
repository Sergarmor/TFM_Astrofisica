def ploting_2pcf_ratio(pcf_original, pcf_shuffled, n, L, bin_feature, sub_bin_feature, shuffle_number):

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    b = pcf_original['xi'] / pcf_shuffled_mean['mean'] # Assembly bias
    sigma = pcf_original['xi']/pcf_shuffled_mean['mean'] * pcf_shuffled_mean['std'] # Assembly bias uncertainty
    xerr = pcf_original['rmax'] - pcf_original['rmin']


    fig, ax = plt.subplots(1, 1, figsize=(6, 5))

    ax.errorbar((pcf_original['ravg']), 
            (b), 
            xerr = xerr,
            yerr = n*sigma,
            color='C1', label= bin_feature + ' and ' + sub_bin_feature + f' shuffle ({shuffle_number})', linestyle='--', marker='.', ecolor='C0')


    ax.set_xlabel('Spatial scale [Mpc]')
    ax.set_ylabel(r'$\xi_{orig}$ / $\xi_{shuff}$')
    ax.set_title('2PCF ratio')

    plt.vlines(L*0.1, -0.5, 2.5, linestyle='--', color='C3')
    ax.hlines(1, -(10), (100), linestyle='--', color='C3')

    ax.set_ylim([-0.5, 2.5])
    ax.set_xlim([0, ((max(pcf_original['ravg'])))])
    ax.legend()
    plt.savefig('Figuras/2pcf_ratio.png', bbox_inches='tight')

    ##### ZOOM TO SMALL SCALES
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))

    ax.plot(np.log10(pcf_original['ravg']), 
                (b), 
                color='C0', label= bin_feature + ' and ' + sub_bin_feature + f' shuffle ({shuffle_number})', linestyle='--', marker='.')
    ax.fill_between(np.log10(pcf_original['ravg']), 
                        (b + n*sigma), 
                        (b - n*sigma), 
                        color='C1', label='Uncertainty', alpha=0.5)
    ax.set_xlabel(r'Spatial scale [$\log_{10}$(Mpc)]')
    ax.set_ylabel(r'$\xi_{orig}$ / $\xi_{shuff}$')
    ax.set_title('2PCF ratio: small scale')

    plt.vlines(L*0.1, -0.5, 2.5, linestyle='--', color='C3')
    ax.hlines(1, -(10), (100), linestyle='--', color='C3')

    ax.set_ylim([0.5, 1.5])
    ax.set_xlim([-1, np.log10(20)])
    ax.legend()
    plt.savefig('Figuras/2pcf_ratio_small_scale.png', bbox_inches='tight')