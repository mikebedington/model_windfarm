import sys
sys.path.append(r'/home/michael/Code/gotm_tools/ersem')
from make_var import *

out_file = 'orig_r6_cer_without_ycs.nc'
bb = gotm_output(out_file, drop_times=365)

rs_obs = np.load('station_cci.npy', allow_pickle=True)
aa = np.ma.masked_array(rs_obs[1], mask=rs_obs[1] > 10000)


plt.plot(bb.time_dt[365:], np.mean(bb.total_chl[365:,-10:], axis=1))
plt.plot(rs_obs[0], aa)


station_loc = [4.54, 59.2]


cmems_outdir = '/home/michael/Projects/Winfarm_carbon/Code/model_windfarm/setups/cmems_data'


comp_vars = {'diato':'P1_c', 'dino':None, 'nano':'P2_c', 'ph', 'nppv', 'pico':'P3_c', 'phyc':'phyto_c', 'chl':'total_chl', 'spco2'}

this_var = 'chl'
this_nc = nc.Dataset(f'{cmems_outdir}/{this_var}_out.nc')

near_lon = np.argmin(np.abs(this_nc['longitude'][:] - station_loc[0]))
near_lat = np.argmin(np.abs(this_nc['latitude'][:] - station_loc[1]))

time_dt = np.asarray([dt.datetime.strptime(this_t.isoformat(), '%Y-%m-%dT%H:%M:%S') for this_t in nc.num2date(this_nc['time'][:], this_nc['time'].units)])

data = this_nc[this_var][:,:,near_lat, near_lon]

mask_dep = np.min(np.where(data.mask)[1])

plt.figure()
plt.pcolormesh(time_dt, -this_nc['depth'][0:mask_dep], data[:,0:mask_dep].T)
