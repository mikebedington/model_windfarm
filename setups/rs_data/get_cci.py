

station_loc = [4.54, 59.2]

lon = nc.Dataset('https://www.oceancolour.org/thredds/dodsC/CCI_ALL-v5.0-5DAY?lon')['lon'][:]
lat = nc.Dataset('https://www.oceancolour.org/thredds/dodsC/CCI_ALL-v5.0-5DAY?lat')['lat'][:]

time_ds = nc.Dataset('https://www.oceancolour.org/thredds/dodsC/CCI_ALL-v5.0-5DAY?time')
time_dt = np.asarray([dt.datetime.strptime(this_t.isoformat(), '%Y-%m-%dT%H:%M:%S') for this_t in nc.num2date(time_ds['time'][:], time_ds['time'].units)])

near_lon = np.argmin(np.abs(lon - station_loc[0]))
near_lat = np.argmin(np.abs(lat - station_loc[1]))

chl = np.squeeze(nc.Dataset(f'https://www.oceancolour.org/thredds/dodsC/CCI_ALL-v5.0-5DAY?chlor_a[0:1:{len(time_dt)-1}][{near_lat}:1:{near_lat}][{near_lon}:1:{near_lon}]')['chlor_a'][:])

np.save('station_cci.npy', [time_dt, chl])
