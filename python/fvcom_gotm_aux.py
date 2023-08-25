import numpy as np
import datetime as dt
import netCDF4 as nc


# Adapted from pyfvcom.grid
def unstructured_grid_depths(h, zeta, sigma):
    """
    Calculate the depth time series for cells in an unstructured grid.

    Parameters
    ----------
    h : np.ndarray
        Water depth
    zeta : np.ndarray
        Surface elevation time series
    sigma : np.ndarray
        Sigma vertical distribution, range 0-1 (`siglev' or `siglay' in FVCOM)
    nan_invalid : bool, optional
        Set values shallower than the mean sea level (`h') to NaN. Defaults to not doing that.

    Returns
    -------
    depths : np.ndarray
        Time series of model depths.

    """

    abs_water_depth = zeta + h
    # Add zeta again so the range is surface elevation (`zeta') to mean water depth rather (`h') than zero to water
    # depth (`h' + `zeta') which is much more useful for plotting.
    depths = abs_water_depth[:, np.newaxis] * sigma[np.newaxis, :] + zeta[:, np.newaxis]

    return depths


def nc_to_profile_dict(nc_file_str, variable, col_h=None, siglay=None, ll_ind=None):
    nc_file = nc.Dataset(nc_file_str)
    if ll_ind is None:
        data_raw = nc_file[variable][:]
    else:
        data_raw = nc_file[varable][ll_ind]

    time_dt = [dt.datetime(td.year, td.month, td.day, td.hour, td.minute, td.second) for td in nc.num2date(nc_file['time'][:],nc_file['time'].units)]

    if col_h is None:
        col_h = nc_file['h'][:]
    if siglay is None:
        siglay = nc_file['siglay'][:]

    dep_series = unstructured_grid_depths(col_h, nc_file['zeta'][:], siglay)

    profile_data_dict = {}
    for i, this_dt in enumerate(time_dt):
        profile_data_dict[this_dt] = np.asarray([dep_series[i,:], data_raw[i,:]]).T
    
    return profile_data_dict

def reg_nc_to_profile_dict(nc_file_str, variable, ll_ind):
    nc_file = nc.Dataset(nc_file_str)
    data_raw = nc_file[variable][:,:,ll_ind[0],ll_ind[1]]
    valid_deps = ~data_raw.mask[0,:]
    dep_series = nc_file['depth'][valid_deps]

    time_dt = [dt.datetime(td.year, td.month, td.day, td.hour, td.minute, td.second) for td in nc.num2date(nc_file['time'][:],nc_file['time'].units)]

    profile_data_dict = {}
    for i, this_dt in enumerate(time_dt):
        profile_data_dict[this_dt] = np.asarray([dep_series, data_raw[i,valid_deps]]).T

    return profile_data_dict

def nc_to_timestep(nc_file, var_list):
    time_str = [b''.join(this_str).decode('utf-8') for this_str in nc_file['Times'][:]]
    time_dt = np.asarray([dt.datetime.strptime(this_str, '%Y-%m-%dT%H:%M:%S.000000') for this_str in time_str])
    
    data = []
    for this_var in var_list:
        data.append(nc_file[this_var][:])
    data = np.vstack(data)

    return time_dt, data

def write_profile_file(profile_data_dict, output_name):
    with open(output_name, 'w') as f:
        for this_date, this_data in profile_data_dict.items():
            f.write(f'{this_date.strftime("%Y-%m-%d %H:%M:%S")}  {this_data.shape[0]} {this_data.shape[1]}\n')
            for this_line in this_data:
                line_str = ' '
                for this_pt in this_line:
                    line_str+=f'{this_pt} '
                f.write(f'{line_str[0:-1]}\n')

def write_one_level_file(time_dt, data, output_name, format_str=None):
    if format_str is None:
        format_str = '.4f'
    with open(output_name, 'w') as f:
        for this_date, this_data in zip(time_dt, data):
            this_data_str = ''
            for entry in this_data:
                this_data_str+=f'{entry:{format_str}} '
            f.write(f'{this_date.strftime("%Y-%m-%d %H:%M:%S")}    {this_data_str[0:-1]}\n')
