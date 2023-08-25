import numpy as np
import netCDF4 as nc
sys.path.append('../python')
import fvcom_gotm_aux as fga
import aux_funcs as af

exp_tag = 'first_test'
# GOTM setup
## Location
col_ll = [5.54, 59.2] 

data_basedir = '/home/michael/Projects/Winfarm_carbon/Code/model_windfarm/setups/cmems_data'


## Get depth, T,S,tidal,surface,nutrient forcing
phys_forcing = ['temp', 'sal', 'zeta', 'u', 'v',
tpxo_forcing
surface_forcing = 
ersem_forcing = 

{'phys': {'uo', 'vo', 'thetao', 'so', 'zos'},
 'bio': {'attn', 'o2', 'no3', 'po4', 'ph'}}

# Get indices of ll point to use
test_nc = nc.Dataset(f'{data_basedir}/thetao_out.nc')

forcing_ll = [test_nc['longitude'][:], test_nc['latitude'][:]]


# Write out profile files

for this_var in profile_vars:
    profile_dict = fga.reg_nc_to_profile_dict(, this_var, ll_ind)
    profile_dict_adj = {}
    for this_key, this_data in profile_dict.items():
        profile_dict_adj[dt.datetime(this_key.year + adj_year, this_key.month, this_key.day)] = this_data
    fga.write_profile_file(profile_dict_adj, f'{exp_tag}_{this_var}.txt')

# Write out biofiles for validation
bio_val =  ['attn',  'chl',  'phyc', 'nppv', 'spco2', 'diato', 'dino', 'nano', 'pico'}


# Windfarm setup

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
