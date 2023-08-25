import configparser
import motuclient
import datetime as dt
from time import time

class MotuOptions:
    def __init__(self, attrs: dict):
        super(MotuOptions, self).__setattr__("attrs", attrs)

    def __setattr__(self, k, v):
        self.attrs[k] = v

    def __getattr__(self, k):
        try:
            return self.attrs[k]
        except KeyError:
            return None

cfg = configparser.ConfigParser()
cfg.read('motuclient-python.ini')

user = cfg.get('Main','user')
pwd = cfg.get('Main','pwd')

start_date = dt.datetime(2010,1,1)
end_date = dt.datetime(2020,1,1)
ll_box = [[3.5,5],[59,60]]

service_id = {'phys':'NWSHELF_MULTIYEAR_PHY_004_009-TDS', 'bio':'NWSHELF_MULTIYEAR_BGC_004_011-TDS'}

all_vars = {'phys':{'uo':'cmems_mod_nws_phy-uv_my_7km-3D_P1D-m', 'vo':'cmems_mod_nws_phy-uv_my_7km-3D_P1D-m',
    'thetao':'cmems_mod_nws_phy-t_my_7km-3D_P1D-m', 'so':'cmems_mod_nws_phy-s_my_7km-3D_P1D-m',
    'zos':'cmems_mod_nws_phy-ssh_my_7km-2D_P1D-m'},
	'bio':{'attn':'cmems_mod_nws_bgc-kd_my_7km-3D_P1D-m', 'chl':'cmems_mod_nws_bgc-chl_my_7km-3D_P1D-m',
	'o2':'cmems_mod_nws_bgc-o2_my_7km-3D_P1D-m', 'no3':'cmems_mod_nws_bgc-no3_my_7km-3D_P1D-m',
	'po4':'cmems_mod_nws_bgc-po4_my_7km-3D_P1D-m', 'phyc':'cmems_mod_nws_bgc-phyc_my_7km-3D_P1D-m',
	'nppv':'cmems_mod_nws_bgc-pp_my_7km-3D_P1D-m', 'spco2':'cmems_mod_nws_bgc-spco2_my_7km-2D_P1D-m',
	'ph':'cmems_mod_nws_bgc-ph_my_7km-3D_P1D-m', 'diato':'cmems_mod_nws_bgc-pft_my_7km-3D-diato_P1M-m',
	'dino':'cmems_mod_nws_bgc-pft_my_7km-3D-dino_P1D-m', 'nano':'cmems_mod_nws_bgc-pft_my_7km-3D-nano_P1D-m',
	'pico':'cmems_mod_nws_bgc-pft_my_7km-3D-pico_P1D-m'}}



all_vars = {'bio':{'po4':'cmems_mod_nws_bgc-po4_my_7km-3D_P1D-m', 'phyc':'cmems_mod_nws_bgc-phyc_my_7km-3D_P1D-m',
    'nppv':'cmems_mod_nws_bgc-pp_my_7km-3D_P1D-m', 'spco2':'cmems_mod_nws_bgc-spco2_my_7km-2D_P1D-m',
    'ph':'cmems_mod_nws_bgc-ph_my_7km-3D_P1D-m', 'diato':'cmems_mod_nws_bgc-pft_my_7km-3D-diato_P1M-m',
    'dino':'cmems_mod_nws_bgc-pft_my_7km-3D-dino_P1D-m', 'nano':'cmems_mod_nws_bgc-pft_my_7km-3D-nano_P1D-m',
    'pico':'cmems_mod_nws_bgc-pft_my_7km-3D-pico_P1D-m'}}


data_request_dict = {
    "service_id": service_id,
    "date_min": start_date.strftime('%Y-%m-%d %H:%M:%S'),
    "date_max": end_date.strftime('%Y-%m-%d %H:%M:%S'),
    "longitude_min": ll_box[0][0],
    "longitude_max": ll_box[0][1],
    "latitude_min": ll_box[1][0],
    "latitude_max": ll_box[1][1],
    "depth_min": 0,
    "depth_max": 5000,
    "motu": 'http://my.cmems-du.eu/motu-web/Motu',
    "out_dir": ".",
    "auth_mode": "cas",
    "user": user,
    "pwd": pwd
}

for this_type in all_vars.keys():
	data_request_dict['service_id'] = service_id[this_type]
	var_data = all_vars[this_type]
	for this_var, this_source in var_data.items():
		print(f'Getting {this_var}', flush=True)
		start_time = time()
		outfile = f'{this_var}_out.nc'
		data_request_dict['out_name'] = outfile
		data_request_dict['product_id'] = this_source
		data_request_dict['variable'] = [this_var]

		motuclient.motu_api.execute_request(MotuOptions(data_request_dict))
		print(f'Completed - {time() - start_time:0.2f}s', flush=True)
