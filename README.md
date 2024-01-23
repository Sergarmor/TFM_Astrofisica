# TFM_Sergio_Garcia_Astrofisica

Este repositorio está dedicado al desarrollo de mi TFM. 

Orden de ejecución:
1) calculo_dataframe.py
2) calculo_bins.py
3) main.py

El paso 1) lee los datos originales de IlustrisTNG1 y calcula los DataFrames principales con los que trabajaremos: halos y galaxies.
El paso 2) recoge los resultados del paso anterior y calcula los bins según la masa de los halos para galaxies y halos. Tiene en cuenta el bin_width escogido (implementar que utilice el definido en main)
El paso 3) ejecuta el programa principal, encargado de hacer el shuffling de las galaxias en los bins de masa, calcular las 2PCF y hacer los plots pertinentes (los histogramas se dejan en los cuadernos de prueba, habría que hacer un script que los cree)