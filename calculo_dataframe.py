import numpy as np
import pandas as pd

file = np.load('Datos/ab_v1.npy', allow_pickle=True).item()

# Building Halo DataFrame
halo_id = file['halo_id']
halo_mass = file['halo_mass']
halo_conc = file['halo_conc']
halo_spin = file['halo_spin']
halo_pos = file['halo_pos']
halo_vel = file['halo_vel']

halos = pd.DataFrame(
    data=np.array([halo_id, 
                   halo_mass, 
                   halo_conc, 
                   halo_spin, 
                   halo_pos[:, 0], halo_pos[:, 1], halo_pos[:, 2], 
                   halo_vel[:, 0], halo_vel[:, 1], halo_vel[:, 2]]).transpose(), 
    columns=['HaloID', 'Halo mass', 'Halo concentration', 'Halo spin', 'x', 'y', 'z', 'Vel_x', 'Vel_y', 'Vel_z'])
halos['HaloID'] = halos['HaloID'].astype(int) # We force IDs to be integers

halos = halos.sort_values(by='HaloID')

# Building Galaxies DataFrame
gal_hostid = file['idhost']
gal_cross = file['cross_sub2halo']
gal_type = file['type'] # Guide: 0 --> Central. | 1 --> Satellite
gal_mst = file['mst']
gal_col = file['col'] # Color?
gal_pos = file['pos']
gal_vel = file['vel']

## Didn't use
gal_mhist = file['mhist']
gal_vhist = file['vhist']
##

gal_halo_mass = file['halo_mass'][file['cross_sub2halo']]
gal_halo_conc = file['halo_conc'][file['cross_sub2halo']]
gal_halo_spin = file['halo_spin'][file['cross_sub2halo']]
gal_halo_pos = file['halo_pos'][file['cross_sub2halo']]
gal_halo_vel = file['halo_vel'][file['cross_sub2halo']]


columns = ['HostID', 'Host index', 'Type', 'Stellar mass', 'Halo mass', 'Halo concentration', 'Halo spin', 'Halo_x', 'Halo_y', 'Halo_z', 'Halo_vel_x', 'Halo_vel_y', 'Halo_vel_z', 'Col_x', 'Col_y', 'Col_z', 'Pos_x', 'Pos_y', 'Pos_z','COP_x', 'COP_y', 'COP_z','Vel_x', 'Vel_y', 'Vel_z','COP_vel_x', 'COP_vel_y', 'COP_vel_z']

galaxies = pd.DataFrame(
    data=np.array([gal_hostid, 
                   gal_cross,
                   gal_type, 
                   gal_mst, 
                   gal_halo_mass, 
                   gal_halo_conc, 
                   gal_halo_spin, 
                   gal_halo_pos[:, 0], gal_halo_pos[:, 1], gal_halo_pos[:, 2], 
                   gal_halo_vel[:, 0], gal_halo_vel[:, 1], gal_halo_vel[:, 2], 
                   gal_col[:, 0], gal_col[:, 1], gal_col[:, 2], 
                   gal_pos[:, 0], gal_pos[:, 1], gal_pos[:, 2], 
                   gal_pos[:, 0] - gal_halo_pos[:, 0], gal_pos[:, 1] - gal_halo_pos[:, 1], gal_pos[:, 2] - gal_halo_pos[:, 2],
                   gal_vel[:, 0], gal_vel[:, 1], gal_vel[:, 2],
                   gal_vel[:, 0] - gal_halo_vel[:, 0], gal_vel[:, 1] - gal_halo_vel[:, 1], gal_vel[:, 2] - gal_halo_vel[:, 2],
                   ]).transpose(),
    columns=columns)
    

# We force columns to be integers
galaxies['HostID'] = galaxies['HostID'].astype(int)
galaxies['Host index'] = galaxies['Host index'].astype(int)
galaxies['Type'] = galaxies['Type'].astype(int)

galaxies = galaxies.sort_values(by='HostID')

galaxies.to_csv('Resultados/galaxies.csv', index=False)
halos.to_csv('Resultados/halos.csv', index=False)