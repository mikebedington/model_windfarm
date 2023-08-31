import numpy as np
import cdsapi

c = cdsapi.Client()

years = np.arange(2010,2021)


for this_year in years:
	c.retrieve(
		'reanalysis-era5-single-levels',
		{
			'product_type': 'reanalysis',
			'format': 'netcdf',
			'variable': [
				'10m_u_component_of_wind', '10m_v_component_of_wind', '2m_temperature',
				'mean_top_net_short_wave_radiation_flux_clear_sky', 'total_cloud_cover', 'total_precipitation',
				'2m_dewpoint_temperature', 'mean_surface_net_short_wave_radiation_flux_clear_sky', 'surface_pressure',
			],
			'year': f'{this_year}',
			'month': [
				'01', '02', '03',
				'04', '05', '06',
				'07', '08', '09',
				'10', '11', '12',
			],
			'day': [
				'01', '02', '03',
				'04', '05', '06',
				'07', '08', '09',
				'10', '11', '12',
				'13', '14', '15',
				'16', '17', '18',
				'19', '20', '21',
				'22', '23', '24',
				'25', '26', '27',
				'28', '29', '30',
				'31',
			],
			'time': [
				'00:00', '01:00', '02:00',
				'03:00', '04:00', '05:00',
				'06:00', '07:00', '08:00',
				'09:00', '10:00', '11:00',
				'12:00', '13:00', '14:00',
				'15:00', '16:00', '17:00',
				'18:00', '19:00', '20:00',
				'21:00', '22:00', '23:00',
			],
			'area': [
				60, 3.5, 59,
				5,
			],
		},
		f'era_data_{this_year}.nc')
