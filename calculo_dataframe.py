import numpy as np
import pandas as pd

file = np.load('Datos/ab_v0.npy', allow_pickle=True).item()

# Galaxies. 76 125 galaxies
gal_mstar = file["gal_mstar"]
gal_hostid = file["gal_hostid"]
gal_pos = file['gal_pos']

# Haloes. 345 469 halos
halo_mass = file["halo_mass"]
halo_pos = file["halo_pos"]
halo_id = file["halo_id"]

# Column names for the data frame
columns=['HostID', 'Halo mass', 'Stellar mass', 'Gal_x', 'Gal_y', 'Gal_z', 'Halo_x', 'Halo_y', 'Halo_z', 'Halo mass squared']
length=gal_mstar.size # Number of rows. Made for debuging and faster compilation

# Auxiliary columns to assing halo mass and pos to each galaxy
halo_mass_aux = np.zeros([length,])
halo_pos_aux = np.zeros([length, 3])

# Loop for all galaxies to create auxiliary columns
for i in range(length):
    print(f'DataFrame calculation: Galaxy number {i} out of 76125')
    id_host=gal_hostid[i]
    halo_mass_aux[i] = halo_mass[halo_id==id_host]
    halo_pos_aux[i, 0] = halo_pos[halo_id==id_host, 0]
    halo_pos_aux[i, 1] = halo_pos[halo_id==id_host, 1]
    halo_pos_aux[i, 2] = halo_pos[halo_id==id_host, 2]

halos = pd.DataFrame(data=np.array([halo_id, halo_mass, halo_pos[:, 0], halo_pos[:, 1], halo_pos[:, 2], halo_mass * halo_mass]).transpose(),
                    columns=['HaloID', 'Halo mass', 'x', 'y', 'z', 'Halo mass squared'])

halos['HaloID'] = halos['HaloID'].astype(int) # We force the ID column to be integers

# Create data array to convert to data frame
galaxies_np = np.zeros([length, 10])
galaxies_np[:length, 0] = gal_hostid[:length]
galaxies_np[:length, 1] = halo_mass_aux[:length]
galaxies_np[:length, 2] = gal_mstar[:length]
galaxies_np[:length, 3] = gal_pos[:length, 0]
galaxies_np[:length, 4] = gal_pos[:length, 1]
galaxies_np[:length, 5] = gal_pos[:length, 2]
galaxies_np[:length, 6] = halo_pos_aux[:length, 0]
galaxies_np[:length, 7] = halo_pos_aux[:length, 1]
galaxies_np[:length, 8] = halo_pos_aux[:length, 2]
galaxies_np[:length, 9] = halo_mass_aux[:length] * halo_mass_aux[:length]

galaxies = pd.DataFrame(data=galaxies_np, columns=columns)
galaxies['HostID'] = galaxies['HostID'].astype(int) # We force the ID column to be integers

galaxies['COP_x'] = galaxies['Gal_x'] - galaxies['Halo_x']
galaxies['COP_y'] = galaxies['Gal_y'] - galaxies['Halo_y']
galaxies['COP_z'] = galaxies['Gal_z'] - galaxies['Halo_z']

galaxies.to_csv('Resultados/galaxies.csv', index=False)
halos.to_csv('Resultados/halos.csv', index=False)