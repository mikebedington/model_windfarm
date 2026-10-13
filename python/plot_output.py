########################################################################################################################
# Plot the vars from GOTM run
import numpy as np
import netCDF4 as nc
import datetime as dt
import matplotlib.pyplot as plt
import glob as gb

vars_to_plot = {'Phosphate':'N1_p', 'Nitrate':'N3_n', 'Ammonium':'N4_n', 'Silicate':'N5_s', 'Oxygen':'O2_o', 'DIC':'O3_c', 'Bacteria (c)':'B1_c',
    'Diatoms (c)':'P1_c', 'Nano-phytoplankton (c)':'P2_c', 'Pico-phytoplankton (c)':'P3_c', 'Micro-phytoplankton (c)':'P4_c', 'Temperature':'temp', 'TKE':'tke', 'Structure fauna (c)':'Ys_c'}

vars_to_plot_sum = {'Phytoplankton (c)':['P1_c', 'P2_c', 'P3_c', 'P4_c'],
                    'Phytoplankton (Chl)':['P1_Chl', 'P2_Chl', 'P3_Chl', 'P4_Chl'],
                    'Zooplankton (c)':['Z4_c', 'Z5_c', 'Z6_c'],
                    'POM (c)':['R4_c', 'R6_c', 'R8_c', 'RS6_c']}

vars_to_plot_2d = {'Air-sea C flux':'O2_fair'}


pcolor_plot = {'Phytoplankton (c)':'phyt', 'Phytoplankton (Chl)':'chl', 'Zooplankton (c)':'zoo', 'POM (c)':'pom', 'Bacteria (c)':'bact', 'Phosphate':'phos', 'Nitrate':'nit', 'Silicate':'sil', 'Oxygen':'oxy'}

tag = 'test_run'
model_source = '/home/michael/Projects/Winfarm_carbon/Models/complete_model/model_windfarm/testing/output/test_nutrients_all'

file_list = gb.glob(f'{model_source}/output_*.nc')
file_list.sort()

tot_vars = {}

for this_name, this_var in vars_to_plot.items():
    data_out = []
    for this_file in file_list:
        file_nc = nc.Dataset(this_file)
        data_out.append(np.squeeze(file_nc[this_var][:]))
    tot_vars[this_name] = np.vstack(data_out)

tot_vars 
for



for this_name, this_var_list in vars_to_plot_sum.items():
    data_out = []
    for this_file in file_list:
        file_nc = nc.Dataset(this_file)
        this_step = file_nc[this_var_list[0]][:]
        for this_var in this_var_list[1:]:
            this_step += file_nc[this_var][:]
        data_out.append(np.squeeze(this_step))
    tot_vars[this_name] = np.vstack(data_out)

for this_name, this_var in vars_to_plot_2d.items():
    data_out = []
    for this_file in file_list:
        file_nc = nc.Dataset(this_file)
        data_out.append(np.squeeze(file_nc[this_var][:]))
    tot_vars[this_name] = np.hstack(data_out)


z_thick = []
for this_file in file_list:
    file_nc = nc.Dataset(this_file)
    z_thick.append(np.squeeze(file_nc['zi'][:,1:,...] - file_nc['zi'][:,0:-1,...]))
    
z_thick = np.vstack(z_thick)

int_vars = {}
for this_var, this_data in tot_vars.items():
    if this_var not in vars_to_plot_2d.keys():
        if this_data.shape[1] == file_nc['z'][:].shape[1]:
        	int_vars[this_var] = np.sum(this_data*z_thick, axis=1)

for this_var, this_save in pcolor_plot.items():
    plt.figure(figsize=[16,14])
    plt.pcolormesh(np.arange(0,1601), np.squeeze(file_nc['zi'][0,...]), tot_vars[this_var].T[:,0:1600])
    cbar = plt.colorbar()
    cbar.set_label(f'{this_var} mg/m^3')
    plt.xlabel('Days of experiment')
    plt.ylabel('Depth (m)')
    plt.tight_layout()
    plt.savefig(f'gotm_pc_{tag}_{this_save}.png', dpi=180)
    plt.close()

phyto_type = ['Diatoms', 'Nano-phytoplankton', 'Pico-phytoplankton', 'Micro-phytoplankton']


plt.figure(figsize=[16,14])
for this_type in phyto_type:
    plt.plot(int_vars[f'{this_type} (c)'][0:1600])
plt.legend(phyto_type)
plt.xlabel('Days of experiment')
plt.ylabel('Integrated water column c (mg)')
plt.tight_layout()
plt.savefig(f'phyto_{tag}.png', dpi=180)
plt.close()

np.save(f'tot_{tag}.npy', tot_vars)
np.save(f'int_{tag}.npy', int_vars)

for this_title, this_data in tot_vars.items():
    if this_data.shape[1] == file_nc['z'][:].shape[1]:
        vert_coord = 'z'
    else:
        vert_coord = 'zi'

    plt.figure(figsize=[18,10])

    plt.pcolormesh(np.arange(0,this_data.shape[0]), np.squeeze(file_nc[vert_coord][0,...]), this_data.T)
    cbar = plt.colorbar()
    cbar.set_label(f'{this_title}')
    plt.xlabel('Days of experiment')
    plt.ylabel('Depth (m)')
    plt.tight_layout()
	try:
    	plt.savefig(f'gotm_pc_{tag}_{vars_to_plot[this_title]}.png', dpi=180)
	except KeyError:
		plt.savefig(f'gotm_pc_{tag}_{pcolor_plot[this_title]}.png', dpi=180)
    plt.close()


	 
