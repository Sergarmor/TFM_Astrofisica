# TFM Sergio Garcia Astrofisica

# A new galaxy assembly bias model

## Abstract

To achieve realistic predictions of the clustering of galaxies, we need numerical simulations that match observations. Due to computational limitations, for large volumes is necessary to populate dark matter simulations with galactic populations a posteriori, using models that assume relationships between the halo mass and the galactic populations. However, only using the halo mass does not capture the entirety of the galactic populations' complexity. The galaxy assembly bias refers to the dependence of galaxy clustering on factors beyond the mass of the host halo, such as halo concentration or spin, which capture around $42.4\%$ and $31.4\%$ of the total galaxy assembly bias. This work proposes and calculates the value of the galaxy assembly bias associated with different halo properties in the IllustrisTNG 300 simulation, such as the ranking by $M_{\rm peak}$ and $V_{\rm peak}$, and the formation times when the halo reaches a certain percentage of its final $M_{\rm peak}$ or $V_{\rm peak}$. To measure the galaxy assembly bias, we implemented the shuffling technique, which involves moving galactic populations of the same sample between halos of similar mass, generating new samples; calculating the two-point correlation function of each generated sample, and comparing the mean of all sample's correlation function with that obtained from shuffling relative to mass and a secondary property. The ratio of both means follows a sigmoid curve that tends towards the value of the galaxy assembly bias captured by the secondary property used. We found that, of the proposed properties, rankings by $M_{\rm peak}$ and $V_{\rm peak}$ achieve maximum fractions of the galaxy assembly bias of $30\%$, lower than that of concentration ($42.4\%$), while formation times achieve similar or higher fractions, with the maximum being $45\%$ and $49.1\%$ of the total galaxy assembly bias for the formation time when the halo reaches 0.9 and 0.125 times its final mass, respectively.

## Content and main work

This repository contains all the code of the Master's Thesis of Sergio García Moreno for the Master's Degree in Astrophysics of the Universidad Complutense de Madrid (UCM), supervised by Dr. Jonás Chaves-Montero, from the Institut de Física d'Altes Energies (IFAE) in Barcelona. This work has been developed during the academic year 2023-2024. It is composed of several files with determined porpouses and execution order. The ```main.py``` file is the first to be executed, calling the rest of files when needed, being followed by the execution of the ```recalc_2pcf.py``` file to calculate the 2PCF of the mass bins. 

After all the calculations from the ```.py``` scripts have been completed, the execution of the two Jupyter Notebooks is necessary to obtain the final results. The ```Fit_results_plots.ipynb``` file calculates the fits of the 2PCF ratios and computes the GAB values associated with each property. Outputs two ```.csv``` files with the results tables and the plots of the 2PCF ratios. The ```Mass_bins_illustration.ipynb``` notebook computes the median halo mass of each mass bin, creates the galaxy histogram of stellar mass and the corner plot with the properties. 

This thesis is available in PDF in the following link:

TO_BE_INCLUDED

# Dependencies

This code makes use of the following packages:

- ```numpy```
- ```pandas```
- ```scipy```
- ```matplotlib```
- ```scienceplots``` (requieres a Latex installation, optional for the jupyter notebooks)
- ```Corrfunc``` (2PCF calculation)
- ```tqdm``` (progress bars)