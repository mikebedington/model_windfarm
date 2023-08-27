import numpy as np
import netCDF4 as nc
import os
import sys
sys.path.append('../python')
import fvcom_gotm_aux as fga
import aux_funcs as af

exp_tag = 'first_test'
# GOTM setup
## Location
col_ll = [4.54, 59.2] 

data_basedir = '/home/michael/Projects/Winfarm_carbon/Code/model_windfarm/setups/cmems_data'
out_dir = f'./{exp_tag}_input'
os.mkdir(out_dir)

## Get depth, T,S,tidal,surface,nutrient forcing

forcing_dict = {'phys': ['uo', 'vo', 'thetao', 'so'],
 'bio': ['attn', 'o2', 'no3', 'po4', 'ph']}

# Get indices of ll point to use
test_nc = nc.Dataset(f'{data_basedir}/thetao_out.nc')

forcing_ll = [test_nc['longitude'][:], test_nc['latitude'][:]]
forcing_ll_all = np.meshgrid(forcing_ll[0], forcing_ll[1])

dists = np.sqrt((forcing_ll_all[0] - col_ll[0])**2 + (forcing_ll_all[1] - col_ll[1])**2)
ll_ind = np.squeeze(np.where(dists == np.min(dists)))

# Write out profile files

for this_var_list in forcing_dict.values():
	for this_var in this_var_list:
		profile_dict = fga.reg_nc_to_profile_dict(f'{data_basedir}/{this_var}_out.nc', this_var, ll_ind)
		fga.write_profile_file(profile_dict, f'{out_dir}/{exp_tag}_{this_var}.txt')

# Write out biofiles for validation
bio_val =  ['attn',  'chl',  'phyc', 'nppv', 'spco2', 'diato', 'dino', 'nano', 'pico']
val_dict = {}
first = True
for this_var in bio_val:
	this_nc = nc.Dataset(f'{data_basedir}/{this_var}_out.nc')

	if len(this_nc[this_var].shape) == 3:
		val_dict[this_var] = this_nc[this_var][:,ll_ind[0], ll_ind[1]]
	else:
		val_dict[this_var] = this_nc[this_var][:,:,ll_ind[0], ll_ind[1]]
	if first:
		val_dict['depth'] = this_nc['depth'][:]
		val_dict['time'] = [dt.datetime(td.year, td.month, td.day, td.hour, td.minute, td.second) for td in nc.num2date(this_nc['time'][:],this_nc['time'].units)]
		first = False
np.save(f'{out_dir}/{exp_tag}_validation_dict.npy', val_dict)

# Surface zo from cmems
tpxo_forcing
surface_forcing =

fga.write_one_level_file(time_dt, file_nc['zeta'][:], f'{out_dir}/{exp_tag}_zeta.txt')

# Depth average vel file
uv_avg_file = 'test_loc_uv_avg.nc'
uv_avg_nc = nc.Dataset(uv_avg_file)

data_uv = np.asarray([np.ones(len(time_dt))*notional_h,uv_avg_nc['ua'][:], uv_avg_nc['va'][:]]).T

fga.write_one_level_file(time_dt, data_uv, f'{out_dir}/{exp_tag}_uv_avg.txt')

# Write out meteo file
meteo_file = 'test_loc_surface.nc'
meteo_nc = nc.Dataset(meteo_file)
meteo_time_dt = [dt.datetime(td.year, td.month, td.day, td.hour, td.minute, td.second) for td in nc.num2date(meteo_nc['time'][:],meteo_nc['time'].units)]

meteo_data = np.asarray([meteo_nc['u10'][:], meteo_nc['v10'][:], meteo_nc['airp'][:], meteo_nc['airt'][:], meteo_nc['hum'][:],
                            meteo_nc['cloud'][:], meteo_nc['precip'][:], meteo_nc['swr'][:]]).T
meteo_data = np.around(meteo_data, 4)
meteo_data[meteo_data[:,5] > 1,5] = 1

fga.write_one_level_file(meteo_time_dt, meteo_data, f'{out_dir}/{exp_tag}_meteo.txt')

## Windfarm setup

area_wind_farm = 10 # in km**2
no_turbines = 10

## Parameters for the surface part of the floating wind farm
surf_part_depth = 
surf_part_area =   # Per turbine

## Parameters for the seabed part of the floating wind farm


## Parameters for mooring cable



## Write files

x_Rate = 0.5 * (X * (d/A))


af.write_seagrass_dat(deps, coeff, ext, x_Rate, reinterp=None)

# Ersem setup
# To do Ys_c and Ys_acf need to overwrite a restart file
# acf is the area_of_site/circumference of object (or equivalently the volume of water column divided by surface area)

# Try with De Borger setup - 238km^2 and 299 turbines, assume 10m diameter monopiles
no_turbines = 299
circumference = 32
farm_area = 238
acf = (farm_area*(1000**2))/(circumference*no_turbines)

donor_file = 'restart.nc'

donor_nc = nc.Dataset(donor_file, 'r+')

donor_nc.CreateVariable(

# Trawling setup
