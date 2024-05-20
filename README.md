# TFM_Sergio_Garcia_Astrofisica

# A new galaxy assembly bias model

## Abstract

## Content and main work

This repository contains all the code of the Master's Thesis of Sergio García Moreno for the Master's Degree in Astrophysics of the Universidad Complutense de Madrid (UCM), supervised by Dr. Jonás Chaves-Montero, from the Institut de Física d'Altes Energies (IFAE) in Barcelona. This work has been developed during the academic year 2023-2024. It is composed of several files with determined porpouses and execution order. The 'main.py' file is the first to be executed, calling the rest of files when needed, being followed by the execution of the 'recalc_2pcf.py' file to calculate the 2PCF of the mass bins. 

After all the calculations from the ```.py``` scripts have been completed, the execution of the two Jupyter Notebooks is necessary to obtain the final results. The ```Fit_results_plots.ipynb``` file calculates the fits of the 2PCF ratios and computes the GAB values associated with each property. Outputs two ```.csv``` files with the results tables and the plots of the 2PCF ratios. The ```Mass_bins_illustration.ipynb``` notebook computes the median halo mass of each mass bin, creates the galaxy histogram of stellar mass and the corner plot with the properties. 

The rest of the ```.py``` files are depecrated scripts that can be removed (like the ```main_part2.py```) or that have been transformed into scripts from a Jupyter Notebook. This thesis is available in PDF in the following link:

TO_BE_INCLUDED

# Dependencies

This code makes use of the following packages:

- ```numpy```
- ```pandas```
- ```scipy```
- ```matplotlib```
- ```scienceplots``` (requieres a Latex installation, optional for the jupyter notebooks)
- ```Corrfunc``` (2pcf calculation)
- ```tqdm``` (progress bars)




<!-- # Citation

If you make use of this work, please aknowledge the project citing the following paper (Here is an example of a BibTeX entry):
```
@SOFTWARE{2024_GAB_Sergio,
    author = {Sergio García},
    title = {A new model for galaxy assembly bias},
    year = {2024}
    }
``` -->