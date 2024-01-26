def ploting_results(pcf_original, b, sigma, n, L):

    import matplotlib.pyplot as plt
    import numpy as np

    # Here we plot everything

    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    ax.plot((pcf_original['ravg']), 
            (b), 
            color='C0', label='Data')
    ax.fill_between((pcf_original['ravg']), 
                    (b + n*sigma), 
                    (b - n*sigma), 
                    color='C1', label='Uncertainty', alpha=0.5)
    ax.set_xlabel('ravg')
    ax.set_ylabel(r'$\xi_{orig}$ / $\xi_{shuff}$')
    ax.set_title('2PCF comparison')
    plt.vlines(L*0.1, -0.5, 2.5, linestyle='--', color='C3')
    ax.hlines(1, -(10), (100), linestyle='--', color='C3')
    ax.set_ylim([-1, 2.5])
    ax.set_xlim([0, (np.ceil(max(pcf_original['ravg'])))])
    ax.legend()
    plt.savefig('Figuras/2pcf_ratio.png', bbox_inches='tight')


    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    ax.plot(np.log10(pcf_original['ravg']), 
            (b), 
            color='C0', label='Data')
    ax.fill_between(np.log10(pcf_original['ravg']), 
                    (b + n*sigma), 
                    (b - n*sigma), 
                    color='C1', label='Uncertainty', alpha=0.5)
    ax.set_xlabel('log10(ravg)')
    ax.set_ylabel(r'$\xi_{orig}$ / $\xi_{shuff}$')
    ax.set_title('2PCF small scale comparison')
    plt.vlines(L*0.1, -0.5, 2.5, linestyle='--', color='C3')
    ax.hlines(1, -(10), (100), linestyle='--', color='C3')
    ax.set_ylim([0.5, 1.75])
    ax.set_xlim([-1, np.log10(20)])
    ax.legend()
    plt.savefig('Figuras/2pcf_ratio_small_scale.png', bbox_inches='tight')