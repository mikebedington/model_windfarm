import datetime as dt
import make_farm as mf

# This is my original test setup
# farm_params = {'area_wind_farm':1, 'no_turbines':10, 'surface_depth':10, 'surface_diameter':5,
#	'bed_depth':10, 'bed_diameter':5, 'cable_diameter':0.01, 'cable_extension':0.01'}
# mf.make_farm('nutrient_test', [4.54, 59.2], dt.datetime(2011,1,1), dt.datetime(2019,1,1), farm_params)

start_date = dt.datetime(2011,1,1)
end_date = dt.datetime(2019,1,1)
location = [4.54, 59.2]

thresh = 0.5

ll_box = [[location[0] - thresh, location[0] + thresh], [location[1] - thresh, location[1] + thresh]]


run ./era5_data ll_box[0][0] ll_box[0][1] ll_box[1][0] ll_box[1][1]

farm_params = {'area_wind_farm':1, 'no_turbines':0, 'surface_depth':0, 'surface_diameter':0,
   'bed_depth':10, 'bed_diameter':0, 'cable_diameter':0, 'cable_extension':0}
location = [4.54, 59.2]
mf.make_farm('no_struct', [4.54, 59.2], dt.datetime(2011,1,1), dt.datetime(2019,1,1), farm_params, make_restart='restart.nc', starting_carbon=0)

farm_params = {'area_wind_farm':1, 'no_turbines':10, 'surface_depth':10, 'surface_diameter':5,
   'bed_depth':10, 'bed_diameter':5, 'cable_diameter':0.01, 'cable_extension':0.01}
mf.make_farm('surface_dep10', [4.54, 59.2], dt.datetime(2011,1,1), dt.datetime(2019,1,1), farm_params, make_restart='restart.nc', starting_carbon=100000)


farm_params = {'area_wind_farm':1, 'no_turbines':10, 'surface_depth':240, 'surface_diameter':5,
   'bed_depth':10, 'bed_diameter':5, 'cable_diameter':5, 'cable_extension':0}
mf.make_farm('monopile', [4.54, 59.2], dt.datetime(2011,1,1), dt.datetime(2019,1,1), farm_params, make_restart='restart.nc', starting_carbon=100000)

