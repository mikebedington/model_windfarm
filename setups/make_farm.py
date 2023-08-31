import numpy as np
import netCDF4 as nc
import datetime as dt
import os
import sys
sys.path.append('../python')
import fvcom_gotm_aux as fga
import aux_funcs as af

#######################################################################################################################################################################
exp_tag = 'nutrient_test'

ext_force = 'vel_avg'
# GOTM setup
## Location
col_ll = [4.54, 59.2] 

start_dt = dt.datetime(2011,1,1)
end_dt = dt.datetime(2019,1,1)

gebco_nc = nc.Dataset('/home/michael/Data/gebco_2023/GEBCO_2023.nc')
gebco_ll = [gebco_nc['lon'][:], gebco_nc['lat'][:]]

thresh = 2
subset_lon = np.logical_and(gebco_ll[0] >= col_ll[0] - thresh, gebco_ll[0] <= col_ll[0] + thresh)
subset_lat = np.logical_and(gebco_ll[1] >= col_ll[1] - thresh, gebco_ll[1] <= col_ll[1] + thresh)

subset_all = np.meshgrid(gebco_ll[0][subset_lon], gebco_ll[1][subset_lat]) 
dists = np.sqrt((subset_all[0] - col_ll[0])**2 + (subset_all[1] - col_ll[1])**2)
gebco_ll_ind = np.squeeze(np.where(dists == np.min(dists)))

col_depth = -int(np.floor(gebco_nc['elevation'][subset_lat,:][:,subset_lon][gebco_ll_ind[1],gebco_ll_ind[0]]))

data_basedir = '/home/michael/Projects/Winfarm_carbon/Code/model_windfarm/setups/cmems_data'
out_dir = f'./{exp_tag}'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

#######################################################################################################################################################################
## Get depth, T,S,tidal,surface,nutrient forcing

forcing_dict = {'phys': ['thetao', 'so'],
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
        fga.write_profile_file(profile_dict, f'{out_dir}/{exp_tag}_{this_var}.dat')

# Write out sst file
thetao_time_dt = [dt.datetime(td.year, td.month, td.day, td.hour, td.minute, td.second) for td in nc.num2date(test_nc['time'][:],test_nc['time'].units)]
fga.write_one_level_file(thetao_time_dt, test_nc['thetao'][:][:,0,ll_ind[0],ll_ind[1],np.newaxis], f'{out_dir}/{exp_tag}_sst.dat')

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

# Surface zo and depth averaged velocities from cmems
zeta_nc = nc.Dataset(f'{data_basedir}/zos_out.nc')
zeta_time_dt = [dt.datetime(td.year, td.month, td.day, td.hour, td.minute, td.second) for td in nc.num2date(zeta_nc['time'][:],zeta_nc['time'].units)]
fga.write_one_level_file(zeta_time_dt, zeta_nc['zos'][:,ll_ind[0], ll_ind[1]][:,np.newaxis], f'{out_dir}/{exp_tag}_zeta.dat')

v_nc = nc.Dataset(f'{data_basedir}/vo_out.nc')
u_nc = nc.Dataset(f'{data_basedir}/uo_out.nc')
uv_time_dt = [dt.datetime(td.year, td.month, td.day, td.hour, td.minute, td.second) for td in nc.num2date(v_nc['time'][:],v_nc['time'].units)]

uv_data = np.hstack([(np.ones(len(uv_time_dt))*col_depth)[:,np.newaxis], u_nc['uo'][:,ll_ind[0], ll_ind[1]][...,np.newaxis], v_nc['vo'][:,ll_ind[0], ll_ind[1]][...,np.newaxis]])
fga.write_one_level_file(uv_time_dt, uv_data, f'{out_dir}/{exp_tag}_uv_avg.dat')

avg_vel_yaml_dict = {'type':'average_velocity', 'dpdx':{'method':'file', 'constant_value':0.0, 'file':f'{exp_tag}_uv_avg.txt', 'column':2, 'tidal':{'amp_1':0.0, 'phase_1':0.0}},
                'dpdy':{'method':'file', 'constant_value':0.0, 'file':f'{exp_tag}_uv_avg.txt', 'column':3, 'tidal':{'amp_1':0.0, 'phase_1':0.0}},
                'h':{'method':'file', 'constant_value':0.0, 'file':f'{exp_tag}_uv_avg.txt', 'column':3}}

avg_vel_zeta_yaml_dict = {'method':'file', 'constant_value':0.0, 'file':f'{exp_tag}_zeta.txt', 'column':1,'tidal':{'amp_1':0.0, 'phase_1':0.0}}

# Write out meteo file
meteo_file_cols = {'u10':1, 'v10':2, 'airp':3, 'airt':4, 'hum':5, 'cloud':6, 'precip':7, 'swr':8}

meteo_basedir = '/home/michael/Projects/Winfarm_carbon/Code/model_windfarm/setups/era5_data'
meteo_file = f'{meteo_basedir}/era_out.nc'
meteo_nc = nc.Dataset(meteo_file)

meteo_ll = [meteo_nc['longitude'][:], meteo_nc['latitude'][:]]
meteo_ll_all = np.meshgrid(meteo_ll[0], meteo_ll[1])
dists = np.sqrt((meteo_ll_all[0] - col_ll[0])**2 + (meteo_ll_all[1] - col_ll[1])**2)
meteo_ll_ind = np.squeeze(np.where(dists == np.min(dists)))

meteo_time_dt = [dt.datetime(td.year, td.month, td.day, td.hour, td.minute, td.second) for td in nc.num2date(meteo_nc['time'][:],meteo_nc['time'].units)]

# No humidity from ERA5 so calculate specific humidity from dewpoint temp, temp, and airpressure
# https://confluence.ecmwf.int/pages/viewpage.action?pageId=171411214

T = meteo_nc['t2m'][:, meteo_ll_ind[0], meteo_ll_ind[1]]
T_dew = meteo_nc['d2m'][:, meteo_ll_ind[0], meteo_ll_ind[1]]
sp = meteo_nc['sp'][:, meteo_ll_ind[0], meteo_ll_ind[1]]

Rdry=287.0597 ; Rvap=461.5250 ; a1=611.21 ; a3=17.502 ; a4=32.19 ; T0=273.16
E=a1*np.exp(a3*(T_dew-T)/(T_dew-a4))
qsat=(Rdry/Rvap)*E/(sp-((1-Rdry/Rvap)*E))

meteo_data = np.asarray([meteo_nc['u10'][:, meteo_ll_ind[0], meteo_ll_ind[1]], meteo_nc['v10'][:, meteo_ll_ind[0], meteo_ll_ind[1]], sp, T, qsat,
                            meteo_nc['tcc'][:, meteo_ll_ind[0], meteo_ll_ind[1]], meteo_nc['tp'][:, meteo_ll_ind[0], meteo_ll_ind[1]],
                            meteo_nc['msnswrfcs'][:, meteo_ll_ind[0], meteo_ll_ind[1]]]).T
meteo_data = np.around(meteo_data, 4)
meteo_data[meteo_data[:,5] > 1,5] = 1

fga.write_one_level_file(meteo_time_dt, meteo_data, f'{out_dir}/{exp_tag}_meteo.dat')

# Calc TPXO tidal forcing
# M2, S2, N2, O1, K1, and K2 are dominant constituents in N sea - Hagen et al 2021 JGR Oceans
# amp=abs(hRe+i*hIm);GMT phase=atan2(-hIm,hRe)/pi*180

if ext_force == 'tpxo':
	tidal_const = {'m2': 44712.0, 's2': 43200.0, 'n2': 45576.0, 'o1': 92952.0, 'k1': 86148.0, 'k2': 43092.0}


	tpxo_datadir = '/home/michael/Data/TPXO_tides/TPXO9_atlas_v5_nc'

	tide_nc = nc.Dataset(f'{tpxo_datadir}/h_m2_tpxo9_atlas_30_v5.nc')
	tide_ll = [tide_nc['lon_z'][:], tide_nc['lat_z'][:]]
	tide_ll_all = np.meshgrid(tide_ll[0], tide_ll[1])
	dists = np.sqrt((tide_ll_all[0] - col_ll[0])**2 + (tide_ll_all[1] - col_ll[1])**2)
	tide_ll_ind = np.squeeze(np.where(dists == np.min(dists)))

	del dists
	del tide_ll_all

	tide_yaml_dict = {'type':'elevation', 'dpdx':{'method':'tidal', 'constant_value':0.0, 'file':None, 'column':1, 'tidal':{}},
					'dpdy':{'method':'tidal', 'constant_value':0.0, 'file':None, 'column':1, 'tidal':{}}, 
					 'h':{'method':'constant', 'constant_value':0.0, 'file':None, 'column':1}}

	for i, this_const in enumerate(list(tidal_const.keys())):
		this_tide_nc = nc.Dataset(f'{tpxo_datadir}/h_{this_const}_tpxo9_atlas_30_v5.nc')
		tide_yaml_dict['dpdx']['tidal'][f'amp_{i}'] = np.abs(this_tide_nc['hRe'][tide_ll_ind[1], tide_ll_ind[0]] + np.imag*this_tide_nc['hIm'][tide_ll_ind[1], tide_ll_ind[0]])
		tide_yaml_dict['dpdx']['tidal'][f'phase_{i}'] = (np.atan2(-this_tide_nc['hIm'][tide_ll_ind[1], tide_ll_ind[0]], this_tide_nc['hRe'][tide_ll_ind[1], tide_ll_ind[0]])/np.pi)*180
		tide_yaml_dict['dpdy']['tidal'][f'amp_{i}'] = 0.0
		tide_yaml_dict['dpdy']['tidal'][f'phase_{i}'] = 0.0
		tide_yaml_dict[f'period_{i}'] =  tidal_const[this_const]

#######################################################################################################################################################################
# Write yaml file
# This doesn't work because yaml.dump doesn't preservere the order and does some weird formatting
"""
import yaml

with open('gotm_template.yaml') as f:
     gotm_yaml = yaml.safe_load(f)

gotm_yaml['location']['name'] = f'{exp_tag} experiment'
gotm_yaml['location']['longitude'] = col_ll[0]
gotm_yaml['location']['latitude'] = col_ll[1]
gotm_yaml['location']['depth'] = col_depth

gotm_yaml['time']['start'] = start_dt
gotm_yaml['time']['end'] = end_dt

gotm_yaml['temperature']['file'] = f'{exp_tag}_thetao.txt'
gotm_yaml['salinity']['file'] = f'{exp_tag}_so.txt'

for this_var, this_col in meteo_file_cols.items():
    gotm_yaml['surface'][this_var]['file'] = f'{exp_tag}_meteo.txt'
    gotm_yaml['surface'][this_var]['method'] = 'file'
    gotm_yaml['surface'][this_var]['column'] = this_col

gotm_yaml['surface']['hum']['type'] = 'specific'

if ext_force == 'tpxo':
    gotm_yaml['mimic_3d']['ext_pressure'] = tide_yaml_dict
    gotm_yaml['mimic_3d']['zeta'] = tide_zeta_yaml_dict
elif ext_force == 'avg_vel':
    gotm_yaml['mimic_3d']['ext_pressure'] = avg_vel_yaml_dict
    gotm_yaml['mimic_3d']['zeta'] = avg_vel_zeta_yaml_dict

with open(f'{out_dir}/{exp_tag}_gotm.yaml', 'w') as f:
    yaml.dump(gotm_yaml, f)
"""

start_str = f'{start_dt.strftime("%Y-%m-%d %H:%M:%S")}'
end_str = f'{end_dt.strftime("%Y-%m-%d %H:%M:%S")}'

with open('edit_yaml.sh', 'r') as fp:
    data = fp.read()
    new = data.replace('exp_name=', f'exp_name={exp_tag}')
    new = new.replace('lon=', f'lon={col_ll[0]}')
    new = new.replace('lat=', f'lat={col_ll[1]}')
    new = new.replace('dep=', f'dep={col_depth}')
    new = new.replace('start_t=', f'start_t="{start_str}"')
    new = new.replace('end_t=', f'end_t="{end_str}"')

with open(f'{exp_tag}_edit_yaml.sh', 'w') as fp:
    fp.write(new)


import os
os.system(f'bash ./{exp_tag}_edit_yaml.sh')
os.system(f'rm ./{exp_tag}_edit_yaml.sh')
#######################################################################################################################################################################
## Windfarm setup

area_wind_farm = 1 # in km**2
no_turbines = 10

deps = np.arange(0,col_depth) # deps by metre
## Parameters for the surface part of the floating wind farm
surface_depth = 10
surface_diameter = 5

## Parameters for the seabed part of the floating wind farm
bed_depth = 10
bed_diameter = 5

## Parameters for mooring cable
cable_diameter = 0.1
cable_extension = 0.01

## Interpolate these to the water column
bed_lays = deps >= col_depth -bed_depth 

surf_lays = deps <= surface_depth
mid_lays = np.ones(len(deps), dtype=bool)
mid_lays[np.logical_and(bed_lays, surf_lays)] = False

A = np.ones(len(deps))*area_wind_farm*(1000**2) # presume this is in m^2
X = np.ones(len(deps))*no_turbines

d = np.ones(len(deps))*cable_diameter
d[surf_lays] = surface_diameter
d[bed_lays] = bed_diameter

ext = np.zeros(len(deps))
ext[mid_lays] = cable_extension

## Write files, coefficient approach from Rennau et al 2012
coeff = np.ones(len(deps))*0.63 # Smooth cylinder
x_Rate = 0.5 * (X * (d/A)) # Area density - X no of cylinders, d - diameter of cylinder, A area for deceleration of flow

af.write_seagrass_dat(deps, coeff, ext, x_Rate, outfile=f'{out_dir}/seagrass.dat', reinterp=None)
os.system(f'cp seagrass.nml ./{exp_tag}_input/')

os.system(f'cp fabm.yaml ./{exp_tag}_input/')
"""
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
"""

