import netCDF4 as nc
import numpy as np
import matplotlib
font = {'family' : 'normal',
        'size'   : 16}

matplotlib.rc('font', **font)

from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt

ncs_to_comp = {'fixed1':'seagrass_varxp1.nc', 'fixed05':'seagrass_varxp05.nc',
				'var05_1':'seagrass_varxp05_1.nc'}

vars_to_plot = ['drag', 'u', 'x_excur', 'tke', 'xP', 'P']

all_ds = {}
for this_name, this_nc in ncs_to_comp.items():
	all_ds[this_name] = nc.Dataset(this_nc)

n_exp = len(ncs_to_comp.keys())
for this_var in vars_to_plot:
	fig, ax = plt.subplots(1,n_exp, figsize=[9*n_exp, 14])
	i = 0
	for this_name, this_ds in all_ds.items():
		if this_ds[this_var][:].shape[1] == this_ds['z'][:].shape[1]:
			vert_coord = 'z'
		else:
			vert_coord = 'zi'

		pc = ax[i].pcolormesh(this_ds['time'][:], np.squeeze(this_ds[vert_coord][0,...]), np.squeeze(this_ds[this_var][:]).T)
		ax[i].set_title(this_name)
        divider = make_axes_locatable(ax[i])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(pc, cax=cax, orientation='vertical')
		i+=1

	fig.suptitle(f'{this_var}')
	fig.tight_layout()
	fig.savefig(f'{this_var}.png', dpi=180)
	plt.close()

