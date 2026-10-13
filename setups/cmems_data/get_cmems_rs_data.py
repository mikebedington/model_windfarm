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

service_id = {'rs_chl':'OCEANCOLOUR_NWS_BGC_HR_L3_NRT_009_203-TDS'}

all_vars = {'rs_chl':{'rs_chl':'cmems_obs_oc_nws_bgc_tur-spm-chl_nrt_l3-hr-mosaic_P1D-m'}}

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
